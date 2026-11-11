Add-Type -AssemblyName System.Drawing

$bmp = New-Object System.Drawing.Bitmap 1024, 1024
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# 1. Fundo Escuro Moderno (#090d16)
$bgBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 9, 13, 22))
$g.FillRectangle($bgBrush, 0, 0, 1024, 1024)

# 2. Circulo Verde Neon Externo (#10b981)
$penNeon = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 16, 185, 129)), 16
$g.DrawEllipse($penNeon, 50, 50, 924, 924)

# 3. Monograma C&V Central
$fontCV = New-Object System.Drawing.Font ("Arial Black", [float]150, [System.Drawing.FontStyle]::Bold)
$whiteBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center

$g.DrawString("C&V", $fontCV, $whiteBrush, 512, 410, $sf)

# 4. Linha Divisoria
$penLine = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 16, 185, 129)), 8
$g.DrawLine($penLine, 240, 580, 784, 580)

# 5. Subtitulo COMPRA & VAREJO
$fontSub = New-Object System.Drawing.Font ("Arial", [float]44, [System.Drawing.FontStyle]::Bold)
$neonBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 16, 185, 129))
$g.DrawString("COMPRA & VAREJO", $fontSub, $neonBrush, 512, 660, $sf)

# 6. Tagline ITU • PRONTA ENTREGA
$fontTag = New-Object System.Drawing.Font ("Arial", [float]26, [System.Drawing.FontStyle]::Bold)
$grayBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 148, 163, 184))
$g.DrawString("ITU • PRONTA ENTREGA", $fontTag, $grayBrush, 512, 735, $sf)

$g.Dispose()

$dest = "c:\Users\ALLAN\Desktop\C&V\magodaultilidade\_Painel\logo_cv.png"
$bmp.Save($dest, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()

Write-Output "PNG gerado com sucesso em: $dest"
