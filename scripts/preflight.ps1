param(
    [string]$CodexHome = $env:CODEX_HOME,
    [int]$BrokerPort = 38808
)

$ErrorActionPreference = "Stop"

function Write-Check {
    param([string]$Name, [bool]$Ok, [string]$Detail = "")
    $status = if ($Ok) { "OK" } else { "FAIL" }
    if ($Detail) {
        Write-Output "[$status] $Name - $Detail"
    } else {
        Write-Output "[$status] $Name"
    }
    if (-not $Ok) { $script:HadFailure = $true }
}

$script:HadFailure = $false

Write-Check "CODEX_HOME present" (-not [string]::IsNullOrWhiteSpace($CodexHome)) $CodexHome

if ($CodexHome) {
    $config = Join-Path $CodexHome "config.toml"
    Write-Check "config.toml exists" (Test-Path $config) $config

    if (Test-Path $config) {
        $text = Get-Content -Raw -Path $config
        Write-Check "xhigh reasoning configured" ($text -match 'model_reasoning_effort\s*=\s*"xhigh"')
        Write-Check "400K context policy configured" ($text -match 'model_context_window\s*=\s*400000')
        Write-Check "360K compaction policy configured" ($text -match 'model_auto_compact_token_limit\s*=\s*360000')
        Write-Check "shared MCP URL configured" ($text -match 'http://127\.0\.0\.1:38808/servers/.+/mcp')
    }
}

$connection = Get-NetTCPConnection -LocalPort $BrokerPort -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
Write-Check "shared broker is listening" ($null -ne $connection) "127.0.0.1:$BrokerPort"

if (Get-Command codex -ErrorAction SilentlyContinue) {
    $mcpList = codex mcp list 2>$null | Out-String
    Write-Check "codex mcp list works" (-not [string]::IsNullOrWhiteSpace($mcpList))
    Write-Check "MCP entries use HTTP URLs" ($mcpList -match 'http://127\.0\.0\.1:38808/servers/.+/mcp')
    Write-Check "no obvious stdio command entries" ($mcpList -notmatch '\b(npx|uvx|python|powershell)\b')
} else {
    Write-Check "codex CLI available" $false "codex command not found"
}

if ($script:HadFailure) {
    exit 1
}

Write-Output "preflight-ok"
