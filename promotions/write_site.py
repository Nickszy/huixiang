"""Author static promotion pages; does not read product or user data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"


def page(title, description, body, current="", script=""):
    links = [("features.html", "功能与范围"), ("privacy.html", "隐私与边界"), ("download.html", "下载预览版")]
    nav = "".join(f'<a href="{url}"'+(' aria-current="page"' if current == url else '')+f'>{text}</a>' for url, text in links)
    return f'''<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#102a23"><meta name="description" content="{description}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:type" content="website"><meta property="og:image" content="https://huixiang.nickszy.com/assets/social-cover.png">
<title>{title}</title><link rel="stylesheet" href="styles.css">{script}</head>
<body><a class="skip-link" href="#main">跳到正文</a>
<header class="site-header"><div class="wrap nav-row"><a class="brand" href="index.html" aria-label="回响 INSIGHT 首页"><span class="brand-mark" aria-hidden="true">✳</span><span>回响 <small>/ INSIGHT</small></span></a><nav aria-label="主导航">{nav}<a href="https://github.com/Nickszy/huixiang">GitHub ↗</a></nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">✳</span><span>回响 <small>/ INSIGHT</small></span></a><p>散户投资者的本机研究工作台 · 独立技术预览 · 非微信官方产品</p><nav aria-label="页脚导航"><a href="features.html">功能</a><a href="privacy.html">隐私</a><a href="download.html">下载</a><a href="release-notes.html">版本记录</a></nav></div></footer></body></html>'''


hero = '''<section class="hero"><div class="hero-grid" aria-hidden="true"></div><div class="wrap hero-layout">
<div class="hero-copy"><p class="eyebrow light"><span class="status-dot" aria-hidden="true"></span> 面向散户投资者 / WINDOWS 技术预览</p>
<h1>群聊里的线索，<br><em>成为研究起点。</em></h1><p class="hero-lead">关注自己认可的优质投资群，把标的讨论、图表与研报附件整理到本机。看到一条线索，再回查原话、核对依据。</p>
<div class="button-row"><a class="button primary" href="#experience">看看投资研究场景 ↗</a><a class="button ghost" href="download.html">查看发布版本 →</a></div>
<p class="hero-note">档案功能已在本机研发验证 · 尚未打包公开<br>当前公开 0.1.0 为早期演示版，功能范围见版本记录。</p></div>
<figure class="workspace-figure"><img src="assets/workspace.png" alt="合成界面示意：会话分类、消息和媒体标签，所有人物与内容均为演示数据" width="1200" height="960"><figcaption>研发体验 · 合成界面示意 · 非真实聊天录屏</figcaption></figure>
</div><div class="wrap hero-bottom"><span>FOLLOW THE RESEARCH TRAIL</span><span>优质群聊 · 标的讨论 · 研报资料 · 有据可查</span><span aria-hidden="true">↓</span></div></section>'''

home = hero + '''<section class="section wrap" id="experience" aria-labelledby="experience-title"><div class="section-heading"><div><p class="eyebrow">01 / FOR INDIVIDUAL INVESTORS</p><h2 id="experience-title">从群聊的观点，<br><span class="accent-text">回到研究的依据。</span></h2></div><p>给自行研究的散户投资者：关注认可的群，找到讨论过的标的和资料。这里整理研究线索，不判断群的质量，也不提供买卖信号。</p></div>
<div class="steps"><article><span class="step-no">01 / 会话</span><span class="step-symbol" aria-hidden="true">◎</span><h3>关注优质投资群</h3><p>自己选择认可的投资群或研究公众号，添加关注。按最近消息浏览，减少在无关会话之间来回切换。</p></article><article><span class="step-no">02 / 消息</span><span class="step-symbol" aria-hidden="true">▤</span><h3>回查标的讨论</h3><p>用标的名称搜索当前已载入的消息，回看不同观点、时间和原话。滚动载入更早消息，逐步核对讨论依据。</p></article><article><span class="step-no">03 / 媒体</span><span class="step-symbol" aria-hidden="true">▦</span><h3>找到研报与资料</h3><p>在会话和媒体库找到研报 PDF、估值表 Excel 或交流纪要，按文件名搜索、分类和排序，打开可读取的本机附件。</p></article></div></section>
<section class="section feature-band"><div class="wrap product-split"><div><p class="eyebrow">02 / A CLOSER LOOK</p><h2>研报与图表，<br>留在研究上下文。</h2><p class="body-copy">群里分享的行业资料、公司研究与图表，都可以成为下一步核查的材料。找到文件，再用系统应用打开；本机有可解码原图时，尝试更清晰的图表版本。</p><div class="feature-tags"><span>研报 PDF</span><span>估值表 Excel</span><span>纪要与音频</span><span>图表原图</span></div><p class="fine-print">原图文件存在不代表一定可解码。缺失文件无法恢复；部分格式需要本机 FFmpeg。视频与文件的发送者信息尚未完整关联。</p><a class="inline-link" href="features.html">查看功能与限制 ↗</a></div><figure class="media-figure"><img loading="lazy" src="assets/media-library.png" width="1200" height="960" alt="合成投资资料库示意，展示 PDF 研报、Excel 估值表、纪要分类与翻页"><figcaption>合成界面示意 · 所有素材均为演示内容</figcaption></figure></div></section>
<section class="section wrap video-section" aria-labelledby="video-title"><div><p class="eyebrow">03 / WATCH THE WALKTHROUGH</p><h2 id="video-title">用 48 秒，<br>认识回响。</h2><p class="body-copy">关注投资群，回查虚构标的的讨论，找到研报附件。用一个合成投资研究场景认识回响。</p><p class="fine-print">视频使用合成界面与本机合成旁白，包含中文字幕。公开 0.1.0 安装包仍是早期演示版，未包含视频中的新档案功能。</p><a class="inline-link" href="assets/echo-insight-intro.mp4">打开介绍视频 ↗</a></div><video controls playsinline preload="none" poster="assets/video-cover.png" aria-label="回响产品介绍视频：研发体验，合成演示，48秒"><source src="assets/echo-insight-intro.mp4" type="video/mp4"><track kind="captions" src="assets/intro.vtt" srclang="zh" label="中文字幕" default>你的浏览器不支持视频，请使用左侧链接打开。</video></section>
<section class="section feature-band"><div class="wrap trust-layout"><div><p class="eyebrow">04 / LOCAL BY DEFAULT</p><h2>自己的研究资料，<br><span class="accent-text">留在自己的电脑。</span></h2><p class="body-copy">选择保存目录，在本机解密、解析和浏览。应用打开时默认每 5 分钟检查数据库变化；发生变化的库才重新处理。</p><a class="inline-link" href="privacy.html">了解数据保存与缓存 ↗</a></div><div class="trust-panel"><div class="trust-title">本机档案流程 <span>IN DEVELOPMENT</span></div><div class="trust-row"><span>保存位置</span><strong>你选择的目录</strong></div><div class="trust-row"><span>数据库密钥</span><strong>加密保存在本机</strong></div><div class="trust-row"><span>档案浏览</span><strong>本机读取，无需云端模型</strong></div><div class="trust-row"><span>数据刷新</span><strong>应用打开时检查变化</strong></div><p>解密数据库与图片缓存含明文私人内容，请保护保存目录。数据刷新与软件升级是两回事。</p></div></div></section>
<section class="section wrap roadmap"><p class="eyebrow">WHAT COMES NEXT / 规划中</p><h2>从资料整理，<br>走向研究辅助。</h2><p class="body-copy">后续希望把群聊中的标的提及整理为待研究清单，汇总不同观点，并对研报附件提取要点与关键假设。自动标的提取、附件自动总结与真实聊天 AI 总结尚未接入；当前合成摘要只演示群聊文字整理与原话引用，不读取 PDF 正文。</p><div class="roadmap-row"><span>标的线索自动整理 · 规划中</span><span>附件自动总结 · 规划中</span><span>跨群观点与研究简报 · 规划中</span></div></section>
<section class="closing"><div class="wrap closing-inner"><div><p class="eyebrow light">A WORKSPACE FOR YOUR RESEARCH</p><h2>把群聊线索，<br>变成研究材料。</h2></div><div><p>关注新档案版本的发布进展，或先体验公开的早期演示版。Windows 优先，macOS 尚未发布。</p><a class="button primary" href="download.html">版本与下载 ↗</a><a class="closing-github" href="https://github.com/Nickszy/huixiang">GitHub · 项目与更新 ↗</a></div></div></section>'''

SITE.joinpath("index.html").write_text(page("回响 / Echo Insight — 散户投资者的本机研究工作台", "面向散户投资者，关注优质投资群、回查标的讨论、归档研报与图表。附件自动总结与标的自动提取规划中；公开 0.1.0 为早期演示版。", home), encoding="utf-8")


def intro(label, heading, description):
    return f'<section class="page-hero"><div class="wrap"><p class="eyebrow light">{label}</p><h1>{heading}</h1><p>{description}</p></div></section>'


def block(label, summary, heading, content):
    return f'<aside class="side-note"><span>{label}</span><strong>{summary}</strong></aside><section class="content-block"><h2>{heading}</h2>{content}</section>'


features = intro("CAPABILITIES / 实现与发布范围", "群聊、标的、研报，<br>沿着<span>线索去核查。</span>", "能力分为当前档案研发版、公开 0.1.0 和后续计划。下载旧版不会获得研发中的新功能。")
features += '<div class="wrap prose-grid">' + block("01 / 档案研发版", "整理自己的投资研究资料。", "现有能力如何用于投资研究", '''<ul><li>Windows 微信 4.x 账号检测、数据库密钥提取与本机保存；选择目录解密、解析，再从已保存结果浏览。兼容性仍在验证，无法保证所有客户端版本。</li><li>会话、联系人、群聊与公众号分类；最近消息优先、列表翻页、会话名称搜索、关注与关注筛选。</li><li>更早消息滚动加载；消息搜索仅覆盖当前已载入内容，不是整个档案的全文检索。可在会话中切换图片、视频、文件。</li><li>本机头像、可读取的分享链接与附件；原消息没有 URL 时不会凭空生成链接。</li><li>媒体库搜索文件名、翻页，按时间、大小、名称升序或倒序；区分图片、视频及音频、PDF、Word、Excel、PPT、压缩包等文件类别。</li><li>图片本机解码、放大预览，优先尝试原图；支持原图文件存在、仅缩略图、缺失文件筛选。是否能恢复清晰版本取决于文件、密钥与格式；部分格式需要 FFmpeg。</li><li>应用打开时默认每 5 分钟检查变化，只重新解密变化的整库并替换结果，不逐行实时同步；未变化库跳过。应用关闭后不检查。</li></ul><div class="callout"><b>当前交付边界</b><p>以上功能已在本机研发验证，尚未打包公开。视频和界面图片均为合成示意，不能当作公开安装包的功能承诺。</p></div>''')
features += block("02 / 公开下载", "0.1.0 是早期演示版。", "公开 Windows 0.1.0", '<p>包含本地合成群摘要、保存报告与引用回查、模型配置保存和账号目录检测。未启用真实微信连接、聊天档案或云端 AI 调用。它适合了解早期产品流程，无法体验本页的新档案功能。</p><a class="inline-link" href="release-notes.html">逐版功能与安装包记录 ↗</a>')
features += block("03 / 已知限制", "知道限制，才好使用。", "仍需完善的体验", '<ul><li>语音播放、表情资源、整个档案全文搜索尚未接入。</li><li>部分图片密钥、格式或本机文件不可用时只能预览缩略图，或无法显示；原图文件存在不代表能解码。</li><li>媒体来源关联尚不完整，尤其是视频和文件的群聊与发送者。</li><li>部分索引库需要微信自定义 SQLite 扩展，普通 SQLite 无法读取其中的全文索引。</li><li>macOS 采集与安装包尚未发布；Windows 新档案安装包与广泛版本兼容性仍待验证。</li></ul>')
features += block("04 / 后续计划", "从线索到待核实问题。", "标的整理与附件总结 · 规划中", '<p>标的名称与代码自动提取、跨群观点归纳、研报附件自动总结与原文定位、定时研究简报是后续方向。当前支持会话关注与资料浏览，不自动发现优质群、不输出买卖信号；合成群摘要只整理预置文字，没有读取附件正文。真实聊天与附件 AI 总结尚未接入，不承诺上线日期。若未来由用户触发模型调用，所选内容可能发送到用户配置的 HTTPS 服务，需要单独确认范围与目的地。</p>') + '</div>'
SITE.joinpath("features.html").write_text(page("功能与范围 — 回响 / INSIGHT", "回响聊天档案与媒体库研发能力、公开安装包范围和已知限制。", features, "features.html"), encoding="utf-8")

privacy = intro("PRIVACY / 数据在哪里", "你的聊天，<br>需要<span>清楚的边界。</span>", "说明网站、桌面本机档案与可能的模型调用分别处理什么数据。以下范围随实际版本更新。")
privacy += '<div class="wrap prose-grid">' + block("01 / 网站", "浏览介绍，无需交出聊天。", "静态产品网站", '<p>没有账户、聊天上传表单、分析脚本、第三方字体或 CDN。介绍图片、视频与字幕均由本站提供；演示人物与内容全部合成。下载页读取同站点发布清单，按用户操作获取安装包并计算 SHA-256。</p><p>本站由 Cloudflare Pages 托管，托管方可能产生常规访问日志；不声称零日志。网站不读取你的微信聊天、数据库密钥或模型凭据。</p>')
privacy += block("02 / 档案研发版", "解密之后，文件含明文。", "本机数据库、密钥与图片缓存", '<p>用户授权后，Windows 连接流程可读取本机微信进程内存以提取自己账号的数据库密钥，密钥加密保存在本机。解密数据库保存在用户选择的账号目录；保存结果用于档案浏览。此流程属于尚未打包公开的档案研发版。</p><p>解密后的数据库、媒体预览与本地设置都可能包含私人内容。本机图片解码会产生明文临时图片；放大预览采用容量受限的本机缓存，传输有效期约 90 秒。有效期是读取窗口，不保证文件到期立即删除，缓存会随后续写入轮换。</p><p>请保护所选目录和应用数据目录；复制、云盘同步或备份这些目录也会复制其中的明文内容。删除应用并不自动删除你另外选择的档案目录。</p>')
privacy += block("03 / 数据刷新", "应用打开，才检查变化。", "默认 5 分钟增量检查", '<p>当前档案研发版在应用打开时检查数据库文件变化；变化的整库重新处理并替换本机结果，未变化的库跳过。处理时长取决于变化库大小、磁盘和解密开销；没有固定耗时或零性能开销承诺。应用关闭后不检查，也不自动升级软件。</p>')
privacy += block("04 / 模型与分享", "浏览档案不调用云端模型。", "明确外发范围与目的地", '<p>本机档案浏览无需向云端模型发送聊天。公开 0.1.0 的模型配置仅保存、不发起调用；真实聊天 AI 总结尚未接入。后续若用户触发 HTTPS 模型服务处理，所选内容会按当时界面说明发送至该服务，服务商的留存与训练政策需单独核实。</p><p>请只处理有权访问的内容，分享档案前尊重聊天参与者。回响是独立技术预览，非微信官方产品。</p><a class="inline-link" href="release-notes.html">查看各版本边界 ↗</a>') + '</div>'
SITE.joinpath("privacy.html").write_text(page("隐私与边界 — 回响 / INSIGHT", "本机数据库、加密密钥、明文图片缓存与模型调用的数据边界。", privacy, "privacy.html"), encoding="utf-8")

# Preserve the existing installer identities and download controls.
download = SITE.joinpath("download.html").read_text(encoding="utf-8")
download = download.replace('Windows Beta</h2>', 'Windows · 0.1.0 早期演示版</h2>')
download = download.replace('公开下载以发布清单为准；缺少批准、版本信息或有效安装包时保持关闭。', '仅含合成群摘要演示与账号目录检测。未启用真实微信连接、聊天档案或媒体库；新档案安装包尚未公开。')
download = download.replace('现阶段目标仅为用户手动生成群摘要；模型服务须由用户显式配置 HTTPS 端点，处理内容时可能向该服务外发。', '公开 0.1.0 仅保存模型配置，不发起调用。档案研发版的本机浏览无需云端模型；真实聊天 AI 总结尚未接入。')
if 'release-warning' not in download:
    download = download.replace('<section class="section wrap download-grid"', '<div class="wrap"><div class="callout release-warning"><b>先确认版本范围</b><p>首页视频展示的档案新功能尚未打包公开。下面的 0.1.0 是早期演示版，下载后不会获得视频中的聊天与媒体体验。</p></div></div><section class="section wrap download-grid"')
download_body = download.split('<main id="main">', 1)[1].split('</main>', 1)[0]
SITE.joinpath("download.html").write_text(page("下载预览版 — 回响 / INSIGHT", "公开 Windows 0.1.0 是早期演示版；聊天档案与媒体库新安装包尚未公开。", download_body, "download.html", '<script type="module" src="download.js"></script>'), encoding="utf-8")

notes = SITE.joinpath("release-notes.html").read_text(encoding="utf-8")
if 'IN DEVELOPMENT / 尚未打包' not in notes:
    notes = notes.replace('<div class="wrap prose-grid">', '<div class="wrap prose-grid">'+block('IN DEVELOPMENT / 尚未打包', '2026-10-02 · 档案研发进展', '新档案体验 · 不属于 0.1.0', '<p>当前源码已加入本机聊天浏览、会话分类与关注、联系人和群聊翻页、媒体分类与筛选、图片解码及原图候选选择、应用打开时的 5 分钟增量检查；修复大库 SQLite 保留锁页导致的解密失败。兼容性仍在验证。</p><p>官网图片和视频为合成示意。此次发布更新网站与介绍素材，没有替换 0.1.0 安装包；尚未发布包含这些功能的新安装包。公开构建以下载清单和下方记录为准。</p>'))
notes = notes.replace('没有自动更新、自动监控、定时摘要或自动推送；P0 目标仅为手动群摘要。', '公开 0.1.0 不提供自动监控、定时摘要或自动推送。新档案研发版的数据库定期检查是数据刷新，不是软件自动升级。')
notes = notes.replace('用户配置的 HTTPS 模型服务可能接收选定内容；使用前核对该服务的数据处理条款。端点故障或凭据失效会影响生成。', '公开 0.1.0 仅保存模型配置，不发起模型调用。真实聊天 AI 总结尚未接入；后续若调用用户配置的模型服务，应核实数据目的地与处理政策。')
notes_body = notes.split('<main id="main">', 1)[1].split('</main>', 1)[0]
SITE.joinpath("release-notes.html").write_text(page("版本记录 — 回响 / INSIGHT", "公开 0.1.0、档案研发进展及安装包的准确功能边界。", notes_body), encoding="utf-8")
print('Updated product pages; existing release metadata unchanged.')
