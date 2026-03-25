Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Host ''
Write-Host '== Jerry LLM Workbench: Windows Setup ==' -ForegroundColor Cyan

$pythonLauncher = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonLauncher = 'py'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonLauncher = 'python'
} else {
    throw 'Python 3 was not found. Install Python 3.11+ and re-run setup_windows.ps1.'
}

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    if ($pythonLauncher -eq 'py') {
        & py -3 @Args
    } else {
        & python @Args
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: $($Args -join ' ')"
    }
}

Write-Host 'Checking Python version...'
if ($pythonLauncher -eq 'py') {
    & py -3 --version
} else {
    & python --version
}
if ($LASTEXITCODE -ne 0) {
    throw 'Could not execute Python. Check your Python installation and PATH.'
}

$venvPath = Join-Path $repoRoot '.venv'
$venvPython = Join-Path $venvPath 'Scripts/python.exe'

if (-not (Test-Path $venvPython)) {
    Write-Host 'Creating virtual environment (.venv)...'
    Invoke-Python -Args @('-m', 'venv', $venvPath)
} else {
    Write-Host 'Virtual environment already exists. Reusing .venv'
}

Write-Host 'Ensuring pip is available in .venv...'
& $venvPython -m pip --version
if ($LASTEXITCODE -ne 0) {
    throw 'pip is not available in the virtual environment.'
}

Write-Host 'Upgrading pip (optional)...'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Warning 'pip upgrade failed. Continuing with current pip version.'
}

$requirementsPath = Join-Path $repoRoot 'requirements.txt'
if (Test-Path $requirementsPath) {
    Write-Host 'Installing requirements.txt...'
    & $venvPython -m pip install -r $requirementsPath
    if ($LASTEXITCODE -ne 0) {
        throw 'Requirements install failed.'
    }
}

$envExamplePath = Join-Path $repoRoot '.env.example'
$envPath = Join-Path $repoRoot '.env'
if ((Test-Path $envExamplePath) -and (-not (Test-Path $envPath))) {
    Copy-Item $envExamplePath $envPath
    Write-Host 'Created .env from .env.example'
} elseif (Test-Path $envPath) {
    Write-Host '.env already exists. Keeping current values.'
}

Write-Host ''
Write-Host 'Setup complete.' -ForegroundColor Green
Write-Host 'Next steps:'
Write-Host '1) Start Ollama desktop app (or ollama serve).'
Write-Host '2) Pull a model: ollama pull qwen2.5-coder:7b'
Write-Host '3) Run smoke tests:'
Write-Host '   .\.venv\Scripts\python.exe scripts\system_check.py'
Write-Host '   .\.venv\Scripts\python.exe scripts\ollama_model_list.py'
Write-Host '   .\.venv\Scripts\python.exe scripts\ollama_hello.py'
Write-Host ''
