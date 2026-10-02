param([string]$OutputDirectory = (Join-Path $PSScriptRoot 'media'))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $chineseVoice = $voice.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -eq 'zh-CN' } | Select-Object -First 1
    if (-not $chineseVoice) { throw 'A local zh-CN voice is required for narration.' }
    $voice.SelectVoice($chineseVoice.VoiceInfo.Name)
    $voice.Rate = 2
    [void](New-Item -ItemType Directory -Path $OutputDirectory -Force)
    $lines = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'narration.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $voice.SetOutputToWaveFile((Join-Path $OutputDirectory ('narration-{0:D2}.wav' -f ($i + 1))))
        $voice.Speak($lines[$i])
        $voice.SetOutputToNull()
    }
    Write-Output ('Rendered {0} local narration segments.' -f $lines.Count)
} finally { $voice.Dispose() }
