// Supabase auth + usage tracking
// Shared by all tool pages

const SUPABASE_URL = 'https://zzxtgfjdbtfmibdfweoo.supabase.co';
const SUPABASE_ANON = 'sb_publishable_PsS6dz2iP5kOtuZgjhwU7Q_WblXz9QI';

// ── Supabase client (no bundler, plain fetch) ─────────────────────────────

async function sbRequest(path, method = 'GET', body = null, token = null) {
    const headers = {
        'apikey': SUPABASE_ANON,
        'Content-Type': 'application/json',
    };
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(SUPABASE_URL + path, opts);
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error_description || err.message || res.statusText);
    }
    return res.status === 204 ? null : res.json();
}

// ── Session ───────────────────────────────────────────────────────────────

let _session = null;

async function getSession() {
    if (_session) return _session;
    const raw = localStorage.getItem('sb_session');
    if (!raw) return null;
    try {
        const s = JSON.parse(raw);
        if (Date.now() / 1000 > s.expires_at - 60) {
            // Refresh
            const data = await sbRequest('/auth/v1/token?grant_type=refresh_token', 'POST',
                { refresh_token: s.refresh_token });
            _session = data;
            localStorage.setItem('sb_session', JSON.stringify(data));
        } else {
            _session = s;
        }
        return _session;
    } catch {
        localStorage.removeItem('sb_session');
        return null;
    }
}

async function signInWithOtp(email) {
    await sbRequest('/auth/v1/otp', 'POST', {
        email,
        create_user: true,
        options: { email_redirect_to: window.location.href }
    });
}

async function verifyOtp(email, token) {
    const data = await sbRequest('/auth/v1/verify', 'POST', {
        type: 'email',
        email,
        token
    });
    _session = data;
    localStorage.setItem('sb_session', JSON.stringify(data));
    return data;
}

async function signOut() {
    const s = await getSession();
    if (s) {
        await sbRequest('/auth/v1/logout', 'POST', {}, s.access_token).catch(() => {});
    }
    _session = null;
    localStorage.removeItem('sb_session');
}

function getUser() {
    if (!_session) return null;
    return _session.user || null;
}

// ── Usage tracking ────────────────────────────────────────────────────────
// For anonymous users: localStorage (fingerprintable / bypassable by design)
// For logged-in users: Supabase table `tool_usage`

const LOCAL_PREFIX = 'tool_uses_';

async function getUseCount(toolName) {
    const s = await getSession();
    if (s) {
        try {
            const rows = await sbRequest(
                `/rest/v1/tool_usage?user_id=eq.${s.user.id}&tool_name=eq.${toolName}&select=uses`,
                'GET', null, s.access_token
            );
            return rows && rows.length ? rows[0].uses : 0;
        } catch { /* fall through to localStorage */ }
    }
    return parseInt(localStorage.getItem(LOCAL_PREFIX + toolName) || '0');
}

async function incrementUseCount(toolName) {
    const s = await getSession();
    if (s) {
        try {
            const current = await getUseCount(toolName);
            await sbRequest('/rest/v1/tool_usage', 'POST', {
                user_id: s.user.id,
                tool_name: toolName,
                uses: current + 1
            }, s.access_token);
            // If row already exists, upsert via PATCH
        } catch {
            try {
                const current = await getUseCount(toolName);
                await sbRequest(
                    `/rest/v1/tool_usage?user_id=eq.${s.user.id}&tool_name=eq.${toolName}`,
                    'PATCH', { uses: current + 1 }, s.access_token
                );
            } catch { /* ignore */ }
        }
        return;
    }
    const n = parseInt(localStorage.getItem(LOCAL_PREFIX + toolName) || '0') + 1;
    localStorage.setItem(LOCAL_PREFIX + toolName, n);
}

// ── Auth modal (shared UI) ────────────────────────────────────────────────

