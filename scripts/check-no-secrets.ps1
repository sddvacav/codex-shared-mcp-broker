$ErrorActionPreference = "Stop"

$patterns = @(
    'sk-[A-Za-z0-9_\-]{20,}',
    'gh[opusr]_[A-Za-z0-9_]{20,}',
    '(?i)(api[_-]?key|auth[_-]?token|bearer[_-]?token)\s*=\s*[''"][^''"]{8,}[''"]',
    '(?i)password\s*=\s*[''"][^''"]{6,}[''"]',
    '(?i)\bsub2api\b',
    '(?i)\.codex_home',
    '(?i)\bLAPTOP-[A-Z0-9\-]+',
    '(?i)C:\\Users\\[^\\\s]+',
    '(?i)D:\\(?!path\\to\\your\\b)[^ \n\r\t"'')]+'
)

$files = Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\.git\\' -and
        $_.FullName -notmatch '\\dist\\' -and
        $_.Extension -match '\.(md|py|ps1|toml|json|svg|yml|yaml|txt)$'
    }

$failed = $false
foreach ($file in $files) {
    $relative = Resolve-Path -Relative $file.FullName
    if ($relative -eq ".\src\codex_shared_mcp_broker\audit.py" -or $relative -eq ".\scripts\check-no-secrets.ps1") {
        continue
    }
    $text = Get-Content -Raw -Path $file.FullName -ErrorAction SilentlyContinue
    foreach ($pattern in $patterns) {
        if ($text -match $pattern) {
            Write-Output "[FAIL] possible secret in $($file.FullName)"
            $failed = $true
        }
    }
}

if ($failed) {
    exit 1
}

Write-Output "secret-scan-ok"
