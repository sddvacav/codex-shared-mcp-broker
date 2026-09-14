"""
run_broker.py — foreground entrypoint for the shared MCP broker.

mcp-proxy (v0.11+) serves every stdio MCP declared in named_servers.json
on a single HTTP/SSE listener. Claude Code sessions point at the listener
instead of each spawning their own stdio subprocess, collapsing:

    N_sessions x M_servers  →  1 x M_servers

The wrapper exists so we can register the process under Task Scheduler
with a stable command string and log to a known location without piping
mcp-proxy stdout to a file descriptor that breaks MCP's own stdio
framing (mcp-proxy runs as SSE *server* here, not stdio client, so
piping is actually safe — but the wrapper keeps the XML arguments tidy).

Run manually:
    D:/软件/Python313/python.exe D:/codex_project/mcp_broker/run_broker.py

Under the schtask we invoke via hidden_launcher.vbs + pythonw.exe for
absolute silence on boot/logon.
"""
from __future__ import annotations

import json
import logging
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BROKER_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BROKER_DIR / "named_servers.json"
LOG_FILE = Path(r"D:\codex_project\logs\claude_mcp_broker.log")
PID_FILE = BROKER_DIR / "broker.pid"
MCP_PROXY_PYTHONW = Path(
    r"C:\Users\lenovo\AppData\Roaming\uv\tools\mcp-proxy\Scripts\pythonw.exe"
)
MCP_PROXY_MODULE = "mcp_proxy"

HOST = "127.0.0.1"
PORT = 38808
PORTS = tuple(
    int(item.strip())
    for item in os.environ.get("MCP_BROKER_PORTS", "38808,38809").split(",")
    if item.strip()
)

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)
log = logging.getLogger("mcp_broker")

CREATE_NO_WINDOW = 0x08000000
COMMANDS = ("start", "status", "servers", "endpoints", "completion", "help")
COMPLETION_SHELLS = ("powershell",)
HELP_TEXT = f"""Usage:
  run_broker.py [start]
  run_broker.py status
  run_broker.py servers [name-prefix]
  run_broker.py endpoints [name-prefix]
  run_broker.py completion powershell

Default command:
  start

Commands:
  start                 start the shared mcp-proxy broker
  status                print broker health JSON from /status
  servers [prefix]      print enabled named servers
  endpoints [prefix]    print MCP/SSE URLs for enabled named servers
  completion powershell print a PowerShell argument completer
  help                  print this help

Environment:
  MCP_BROKER_PORTS      comma-separated broker ports, default {','.join(map(str, PORTS))}
"""


def _load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        log.error("broker config unreadable at %s: %s", CONFIG_PATH, exc)
        raise


def _enabled_servers() -> dict[str, dict]:
    data = _load_config()
    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict):
        log.error("broker config has invalid mcpServers payload")
        return {}
    enabled: dict[str, dict] = {}
    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            enabled[name] = {}
        elif cfg.get("enabled", True):
            enabled[name] = cfg
    return dict(sorted(enabled.items()))


def _port_accepts(port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((HOST, port), timeout=timeout):
            return True
    except OSError:
        return False


def _terminate_tree(pid: int) -> None:
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            timeout=20,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception as exc:
        log.warning("failed to terminate stale broker pid=%d: %s", pid, exc)


def _read_pid_for_port(port: int) -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        raw = PID_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            return int(raw)
        except ValueError:
            return None
    if isinstance(data, dict):
        try:
            return int(data.get(str(port), 0))
        except (TypeError, ValueError):
            return None
    try:
        return int(data)
    except (TypeError, ValueError):
        return None


def _read_pid_map() -> dict[int, int]:
    if not PID_FILE.exists():
        return {}
    try:
        raw = PID_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return {}
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            return {PORT: int(raw)}
        except ValueError:
            return {}
    if isinstance(data, dict):
        result: dict[int, int] = {}
        for port, pid in data.items():
            try:
                result[int(port)] = int(pid)
            except (TypeError, ValueError):
                continue
        return result
    try:
        return {PORT: int(data)}
    except (TypeError, ValueError):
        return {}


def _process_age_seconds(pid: int) -> float | None:
    """Return age of the process in seconds, or None if it cannot be inspected."""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"$p = Get-CimInstance Win32_Process -Filter \"ProcessId={pid}\";"
             " if ($p) { ((Get-Date) - $p.CreationDate).TotalSeconds } else { '' }"],
            capture_output=True, text=True, timeout=10,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception as exc:
        log.warning("failed to read age for pid=%d: %s", pid, exc)
        return None
    raw = (r.stdout or "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# How long a freshly-spawned broker is allowed to finish stdio handshakes
# (12 named MCP servers) before we treat it as "stale because port is silent".
WARMUP_GRACE_SECONDS = 120.0


def _already_running(port: int = PORT) -> int | None:
    """Return a healthy broker PID if one is already listening on port.

    A broker that just spawned may take 30-90s to bind because mcp-proxy
    initialises every named stdio MCP serially. Within WARMUP_GRACE_SECONDS
    we treat an alive mcp-proxy process as healthy even if the port has not
    started accepting connections yet — otherwise a watchdog tick would
    kill it mid-handshake and leak its child stdio MCPs.
    """
    pid = _read_pid_for_port(port)
    if pid is None:
        return None
    if pid <= 0:
        return None
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"Get-CimInstance Win32_Process -Filter \"ProcessId={pid}\" | "
         "Select ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],
        capture_output=True, text=True, timeout=10,
        creationflags=CREATE_NO_WINDOW,
    )
    if pid and r.stdout.strip():
        out = r.stdout.lower()
        is_proxy = ("mcp-proxy" in out or "mcp_proxy" in out or f"--port {port}" in out)
        if is_proxy and _port_accepts(port):
            return pid
        if is_proxy:
            age = _process_age_seconds(pid)
            if age is not None and age < WARMUP_GRACE_SECONDS:
                log.info(
                    "broker pid=%d for port=%d still warming up (age=%.1fs < %.0fs); skipping kill",
                    pid, port, age, WARMUP_GRACE_SECONDS,
                )
                return pid
        log.warning("stale broker pid=%d for port=%d; process exists but port is unhealthy", pid, port)
        _terminate_tree(pid)
    return None


