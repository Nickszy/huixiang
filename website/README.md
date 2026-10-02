# 回响产品网站

静态官网：<https://huixiang.nickszy.com>；Cloudflare Pages 备用域名：<https://echo-insight-cyz.pages.dev>。项目名 `echo-insight`，生产分支 `main`。

介绍当前本机档案研发能力、公开 0.1.0 的准确范围及后续计划。公开安装包没有被这次官网更新替换；合成界面图和 48 秒介绍视频不得写成公开安装包录屏。

## 本地预览

Node.js 20+；浏览器预览可使用 Python：

安装包不进入 Git。首次克隆发布仓库时，先用 GitHub CLI 获取已有公开制品；测试与站点打包都会校验其实际大小和哈希：

```powershell
gh release download v0.1.0 --repo Nickszy/huixiang --pattern echoinsight-0.1.0-windows-x64-setup.exe --dir website/artifacts
```

```powershell
python -m http.server 8765 --directory website
node --test website/site.test.mjs
```

访问 `http://localhost:8765`。网站不依赖远程字体、脚本或图片；所有界面示意均为合成数据。

## 更新素材

安装 Python Pillow 和本机 FFmpeg；Windows 本机 zh-CN 语音用于旁白：

```powershell
powershell -NoProfile -File promotions/narration.ps1
python promotions/render_assets.py
```

生成图片、视频、字幕与图文卡；源文案和分镜保存在 `promotions/`。素材脚本不读取任何用户档案。`write_site.py` 用于生成首页、功能、隐私及补充版本说明；其余下载逻辑仍由已有模块提供。

## 发布官网

需要 Cloudflare Pages 的现有登录状态，不把凭据写进仓库。先运行测试，再生成一个不存在的输出目录：

首次使用 Wrangler 可先运行 `npm ci --prefix website`。下面的部署命令从仓库根目录执行，因此用 `--prefix website` 找到已锁定的工具：

```powershell
node --test website/site.test.mjs
node website/build-site.mjs website/dist-publish-new
npm exec --prefix website -- wrangler pages deploy website/dist-publish-new --project-name=echo-insight --branch=main
```

`build-site.mjs` 只复制固定的页面、公开素材及通过实际字节数 / SHA-256 检查的安装包。不复制聊天档案、开发日志、模型配置或本机密钥；使用新目录避免旧发布残留。生产发布后检查首页视频、下载页面以及域名。

## 安装包与闸门

`release-manifest.json` schemaVersion 2，Windows / macOS ARM64 / macOS x64 独立管理发布。未发布的构建保持 null；全局 unreleased 时所有构建关闭。每个真实安装包必须完成来源复核、目标系统安装验证、版本记录、字节数和 SHA-256 核对，再填写 publishGate。哈希只能验证文件与清单一致，不能独立证明发布者身份。

公开 Windows 0.1.0 未启用真实连接器；清单 0.0.0 表示没有验证微信客户端版本，不能当作微信版本。新档案构建需要另行生成、验证和发布，不能仅修改清单冒充新版本。

大型安装包的浏览器校验会占用内存；同站点制品与清单需要保持同一发布版本。GitHub Releases 的安装包另行管理。
