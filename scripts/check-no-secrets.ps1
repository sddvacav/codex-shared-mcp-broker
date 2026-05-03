$ErrorActionPreference = "Stop"

$patterns = @(
    'sk-[A-Za-z0-9_\-]{20,}',
    'gh[opusr]_[A-Za-z0-9_]{20,}',
    '(?i)(api[_-]?key|auth[_-]?token|bearer[_-]?token)\s*=\s*[''"][^''"]{8,}[''"]',
    '(?i)password\s*=\s*[''"][^''"]{6,}[''"]'
)

$files = Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\.git\\' -and
        $_.FullName -notmatch '\\dist\\' -and
        $_.Extension -match '\.(md|py|ps1|toml|json|svg|yml|yaml|txt)$'
    }

$failed = $false
foreach ($file in $files) {
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
