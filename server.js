#!/usr/bin/env node
/**
 * MCP Mago Avatar Generator — server.js
 * Servidor MCP principal com 3 ferramentas para gerar avatares estilo Xbox 3D
 * a partir da imagem do Mago das Utilidades.
 *
 * ✅ Usa Google Gemini (GRATUITO — 1500 req/dia)
 * Chave gratuita em: https://aistudio.google.com/apikey
 *
 * Ferramentas:
 *  1. transform_mago_to_avatar   — imagem real → prompt de avatar Xbox
 *  2. create_avatar_from_scratch — descrição textual → prompt de avatar
 *  3. batch_avatar_generation    — imagem + variações → múltiplos prompts
 */

const fs   = require('fs');
const path = require('path');
const https = require('https');

// ─── Verificar API Key ───────────────────────────────────────────────────────
// Prioridade: variável de ambiente > chave local no arquivo
// Chave GRATUITA em: https://aistudio.google.com/apikey
const GEMINI_API_KEY_LOCAL = 'AIzaSyDh_PV3JXo6Ms_5alnpA30bxaleq0DjMVs';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || GEMINI_API_KEY_LOCAL;
const GEMINI_MODEL   = 'gemini-flash-latest'; // Alias estável disponível na API v1beta em 2026
const GEMINI_URL     = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`;

/** 
 * Chama a API REST do Gemini. 
 * parts = array de {text: "..."} ou {inlineData: {mimeType, data}} 
 */
function geminiCall(parts, systemInstruction = '') {
    return new Promise((resolve, reject) => {
        const payload = {
            contents: [{ role: 'user', parts }]
        };

        if (systemInstruction) {
            payload.system_instruction = { parts: [{ text: systemInstruction }] };
        }

        const body = JSON.stringify(payload);

        const url = new URL(GEMINI_URL);
        const options = {
            hostname: url.hostname,
            path:     url.pathname + url.search,
            method:   'POST',
            headers:  { 
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            },
        };

        const req = https.request(options, res => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.error) return reject(new Error(`Gemini API Error: ${json.error.message}`));
                    const text = json.candidates?.[0]?.content?.parts?.[0]?.text || '';
                    if (!text) {
                        console.error('Gemini Resposta Vazia:', JSON.stringify(json, null, 2));
                        return reject(new Error('Resposta vazia da API do Gemini'));
                    }
                    resolve(text);
                } catch (e) { 
                    console.error('Erro ao processar JSON do Gemini:', data);
                    reject(e); 
                }
            });
        });

        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

// ─── Configurações padrão do avatar ─────────────────────────────────────────
const AVATAR_DEFAULTS = {
    hatColor:    'azul royal',
    outfitStyle: 'mago medieval',
    beardStyle:  'barba longa branca',
    background:  'transparente',
    addStaff:    true,
    renderStyle: 'Xbox 360 avatar 3D cartoon',
    viewAngle:   'vista frontal ligeiramente diagonal',
};

// ─── Prompt base para avatar Xbox ───────────────────────────────────────────
function buildAvatarBasePrompt(config = {}) {
    const c = { ...AVATAR_DEFAULTS, ...config };
    return `
Crie um avatar 3D estilo Xbox 360 / cartoon tridimensinal de um mago das utilidades com as seguintes características:

ESTILO VISUAL:
- Renderização 3D cartoon no estilo Xbox 360 Avatar / Pixar
- Proporções ligeiramente exageradas (cabeça grande, corpo robusto)
- Superfícies com brilho suave (material plástico/cartoon)
- Iluminação três pontos com borda luminosa
- Ângulo: ${c.viewAngle}
- Fundo: ${c.background}

PERSONAGEM:
- Chapéu de mago cônico alto, cor: ${c.hatColor}, com estrelas e detalhes dourados
- Robe/manto longo, estilo: ${c.outfitStyle}
- Barba: ${c.beardStyle}
- Expressão amigável e sábia, olhos expressivos grandes
- Pele com tom dourado-bege cartoon
${c.addStaff ? '- Cajado mágico na mão direita com cristal brilhante na ponta' : ''}

