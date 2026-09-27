# 重构后 SEO / GEO 优化记录

本轮修改已在本地完成，未提交、推送或部署。保留原有 40 页正文、视觉模块和客服配置。

## 已发现并处理

| 优先级 | 问题与证据 | 本地处理 |
| --- | --- | --- |
| P0 | 线上随机不存在路径 `/seo-audit-missing-page-20260927` 返回 200，内容与首页相同 | 新增根目录 `404.html`，标记 noindex，提供中英文返回入口；部署后验证 HTTP 404 |
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
- 40 页 body 与修改前内容一致；六个品牌页面生成函数均输出新增 SEO 规则。
- 已有客服配置文件与开始工作时备份一致。
- 线上直接请求首页与 `/studio/` 为 200；旧 `/services/ai-mvp.html` 最终转到无扩展名地址并返回 200。
- Python HTTP 客户端收到 403；curl 可访问相同首页。这不能证明真实搜索爬虫被拦截，需要服务端日志或 Search Console 抓取测试确认。
- 搜索工具读取到旧首页，直接请求读取到新版；仅能说明两个抓取渠道内容不同，不能据此断定 Google 索引状态。

没有运行完整页面生成器：当前生成模板与已精修页面存在其他差异，整页重建可能覆盖现有设计。本轮用仅处理 head 的脚本更新输出，同时将结构化数据逻辑接入原生成器。

## 发布后验收与后续重点

1. 检查随机不存在路径返回 HTTP 404；确认正常服务页仍为 200、旧 .html 地址重定向仍正常。
2. 在线验证六个品牌页的 canonical、hreflang 与 JSON-LD，确认新元数据已发布。
3. 在 Google Search Console / Bing Webmaster 中查看两条业务线的收录与查询数据，提交现有 sitemap；本轮未读取账户数据，也未提交索引请求。
4. 以 28 天为窗口，分别观察产品开发与作品集业务的展现、点击、有效咨询。按真实查询扩展内容，避免两条业务线争抢同一泛关键词。
5. GEO 内容重点是明确服务范围、交付边界、可核验案例和引用来源；llms.txt 只是辅助导航，不代表排名或 AI 引用保证。本轮未新增未经证实的业绩、评价或录取结果。

## 官方依据

- [Google：AI 搜索功能仍遵循基础 SEO，无需特殊 AI 标记](https://developers.google.com/search/docs/appearance/ai-features)
- [Google：多语言版本与双向 hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Schema.org：sameAs 表示同一实体](https://schema.org/sameAs)
- [Schema.org：最低价格表达](https://schema.org/PriceSpecification)
- [Cloudflare Pages：404 与 SPA 回退规则](https://developers.cloudflare.com/pages/configuration/serving-pages/)
