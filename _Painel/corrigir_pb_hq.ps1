Add-Type -AssemblyName System.Drawing
$src = "C:\Users\ALLAN\.gemini\antigravity\brain\440e60c7-235e-4fec-a091-425646f2194b\.user_uploaded\media_1794822318703_02b005e7.jpg"
$outPath = "C:\Users\ALLAN\Desktop\C&V\magodaultilidade\_Painel\powerbank_89_editado.jpg"
$img = [System.Drawing.Bitmap]::FromFile($src)
$bmp = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.DrawImage($img, 0, 0, $img.Width, $img.Height)

# Completely erase the white area: x=384 to 887, y=125 to 192
$brushWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$g.FillRectangle($brushWhite, 384, 125, 503, 67)

# Fonts
$fontSym = New-Object System.Drawing.Font("Arial", 18, [System.Drawing.FontStyle]::Bold)
$fontBig = New-Object System.Drawing.Font("Arial", 30, [System.Drawing.FontStyle]::Bold)
$fontPoupe = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$fontStrike = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Strikeout)

$brushAliRed = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(236, 35, 27))
$brushGrey = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(153, 153, 153))

$startX = 402
$startY = 136

# Draw "R$"
$g.DrawString("R$", $fontSym, $brushAliRed, [float]$startX, [float]($startY + 10))
$sizeSym = $g.MeasureString("R$", $fontSym)

# Draw "89,90"
$g.DrawString("89,90", $fontBig, $brushAliRed, [float]($startX + $sizeSym.Width - 6), [float]$startY)
$sizeBig = $g.MeasureString("89,90", $fontBig)

# Draw Poupe & Strikeout
$poupeX = $startX + $sizeSym.Width + $sizeBig.Width + 10
$g.DrawString("Poupe R$ 20,09", $fontPoupe, $brushAliRed, [float]$poupeX, [float]($startY + 8))
$g.DrawString("R$ 109,99", $fontStrike, $brushGrey, [float]$poupeX, [float]($startY + 24))

# Save HQ JPEG
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
$encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
$encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]95)

$bmp.Save($outPath, $codec, $encoderParams)
$g.Dispose()
$bmp.Dispose()
$img.Dispose()
"HQ Salvo com sucesso!"
