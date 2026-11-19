# installa-windows.ps1 — il kit delle prove sulla RTX 4050 su Windows, via WSL2 (ADR-0136,
# scelta del DM sulla card del 17/11: WSL2 con Ubuntu 24.04).
#
# Su Windows le prove non girano native: girano in WSL2, con gli stessi script e le stesse verifiche
# di Bazzite, Debian 13 e CachyOS, in modo «diretto» (niente Distrobox). La GPU arriva in WSL2 dal
# driver NVIDIA di Windows: dentro Ubuntu non si installa nessun driver.
#
# Uso, da PowerShell come amministratore (serve solo la prima volta, per abilitare WSL):
#   Set-ExecutionPolicy -Scope Process Bypass
#   .\scripts\prove-4050\installa-windows.ps1                 # prepara tutto
#   .\scripts\prove-4050\installa-windows.ps1 -Memoria 12     # e dà 12 GB di RAM a WSL2
#   .\scripts\prove-4050\installa-windows.ps1 -Mostra         # dice cosa farebbe e basta
#
# Poi le prove:  wsl -d Ubuntu-24.04 -- bash -lc "cd ~/RumblingStone && scripts/prove-4050/kit.sh tutte"
#
# Log: tutto quello che lo script scrive finisce anche in
# %USERPROFILE%\rumblingstone-prove-4050\log\installa-windows-<data-ora>.log (Start-Transcript).
# Dentro WSL2 installa.sh tiene il suo log in ~/rumblingstone-prove-4050/<giorno>/log/.
[CmdletBinding()]
param(
    [switch]$Mostra,
    [int]$Memoria = 0,
    [string]$Distro = "Ubuntu-24.04",
    [string]$Repo = "https://github.com/gsamuele78/RumblingStone.git"
)
$ErrorActionPreference = "Stop"
# wsl.exe di serie scrive in UTF-16: con questa variabile (WSL recente) scrive in UTF-8
$env:WSL_UTF8 = "1"

# Il transcript di PowerShell, lo strumento di serie. In Windows PowerShell 5.1 l'uscita di un
# eseguibile nativo (wsl.exe, nvidia-smi.exe) entra nel transcript solo se passa dalla pipeline:
# per questo ogni chiamata nativa qui sotto finisce in «| Out-Host». Mai «2>&1» su un nativo: con
# ErrorActionPreference=Stop la prima riga su stderr fermerebbe lo script. Lo stderr di wsl.exe va
# sul terminale e non nel transcript; quello del kit dentro WSL2 lo tiene il log di installa.sh.
$logDir = Join-Path $env:USERPROFILE "rumblingstone-prove-4050\log"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$transcript = Join-Path $logDir ("installa-windows-{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HHmmss"))
Start-Transcript -Path $transcript | Out-Null
try {

function Esegui([string]$Descrizione, [scriptblock]$Blocco) {
    Write-Host "    $Descrizione"
    if (-not $Mostra) { & $Blocco }
}

Write-Host "==> 1/5 driver NVIDIA di Windows"
$smi = Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue
if ($smi) {
    & nvidia-smi.exe --query-gpu=name,memory.total,driver_version --format=csv,noheader | Out-Host
} else {
    Write-Warning "nvidia-smi.exe non trovato: installa il driver NVIDIA (Game Ready o Studio) da nvidia.com, poi rilancia."
    if (-not $Mostra) { exit 3 }
}

Write-Host "==> 2/5 WSL2 e $Distro"
$distro = (wsl.exe --list --quiet 2>$null) -replace "`0", "" | Where-Object { $_ -eq $Distro }
if (-not $distro) {
    Esegui "wsl --install -d $Distro  (poi riavvia Windows se lo chiede, apri Ubuntu una volta per creare l'utente, e rilancia questo script)" {
        wsl.exe --install -d $Distro | Out-Host
    }
    if (-not $Mostra) { exit 0 }
} else {
    Write-Host "    $Distro c'è già"
}
Esegui "wsl --update  (il kernel di WSL2 aggiornato serve al passaggio della GPU)" { wsl.exe --update | Out-Host }

Write-Host "==> 3/5 memoria di WSL2"
# Di serie WSL2 prende metà della RAM: sui 16 GB dell'ASUS sono 8, pochi per FLUX (8,3 GB di pesi in
# RAM) e per il 12B della prosa. Con -Memoria si scrive %UserProfile%\.wslconfig, solo se non c'è.
$cfg = Join-Path $env:USERPROFILE ".wslconfig"
if ($Memoria -gt 0) {
    if (Test-Path $cfg) {
        Write-Warning "$cfg esiste già: non lo tocco. Controlla che [wsl2] abbia memory=${Memoria}GB."
    } else {
        Esegui "scrivo $cfg con memory=${Memoria}GB e swap=16GB" {
            Set-Content -Path $cfg -Encoding ascii -Value "[wsl2]`r`nmemory=${Memoria}GB`r`nswap=16GB`r`n"
            wsl.exe --shutdown | Out-Host
        }
    }
} else {
    Write-Host "    lascio la memoria di serie (per FLUX e la prosa: -Memoria 12)"
}

Write-Host "==> 4/5 il repo dentro WSL2 (nella home di Linux, non in /mnt/c: lì il disco è molto più lento)"
$clona = "set -e; cd ~; [ -d RumblingStone ] || git clone '$Repo' RumblingStone; cd RumblingStone; git switch main; git pull --ff-only"
Esegui "wsl -d $Distro -- bash -lc `"$clona`"" { wsl.exe -d $Distro -- bash -lc $clona | Out-Host }

Write-Host "==> 5/5 il kit dentro WSL2 (apt, Ollama, CUDA; chiede la password di Ubuntu)"
$installa = "cd ~/RumblingStone && scripts/prove-4050/installa.sh"
if ($Mostra) { $installa = "$installa --mostra" }
wsl.exe -d $Distro -- bash -lc $installa | Out-Host
if ($LASTEXITCODE -ne 0) {
    Write-Warning "installa.sh dentro WSL2 e' uscito con $LASTEXITCODE: leggi l'errore qui sopra, correggi e rilancia."
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Fatto. Le prove:"
Write-Host "  wsl -d $Distro -- bash -lc `"cd ~/RumblingStone && scripts/prove-4050/kit.sh tutte`""
Write-Host "L'archivio da caricare nel thread finisce in \\wsl`$\$Distro\home\<utente>\rumblingstone-prove-4050\"
} finally {
    Stop-Transcript | Out-Null
    Write-Host "Log di questo giro: $transcript"
}
