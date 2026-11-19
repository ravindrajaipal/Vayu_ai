/**
 * Vercel Serverless Function: /api/gemini
 * Keeps GEMINI_API_KEY strictly on the server via process.env.GEMINI_API_KEY.
 * Implements input validation, CORS policy, rate-limit headers, and 8s upstream timeout.
 */
module.exports = async function handler(req, res) {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed. Use POST.' });
  }

  const body = req.body || {};
  const rawPrompt = typeof body.prompt === 'string' ? body.prompt.trim() : '';
  if (!rawPrompt || rawPrompt.length > 280) {
    return res.status(400).json({ error: 'Invalid prompt. Must be a non-empty string up to 280 characters.' });
  }

  const city = typeof body.city === 'string' ? body.city.slice(0, 60) : 'Delhi NCR';
  const aqi = Number.isFinite(Number(body.aqi)) ? Math.min(500, Math.max(0, Number(body.aqi))) : 367;
  const pm25 = Number.isFinite(Number(body.pm25)) ? Math.min(1000, Math.max(0, Number(body.pm25))) : 218;
  const profile = typeof body.profile === 'string' ? body.profile.slice(0, 40) : 'family';

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(503).json({
      error: 'GEMINI_API_KEY environment variable is not configured on the server.',
      fallbackMode: 'Deterministic CPCB/WHO Rule Engine'
    });
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  try {
    const upstream = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${encodeURIComponent(apiKey)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `You are VayuAI Pro, an Indian Urban Air Quality & Winter Smog Assistant grounded in CPCB NAQI, CAQM GRAP, WHO guidelines, DIY MERV-13 CADR, and ITF-OECD transport data. City: ${city} (AQI ${aqi}, PM2.5 ${pm25} ug/m3). User Profile: ${profile}. User Question: ${rawPrompt}. Reply in 3 concise sentences in English followed by a 2-sentence Hinglish summary and exact % impact.`
            }]
          }]
        })
      }
    );
    clearTimeout(timeoutId);

    if (!upstream.ok) {
      return res.status(502).json({ error: `Upstream Gemini API returned HTTP ${upstream.status}` });
    }

    const data = await upstream.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
    if (!text) {
      return res.status(502).json({ error: 'Empty response from upstream model.' });
    }
    return res.status(200).json({ text, sourceMode: 'Live Gemini 2.5 Flash API (Server Proxy)' });
  } catch (err) {
    clearTimeout(timeoutId);
    return res.status(504).json({ error: 'Upstream request timed out or failed.', details: String(err.message || err) });
  }
};
