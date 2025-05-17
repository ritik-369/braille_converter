#!/usr/bin/env bash
# set -o errexit

# Update package lists (no sudo)
# apt-get update -y

# Install system dependencies (no sudo)
apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    ffmpeg

# Install Python dependencies
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate