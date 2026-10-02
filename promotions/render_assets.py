"""Create synthetic product illustrations, social cards and a narrated video.

No application data, contacts, decrypted files or user screenshots are read.
Requires Pillow, FFmpeg and the six WAV files from narration.ps1.
"""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "promotions" / "media"
ASSETS = ROOT / "website" / "assets"
PAPER = "#faf9f4"
INK = "#102a23"
MUTED = "#697a6f"
GREEN = "#43d99a"
LINE = "#dbe4da"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
NARRATION = json.loads((ROOT / "promotions" / "narration.json").read_text(encoding="utf-8"))


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def text(draw, xy, value, size=24, fill=INK, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def box(draw, rect, fill="white", radius=14, outline=None):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline)


def avatar(draw, xy, value, fill="#e4eee4", size=46):
    x, y = xy
    box(draw, (x, y, x + size, y + size), fill, 12)
    text(draw, (x + 10, y + 8), value, 22, INK, True)


def illustration(media=False):
    im = Image.new("RGB", (1200, 960), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1200, 54), fill="#e8ede5")
    for x, color in [(22, "#c99781"), (44, "#d5bd76"), (66, "#8ba690")]:
        d.ellipse((x, 22, x + 10, 32), fill=color)
    text(d, (450, 15), "回响 / ECHO INSIGHT", 18, MUTED)
    text(d, (1000, 15), "合成示意", 18, MUTED)
    d.rectangle((0, 54, 192, 960), fill=INK)
    text(d, (24, 89), "回响", 34, "white", True)
    text(d, (24, 141), "本地工作空间", 16, "#9fbaa9")
    box(d, (18, 183, 174, 224), "#26483a", 7)
    text(d, (32, 193), "演示档案  v", 18, "#d8ecdc")
    for i, value in enumerate(["总览", "聊天记录", "联系人", "群聊", "公众号", "媒体库"]):
        y = 274 + i * 60
        active = (media and i == 5) or (not media and i == 1)
        if active:
            box(d, (16, y - 8, 176, y + 38), "#2a5440", 6)
        text(d, (32, y), value, 20, GREEN if active else "#bacdbd", active)
    text(d, (24, 891), "合成演示内容", 16, "#93b5a1")
    if media:
        text(d, (228, 93), "媒体库", 36, INK, True)
        text(d, (228, 149), "研报、图表、纪要，为研究留存依据。", 21, MUTED)
        box(d, (228, 214, 1165, 268), "white", 9, LINE)
        text(d, (248, 229), "搜索文件名…", 20, MUTED)
        for x, label in [(228, "图片"), (370, "视频"), (512, "文件")]:
            box(d, (x, 296, x + 120, 339), INK if x == 512 else "#e7ede4", 7)
            text(d, (x + 33, 306), label, 19, "white" if x == 512 else INK)
        text(d, (228, 375), "全部文件  ·  PDF  ·  Excel  ·  纪要  ·  音频", 20, MUTED)
        for n in range(6):
            x, y = 228 + (n % 3) * 317, 427 + (n // 3) * 218
            box(d, (x, y, x + 295, y + 198), "white", 10, LINE)
            box(d, (x + 10, y + 10, x + 285, y + 139), ["#d2e1d5", "#c3d6c8", "#dfe7d9"][n % 3], 8)
            types = ["PDF", "XLS", "DOC", "PDF", "PPT", "MP3"]
            names = ["示例科技_研究资料.pdf", "示例科技_估值表.xlsx", "行业交流_纪要.docx", "行业观察_资料.pdf", "研究假设_示例.pptx", "行业交流_示例.mp3"]
            text(d, (x + 90, y + 45), types[n], 42, "#2a6447", True)
            text(d, (x + 15, y + 149), names[n], 18, INK)
            text(d, (x + 15, y + 175), "合成文件示意 · 本机资料", 14, MUTED)
        text(d, (228, 900), "共 128 项 · 每页 6 项", 18, MUTED)
        text(d, (963, 900), "‹   1 / 22   ›", 18, INK)
    else:
        d.rectangle((193, 54, 523, 960), fill="#f1f4ed")
        d.line((523, 54, 523, 960), fill=LINE)
        text(d, (219, 92), "你的会话", 30, INK, True)
        box(d, (218, 153, 497, 200), "white", 9, LINE)
        text(d, (236, 165), "搜索会话…", 17, MUTED)
        text(d, (220, 226), "全部  ·  个人  ·  群聊  ·  公众号", 16, MUTED)
        contacts = [("研", "标的研究演示群", "示例科技：核对公告依据", "14:26"), ("报", "研报共读演示群", "资料放在本机附件里", "12:08"), ("林", "林研（虚构）", "回查原话与不同假设", "昨天"), ("行", "行业观察（演示）", "讨论仅为待核实线索", "昨天")]
        for i, (initial, name, message, time) in enumerate(contacts):
            y = 290 + i * 115
            if i == 0:
                box(d, (205, y - 13, 511, y + 86), "#ddebdc", 8)
            avatar(d, (220, y), initial)
            text(d, (278, y + 2), name, 19, INK, True)
            text(d, (278, y + 34), message, 14, MUTED)
            text(d, (278, y + 59), time + ("  ·  已关注" if i == 0 else ""), 13, MUTED)
        text(d, (233, 900), "‹   1 / 8   ›", 18, MUTED)
        avatar(d, (550, 88), "研")
        text(d, (610, 86), "标的研究演示群", 27, INK, True)
        text(d, (610, 131), "群聊 · 虚构标的 DEMO-01", 16, MUTED)
        d.line((523, 174, 1200, 174), fill=LINE)
        text(d, (553, 193), "对话    图片    视频    文件", 20, INK)
        box(d, (550, 248, 1170, 294), "white", 8, LINE)
        text(d, (570, 260), "搜索已载入消息：示例科技", 18, MUTED)
        text(d, (790, 331), "周六 14:26", 15, MUTED)
        avatar(d, (550, 385), "林")
        text(d, (612, 381), "林研（虚构）", 17, MUTED)
        box(d, (610, 416, 1090, 481), "white", 10, LINE)
        text(d, (635, 435), "示例科技：订单变化仍需核实。", 24, INK)
        avatar(d, (550, 526), "陈", "#dedec7")
        text(d, (612, 522), "陈研（虚构）", 17, MUTED)
        box(d, (610, 557, 1116, 672), "white", 10, LINE)
        text(d, (633, 579), "PDF  ·  示例科技_研究资料.pdf", 22, INK, True)
        text(d, (633, 629), "本地附件   ·   用系统应用打开 ↗", 17, MUTED)
        box(d, (747, 729, 1167, 795), "#d6edcf", 10)
        text(d, (773, 748), "先回查公告，再核对假设。", 24, INK)
        text(d, (758, 883), "只读档案 · 合成界面示意", 16, MUTED)
    return im


SCENES = [
    ("FOR INDIVIDUAL INVESTORS", ["群聊里的线索，", "成为研究起点。"], "回响 / 散户投资者的本机研究工作台", "投资研究场景", False),
    ("01 / FOLLOW YOUR GROUPS", ["关注优质群，", "留下讨论依据。"], "自己选择认可的群 · 最近消息优先", "会话关注", False),
    ("02 / RESEARCH THE IDEA", ["讨论过的标的，", "回到原话核查。"], "示例科技 DEMO-01 · 虚构标的", "回查标的讨论", False),
    ("03 / FIND THE MATERIAL", ["研报和估值表，", "找到再核对。"], "PDF · Excel · 纪要 · 音频", "本机资料浏览", True),
    ("04 / WHAT COMES NEXT", ["附件自动总结，", "是下一步方向。"], "规划中 · 尚未接入 · 当前不读正文", "自动总结规划", True),
    ("ECHO INSIGHT / PREVIEW", ["把投资群线索，", "留作研究材料。"], "huixiang.nickszy.com", "开发体验示意", False),
]


def scene(index, ui):
    label, headings, subheading, caption, _ = SCENES[index]
    im = Image.new("RGB", (1080, 1920), INK)
    d = ImageDraw.Draw(im)
    text(d, (68, 83), "回响 / INSIGHT", 30, "white", True)
    text(d, (68, 218), label, 24, GREEN)
    for i, heading in enumerate(headings):
        text(d, (60, 286 + i * 114), heading, 82, "white" if i == 0 else GREEN, True)
    text(d, (68, 538), subheading, 31, "#c9dfd0")
    display = ui.resize((944, 755), Image.Resampling.LANCZOS)
    im.paste(display, (68, 648))
    text(d, (68, 1435), "研发体验 · 合成界面示意 · 非真实录屏", 23, "#abc4b3")
    # Wrap at a deliberate phrase boundary so captions fit the mobile safe area.
    spoken = NARRATION[index]
    chunks = [spoken[i:i + 22] for i in range(0, len(spoken), 22)]
    for i, line in enumerate(chunks):
        text(d, (68, 1550 + i * 54), line, 34, "white", True)
    if index == 5:
        text(d, (68, 1658), "公开 0.1.0 是早期演示版，不含新档案功能。", 24, "#abc4b3")
    text(d, (68, 1795), f"0{index + 1} / 06", 22, "#abc4b3")
    for i in range(6):
        box(d, (730 + i * 42, 1815, 758 + i * 42, 1820), GREEN if i <= index else "#3a5445", 2)
    return im


def timestamp(seconds, vtt=False):
    return f"00:00:{seconds:02d}{'.' if vtt else ','}000"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"))
    args = parser.parse_args()
    if not args.ffmpeg:
        raise SystemExit("FFmpeg is required; pass --ffmpeg <executable>.")
    for folder in (MEDIA, ASSETS):
        folder.mkdir(parents=True, exist_ok=True)
    workspace, media = illustration(), illustration(True)
    workspace.save(ASSETS / "workspace.png")
    media.save(ASSETS / "media-library.png")
    frames = []
    for i in range(6):
        frame = scene(i, media if SCENES[i][4] else workspace)
        frame.save(MEDIA / f"scene-{i + 1:02}.png")
        card = frame.resize((810, 1440), Image.Resampling.LANCZOS)
        card.save(MEDIA / f"card-{i + 1:02}.png")
        frames.append(frame)
    frames[0].save(ASSETS / "video-cover.png")
    # 3:4 social cover is composed separately, rather than cropping video text.
    cover = Image.new("RGB", (1080, 1440), INK)
    d = ImageDraw.Draw(cover)
    text(d, (68, 86), "回响 / ECHO INSIGHT", 32, GREEN, True)
    text(d, (60, 207), "投资群里的线索", 88, "white", True)
    text(d, (60, 334), "终于有处可查", 88, GREEN, True)
    text(d, (68, 476), "关注优质群 · 回查标的 · 归档研报", 32, "#c9dfd0")
    cover.paste(workspace.resize((944, 755), Image.Resampling.LANCZOS), (68, 584))
    text(d, (68, 1370), "研发体验 · 合成示意 · 新功能尚未打包公开", 22, "#abc4b3")
    cover.save(MEDIA / "cover-xiaohongshu.png")
    social = Image.new("RGB", (1200, 630), INK)
    sd = ImageDraw.Draw(social)
    text(sd, (65, 75), "回响 / ECHO INSIGHT", 28, GREEN, True)
    text(sd, (60, 175), "群聊里的线索，", 62, "white", True)
    text(sd, (60, 270), "成为研究起点。", 62, GREEN, True)
    text(sd, (65, 445), "散户投资者的研究工作台", 30, "#c9dfd0")
    text(sd, (65, 532), "研发体验 · 合成示意 · 新档案版尚未公开", 20, "#abc4b3")
    social.paste(workspace.resize((480, 384), Image.Resampling.LANCZOS), (675, 133))
    social.save(ASSETS / "social-cover.png")
    subtitles = "\n\n".join(f"{i + 1}\n{timestamp(i * 8)} --> {timestamp((i + 1) * 8)}\n{NARRATION[i]}" for i in range(6))
    (MEDIA / "intro.srt").write_text(subtitles + "\n", encoding="utf-8")
    vtt = "WEBVTT\n\n" + "\n\n".join(f"{timestamp(i * 8, True)} --> {timestamp((i + 1) * 8, True)}\n{NARRATION[i]}" for i in range(6))
    (ASSETS / "intro.vtt").write_text(vtt + "\n", encoding="utf-8")
    segments = []
    for i in range(6):
        audio = MEDIA / f"narration-{i + 1:02}.wav"
        with wave.open(str(audio)) as wav:
            duration = wav.getnframes() / wav.getframerate()
        speed = max(1, duration / 7.3)
        if speed > 2:
            raise ValueError("Narration is too long for an eight-second scene.")
        segment = MEDIA / f"segment-{i + 1:02}.mp4"
        vf = "zoompan=z='min(zoom+0.00003,1.007)':d=1:s=1080x1920:fps=30:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2',fade=t=in:st=0:d=0.3,fade=t=out:st=7.7:d=0.3"
        cmd = [args.ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(MEDIA / f"scene-{i + 1:02}.png"), "-i", str(audio), "-vf", vf, "-af", f"atempo={speed:.5f},apad", "-t", "8", "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-threads", "2", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(segment)]
        subprocess.run(cmd, check=True)
        segments.append(segment)
        print(f"Encoded scene {i + 1}/6", flush=True)
    concat = MEDIA / "segments.txt"
    concat.write_text("\n".join(f"file '{s.name}'" for s in segments), encoding="utf-8")
    result = MEDIA / "echo-insight-intro.mp4"
    subprocess.run([args.ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(result)], check=True)
    shutil.copyfile(result, ASSETS / result.name)
    (MEDIA / "manifest.json").write_text(json.dumps({"synthetic": True, "width": 1080, "height": 1920, "fps": 30, "seconds": 48, "narration": "local Windows zh-CN TTS", "publicInstallerContainsArchiveFeatures": False}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created narrated video: {result}")


if __name__ == "__main__":
    main()
