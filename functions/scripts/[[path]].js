// 1% Design Lab · /scripts/* — 维护工具不是站点内容，对外一律 404
// Pages 会把仓库根目录整个发布，没有排除文件的机制，所以用这个 Function 拦住下载。
// 工具本身留在 scripts/ 里：SEO 提交与检查、图片工具、录取数据导入、本地预览。

export async function onRequest() {
  return new Response('Not Found', {
    status: 404,
    headers: { 'content-type': 'text/plain; charset=utf-8' }
  });
}
