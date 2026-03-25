2026年03月25日23:47:10
**PLAN:**
1、我可以继续帮你直接安装依赖并本地启动前后端，完成首轮联调与接口验收。
2、把检索从当前词频相似度升级为真实 Embedding + Chroma（贴合需求文档技术栈）。
3、补权限拒答精判与评测门禁阈值校验（越权率必须为 0 的自动断言）

**QUESTION:**
1、创建虚拟环境失败

**TODO:**
1、重新安装 homebrew，解决安装速度慢的问题
2、pyenv 版本管理


终端代理：https://github.com/youngzil/notes/blob/master/docs/tech/OperatingSystem/MAC/Mac%E8%AE%A9%E7%BB%88%E7%AB%AF%E8%B5%B0%E4%BB%A3%E7%90%86%E7%9A%84%E5%87%A0%E7%A7%8D%E6%96%B9%E6%B3%95.md

git 代理
git config --global --unset https.proxy
git config --global --unset http.proxy

git config --global https.proxy http://127.0.0.1:7890
git config --global http.proxy http://127.0.0.1:7890

