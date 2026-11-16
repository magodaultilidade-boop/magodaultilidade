Add-Type -AssemblyName System.Drawing
$src = "C:\Users\ALLAN\.gemini\antigravity\brain\440e60c7-235e-4fec-a091-425646f2194b\.user_uploaded\media_1794822318703_02b005e7.jpg"
$outPath = "C:\Users\ALLAN\Desktop\C&V\magodaultilidade\_Painel\powerbank_89_editado.jpg"
$img = [System.Drawing.Bitmap]::FromFile($src)
$bmp = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.DrawImage($img, 0, 0, $img.Width, $img.Height)

# Erase the white box from x=430 to 880, y=128 to 190
$brushWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$g.FillRectangle($brushWhite, 430, 128, 450, 62)

# Fonts
$fontSym = New-Object System.Drawing.Font("Arial", 18, [System.Drawing.FontStyle]::Bold)
$fontBig = New-Object System.Drawing.Font("Arial", 28, [System.Drawing.FontStyle]::Bold)
$fontPoupe = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$fontStrike = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Strikeout)

$brushRed = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(235, 30, 60))
$brushGrey = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(150, 150, 150))

# Draw R$ 89,90 in red
$startX = 438
$startY = 140

$g.DrawString("R$", $fontSym, $brushRed, [float]$startX, [float]($startY + 8))
$sizeSym = $g.MeasureString("R$", $fontSym)

$g.DrawString("89,90", $fontBig, $brushRed, [float]($startX + $sizeSym.Width - 4), [float]$startY)
$sizeBig = $g.MeasureString("89,90", $fontBig)

# Draw Poupe and Strikeout
$poupeX = $startX + $sizeSym.Width + $sizeBig.Width + 8
$g.DrawString("Poupe R$ 20,09", $fontPoupe, $brushRed, [float]$poupeX, [float]($startY + 5))
$g.DrawString("R$ 109,99", $fontStrike, $brushGrey, [float]$poupeX, [float]($startY + 21))

$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$g.Dispose()
$bmp.Dispose()
$img.Dispose()
"Salvo com sucesso em " + $outPath
