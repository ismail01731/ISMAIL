param(
    [string]$Setting,
    [int]$Value
)

$cssPath = ".\frontend\style.css"

if (!(Test-Path $cssPath)) {
    Write-Host "style.css not found." -ForegroundColor Red
    exit
}

switch ($Setting) {

    "input-up" {

        $css = Get-Content $cssPath -Raw

        $controlStart = "/* ISMAIL UI CONTROL - INPUT POSITION */"
        $controlEnd = "/* ISMAIL UI CONTROL - END */"

        $newBlock = @"
$controlStart
@media (max-width: 600px) {
    .chat-input-area {
        position: relative;
        bottom: ${Value}px;
    }
}
$controlEnd
"@

        if ($css.Contains($controlStart)) {

            $pattern = [regex]::Escape($controlStart) +
                       "[\s\S]*?" +
                       [regex]::Escape($controlEnd)

            $css = [regex]::Replace(
                $css,
                $pattern,
                $newBlock
            )

        } else {

            $css = $css.TrimEnd() + "`r`n`r`n" + $newBlock
        }

        Set-Content -Path $cssPath -Value $css -Encoding UTF8

        Write-Host "Mobile input bar moved UP by $Value px." -ForegroundColor Green
    }

    default {

        Write-Host "Unknown setting: $Setting" -ForegroundColor Yellow
        Write-Host "Available setting: input-up"
    }
}