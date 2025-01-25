#!/usr/bin/python3
import json
import os
import subprocess
import shutil
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from picamera2 import Picamera2, Preview
from PIL import Image, ImageDraw, ImageFont
from smtplib import SMTP

from environment import getTempAndHumidity


def loadConfig() -> object:
    """Loads config file"""
    with open("config.json", "r") as f:
        cfg: object = json.load(f)

    return cfg


def updateConfig(vars: object) -> object:
    cfg["variables"] = vars

    return cfg


def getTimestamp() -> str:
    """Returns times stamp used for album name"""
    timestamp: str = time.strftime("%b_%d_%Y_%H:%M:%S")

    return timestamp


def getAlbumName(folder: str, subfolder: str) -> str:
    """Returns name of the main directory for images and video"""
    album_name: str = f"{folder}/{subfolder}/"

    return album_name


def drawText(path: str, font: object, fill: object) -> None:
    """Opens image file, draw text, deletes original file and saves the new image"""
    img: object = Image.open(path)
    draw: object = ImageDraw.Draw(img, mode="RGBA")
    os.remove(path)

    temperature, humidity = getTempAndHumidity()
    # temperature, humidity = 75, 40

    draw.text((10, 420), time.strftime("%b_%d_%Y"), font=font, fill=fill)
    draw.text((10, 440), time.strftime("%H:%M:%S"), font=font, fill=fill)
    draw.text((10, 460), f"Temp: {temperature:.1f}°f", font=font, fill=fill)
    draw.text((10, 480), f"Humid: {humidity:.1f}%", font=font, fill=fill)

    img.save(path)


def takePictures(cfg: object, timestamp: str) -> None:
    """Take Pictures for timelapse series"""

    photos: int = int(cfg["server_settings"]["number_of_photos"])
    photo_delay: int = int(cfg["server_settings"]["secs_between_photos"])
    tuning_file: str = cfg["video_settings"]["tuning_file"]
    output_dir: str = cfg["video_settings"]["output_folder"]
    show_preview: bool = cfg["general_settings"]["show_preview"]

    # picam2: Picamera2 = Picamera2(tuning=Picamera2.load_tuning_file("imx477.json"))
    picam2: Picamera2 = Picamera2(tuning=Picamera2.load_tuning_file(tuning_file))
    config: dict = picam2.create_preview_configuration(main={"size": (800, 600)})
    preview: Preview = Preview.QT if show_preview else Preview.NULL

    picam2.start_preview(preview)
    picam2.start(config=config, show_preview=show_preview)

    album_name: str = f"{output_dir}/{timestamp}/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.makedirs(album_name)
    os.makedirs(f"{album_name}images")

    start_time: float = time.time()
    image_font: object = ImageFont.truetype("fonts/FreeMono.ttf", 18)
    image_fill: object = (255, 255, 255)

    for i in range(0, photos):
        image_num: int = f"{i + 1:03d}"
        image_path: str = f"{album_name}/images/image{image_num}.jpg"

        request: None = picam2.capture_request()
        request.save("main", image_path)
        request.release()

        drawText(image_path, image_font, image_fill)

        print(
            f"Captured image {image_num} of {photos} at {time.time() - start_time:.2f}s"
        )
        time.sleep(photo_delay)

    picam2.close()


def createVideo(
    input_pattern: str,
    output_file: str,
    fps: int = 30,
    pix_fmt: str = "yuv420p",
    codec: str = "libx264",
) -> None:
    """Creates a timelapse video from the images, using FFMPEG."""
    cmd: list = [
        "ffmpeg",
        "-r",
        str(fps),  # Set the desired frame rate for the output video
        "-pattern_type",
        "glob",  # Use glob pattern matching for input files
        "-i",
        input_pattern,  # Input image pattern (e.g., '*.jpg')
        "-c:v",
        codec,  # Specify the video codec (e.g., libx264, h265)
        "-pix_fmt",
        pix_fmt,  # Set the pixel format (e.g., yuv420p)
        output_file,  # Output video file
    ]

    subprocess.run(cmd)


def sendEmail(cfg: object, video_file: MIMEBase, timestamp: str) -> None:
    """Email video file"""
    output_dir: str = cfg["video_settings"]["output_folder"]
    mp4_name: str = cfg["video_settings"]["mp4_name"]
    subject: str = cfg["email_settings"]["subject"]
    mail_sever: str = cfg["email_settings"]["mail_server"]
    app_pwd: str = cfg["email_settings"]["app_password"]
    from_addr: str = cfg["email_settings"]["from_addr"]
    to_addrs: list = cfg["email_settings"]["to_addrs"]

    album_name: str = f"{output_dir}/{timestamp}/"
    mp4_path: str = f"{album_name}{mp4_name}"

    video_file: MIMEBase = MIMEBase("application", "octet-stream")
    video_file.set_payload(open(mp4_path, "rb").read())
    video_file.add_header(
        "content-disposition", "attachment; filename={}".format(mp4_path)
    )

    # Delete images file
    shutil.rmtree(f"{album_name}images")

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    recipients: str = ", ".join(to_addrs)

    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = recipients
    msg["Subject"] = subject
    msg["Content"] = timestamp

    msg.attach(video_file)

    server: SMTP = SMTP(mail_sever, 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=recipients)


def sendTimelapse(cfg: object, timestamp: str) -> str:
    """
    Take images based on config.json inputs
    Creates timelapse video file out of images
    Sends timelapse video by email
    """
    fps: int = cfg["server_settings"]["frames_per_second"]
    output_dir: str = cfg["video_settings"]["output_folder"]
    mp4_name: str = cfg["video_settings"]["mp4_name"]
    make_video: bool = cfg["general_settings"]["convert_to_video"]
    send_email: bool = cfg["general_settings"]["send_email"]
    timestamp: str = timestamp
    album_name: str = f"{output_dir}/{timestamp}/"
    mp4_path: str = f"{album_name}{mp4_name}"
    input_pattern: str = f"{album_name}/images/image*.jpg"

    takePictures(cfg, timestamp)

    if make_video:
        video_file = createVideo(input_pattern, mp4_path, fps)
        # createVideo(input_pattern, mp4_path, fps)

    if send_email:
        sendEmail(cfg, video_file, timestamp)


def run() -> None:
    timestamp = getTimestamp()
    sendTimelapse(cfg, timestamp)


if __name__ == "__main__":
    cfg: object = loadConfig()
    timestamp: str = getTimestamp()
    output_dir: str = cfg["video_settings"]["output_folder"]
    mp4_name: str = cfg["video_settings"]["mp4_name"]
    album_name: str = f"{output_dir}/{timestamp}/"

    make_video: bool = cfg["general_settings"]["convert_to_video"]
    send_email: bool = cfg["general_settings"]["send_email"]
    debug: bool = cfg["general_settings"]["DEBUG"]

    takePictures(cfg, timestamp)

    if make_video:
        input_pattern: str = f"{album_name}/images/image*.jpg"
        output_file: str = f"{album_name}/{mp4_name}"
        fps: int = cfg["server_settings"]["frames_per_second"]

        video_file = createVideo(input_pattern, output_file, fps)

    if send_email:
        sendEmail(cfg, video_file, timestamp)