QUALIDADE:
- Alta definição, bordas suaves sem pixelização
- Sombras suaves realistas
- Reflexos especulares nos olhos
- Proporções heroicas mas acessíveis

Render this as a high-quality 3D cartoon character, Xbox-avatar style, full body visible.
`.trim();
}

// ─── Analisar imagem com Gemini Vision ───────────────────────────────────────
async function analyzeWizardImage(imagePath) {
    const absPath = path.resolve(imagePath);
    if (!fs.existsSync(absPath)) {
        throw new Error(`Imagem não encontrada: ${absPath}`);
    }

    const ext = path.extname(absPath).toLowerCase().replace('.', '');
    const mediaTypeMap = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', gif: 'image/gif' };
    const mimeType = mediaTypeMap[ext] || 'image/jpeg';

    const imageData = fs.readFileSync(absPath);
    const base64    = imageData.toString('base64');

    console.log(`📸 Analisando imagem com Gemini Vision: ${path.basename(absPath)}...`);

    const text = await geminiCall(
        [
            { inlineData: { data: base64, mimeType } },
            { text: `Analise esta imagem de um mago e descreva em detalhes:
1. Cores predominantes (chapéu, manto, pele)
2. Estilo da barba e cabelo
3. Acessórios (cajado, cristal, etc.)
4. Expressão facial
5. Características únicas

Responda em formato JSON com as chaves: hatColor, robeColor, beardStyle, accessories, expression, uniqueFeatures` }
        ],
        "Você é um assistente especializado em análise visual e descrição de personagens."
    );

    try {
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (jsonMatch) return JSON.parse(jsonMatch[0]);
    } catch {}

    return { raw: text };
}

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 1: transform_mago_to_avatar
// ─────────────────────────────────────────────────────────────────────────────
async function transformMagoToAvatar({ imagePath, config = {} }) {
    console.log('\n🔮 Ferramenta: transform_mago_to_avatar');

    let imageAnalysis = null;
    let analysisText  = '';

    if (imagePath) {
        try {
            imageAnalysis = await analyzeWizardImage(imagePath);
            analysisText  = `\nCaracterísticas detectadas na imagem original:\n${JSON.stringify(imageAnalysis, null, 2)}\n`;
        } catch (err) {
            console.warn(`⚠️  Não foi possível analisar a imagem: ${err.message}`);
        }
    }

    const mergedConfig = {
        hatColor:    imageAnalysis?.hatColor    || config.hatColor    || AVATAR_DEFAULTS.hatColor,
        beardStyle:  imageAnalysis?.beardStyle  || config.beardStyle  || AVATAR_DEFAULTS.beardStyle,
        outfitStyle: config.outfitStyle || AVATAR_DEFAULTS.outfitStyle,
        background:  config.background  || AVATAR_DEFAULTS.background,
        addStaff:    config.addStaff !== undefined ? config.addStaff : AVATAR_DEFAULTS.addStaff,
    };

    const basePrompt = buildAvatarBasePrompt(mergedConfig);

    const finalPrompt = (await geminiCall([
        { text: `Você é um especialista em criar prompts para geradores de imagem IA.\n${analysisText}\nBaseado nas características acima, melhore e otimize este prompt para gerar um avatar no estilo Xbox 360:\n\n${basePrompt}\n\nRetorne APENAS o prompt final otimizado, sem explicações. O prompt deve ser em inglês para melhor compatibilidade com DALL-E e Midjourney.` }
    ])).trim();

    return {
        success: true,
        tool:    'transform_mago_to_avatar',
        prompt:  finalPrompt,
        config:  mergedConfig,
        imageAnalysis,
        usage: {
            dalle:      `Use em: https://chat.openai.com → Image → DALL-E`,
            midjourney: `Use em Discord: /imagine ${finalPrompt}`,
            stable:     `Use em: https://stability.ai ou Automatic1111`,
        }
    };
}

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 2: create_avatar_from_scratch
// ─────────────────────────────────────────────────────────────────────────────
async function createAvatarFromScratch({ description, config = {} }) {
    console.log('\n✨ Ferramenta: create_avatar_from_scratch');

    const mergedConfig = { ...AVATAR_DEFAULTS, ...config };
    const basePrompt   = buildAvatarBasePrompt(mergedConfig);

    const finalPrompt = (await geminiCall([
        { text: `Você é um especialista em prompts para IA de imagem.\n\nCrie um prompt detalhado em inglês para gerar um avatar de mago estilo Xbox 360 com base na seguinte descrição:\n"${description}"\n\nUse este template como base:\n${basePrompt}\n\nRetorne APENAS o prompt final em inglês, otimizado para DALL-E 3 / Midjourney.` }
    ])).trim();

    return {
        success:     true,
        tool:        'create_avatar_from_scratch',
        description,
        prompt:      finalPrompt,
        config:      mergedConfig,
    };
}

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 3: batch_avatar_generation
// ─────────────────────────────────────────────────────────────────────────────
async function batchAvatarGeneration({ imagePath, variations = [] }) {
    console.log('\n⚗️  Ferramenta: batch_avatar_generation');

    const defaultVariations = [
        { hatColor: 'azul royal', outfitStyle: 'mago clássico',   background: 'transparente' },
        { hatColor: 'roxo',       outfitStyle: 'mago sombrio',    background: 'névoa mágica' },
        { hatColor: 'ouro',       outfitStyle: 'mago real',       background: 'biblioteca mágica' },
        { hatColor: 'preto',      outfitStyle: 'mago das trevas', background: 'chamas roxas' },
    ];

    const targetVariations = variations.length > 0 ? variations : defaultVariations;
    const results = [];

    for (let i = 0; i < targetVariations.length; i++) {
        const variation = targetVariations[i];
        console.log(`  Variação ${i + 1}/${targetVariations.length}: chapéu ${variation.hatColor}...`);
        const result = await transformMagoToAvatar({ imagePath, config: variation });
        results.push({
            variation: i + 1,
            label:     `${variation.outfitStyle} — Chapéu ${variation.hatColor}`,
            prompt:    result.prompt,
            config:    variation,
        });
    }

    return {
        success:    true,
        tool:       'batch_avatar_generation',
        total:      results.length,
        variations: results,
    };
}

