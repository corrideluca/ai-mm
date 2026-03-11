"""
Video Creator — Generate faceless short-form videos for TikTok/Instagram Reels
Uses Pillow for frame generation + moviepy for video assembly
No ffmpeg binary needed — imageio-ffmpeg bundles it
"""

import os
import sys
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Video dimensions (vertical 9:16)
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Colors
BG_COLOR = (10, 10, 15)  # Near-black
ACCENT_GREEN = (0, 255, 136)  # Neon green
ACCENT_BLUE = (0, 170, 255)  # Electric blue
ACCENT_RED = (255, 60, 60)  # Alert red
WHITE = (255, 255, 255)
GRAY = (150, 150, 160)
YELLOW = (255, 220, 50)

# Output directory
OUTPUT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "content" / "videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size, bold=False):
    """Try to load a good font, fallback to default."""
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def create_frame(width=WIDTH, height=HEIGHT, bg_color=BG_COLOR):
    """Create a blank frame."""
    img = Image.new('RGB', (width, height), bg_color)
    return img, ImageDraw.Draw(img)


def draw_centered_text(draw, text, y, font, color=WHITE, max_width=None):
    """Draw centered text, return bounding box height."""
    if max_width:
        lines = textwrap.wrap(text, width=max_width)
    else:
        lines = [text]

    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (WIDTH - text_width) // 2
        draw.text((x, y + total_height), line, font=font, fill=color)
        total_height += text_height + 10

    return total_height


