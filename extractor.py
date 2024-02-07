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
    # Convert the image to grayscale for better readability
    img = img.convert('L')
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

        # Calculate half, one-fourth, and three-fourth of the image's width
        HALF_WD = int(width/2)
        ONE_FORTH_WD = int(width/4)
        THREE_FOURTH_WD = HALF_WD + ONE_FORTH_WD
        # X at the top-left and top-right corner of the image
        x_start, _ = position[0]
        x_end, _ = position[1]
        # Y at the top-right and bottom-right corner of the image
        _, y_start = position[1]
        _, y_end = position[2]

        # If the starting and ending of the message box is within 50% from the
        # half of the image, or the message box width is less than half of
        # one fourth and the height is less that 45 (an arbitrary value)
        # chances that it is most probably a system message, e.g. time.
        if ((x_start > ONE_FORTH_WD) and (x_end < (THREE_FOURTH_WD))) \
                or (((x_end - x_start) < ONE_FORTH_WD/2) and (y_end - y_start) <= 45):
            sender = 'system'

        # If starting of the message box is less than one-fourth of the width
        # and end of the message box is within the third divider line, then
        # it is most probably an incoming message.
        elif (x_start < ONE_FORTH_WD) and (x_end < (THREE_FOURTH_WD + ONE_FORTH_WD/2)):
            sender = 'she'

        # If the ending of the message box is way out of the third divider line,
        # it is most probably a outgoing message.
        elif x_end > THREE_FOURTH_WD:
            sender = 'he'

        # If none of the above conditions are satisfied, ignore the message.
        else:
            continue

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