def _broker_env() -> dict[str, str]:
    env = os.environ.copy()
    # mcp-proxy currently opens config files with the interpreter default
    # encoding on Windows. Force UTF-8 so UTF-8 JSON stays readable.
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env


def _has_enabled_servers() -> bool:
    return bool(_enabled_servers())


def _spawn_broker(log_handle, port: int = PORT) -> subprocess.Popen:
    return subprocess.Popen(
        [
            str(MCP_PROXY_PYTHONW),
            "-m",
            MCP_PROXY_MODULE,
            "--named-server-config",
            str(CONFIG_PATH),
            "--host",
            HOST,
            "--port",
            str(port),
            "--allow-origin",
            "*",
            "--log-level",
            "INFO",
        ],
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        creationflags=0x00000008 | 0x00000200 | CREATE_NO_WINDOW,
        close_fds=True,
        env=_broker_env(),
    )


def _write_pids(pids: dict[int, int]) -> None:
    tmp = PID_FILE.with_suffix(".pid.tmp")
    if len(pids) == 1 and PORT in pids:
        tmp.write_text(str(pids[PORT]), encoding="utf-8")
    else:
        tmp.write_text(json.dumps({str(port): pid for port, pid in pids.items()}, sort_keys=True), encoding="utf-8")
    os.replace(tmp, PID_FILE)


def _write_pid(pid: int) -> None:
    _write_pids({PORT: pid})


def _http_get_json(url: str, timeout: float = 5.0) -> tuple[int | None, dict | None, str | None]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                payload = None
            return response.status, payload, None
    except urllib.error.HTTPError as exc:
        return exc.code, None, str(exc)
    except OSError as exc:
        return None, None, str(exc)


def _broker_status() -> dict:
    pid_map = _read_pid_map()
    status = {
        "host": HOST,
        "ports": [],
        "pid_file": str(PID_FILE),
        "config": str(CONFIG_PATH),
        "log": str(LOG_FILE),
        "enabled_servers": list(_enabled_servers().keys()),
    }
    for port in PORTS:
        pid = pid_map.get(port)
        http_status, payload, error = _http_get_json(f"http://{HOST}:{port}/status")
        status["ports"].append(
            {
                "port": port,
                "pid": pid,
                "accepts_tcp": _port_accepts(port, timeout=0.5),
                "process_age_seconds": _process_age_seconds(pid) if pid else None,
                "status_http_code": http_status,
                "status_ok": http_status == 200,
                "status_error": error,
                "server_instances": (payload or {}).get("server_instances", {}),
            }
        )
    return status


def _server_names(prefix: str | None = None) -> list[str]:
    names = list(_enabled_servers().keys())
    if prefix:
        names = [name for name in names if name.startswith(prefix)]
    return names


def _server_endpoints(prefix: str | None = None) -> list[dict[str, str | int]]:
    endpoints: list[dict[str, str | int]] = []
    for port in PORTS:
        for name in _server_names(prefix):
            base = f"http://{HOST}:{port}/servers/{name}"
            endpoints.append(
                {
                    "name": name,
                    "port": port,
                    "mcp": f"{base}/mcp",
                    "sse": f"{base}/sse",
                }
            )
    return endpoints


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _print_powershell_completion() -> None:
    commands = ", ".join(f"'{item}'" for item in COMMANDS)
    shells = ", ".join(f"'{item}'" for item in COMPLETION_SHELLS)
    servers = ", ".join(f"'{item}'" for item in _enabled_servers().keys())
    print(
        f"""# Source this file from your PowerShell profile.
# Example:
#   & D:\\codex_project\\mcp_broker\\mcp-broker.ps1 completion powershell |
#     Set-Content $env:USERPROFILE\\Documents\\WindowsPowerShell\\mcp-broker-completion.ps1
#   . $env:USERPROFILE\\Documents\\WindowsPowerShell\\mcp-broker-completion.ps1

$script:McpBrokerCommands = @({commands})
$script:McpBrokerCompletionShells = @({shells})
$script:McpBrokerServers = @({servers})

Register-ArgumentCompleter -Native -CommandName 'mcp-broker','mcp-broker.ps1','run_broker.py' -ScriptBlock {{
    param($wordToComplete, $commandAst, $cursorPosition)
    $words = @($commandAst.CommandElements | ForEach-Object {{ $_.Extent.Text.Trim('"') }})
    $previous = if ($words.Count -ge 2) {{ $words[-2] }} else {{ '' }}
    $candidates = $script:McpBrokerCommands
    if ($previous -eq 'completion') {{
        $candidates = $script:McpBrokerCompletionShells
    }} elseif ($previous -in @('servers','endpoints')) {{
        $candidates = $script:McpBrokerServers
    }}
    $candidates |
        Where-Object {{ $_ -like "$wordToComplete*" }} |
        ForEach-Object {{ [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_) }}
}}
"""
    )


