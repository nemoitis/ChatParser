from urllib.parse import urlparse
import easyocr
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from uuid import uuid4
import os
import re
from gibberish_detector import detector

reader = easyocr.Reader(['en'])
gd = detector.create_from_model('./big.model')


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def download(url):
    if not validate_url(url):
        raise ValueError("Invalid URL")

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to download image")
    return response.content


def read(img):
    og_width, og_height = img.size
    # Crop the image 15% from top, 10% from bottom to
    # filter out unwanted artifacts
    img = img.crop((
        0,
        int((15 * og_height)/100),
        og_width,
        (og_height - int((10 * og_height)/100))
    ))
    return reader.readtext(np.array(img), paragraph=True, detail=1)


def annotate(lines, width, list=False):
    annotated_lines = []
    for position, line in lines:
        # Replace misplaced |
        line = line.replace("|", "I")

        # Check if the text matches with some known noise patterns,
        # or, if it's some random gibberish text
        if not is_desired_text(line) or gd.is_gibberish(line):
            continue

        # Determine the sender by comparing the X position
        # with an arbitrary threshold
        sender = 'he' if position[0][0] > int((width * 20)/100) else 'she'

        if list:
            annotated_lines.append(f"{sender}: {line}")
        else:
            annotated_lines.append({'sender': sender, 'body': line})

    return annotated_lines


def is_desired_text(text):
    undesired_patterns = [
        "Type a message Send",
        "Snapchat",
        "Ne Sent",
        "Delivered",
        "Message\n\n",
        "iMessage",
        "Reply Sent"
        '((1[0-2]|0?[1-9]):([0-5][0-9]))'
    ]

    if any(re.search(pattern, text) for pattern in undesired_patterns):
        return False
    return True


def extract(path, list=False):
    if not path:
        return

    content = path if os.path.exists(path) else BytesIO(download(path))
    img = Image.open(content)
    lines = read(img)
    return annotate(lines, img.width, list)
