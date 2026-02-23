#!/usr/bin/env bash
# تثبيت FFmpeg يدوياً في سيرفر Render
apt-get update && apt-get install -y ffmpeg
# تثبيت مكتبات بايثون
pip install -r requirements.txt
