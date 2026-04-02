# 可配置按钮管理项目

基于 Vue3 + Vite + TypeScript，实现了按钮配置与按钮展示两大页面。

## 功能

- 配置页支持按钮增删改
- 可编辑显示文本、样式、排序、动作
- 动作支持：
  - 跳转三方链接
  - 调用后台方法名（示例：ping、submitButtonLog）
  - 执行自定义 JS
- 自定义 JS 可直接调用 utils.httpRequest
- 展示页按排序渲染并执行动作
- 配置自动持久化到 localStorage

## 关键目录

- src/pages/ConfigPage.vue：配置页面
- src/pages/DisplayPage.vue：展示页面
- src/state/buttonStore.ts：按钮状态和持久化
- src/services/actionExecutor.ts：动作执行器
- src/services/backendMethods.ts：后台方法映射
- src/utils/http.ts：axios 请求封装
- src/router/index.ts：路由配置

## 启动

1. 安装依赖

   npx -y pnpm install

2. 本地开发

   npx -y pnpm dev

3. 构建

   npx -y pnpm build
