// 1% Design Lab · /api/chat — 服务端代理, key 只存在 Cloudflare 环境变量
// 部署后配置: Pages Dashboard → Settings → Environment variables → GLM_KEY = <你的新key>

const ALLOWED_MODELS = new Set(['glm-4-flash', 'glm-5.3']);
const ALLOWED_ORIGINS = new Set([
  'https://1-design-lab.com',
  'https://www.1-design-lab.com',
  'http://localhost:8765',
  'http://127.0.0.1:8765'
]);
const MAX_CHARS = 8000;      // messages 总长度上限
const MAX_TOKENS = 800;      // 单次回复上限
const RATE_LIMIT = 15;       // 每 IP 窗口内请求数
const RATE_WINDOW = 5 * 60 * 1000;

const hits = new Map(); // best-effort 内存限速, 不持久

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : 'https://1-design-lab.com';
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  };
}

function limited(ip) {
  const now = Date.now();
  const rec = hits.get(ip);
  if (!rec || now - rec.t > RATE_WINDOW) {
    hits.set(ip, { t: now, n: 1 });
    if (hits.size > 5000) hits.clear(); // 防内存膨胀
    return false;
  }
  rec.n += 1;
  return rec.n > RATE_LIMIT;
}

export async function onRequestOptions({ request }) {
  return new Response(null, { status: 204, headers: corsHeaders(request.headers.get('Origin') || '') });
}

export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('Origin') || '';
  const h = corsHeaders(origin);

  if (!env.GLM_KEY) {
    return Response.json({ error: 'GLM_KEY not configured' }, { status: 503, headers: h });
  }

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (limited(ip)) {
    return Response.json({ error: 'too many requests' }, { status: 429, headers: h });
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return Response.json({ error: 'bad json' }, { status: 400, headers: h });
  }

  const model = ALLOWED_MODELS.has(body.model) ? body.model : 'glm-4-flash';
  const messages = Array.isArray(body.messages) ? body.messages : null;
  if (!messages || !messages.length) {
    return Response.json({ error: 'messages required' }, { status: 400, headers: h });
  }
  const total = messages.reduce((s, m) => s + (typeof m.content === 'string' ? m.content.length : 0), 0);
  if (total > MAX_CHARS) {
    return Response.json({ error: 'payload too large' }, { status: 413, headers: h });
  }

  const upstream = await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + env.GLM_KEY
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.7,
      max_tokens: MAX_TOKENS,
      stream: true
    })
  });

  if (!upstream.ok || !upstream.body) {
    return Response.json({ error: 'upstream ' + upstream.status }, { status: 502, headers: h });
  }

  // 流式透传
  return new Response(upstream.body, {
    status: 200,
    headers: Object.assign(h, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-store'
    })
  });
}