def draw_stat_block(draw, label, value, y, label_color=GRAY, value_color=ACCENT_GREEN):
    """Draw a stat with label above and big value below."""
    label_font = get_font(36)
    value_font = get_font(72, bold=True)

    # Label
    bbox = draw.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    draw.text(((WIDTH - lw) // 2, y), label, font=label_font, fill=label_color)

    # Value
    bbox = draw.textbbox((0, 0), value, font=value_font)
    vw = bbox[2] - bbox[0]
    draw.text(((WIDTH - vw) // 2, y + 50), value, font=value_font, fill=value_color)

    return 130  # block height


def draw_progress_bar(draw, y, progress, width=800, height=20, color=ACCENT_GREEN):
    """Draw a progress bar."""
    x = (WIDTH - width) // 2
    # Background
    draw.rounded_rectangle([(x, y), (x + width, y + height)], radius=10, fill=(40, 40, 50))
    # Fill
    fill_width = int(width * progress)
    if fill_width > 0:
        draw.rounded_rectangle([(x, y), (x + fill_width, y + height)], radius=10, fill=color)
    return height + 20


def generate_day_recap_frames(day_num, balance, started_with, trades_won, trades_lost,
                               followers, articles, tools_shipped, bounty_pending,
                               highlight_text="", extra_stats=None):
    """Generate frames for a daily recap video."""
    frames = []

    # --- FRAME 1: Hook (2 seconds = 60 frames) ---
    for i in range(60):
        img, draw = create_frame()

        # Animated fade-in effect
        alpha = min(1.0, i / 20)

        hook_font = get_font(64, bold=True)
        sub_font = get_font(40)

        # Main hook
        opacity = int(255 * alpha)
        hook_color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))

        draw_centered_text(draw, f"DAY {day_num}/100", 600, hook_font, color=YELLOW)
        draw_centered_text(draw, "AI AGENT vs $20", 700, get_font(56, bold=True), color=WHITE)

        # Subtitle appears after 0.5s
        if i > 15:
            sub_alpha = min(1.0, (i - 15) / 15)
            sub_color = (int(150 * sub_alpha), int(150 * sub_alpha), int(160 * sub_alpha))
            draw_centered_text(draw, "Can an AI turn $20 into $1K?", 820, sub_font, color=sub_color)

        # Bottom watermark
        wm_font = get_font(28)
        draw_centered_text(draw, "@agent_20usd", 1780, wm_font, color=GRAY)

        frames.append(img)

    # --- FRAME 2: Balance (2 seconds) ---
    for i in range(60):
        img, draw = create_frame()

        title_font = get_font(44, bold=True)
        draw_centered_text(draw, f"DAY {day_num} RESULTS", 200, title_font, color=ACCENT_BLUE)

        # Divider line
        draw.line([(200, 280), (880, 280)], fill=ACCENT_BLUE, width=2)

        y = 350

        # Balance with color coding
        balance_color = ACCENT_GREEN if balance >= started_with else ACCENT_RED
        y += draw_stat_block(draw, "CURRENT BALANCE", f"${balance:.2f}", y, value_color=balance_color)
        y += 30

        # P&L
        pnl = balance - started_with
        pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        pnl_color = ACCENT_GREEN if pnl >= 0 else ACCENT_RED
        y += draw_stat_block(draw, "P&L FROM $20", pnl_str, y, value_color=pnl_color)
        y += 30

        # Progress bar to $1K
        progress = balance / 1000
        draw_centered_text(draw, "PROGRESS TO $1K", y, get_font(32), color=GRAY)
        y += 45
        draw_progress_bar(draw, y, progress, color=ACCENT_BLUE)
        y += 50
        pct = f"{progress * 100:.6f}%"
        draw_centered_text(draw, pct, y, get_font(36, bold=True), color=ACCENT_BLUE)

        # Watermark
        draw_centered_text(draw, "@agent_20usd", 1780, get_font(28), color=GRAY)

        frames.append(img)

    # --- FRAME 3: Stats Grid (2.5 seconds) ---
    for i in range(75):
        img, draw = create_frame()

        title_font = get_font(44, bold=True)
        draw_centered_text(draw, "WHAT I DID TODAY", 200, title_font, color=WHITE)
        draw.line([(200, 280), (880, 280)], fill=ACCENT_GREEN, width=2)

        y = 340
        stat_font = get_font(42, bold=True)
        label_font = get_font(32)

        stats = [
            ("Trades Won / Lost", f"{trades_won}W / {trades_lost}L", YELLOW),
            ("Twitter Followers", str(followers), ACCENT_BLUE),
            ("Articles Published", str(articles), ACCENT_GREEN),
            ("Tools Shipped", str(tools_shipped), ACCENT_GREEN),
            ("Bounties Pending", f"${bounty_pending}", YELLOW),
        ]

        if extra_stats:
            stats.extend(extra_stats)

        for label, value, color in stats:
            # Show stats appearing one by one
            stat_index = stats.index((label, value, color))
            appear_frame = stat_index * 8

            if i > appear_frame:
                # Label (left aligned)
                draw.text((120, y), label, font=label_font, fill=GRAY)
                # Value (right aligned)
                bbox = draw.textbbox((0, 0), value, font=stat_font)
                vw = bbox[2] - bbox[0]
                draw.text((WIDTH - 120 - vw, y - 5), value, font=stat_font, fill=color)

                # Separator line
                draw.line([(120, y + 55), (WIDTH - 120, y + 55)], fill=(30, 30, 40), width=1)

            y += 70

        draw_centered_text(draw, "@agent_20usd", 1780, get_font(28), color=GRAY)
        frames.append(img)

    # --- FRAME 4: Highlight / Call to Action (2 seconds) ---
    for i in range(60):
        img, draw = create_frame()

        if highlight_text:
            # Big highlight message
            draw_centered_text(draw, "TODAY'S HIGHLIGHT", 500, get_font(36), color=GRAY)
            draw_centered_text(draw, highlight_text, 580, get_font(48, bold=True), color=ACCENT_GREEN, max_width=25)

        # CTA
        cta_y = 1000
        draw_centered_text(draw, "Follow the journey", cta_y, get_font(44, bold=True), color=WHITE)
        draw_centered_text(draw, "@agent_20usd on X/Twitter", cta_y + 60, get_font(36), color=ACCENT_BLUE)
        draw_centered_text(draw, "ai-hustle-lab-three.vercel.app", cta_y + 120, get_font(32), color=GRAY)

        # Day counter
        draw_centered_text(draw, f"Day {day_num} of 100", cta_y + 200, get_font(40, bold=True), color=YELLOW)

        draw_centered_text(draw, "@agent_20usd", 1780, get_font(28), color=GRAY)
        frames.append(img)

    return frames


def frames_to_video(frames, output_path, fps=FPS):
    """Assemble PIL frames into a video file using moviepy."""
    import numpy as np
    from moviepy import ImageSequenceClip

    # Convert PIL images to numpy arrays
    np_frames = [np.array(frame) for frame in frames]

    clip = ImageSequenceClip(np_frames, fps=fps)
    clip.write_videofile(
        str(output_path),
        codec='libx264',
        audio=False,
        fps=fps,
        preset='medium',
        logger=None
    )

    return str(output_path)


def create_day_video(day_num, balance, started_with=20.0, trades_won=0, trades_lost=0,
                     followers=1, articles=14, tools_shipped=6, bounty_pending=600,
                     highlight_text="", extra_stats=None, filename=None):
    """Create a complete day recap video."""

    if not filename:
        filename = f"day-{day_num:03d}-recap.mp4"

    output_path = OUTPUT_DIR / filename

    print(f"Generating frames for Day {day_num} video...")
    frames = generate_day_recap_frames(
        day_num=day_num,
        balance=balance,
        started_with=started_with,
        trades_won=trades_won,
        trades_lost=trades_lost,
        followers=followers,
        articles=articles,
        tools_shipped=tools_shipped,
        bounty_pending=bounty_pending,
        highlight_text=highlight_text,
        extra_stats=extra_stats,
    )

    print(f"Assembling {len(frames)} frames into video...")
    result = frames_to_video(frames, output_path)

    file_size = os.path.getsize(result) / (1024 * 1024)
    duration = len(frames) / FPS

    print(f"Video created: {result}")
    print(f"Duration: {duration:.1f}s | Size: {file_size:.1f}MB | Frames: {len(frames)}")

    return result


if __name__ == "__main__":
    # Day 3 recap video
    video = create_day_video(
        day_num=3,
        balance=2.17,
        started_with=20.0,
        trades_won=2,
        trades_lost=3,
        followers=1,
        articles=14,
        tools_shipped=6,
        bounty_pending=600,
        highlight_text="Built AI chatbot + 5 thread replies + 2 Gumroad products ready",
        extra_stats=[
            ("Thread Replies", "5", ACCENT_BLUE),
            ("Gumroad Products", "2 ready", YELLOW),
        ]
    )
    print(f"\nDone! Video saved to: {video}")
