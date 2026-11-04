/**
 * api.js — Backend Express para o Avatar Generator
 * Expõe as ferramentas do server.js via endpoints REST
 * Execute: node api.js → http://localhost:3000
 */

const express = require('express');
const cors    = require('cors');
const multer  = require('multer');
const path    = require('path');
const fs      = require('fs');
const os      = require('os');

const { transformMagoToAvatar, createAvatarFromScratch, batchAvatarGeneration } = require('./server');

const app  = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.static('.'));  // Serve avatar-generator.html e arquivos estáticos

// Upload para pasta temporária
const upload = multer({
    dest:   os.tmpdir(),
    limits: { fileSize: 10 * 1024 * 1024 }, // 10MB max
    fileFilter: (req, file, cb) => {
        const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
        allowed.includes(file.mimetype) ? cb(null, true) : cb(new Error('Só imagens são aceitas (jpg, png, webp)'));
    }
});

// ── Endpoint 1: Transformar imagem do mago em prompt de avatar ───────────────
app.post('/api/generate-avatar', upload.single('image'), async (req, res) => {
    const tmpPath = req.file?.path;
    try {
        // Parse config do body (pode vir como string JSON)
        let config = {};
        if (req.body.config) {
            try { config = JSON.parse(req.body.config); } catch {}
        } else {
            // Aceita campos individuais
            const { hatColor, outfitStyle, beardStyle, background, addStaff, viewAngle } = req.body;
            if (hatColor)    config.hatColor    = hatColor;
            if (outfitStyle) config.outfitStyle = outfitStyle;
            if (beardStyle)  config.beardStyle  = beardStyle;
            if (background)  config.background  = background;
            if (viewAngle)   config.viewAngle   = viewAngle;
            if (addStaff !== undefined) config.addStaff = addStaff === 'true';
        }

        console.log(`📥 [generate-avatar] imagem: ${req.file?.originalname || 'nenhuma'} | config:`, config);

        const result = await transformMagoToAvatar({
            imagePath: tmpPath || null,
            config
        });

        res.json(result);

    } catch (err) {
        console.error('❌ Erro em /api/generate-avatar:', err.message);
        res.status(500).json({ success: false, error: err.message });
    } finally {
        if (tmpPath && fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
    }
});

// ── Endpoint 2: Criar avatar do zero por descrição textual ───────────────────
app.post('/api/create-avatar', async (req, res) => {
    try {
        const { description, config = {} } = req.body;
        if (!description) return res.status(400).json({ success: false, error: 'Campo "description" é obrigatório' });

        console.log(`📥 [create-avatar] descrição: "${description}"`);
        const result = await createAvatarFromScratch({ description, config });
        res.json(result);

    } catch (err) {
        console.error('❌ Erro em /api/create-avatar:', err.message);
        res.status(500).json({ success: false, error: err.message });
    }
});

// ── Endpoint 3: Gerar múltiplas variações em batch ──────────────────────────
app.post('/api/batch', upload.single('image'), async (req, res) => {
    const tmpPath = req.file?.path;
    try {
        let variations = [];
        if (req.body.variations) {
            try { variations = JSON.parse(req.body.variations); } catch {}
        }

        console.log(`📥 [batch] variações solicitadas: ${variations.length || 'padrão (4)'}`);

        const result = await batchAvatarGeneration({
            imagePath:  tmpPath || null,
            variations
        });

        res.json(result);

    } catch (err) {
        console.error('❌ Erro em /api/batch:', err.message);
        res.status(500).json({ success: false, error: err.message });
    } finally {
        if (tmpPath && fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
    }
});

// ── Health check ─────────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
    res.json({
        status:  'ok',
        version: '1.0.0',
        api_key: (process.env.GEMINI_API_KEY || 'AIzaSyDh_PV3JXo6Ms_5alnpA30bxaleq0DjMVs') ? '✅ configurada (Gemini)' : '❌ não configurada',
        endpoints: [
            'POST /api/generate-avatar  — imagem → prompt de avatar',
            'POST /api/create-avatar    — texto → prompt de avatar',
            'POST /api/batch           — imagem → múltiplos prompts',
        ]
    });
});

// ── Iniciar servidor ─────────────────────────────────────────────────────────
app.listen(PORT, () => {
    console.log(`
╔══════════════════════════════════════════════════════╗
║  🧙 Mago Avatar API — rodando!                      ║
║  http://localhost:${PORT}                              ║
╠══════════════════════════════════════════════════════╣
║  Interface:  http://localhost:${PORT}/avatar-generator.html ║
║  Health:     http://localhost:${PORT}/health           ║
╚══════════════════════════════════════════════════════╝
`);
    console.log('✅ Servidor pronto — chave Gemini carregada via server.js\n');
});
