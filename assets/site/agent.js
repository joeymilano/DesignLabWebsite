/* 1% Design Lab · 小梦 AI 助手
   免费 AI: Puter.js (js.puter.com) 懒加载, 不可用时回退本地知识库 */
(function () {
  'use strict';
  if (window.__agentInit) return; window.__agentInit = true;

  var KNOWLEDGE = [
    { k: ['价格', '收费', '多少钱', '费用', '报价', '预算'],
      a: '两条业务的价格都不一样\n\n【作品集学院】\n· 作品集原创设计 ¥100 起\n· 留学生作业辅导 ¥200 起\n· 博士研究计划 ¥100 起\n· 上海线下个展 ¥99.69 起\n· 设计师求职辅导 ¥100 起\n\n【产品工作室】\n· AI 应用 MVP：14 天上线，按范围报价\n\n起步价对应最小规模需求，最终看项目范围和周期，可以先聊聊帮你评估' },
    { k: ['作品集', '留学', '申请', '艺术', 'portfolio'],
      a: '作品集学院做了 6 年，6,000+ 服务案例，学员拿过 600+ 名校 offer（RCA、UCL、哥大、宾大、MIT、CMU、米兰理工、代尔夫特等）\n\n覆盖产品、交互、工业、建筑、景观、服装、视觉媒体，也做博士研究计划（RP）和留学生作业辅导\n\n导师一对一推进，不套模板，从你自己的经历里提炼叙事，你想申什么方向？' },
    { k: ['导师', '老师', 'joey', '团队', '谁带'],
      a: '核心导师 5 位\n\n· Joey：米兰理工产品设计硕士，创始人，带过全球 200+ 学员，学员拿过 40+ 顶尖 offer\n· Jackie：格拉斯哥 HCI 博士，辅导博士申请和交互方向\n· 学小嵩：奥斯陆建筑与设计学院，系统设计策略 / 插画 / 3D\n· 程越：马兰欧尼 + 皇家艺术学院，服装 / 平面 / 动态\n· Jason：UC Berkeley 建筑硕士，建筑 / 景观 / 城市设计\n\n每位学员按专业方向匹配导师，一对一推进' },
    { k: ['产品', '开发', '网站', 'app', 'mvp', '全栈', '外包', '做软件'],
      a: '产品工作室为创业者把产品做上线\n\n· AI 应用 MVP：最快 14 天上线\n· 产品设计 × 全栈开发\n· LOGO / 品牌 VI\n· 工业设计 / 3D\n\n已交付 20+ 数字产品（自研的 Finfold、BillVampire 都在跑），业务操盘经验 $100M+，可以一句话需求先评估可行性' },
    { k: ['时间', '周期', '多久', 'ddl', '来得及', '时间线'],
      a: '作品集一般建议留 4–6 个月：项目取舍 → 设计执行 → 排版打磨 → 网申提交\n\n也有学员考研出分后临时转留学，3 个月倒推 DDL 做完的案例（最后拿了哥大和宾大）\n\n告诉我你的专业和目标院校，我帮你倒推一个时间线' },
    { k: ['微信', '联系', '咨询', '怎么报名', '下单', '淘宝'],
      a: '最直接的方式是微信咨询——点下面的「微信咨询」按钮扫码，或点右下角对话框按钮\n\n也可以淘宝店铺下单，Email 也行：super666joey@gmail.com\n\n先聊清楚需求再决定，不着急' },
    { k: ['背景', '能申', '选校', 'bg', 'gpa', '均分', '跨专业', '二本', '双非'],
      a: '选校要看专业方向、GPA、语言和现有作品情况，6 年里各种背景都带过：二本环艺转建筑拿到 UCL、跨专业零基础半年拿下 RCA、考研出分后 3 个月赶上哥大和宾大\n\n一般规律：设计方向重作品集大于绩点，建筑方向院校背景影响稍大，博士主要看 RP 和匹配度\n\n把你的专业、年级和目标国家告诉我，或者直接微信聊，老师帮你做个免费评估' },
    { k: ['公司', '你们是谁', '梦想管理局', '1%', '工作室在哪', '地址'],
      a: '1% Design Lab · 梦想管理局，上海光有序科技有限公司旗下的设计与创意技术品牌\n\n一支团队两种交付：作品集学院帮申请者做出被记住的作品集，产品工作室帮创业者把产品做上线\n\n办公室在外滩旁边：黄浦区北京东路 668 号裙楼 黄浦汇数智心城' }
  ];

  var SYS = [
    '你是「小梦」，1% Design Lab（梦想管理局）官网的 AI 助手，上海的设计与工程团队，两条业务：作品集学院（艺术设计留学作品集辅导，6 年经验，6000+ 案例，学员拿过 600+ 名校 offer）和产品工作室（AI 应用 MVP、产品设计全栈开发、品牌 VI、工业 3D）。',
    '导师：Joey（米兰理工产品设计硕士，创始人，全球带过 200+ 学员、学员拿过 40+ 顶尖 offer）；Jackie（格拉斯哥大学 HCI 博士）；学小嵩（奥斯陆建筑与设计学院）；程越（马兰欧尼 + 皇家艺术学院）；Jason（UC Berkeley 建筑硕士）。',
    '服务价格：作品集原创设计 ¥100 起、留学生作业辅导 ¥200 起、博士研究计划 ¥100 起、线下个展 ¥99.69 起、设计师求职辅导 ¥100 起。AI MVP 最快 14 天上线。起步价对应最小规模需求。',
    '联系方式：微信扫码咨询（引导用户点「微信咨询」按钮或右下角聊聊按钮）、淘宝店铺、super666joey@gmail.com。地址：上海市黄浦区北京东路 668 号裙楼 黄浦汇数智心城。',
    '风格要求：像懂设计的朋友聊天，回答简短直接（3 句以内最佳，列表可用），口语化，中文回答，不用句号结尾，不用或最多用一个 emoji。不知道就诚实说不知道并引导加微信细聊。不要编造价格、案例或承诺。'
  ].join('\n');

  var WELCOME = '你好呀，我是小梦，梦想管理局的 AI 助手\n\n作品集辅导、做个产品、价格、时间线……什么都可以问我';

  var CHIPS = ['作品集辅导怎么收费', '我的背景能申哪些学校', '做个 AI 产品要多久'];

  var $ = function (t) { return document.createElement(t); };
  var state = { open: false, busy: false, history: [], puterTried: false };

  function fallback(q) {
    var s = q.toLowerCase();
    for (var i = 0; i < KNOWLEDGE.length; i++) {
      for (var j = 0; j < KNOWLEDGE[i].k.length; j++) {
        if (s.indexOf(KNOWLEDGE[i].k[j].toLowerCase()) !== -1) return KNOWLEDGE[i].a;
      }
    }
    return null;
  }

  function el(cls, tag, text) {
    var e = $(tag || 'div'); if (cls) e.className = cls; if (text != null) e.textContent = text; return e;
  }

  // ---- UI ----
  var fab = el('agent-fab', 'button');
  fab.setAttribute('aria-label', '打开 AI 助手小梦');
  fab.setAttribute('aria-expanded', 'false');
  fab.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-8 8H5l-2 2V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/><path d="M9 11h.01M13 11h.01M17 11h.01"/></svg><span class="agent-fab-dot" aria-hidden="true"></span>';

  var panel = el('agent-panel');
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'AI 助手小梦');
  panel.innerHTML =
    '<div class="agent-head">' +
      '<div class="agent-ava"><i class="blink"></i></div>' +
      '<div><h3>小梦</h3><p class="label mono">AI GUIDE · ONLINE</p></div>' +
      '<button class="agent-x" aria-label="关闭">✕</button>' +
    '</div>' +
    '<div class="agent-body"></div>' +
    '<div class="agent-chips"></div>' +
    '<div class="agent-foot">' +
      '<div class="agent-in">' +
        '<textarea rows="1" placeholder="问小梦任何问题…" aria-label="输入问题"></textarea>' +
        '<button class="agent-send" aria-label="发送"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>' +
      '</div>' +
      '<button class="agent-wx">还是人聊舒服 → 微信咨询</button>' +
    '</div>';

  var body = panel.querySelector('.agent-body');
  var chipsBox = panel.querySelector('.agent-chips');
  var input = panel.querySelector('textarea');
  var sendBtn = panel.querySelector('.agent-send');

  function addMsg(text, who) {
    var m = el('agent-msg ' + who); m.textContent = text;
    body.appendChild(m); body.scrollTop = body.scrollHeight;
    return m;
  }

  function setOpen(v) {
    state.open = v;
    fab.setAttribute('aria-expanded', v ? 'true' : 'false');
    panel.classList.toggle('open', v);
    if (v) setTimeout(function () { input.focus(); }, 320);
  }

  fab.addEventListener('click', function () { setOpen(true); });
  panel.querySelector('.agent-x').addEventListener('click', function () { setOpen(false); fab.focus(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && state.open) { setOpen(false); }
  });

  panel.querySelector('.agent-wx').addEventListener('click', function () {
    var btn = document.querySelector('[data-consult]');
    setOpen(false);
    if (btn) btn.click();
  });

  CHIPS.forEach(function (c) {
    var b = el('agent-chip', 'button', c);
    b.addEventListener('click', function () { ask(c); });
    chipsBox.appendChild(b);
  });

  input.addEventListener('input', function () {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 110) + 'px';
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input.value); }
  });
  sendBtn.addEventListener('click', function () { ask(input.value); });

  // ---- AI ----
  function loadPuter(cb) {
    if (window.puter && window.puter.ai) return cb(true);
    if (state.puterTried) return cb(false);
    state.puterTried = true;
    var s = document.createElement('script');
    s.src = 'https://js.puter.com/v2/';
    s.onload = function () { cb(!!(window.puter && window.puter.ai)); };
    s.onerror = function () { cb(false); };
    document.head.appendChild(s);
  }

  function withTimeout(promise, ms) {
    return Promise.race([
      promise,
      new Promise(function (_, rej) { setTimeout(function () { rej(new Error('timeout')); }, ms); })
    ]);
  }

  function askAI(q, onChunk) {
    return new Promise(function (resolve) {
      // provider 1: GLM-4-Flash (配置 window.AGENT_GLM_KEY 后启用, 完全免费)
      if (window.AGENT_GLM_KEY) {
        glmChat(q, onChunk).then(resolve);
        return;
      }
      // provider 2: Puter.js (仅对已登录 Puter 的访客启用, 未登录直接走本地知识库, 避免授权弹窗卡住)
      loadPuter(function (ok) {
        if (!ok) return resolve(null);
        var signed = false;
        try { signed = window.puter.auth.isSignedIn(); } catch (e) {}
        if (!signed) return resolve(null);
        var full = '';
        var settled = false;
        var finish = function () { if (!settled) { settled = true; resolve(full || null); } };
        var timer = setTimeout(finish, 14000);
        var msgs = [{ role: 'system', content: SYS }].concat(state.history.slice(-8), [{ role: 'user', content: q }]);
        window.puter.ai.chat(msgs, { stream: true }).then(function (resp) {
          var handleText = function (t) {
            if (t) { full += t; onChunk(full); }
          };
          if (resp && typeof resp[Symbol.asyncIterator] === 'function') {
            (async function () {
              for await (var part of resp) {
                if (settled) return;
                handleText(part && (part.text || (part.choices && part.choices[0] && part.choices[0].delta && part.choices[0].delta.content)) || '');
              }
              clearTimeout(timer); finish();
            })().catch(function () { clearTimeout(timer); finish(); });
          } else if (resp && typeof resp.read === 'function') {
            var pump = function () {
              return resp.read().then(function (r) {
                if (settled) return;
                if (r.done) { clearTimeout(timer); finish(); return; }
                handleText((r.value && r.value.text) || '');
                pump();
              }).catch(function () { clearTimeout(timer); finish(); });
            };
            pump();
          } else {
            var text = (resp && resp.message && resp.message.content) || (resp && resp.text) || '';
            full = text; if (text) onChunk(text);
            clearTimeout(timer); finish();
          }
        }).catch(function () { clearTimeout(timer); finish(); });
      });
    });
  }

  function glmChat(q, onChunk) {
    var msgs = [{ role: 'system', content: SYS }].concat(state.history.slice(-8), [{ role: 'user', content: q }]);
    return fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + window.AGENT_GLM_KEY },
      body: JSON.stringify({ model: 'glm-4-flash', messages: msgs, temperature: 0.7, stream: true })
    }).then(function (res) {
      if (!res.ok || !res.body) throw new Error('glm http ' + res.status);
      var reader = res.body.getReader();
      var dec = new TextDecoder();
      var buf = '', full = '', settled = false;
      return new Promise(function (resolve) {
        var finish = function () { if (!settled) { settled = true; resolve(full || null); } };
        var timer = setTimeout(finish, 15000);
        var pump = function () {
          reader.read().then(function (r) {
            if (settled) return;
            if (r.done) { clearTimeout(timer); finish(); return; }
            buf += dec.decode(r.value, { stream: true });
            var lines = buf.split('\n'); buf = lines.pop();
            for (var i = 0; i < lines.length; i++) {
              var line = lines[i].trim();
              if (line.indexOf('data:') !== 0) continue;
              var payload = line.slice(5).trim();
              if (payload === '[DONE]') { clearTimeout(timer); finish(); return; }
              try {
                var j = JSON.parse(payload);
                var t = j.choices && j.choices[0] && j.choices[0].delta && j.choices[0].delta.content || '';
                if (t) { full += t; onChunk(full); }
              } catch (e) {}
            }
            pump();
          }).catch(function () { clearTimeout(timer); finish(); });
        };
        pump();
      });
    }).catch(function () { return null; });
  }

  function ask(qRaw) {
    var q = (qRaw || '').trim();
    if (!q || state.busy) return;
    state.busy = true;
    input.value = ''; input.style.height = 'auto';
    sendBtn.disabled = true;
    chipsBox.style.display = 'none';
    addMsg(q, 'user');

    var typing = el('agent-msg bot typing', 'div');
    typing.innerHTML = '<i></i><i></i><i></i>';
    body.appendChild(typing); body.scrollTop = body.scrollHeight;

    var fb = fallback(q);
    askAI(q, function (partial) {
      if (typing) { typing.remove(); typing = null; }
      if (!ask._bubble) ask._bubble = addMsg('', 'bot');
      ask._bubble.textContent = partial;
      body.scrollTop = body.scrollHeight;
    }).then(function (ans) {
      if (typing) typing.remove();
      if (!ans || !ans.trim()) {
        if (ask._bubble) { ask._bubble.remove(); ask._bubble = null; }
        var text = fb || '这个问题我拿不准，怕给你不靠谱的答案\n\n建议直接微信聊，老师会给你准的判断——点下面「微信咨询」就行';
        addMsg(text, 'bot');
      } else {
        if (!ask._bubble) ask._bubble = addMsg(ans.trim(), 'bot');
        else ask._bubble.textContent = ans.trim();
      }
      ask._bubble = null;
      body.scrollTop = body.scrollHeight;
      state.history.push({ role: 'user', content: q });
      state.history.push({ role: 'assistant', content: (ans && ans.trim()) || fb || '' });
      state.busy = false; sendBtn.disabled = false;
      input.focus();
    });
  }

  // ---- mount ----
  function mount() {
    document.body.appendChild(fab);
    document.body.appendChild(panel);
    addMsg(WELCOME, 'bot');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
