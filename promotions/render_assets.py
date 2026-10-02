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
        text(d, (228, 149), "照片与资料，都有自己的位置。", 21, MUTED)
        box(d, (228, 214, 1165, 268), "white", 9, LINE)
        text(d, (248, 229), "搜索文件名…", 20, MUTED)
        for x, label in [(228, "图片"), (370, "视频"), (512, "文件")]:
            box(d, (x, 296, x + 120, 339), INK if x == 228 else "#e7ede4", 7)
            text(d, (x + 33, 306), label, 19, "white" if x == 228 else INK)
        text(d, (228, 375), "全部图片  ·  原图文件存在  ·  仅缩略图", 20, MUTED)
        for n in range(6):
            x, y = 228 + (n % 3) * 317, 427 + (n // 3) * 218
            box(d, (x, y, x + 295, y + 198), "white", 10, LINE)
            box(d, (x + 10, y + 10, x + 285, y + 139), ["#d2e1d5", "#c3d6c8", "#dfe7d9"][n % 3], 8)
            d.polygon([(x + 18, y + 136), (x + 100, y + 55), (x + 161, y + 115), (x + 223, y + 73), (x + 277, y + 136)], fill="#8fac94")
            d.ellipse((x + 230, y + 25, x + 253, y + 48), fill="#f6f2ce")
            text(d, (x + 15, y + 149), f"周末记录_{n + 1:02}.jpg", 18, INK)
            text(d, (x + 15, y + 175), "演示内容 · 原图候选", 14, MUTED)
        text(d, (228, 900), "共 128 项 · 每页 6 项", 18, MUTED)
        text(d, (963, 900), "‹   1 / 22   ›", 18, INK)
    else:
        d.rectangle((193, 54, 523, 960), fill="#f1f4ed")
        d.line((523, 54, 523, 960), fill=LINE)
        text(d, (219, 92), "你的会话", 30, INK, True)
        box(d, (218, 153, 497, 200), "white", 9, LINE)
        text(d, (236, 165), "搜索会话…", 17, MUTED)
        text(d, (220, 226), "全部  ·  个人  ·  群聊  ·  公众号", 16, MUTED)
        contacts = [("周", "周末散步小队", "照片已经放进文件夹啦", "14:26"), ("林", "小林", "那就周六见", "12:08"), ("读", "读书分享", "一起翻翻最近的书", "昨天"), ("城", "城市周报", "本周的城市散步路线", "昨天")]
        for i, (initial, name, message, time) in enumerate(contacts):
            y = 290 + i * 115
            if i == 0:
                box(d, (205, y - 13, 511, y + 86), "#ddebdc", 8)
            avatar(d, (220, y), initial)
            text(d, (278, y + 2), name, 19, INK, True)
            text(d, (278, y + 34), message, 14, MUTED)
            text(d, (278, y + 59), time + ("  ·  已关注" if i == 0 else ""), 13, MUTED)
        text(d, (233, 900), "‹   1 / 8   ›", 18, MUTED)
        avatar(d, (550, 88), "周")
        text(d, (610, 86), "周末散步小队", 27, INK, True)
        text(d, (610, 131), "群聊 · 演示会话", 16, MUTED)
        d.line((523, 174, 1200, 174), fill=LINE)
        text(d, (553, 193), "对话    图片    视频    文件", 20, INK)
        box(d, (550, 248, 1170, 294), "white", 8, LINE)
        text(d, (570, 260), "搜索已载入消息…", 18, MUTED)
        text(d, (790, 331), "周六 14:26", 15, MUTED)
        avatar(d, (550, 385), "林")
        text(d, (612, 381), "小林", 17, MUTED)
        box(d, (610, 416, 1090, 481), "white", 10, LINE)
        text(d, (635, 435), "照片已经放进文件夹啦。", 24, INK)
        avatar(d, (550, 526), "陈", "#dedec7")
        text(d, (612, 522), "小陈", 17, MUTED)
        box(d, (610, 557, 1116, 672), "white", 10, LINE)
        text(d, (633, 579), "PDF  ·  周末散步路线.pdf", 22, INK, True)
        text(d, (633, 629), "本地附件   ·   用系统应用打开 ↗", 17, MUTED)
        box(d, (747, 729, 1167, 795), "#d6edcf", 10)
        text(d, (773, 748), "收到，周六一起出发。", 24, INK)
        text(d, (758, 883), "只读档案 · 合成界面示意", 16, MUTED)
    return im


SCENES = [
    ("KEEP THE CONVERSATION", ["聊天里的生活，", "值得好好收藏。"], "回响 / 你的本地聊天档案", "照片、文件、聊过的事。慢慢翻，也更好找。", False),
    ("01 / CONVERSATIONS", ["关心的会话，", "先看到。"], "个人 · 群聊 · 公众号", "最近消息优先 · 会话搜索 · 关注筛选", False),
    ("02 / INSIDE THE CHAT", ["不止看对话，", "也能找资料。"], "对话 · 图片 · 视频 · 文件", "在会话里切换媒体，找回上下文。", False),
    ("03 / MEDIA LIBRARY", ["照片与文件，", "各有各的位置。"], "搜索 · 分类 · 翻页 · 排序", "可解码原图优先；只有缩略图，也说明。", True),
    ("04 / LOCAL ARCHIVE", ["自己的档案，", "在自己的电脑。"], "选择保存目录 · 默认 5 分钟检查", "应用打开时检查变化，变化的整库才更新。", True),
    ("ECHO INSIGHT / PREVIEW", ["把聊过的事，", "慢慢找回来。"], "huixiang.nickszy.com", "新档案功能尚未打包公开。", False),
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
    text(d, (60, 207), "我给微信聊天", 88, "white", True)
    text(d, (60, 334), "做了个档案馆", 88, GREEN, True)
    text(d, (68, 476), "聊天 · 照片 · 文件 · 在本机慢慢找", 32, "#c9dfd0")
    cover.paste(workspace.resize((944, 755), Image.Resampling.LANCZOS), (68, 584))
    text(d, (68, 1370), "研发体验 · 合成示意 · 新功能尚未打包公开", 22, "#abc4b3")
    cover.save(MEDIA / "cover-xiaohongshu.png")
    social = Image.new("RGB", (1200, 630), INK)
    sd = ImageDraw.Draw(social)
    text(sd, (65, 75), "回响 / ECHO INSIGHT", 28, GREEN, True)
    text(sd, (60, 175), "聊天里的生活，", 62, "white", True)
    text(sd, (60, 270), "值得好好收藏。", 62, GREEN, True)
    text(sd, (65, 445), "你的本地聊天档案", 30, "#c9dfd0")
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