// ─── Interface CLI simples ────────────────────────────────────────────────────
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`
╔══════════════════════════════════════════════════════╗
║       🧙 MCP Mago Avatar Generator v2.0.0           ║
║       ✅ Powered by Google Gemini (GRATUITO)        ║
╠══════════════════════════════════════════════════════╣
║  1. Transformar imagem:                              ║
║     node server.js transform <caminho-imagem>        ║
║                                                      ║
║  2. Criar do zero:                                   ║
║     node server.js create "descrição do mago"       ║
║                                                      ║
║  3. Gerar em batch:                                  ║
║     node server.js batch <caminho-imagem>            ║
║                                                      ║
║  Para a interface web:                               ║
║     npm run api  →  http://localhost:3000            ║
╚══════════════════════════════════════════════════════╝
`);
        return;
    }

    const command = args[0];

    try {
        let result;

        if (command === 'transform') {
            const imagePath = args[1];
            if (!imagePath) throw new Error('Informe o caminho da imagem: node server.js transform <imagem>');
            result = await transformMagoToAvatar({ imagePath });

        } else if (command === 'create') {
            const description = args.slice(1).join(' ');
            if (!description) throw new Error('Informe a descrição: node server.js create "descrição"');
            result = await createAvatarFromScratch({ description });

        } else if (command === 'batch') {
            const imagePath = args[1];
            result = await batchAvatarGeneration({ imagePath });

        } else {
            throw new Error(`Comando desconhecido: ${command}. Use: transform, create, batch`);
        }

        console.log('\n✅ Resultado:\n');
        console.log(JSON.stringify(result, null, 2));

    } catch (err) {
        console.error(`\n❌ Erro: ${err.message}`);
        process.exit(1);
    }
}

// ─── Exportar funções para uso como módulo (api.js) ──────────────────────────
module.exports = { transformMagoToAvatar, createAvatarFromScratch, batchAvatarGeneration };

// Executar CLI se chamado diretamente
if (require.main === module) main();
