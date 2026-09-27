# 重构后 SEO / GEO 优化记录

本轮 SEO 修改已随提交 `86108e164b796e2558c36a5033f4bff9113cf02d` 推送至 main，并在 Cloudflare Pages 生产部署 `a732a2ed-82de-4469-8aa4-d342e157477d` 上线。SEO 修改保留原有 40 页正文及视觉模块；同一提交还包含另一项客服安全更新。

## 已发现并处理

| 优先级 | 问题与证据 | 本地处理 |
| --- | --- | --- |
| P0 | 线上随机不存在路径 `/seo-audit-missing-page-20260927` 返回 200，内容与首页相同 | 新增根目录 `404.html`，标记 noindex，提供中英文返回入口；发布后随机路径已实测返回 HTTP 404 |
| P1 | 六个品牌页面的 Organization.sameAs 把个人网站、Finfold、BillVampire 和个人 GitHub 视作同一机构 | 移除错误身份关联，保留 founder 关系及页面中的产品证据 |
| P1 | 两条业务线的服务报价为“起”，结构化数据却使用固定 price | 改为 PriceSpecification.minPrice，保留原有金额 |
| P1 | 作品集诊断结构化描述为免费，而可见页面写明完整报告 ¥299 | 统一为基础评分免费、完整报告收费；同步 llms.txt |
| P2 | 品牌页缺少页面、网站、服务之间的完整机器可读关系 | 添加 WebPage、WebSite、mainEntity、面包屑关联和语言信息 |
| P2 | 多个服务、案例、工具与文章页的分享字段缺失 | 从现有标题、摘要与封面补全 Twitter 卡片；允许大图预览 |
| P2 | 原验证器只覆盖基础 canonical、链接和 JSON 语法 | 新增重复标题/摘要、单 H1、语言互链、孤立页面、失效锚点、分享图片和结构化语义检查 |

## 验证结果

- `node scripts/validate-seo.mjs`：40 个 canonical 页面通过增强检查。
- `python3 scripts/seo_metadata.py`：第二次运行修改 0 页，处理可重复执行。
- `git diff --check`：通过。
- 发布后逐页检查 40 个 canonical URL：全部返回 HTTP 200，canonical 与分享图片字段正确。首次请求的两个 TLS 连接失败在重试后通过。
- 40 页 body 与修改前内容一致；六个品牌页面生成函数均输出新增 SEO 规则。
- 首轮 SEO 修改未改变当时的客服配置；后续客服安全更新已独立纳入上述提交。
- 线上直接请求首页与 `/studio/` 为 200；旧 `/services/ai-mvp.html` 最终转到无扩展名地址并返回 200。
- Python HTTP 客户端收到 403；curl 可访问相同首页。这不能证明真实搜索爬虫被拦截，需要服务端日志或 Search Console 抓取测试确认。
- 搜索工具读取到旧首页，直接请求读取到新版；仅能说明两个抓取渠道内容不同，不能据此断定 Google 索引状态。

没有运行完整页面生成器：当前生成模板与已精修页面存在其他差异，整页重建可能覆盖现有设计。本轮用仅处理 head 的脚本更新输出，同时将结构化数据逻辑接入原生成器。

## 发布验收与后续重点

1. 随机不存在路径 `/seo-release-missing-20260927` 已实测返回 HTTP 404。
2. 六个品牌页的新 WebPage、身份关系及起步价语义已在线核验；llms.txt 的价格说明已在线核验。
3. IndexNow 已接收 40 个 canonical URL 更新通知（HTTP 200）。这不代表已收录。本轮未读取 Google Search Console / Bing Webmaster 账户数据，后续可据此衡量两条业务线的查询表现。
4. 以 28 天为窗口，分别观察产品开发与作品集业务的展现、点击、有效咨询。按真实查询扩展内容，避免两条业务线争抢同一泛关键词。
5. GEO 内容重点是明确服务范围、交付边界、可核验案例和引用来源；llms.txt 只是辅助导航，不代表排名或 AI 引用保证。本轮未新增未经证实的业绩、评价或录取结果。

## 官方依据

- [Google：AI 搜索功能仍遵循基础 SEO，无需特殊 AI 标记](https://developers.google.com/search/docs/appearance/ai-features)
- [Google：多语言版本与双向 hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Schema.org：sameAs 表示同一实体](https://schema.org/sameAs)
- [Schema.org：最低价格表达](https://schema.org/PriceSpecification)
- [Cloudflare Pages：404 与 SPA 回退规则](https://developers.cloudflare.com/pages/configuration/serving-pages/)
