param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $BrokerArgs
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Entrypoint = Join-Path $ScriptDir "run_broker.py"

$SoftwareDir = "D:\" + [string][char]0x8F6F + [string][char]0x4EF6
$PythonCandidates = @(
    (Join-Path $SoftwareDir "Python313\python.exe"),
    "python.exe",
    "python"
)

$Python = $PythonCandidates | Where-Object {
    $candidate = $_
    if ([System.IO.Path]::IsPathRooted($candidate)) {
        Test-Path -LiteralPath $candidate
    } else {
        $null -ne (Get-Command $candidate -ErrorAction SilentlyContinue)
    }
} | Select-Object -First 1

if (-not $Python) {
    throw "Python executable not found"
}

$ArgumentList = @($Entrypoint) + @($BrokerArgs)
& $Python @ArgumentList
exit $LASTEXITCODE
