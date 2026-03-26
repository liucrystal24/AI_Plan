## 2026-03-26
### 更新点
1、安装依赖并本地启动前后端，完成首轮联调与接口验收。
2、把检索从当前词频相似度升级为真实 Embedding + Chroma（贴合需求文档技术栈）。
3、补权限拒答精判与评测门禁阈值校验（越权率必须为 0 的自动断言）

### 遗留问题

### 笔记

## 2026-03-25**
### 更新点
工程初始化

### 遗留问题
- [x] 创建虚拟环境失败
- [] 重新安装 homebrew，解决安装速度慢的问题: 目前为Tun代理，需要尝试镜像
- [ ] pyenv 版本管理：有时安装失败，需要看效果

### 笔记

```shell
# git 代理配置
git config --global --unset https.proxy
git config --global --unset http.proxy

git config --global https.proxy http://127.0.0.1:7890
git config --global http.proxy http://127.0.0.1:7890

# 杀掉所有 brew 相关进程
pkill -f brew
# 清理锁文件（最常见卡住原因）
rm -rf /usr/local/var/homebrew/locks
# 清理 brew 缓存
rm -rf ~/Library/Caches/Homebrew

```
