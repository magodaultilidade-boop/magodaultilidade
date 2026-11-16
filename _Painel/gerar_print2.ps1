Add-Type -AssemblyName System.Drawing
$src = "C:\Users\ALLAN\.gemini\antigravity\brain\440e60c7-235e-4fec-a091-425646f2194b\.user_uploaded\media_1794820842580_0fd5105c.jpg"
$outPath = "C:\Users\ALLAN\Desktop\C&V\magodaultilidade\_Painel\redragon_blackfriday_143.jpg"
$img = [System.Drawing.Bitmap]::FromFile($src)
$bmp = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.DrawImage($img, 0, 0, $img.Width, $img.Height)

# Erase the area below Black Friday: y=242 to y=330, x=375 to 650 with white
$brushWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$g.FillRectangle($brushWhite, 375, 242, 300, 100)

# Fonts
$fontStrike = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Strikeout)
$fontSym = New-Object System.Drawing.Font("Segoe UI", 15, [System.Drawing.FontStyle]::Regular)
$fontBig = New-Object System.Drawing.Font("Segoe UI", 30, [System.Drawing.FontStyle]::Regular)
$fontCents = New-Object System.Drawing.Font("Segoe UI", 15, [System.Drawing.FontStyle]::Regular)
$fontGreen = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$fontSub = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Regular)

$brushGrey = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(140, 140, 140))
$brushPrice = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(51, 51, 51))
$brushGreen = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(0, 166, 80))
$brushSub = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(100, 100, 100))

# Positions
$startX = 380
$startY = 248

# Draw R$ 189,90 crossed out
$g.DrawString("R$ 189,90", $fontStrike, $brushGrey, [float]$startX, [float]$startY)

# Draw R$ 143,43 big
$pY = $startY + 18
$g.DrawString("R$", $fontSym, $brushPrice, [float]$startX, [float]($pY + 4))
$sizeSym = $g.MeasureString("R$", $fontSym)

$g.DrawString("143", $fontBig, $brushPrice, [float]($startX + $sizeSym.Width - 6), [float]($pY - 8))
$sizeBig = $g.MeasureString("143", $fontBig)

$g.DrawString("43", $fontCents, $brushPrice, [float]($startX + $sizeSym.Width + $sizeBig.Width - 16), [float]($pY + 2))
$sizeCents = $g.MeasureString("43", $fontCents)

# Draw 24% OFF in Green
$g.DrawString("24% OFF", $fontGreen, $brushGreen, [float]($startX + $sizeSym.Width + $sizeBig.Width + $sizeCents.Width - 14), [float]($pY + 3))

$g.DrawString("em 10x R$ 14,34 sem juros", $fontSub, $brushSub, [float]$startX, [float]($pY + 38))

$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$g.Dispose()
$bmp.Dispose()
$img.Dispose()
"Salvo com sucesso em " + $outPath