function injectAuthModal() {
    if (document.getElementById('authModal')) return;
    const el = document.createElement('div');
    el.innerHTML = `
<style>
.auth-modal-overlay{display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);align-items:center;justify-content:center;padding:20px}
.auth-modal-overlay.open{display:flex}
.auth-modal-box{background:#1c1c1c;border:1px solid rgba(82,82,91,.55);border-radius:24px;padding:36px 32px;max-width:380px;width:100%;text-align:center;position:relative}
.auth-modal-close{position:absolute;top:14px;right:16px;background:none;border:none;color:rgba(166,166,176,.7);font-size:22px;cursor:pointer;line-height:1}
.auth-modal-close:hover{color:#fff}
.auth-modal-icon{font-size:36px;margin-bottom:12px}
.auth-modal-title{font-size:20px;font-weight:700;color:#fafafa;margin-bottom:6px}
.auth-modal-sub{font-size:13px;color:rgba(166,166,176,1);margin-bottom:24px;line-height:1.6}
.auth-modal-input{width:100%;padding:12px 16px;background:#232323;border:1px solid rgba(82,82,91,.55);border-radius:12px;color:#fafafa;font-size:14px;font-family:inherit;box-sizing:border-box;transition:border-color .2s;margin-bottom:12px}
.auth-modal-input:focus{outline:none;border-color:rgba(87,255,195,.5)}
.auth-modal-btn{width:100%;padding:13px;border:none;border-radius:12px;background:hsl(159,100%,67%);color:#0f1b16;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;transition:transform .18s,box-shadow .18s;margin-bottom:8px}
.auth-modal-btn:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(87,255,195,.3)}
.auth-modal-btn:disabled{opacity:.45;cursor:not-allowed;transform:none;box-shadow:none}
.auth-modal-note{font-size:11px;color:rgba(166,166,176,.7);line-height:1.6}
.auth-modal-err{font-size:12px;color:#ff6b6b;margin-bottom:10px;display:none}
.auth-modal-success{font-size:14px;color:hsl(159,100%,67%);margin-bottom:10px;display:none}
</style>
<div class="auth-modal-overlay" id="authModal">
  <div class="auth-modal-box">
    <button class="auth-modal-close" id="authModalClose">&times;</button>

    <!-- Step 1: email -->
    <div id="authStep1">
      <div class="auth-modal-icon">&#128274;</div>
      <div class="auth-modal-title" id="authModalTitle">登录后继续使用</div>
      <div class="auth-modal-sub" id="authModalSub">登录即可解锁更多免费次数，跨设备保存你的使用记录</div>
      <div class="auth-modal-err" id="authErr"></div>
      <input class="auth-modal-input" id="authEmail" type="email" placeholder="你的邮箱地址">
      <button class="auth-modal-btn" id="authSendBtn" onclick="authSendCode()">发送验证码 →</button>
      <p class="auth-modal-note">发送一封免密登录邮件，无需设置密码</p>
    </div>

    <!-- Step 2: OTP -->
    <div id="authStep2" style="display:none">
      <div class="auth-modal-icon">&#128140;</div>
      <div class="auth-modal-title">输入验证码</div>
      <div class="auth-modal-sub" id="authOtpSub"></div>
      <div class="auth-modal-err" id="authOtpErr"></div>
      <input class="auth-modal-input" id="authOtp" type="text" inputmode="numeric" pattern="[0-9]*" placeholder="6位验证码" maxlength="6">
      <button class="auth-modal-btn" id="authVerifyBtn" onclick="authVerifyCode()">验证登录 →</button>
      <div class="auth-modal-success" id="authSuccessMsg">✓ 登录成功！</div>
      <p class="auth-modal-note">没收到？检查垃圾邮件，或 <a href="#" onclick="authBack();return false" style="color:hsl(159,100%,67%)">重新发送</a></p>
    </div>
  </div>
</div>`;
    document.body.appendChild(el);

    document.getElementById('authModalClose').addEventListener('click', closeAuthModal);
    document.getElementById('authModal').addEventListener('click', e => {
        if (e.target === document.getElementById('authModal')) closeAuthModal();
    });
}

let _authCallback = null;

function openAuthModal(opts = {}) {
    injectAuthModal();
    if (opts.title) document.getElementById('authModalTitle').textContent = opts.title;
    if (opts.sub) document.getElementById('authModalSub').textContent = opts.sub;
    _authCallback = opts.onSuccess || null;
    document.getElementById('authStep1').style.display = 'block';
    document.getElementById('authStep2').style.display = 'none';
    document.getElementById('authErr').style.display = 'none';
    document.getElementById('authEmail').value = '';
    document.getElementById('authModal').classList.add('open');
}

function closeAuthModal() {
    const m = document.getElementById('authModal');
    if (m) m.classList.remove('open');
}

function authBack() {
    document.getElementById('authStep1').style.display = 'block';
    document.getElementById('authStep2').style.display = 'none';
}

async function authSendCode() {
    const email = document.getElementById('authEmail').value.trim();
    const errEl = document.getElementById('authErr');
    if (!email || !email.includes('@')) {
        errEl.textContent = '请输入有效的邮箱地址';
        errEl.style.display = 'block';
        return;
    }
    errEl.style.display = 'none';
    const btn = document.getElementById('authSendBtn');
    btn.disabled = true;
    btn.textContent = '发送中…';
    try {
        await signInWithOtp(email);
        document.getElementById('authOtpSub').textContent = `验证码已发送至 ${email}`;
        document.getElementById('authStep1').style.display = 'none';
        document.getElementById('authStep2').style.display = 'block';
        document.getElementById('authOtp').focus();
    } catch (e) {
        errEl.textContent = '发送失败：' + e.message;
        errEl.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = '发送验证码 →';
    }
}

async function authVerifyCode() {
    const email = document.getElementById('authEmail').value.trim();
    const token = document.getElementById('authOtp').value.trim();
    const errEl = document.getElementById('authOtpErr');
    if (token.length < 6) {
        errEl.textContent = '请输入6位验证码';
        errEl.style.display = 'block';
        return;
    }
    errEl.style.display = 'none';
    const btn = document.getElementById('authVerifyBtn');
    btn.disabled = true;
    btn.textContent = '验证中…';
    try {
        await verifyOtp(email, token);
        document.getElementById('authSuccessMsg').style.display = 'block';
        setTimeout(() => {
            closeAuthModal();
            if (_authCallback) _authCallback();
        }, 800);
    } catch (e) {
        errEl.textContent = '验证码错误或已过期，请重试';
        errEl.style.display = 'block';
        btn.disabled = false;
        btn.textContent = '验证登录 →';
    }
}

// ── Render logged-in header badge (optional helper) ───────────────────────

async function renderAuthBadge(containerId) {
    const s = await getSession();
    const el = document.getElementById(containerId);
    if (!el) return;
    if (s) {
        const email = s.user.email;
        el.innerHTML = `<span style="font-size:12px;color:rgba(166,166,176,1)">&#10003; ${email}</span>
            <button onclick="authSignOutAndReload()" style="margin-left:8px;font-size:11px;color:rgba(87,255,195,.7);background:none;border:none;cursor:pointer;font-family:inherit">退出</button>`;
    } else {
        el.innerHTML = `<button onclick="openAuthModal()" style="font-size:12px;color:hsl(159,100%,67%);background:none;border:none;cursor:pointer;font-family:inherit;text-decoration:underline">登录</button>`;
    }
}

async function authSignOutAndReload() {
    await signOut();
    window.location.reload();
}
