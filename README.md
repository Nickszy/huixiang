# 回响 / INSIGHT

微信群聊一多，关键讨论就被刷走。回响希望用 AI 跨群梳理话题、跟进你关心的人，并按你设定的时间送来重点。

**当前状态（技术预览）**：已交付本地合成演示数据的群总结闭环（选择演示群 → 生成本地合成摘要 → 报告列表/详情 → 引用原文回查）。真实微信连接器**未启用**（清单记为 0.0.0，表示未验证任何微信客户端版本）；跨群话题、人物追踪、定时任务、推送为规划中能力。摘要由本地固定合成数据生成并明确标注，不代表真实聊天或云端 AI 结果。

## 下载（Windows x64 · 0.1.0 · 2026-09-30）

| 文件 | 大小 | SHA-256 |
|---|---|---|
| [echoinsight-0.1.0-windows-x64-setup.exe](https://github.com/Nickszy/huixiang/releases/download/v0.1.0/echoinsight-0.1.0-windows-x64-setup.exe)（安装版） | 9,346,756 字节 | `eb885f6ed4463c1c706c69197b9d99478202984b5abf7ac21323fbc9f087c78a` |
| [echoinsight-0.1.0-windows-x64-portable.zip](https://github.com/Nickszy/huixiang/releases/download/v0.1.0/echoinsight-0.1.0-windows-x64-portable.zip)（免安装便携版） | 14,284,419 字节 | `6bb6326884fb8e4e49dd4d18016be00c3841c4afd0ad0c96a341612eaeb9c9e0` |

系统要求：Windows 10 1809+ 或 Windows 11（x64，需 WebView2 运行时）。安装包未签名，SmartScreen 可能提示；请核对上方哈希。便携版解压后运行 `echo-insight-desktop.exe`。

官网（含浏览器哈希校验下载）：huixiang.nickszy.com

## 边界说明

- 本仓库仅发布构建产物，暂不含源码。
- 没有自动更新；新版本请在本页重新下载核对。
- 独立技术预览 · 非微信官方产品 · 不提供未经核验的数据兼容性承诺。