def _parse_args(argv: list[str]) -> tuple[str, list[str]]:
    if not argv:
        return "start", []
    if argv[0] in COMMANDS:
        return argv[0], argv[1:]
    return "start", argv


def _dispatch_cli(argv: list[str]) -> int | None:
    command, rest = _parse_args(argv)
    if command == "start":
        return None
    if command == "help":
        print(HELP_TEXT)
        return 0
    if command == "status":
        _print_json(_broker_status())
        return 0
    if command == "servers":
        _print_json(_server_names(rest[0] if rest else None))
        return 0
    if command == "endpoints":
        _print_json(_server_endpoints(rest[0] if rest else None))
        return 0
    if command == "completion":
        shell = rest[0].lower() if rest else "powershell"
        if shell != "powershell":
            print(f"unsupported completion shell: {shell}", file=sys.stderr)
            return 2
        _print_powershell_completion()
        return 0
    return 2


def main(argv: list[str] | None = None) -> int:
    dispatched = _dispatch_cli(sys.argv[1:] if argv is None else argv)
    if dispatched is not None:
        return dispatched

    if not MCP_PROXY_PYTHONW.exists():
        log.error("mcp-proxy pythonw not found at %s", MCP_PROXY_PYTHONW)
        return 2
    if not CONFIG_PATH.exists():
        log.error("broker config not found at %s", CONFIG_PATH)
        return 3
    if not _has_enabled_servers():
        log.info("broker config has no enabled named servers; nothing to start")
        return 0

    existing = _already_running(PORT)
    if existing:
        missing_ports = [port for port in PORTS if port != PORT and not _already_running(port)]
        if missing_ports:
            spawned: dict[int, subprocess.Popen] = {}
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(f"\n===== broker shard spawn {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
                for port in missing_ports:
                    log.info("starting broker shard port=%d", port)
                    spawned[port] = _spawn_broker(f, port)
            pids = {PORT: existing}
            pids.update({port: proc.pid for port, proc in spawned.items()})
            _write_pids(pids)
            log.info("broker shards spawned pids=%s", pids)
            return 0
        log.info("broker already running pid=%d — exiting", existing)
        return 0

    args = [
        str(MCP_PROXY_PYTHONW),
        "-m",
        MCP_PROXY_MODULE,
        "--named-server-config",
        str(CONFIG_PATH),
        "--host",
        HOST,
        "--port",
        str(PORT),
        "--allow-origin",
        "*",
        "--log-level",
        "INFO",
    ]
    log.info("starting broker: %s", " ".join(args))

    # Run foreground so the Task Scheduler entry keeps a handle; redirect
    # stdout/stderr into our log.
    spawned: dict[int, subprocess.Popen] = {}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n===== broker spawn {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
        for port in PORTS:
            log.info("starting broker port=%d", port)
            spawned[port] = _spawn_broker(f, port)
    _write_pids({port: proc.pid for port, proc in spawned.items()})
    proc = spawned[PORT]
    log.info("spawned pids=%s", {port: proc.pid for port, proc in spawned.items()})

    def _stop(*_):
        log.info("signal received, terminating broker pids=%s", {port: proc.pid for port, proc in spawned.items()})
        for child in spawned.values():
            try:
                child.terminate()
            except Exception:
                pass
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    # Block on broker. Restart on crash up to 5 times within 60s.
    deadline = time.time() + 60
    restarts = 0
    while True:
        exited: tuple[int, int] | None = None
        while exited is None:
            for port, child in list(spawned.items()):
                rc = child.poll()
                if rc is not None:
                    exited = (port, rc)
                    break
            time.sleep(1)
        port, rc = exited
        log.warning("broker port=%d exited rc=%s", port, rc)
        if time.time() < deadline and restarts < 5:
            restarts += 1
            log.info("respawn #%d port=%d", restarts, port)
            with LOG_FILE.open("a", encoding="utf-8") as f:
                spawned[port] = _spawn_broker(f, port)
            _write_pids({port: child.pid for port, child in spawned.items()})
            continue
        log.error("broker died too many times, giving up")
        return rc or 1


if __name__ == "__main__":
    sys.exit(main())


