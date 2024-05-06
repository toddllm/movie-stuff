import os

from sys import platform

def set_magick_path():
    # Define possible paths for the ImageMagick binary
    windows_path = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
    mac_path = "/usr/local/bin/magick"

    # Check the platform and set the path accordingly
    if platform == "darwin":  # Darwin is the system name for macOS
        # Check if the magick command exists in the typical macOS install path
        if os.path.isfile(mac_path):
            os.environ["IMAGEMAGICK_BINARY"] = mac_path
        else:
            print("ImageMagick not found on macOS at expected location.")
    elif platform == "win32":  # Win32 covers both 32-bit and 64-bit Windows
        # Check if the magick command exists in the typical Windows install path
        if os.path.isfile(windows_path):
            os.environ["IMAGEMAGICK_BINARY"] = windows_path
        else:
            print("ImageMagick not found on Windows at expected location.")
    else:
        print("Unsupported OS or ImageMagick not found. Please check your installation.")

# Set ImageMagick path before using it with moviepy
set_magick_path()

from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

def create_scrolling_text(text_lines, duration, fps=24, font_size=70, text_color='black', bg_color=(255, 192, 203)):
    # Create a background clip (solid color)
    background_clip = ColorClip(size=(1280, 720), color=bg_color, duration=duration)

    # Initialize variables to calculate text starting positions
    line_spacing = font_size * 2  # Adjust spacing as necessary
    total_height = line_spacing * len(text_lines)

    # Create text clips for each line
    text_clips = []
    for index, line in enumerate(text_lines):  # 
        text_clip = TextClip(line, fontsize=font_size, color=text_color, size=(1280, font_size * 2))
        start_y = -(index * line_spacing)  # Adjust to position lines correctly from the bottom
        text_clip = text_clip.set_position(('center', start_y))
        text_clip = text_clip.set_duration(duration)
        text_clips.append(text_clip)

    # Set the scroll speed
    scroll_speed = 100  # Pixels per second

    # Function to calculate y position during scroll
    def get_y(t, start_y):
        return start_y - scroll_speed * t

    # Animate each text clip
    animated_text_clips = []
    for index, text_clip in enumerate(text_clips):
        start_y = index * line_spacing  # Calculate unique start y for each line from top to bottom
        animated_text_clip = text_clip.set_position(lambda t, sy=start_y: ('center', get_y(t, sy)))
        animated_text_clips.append(animated_text_clip)

    # Composite all text clips over the background
    video = CompositeVideoClip([background_clip] + animated_text_clips)
    video = video.set_duration(duration)

    return video

# Example usage
text_lines = [
    "Fred and Tom Movie",
    "Created by Chelsea Deshane",
    "Copyright 2024",
    "Create with the following: ",
    "ChatGPT + DALLE-E-3",
    "Runway Gen2",
    "Eleven Labs",
    "Udio",
    "OpenShot",
    "Fred and Tom Movie",
    "Created by Chelsea Deshane",
    "Copyright 2024",
    "All Rights Reserved",
]

duration = 18  # Duration of the scrolling effect
video = create_scrolling_text(text_lines, duration)
video.write_videofile("movie_credits.mp4", fps=24)
