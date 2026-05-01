# Obsidian Plugin Auto-Installer
# -----------------------------------------------------------
# Bu script GitHub'dan eklentileri indirir, vault/.obsidian/plugins/
# klasörüne yerleştirir ve community-plugins.json'a ekleyerek aktive eder.
#
# Kullanım (cmd'den):
#   powershell -ExecutionPolicy Bypass -File eklentileri_kur.ps1
#
# Sonra Obsidian'ı kapatıp tekrar aç. Hepsi açık gelir.

$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Bu script Araçlar/ içinde — vault onun bir üstü
$VaultPath  = Split-Path -Parent $PSScriptRoot
$PluginsDir = Join-Path $VaultPath ".obsidian\plugins"
$ConfigFile = Join-Path $VaultPath ".obsidian\community-plugins.json"

# Yüklenecek eklentiler
$Plugins = @(
    @{ name = "Dataview";            id = "dataview";                    repo = "blacksmithgu/obsidian-dataview" },
    @{ name = "Templater";           id = "templater-obsidian";          repo = "SilentVoid13/Templater" },
    @{ name = "Various Complements"; id = "various-complements";         repo = "tadashi-aikawa/obsidian-various-complements-plugin" },
    @{ name = "Translate";           id = "translate";                   repo = "Fevol/obsidian-translate" },
    @{ name = "Calendar";            id = "calendar";                    repo = "liamcain/obsidian-calendar-plugin" },
    @{ name = "Periodic Notes";      id = "periodic-notes";              repo = "liamcain/obsidian-periodic-notes" },
    @{ name = "Excalidraw";          id = "obsidian-excalidraw-plugin";  repo = "zsviczian/obsidian-excalidraw-plugin" },
    @{ name = "Obsidian to Anki";    id = "obsidian-to-anki-plugin";     repo = "Pseudonium/Obsidian_to_Anki" }
)

Write-Host ""
Write-Host "=== Obsidian Plugin Installer ===" -ForegroundColor Cyan
Write-Host "Vault: $VaultPath"
Write-Host ""

if (-not (Test-Path $VaultPath)) {
    Write-Host "[HATA] Vault bulunamadi: $VaultPath" -ForegroundColor Red
    exit 1
}
New-Item -ItemType Directory -Path $PluginsDir -Force | Out-Null

# Eklenti listesini önceden göster
Write-Host "Yuklenecek eklentiler:" -ForegroundColor Yellow
foreach ($p in $Plugins) { Write-Host "  - $($p.name)  ($($p.id))" }
Write-Host ""

$ok = 0
$fail = 0
$failedPlugins = @()

function Download-One {
    param([string]$url, [string]$dest, [bool]$optional = $false)
    try {
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -ErrorAction Stop -TimeoutSec 30
        return $true
    } catch {
        if (-not $optional) {
            Write-Host "    [!] indirilemedi: $url" -ForegroundColor DarkYellow
            Write-Host "        $($_.Exception.Message)" -ForegroundColor DarkGray
        }
        return $false
    }
}

foreach ($p in $Plugins) {
    Write-Host "[*] $($p.name)" -ForegroundColor Yellow
    $dir = Join-Path $PluginsDir $p.id
    New-Item -ItemType Directory -Path $dir -Force | Out-Null

    $base = "https://github.com/$($p.repo)/releases/latest/download"

    # manifest.json — zorunlu
    $manifestOk = Download-One "$base/manifest.json" (Join-Path $dir "manifest.json")
    if ($manifestOk) { Write-Host "    [+] manifest.json" -ForegroundColor Green }

    # main.js — zorunlu
    $mainOk = Download-One "$base/main.js" (Join-Path $dir "main.js")
    if ($mainOk) { Write-Host "    [+] main.js" -ForegroundColor Green }

    # styles.css — opsiyonel (her eklentide olmayabilir)
    $stylesOk = Download-One "$base/styles.css" (Join-Path $dir "styles.css") $true
    if ($stylesOk) { Write-Host "    [+] styles.css" -ForegroundColor Green }

    if ($manifestOk -and $mainOk) {
        $ok++
    } else {
        $fail++
        $failedPlugins += $p.name
        Write-Host "    [HATA] $($p.name) yuklenemedi" -ForegroundColor Red
    }
    Write-Host ""
}

# community-plugins.json güncelle (aktif et)
Write-Host "[*] community-plugins.json guncelleniyor..." -ForegroundColor Yellow

$enabled = @()
if (Test-Path $ConfigFile) {
    $raw = Get-Content $ConfigFile -Raw -Encoding UTF8
    if ($raw -and $raw.Trim()) {
        try {
            $parsed = ConvertFrom-Json $raw
            if ($parsed -is [array]) { $enabled = $parsed } else { $enabled = @($parsed) }
        } catch {
            Write-Host "    [!] mevcut json okunamadi, sifirdan olusturulacak" -ForegroundColor DarkYellow
        }
    }
}

# Sadece başarılı kurulanları aktive et
foreach ($p in $Plugins) {
    $pluginDir = Join-Path $PluginsDir $p.id
    if ((Test-Path (Join-Path $pluginDir "main.js")) -and ($enabled -notcontains $p.id)) {
        $enabled += $p.id
    }
}

# JSON array olarak yaz (tek eleman bile array kalsın)
$json = "[`n  " + (($enabled | ForEach-Object { "`"$_`"" }) -join ",`n  ") + "`n]"
Set-Content -Path $ConfigFile -Value $json -Encoding UTF8
Write-Host "    [+] $($enabled.Count) eklenti aktif: $($enabled -join ', ')" -ForegroundColor Green
Write-Host ""

# Özet
Write-Host "=== Sonuc ===" -ForegroundColor Cyan
Write-Host "  Basarili: $ok / $($Plugins.Count)" -ForegroundColor Green
if ($fail -gt 0) {
    Write-Host "  Hatali  : $fail ($($failedPlugins -join ', '))" -ForegroundColor Red
    Write-Host ""
    Write-Host "Hatalilari Obsidian icinden manuel kurabilirsin:" -ForegroundColor DarkYellow
    Write-Host "  Settings -> Community Plugins -> Browse -> ara"
}
Write-Host ""
Write-Host ">>> SIRA SENDE:" -ForegroundColor Cyan
Write-Host "    1) Obsidian'i tamamen kapat (sistem tepsisinden de)"
Write-Host "    2) Tekrar ac"
Write-Host "    3) Settings -> Community Plugins'te kurulanlari gor"
Write-Host ""
