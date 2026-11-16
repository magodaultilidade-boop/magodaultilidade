Add-Type -AssemblyName System.Drawing
$src = "C:\Users\ALLAN\.gemini\antigravity\brain\440e60c7-235e-4fec-a091-425646f2194b\.user_uploaded\media_1794820842580_0fd5105c.jpg"
$outPath = "C:\Users\ALLAN\Desktop\C&V\magodaultilidade\_Painel\redragon_143_editado.jpg"
$img = [System.Drawing.Bitmap]::FromFile($src)
$bmp = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.DrawImage($img, 0, 0, $img.Width, $img.Height)

# Erase the area from y=220 to y=330, x=375 to 650 with white
$brushWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$g.FillRectangle($brushWhite, 375, 220, 300, 120)

# Draw the big price R$ 143,43 in Mercado Livre style
$fontSym = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Regular)
$fontBig = New-Object System.Drawing.Font("Segoe UI", 32, [System.Drawing.FontStyle]::Regular)
$fontCents = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Regular)
$fontSub = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Regular)

$brushPrice = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(51, 51, 51))
$brushSub = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(102, 102, 102))

# Positions
$startX = 380
$startY = 240

$g.DrawString("R$", $fontSym, $brushPrice, [float]$startX, [float]($startY + 4))
$sizeSym = $g.MeasureString("R$", $fontSym)

$g.DrawString("143", $fontBig, $brushPrice, [float]($startX + $sizeSym.Width - 6), [float]($startY - 8))
$sizeBig = $g.MeasureString("143", $fontBig)

$g.DrawString("43", $fontCents, $brushPrice, [float]($startX + $sizeSym.Width + $sizeBig.Width - 16), [float]($startY + 2))

$g.DrawString("em 10x R$ 14,34 sem juros", $fontSub, $brushSub, [float]$startX, [float]($startY + 42))

$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$g.Dispose()
$bmp.Dispose()
$img.Dispose()
"Salvo com sucesso em " + $outPath
