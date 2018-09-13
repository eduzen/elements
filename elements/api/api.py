import io
import csv
import logging
import requests
from datetime import datetime
from PIL import Image as Pil_image

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Image


URL = (
    'https://docs.google.com/spreadsheet/ccc?key='
    '0Aqg9JQbnOwBwdEZFN2JKeldGZGFzUWVrNDBsczZxLUE&single=true&gid=0&output=csv'
)


def parse_text(text):
    # we remove extra quotes (double or simple)
    text = text.replace("'", "").replace('"', "").strip()
    text = text.replace("\n", ",")
    # If the text has extra commas, we take first element
    return text.split(',')[0]


def get_file_from_url(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == requests.codes.ok:
            return response
    except Exception:
        logging.exception("Could not get a file from that url")


def is_image(content):
    try:
        image = Pil_image.open(io.BytesIO(content))
        return image.format
    except Exception as e:
        logging.warning("The content is not an image. %s", e)
        return False


def retrieve_image(url):
    try:
        response = get_file_from_url(url)
        if not response:
            return None, None

        image_format = is_image(response.content)
        if image_format:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            return (img_temp, image_format)
    except Exception:
        logging.exception("Non image")

    return None, None


def is_valid_url(url):
    val = URLValidator()
    try:
        val(url)
        return True
    except ValidationError:
        return False


def parse_image(image, image_url):
    if not is_valid_url(image_url):
        return

    image_file, img_format = retrieve_image(image_url)
    if image_file:
        name = "{}.{}".format(
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), img_format)
        image.image_original.save(name, File(image_file))


def parse_spreadsheet(spreadsheet):
    """
        This function recieves an spreadsheet_csv file
        and iterates its lines and creates images
    """
    try:
        csv_reader = csv.reader(spreadsheet.splitlines(), delimiter=',')
    except Exception:
        logging.exception("Some text")
        return

    try:
        headers = next(csv_reader)
    except StopIteration:
        logging.exception("Empty csv")
        return
    except Exception:
        logging.exception("Corrupted data")
        return

    for row in csv_reader:
        image = Image()
        for item, header in zip(row, headers):
            if item and 'title' in header:
                image.title = parse_text(item)
            if item and 'description' in header:
                image.description = parse_text(item)
            if item and 'image' in header:
                parse_image(image, item)
        image.save()


def get_spreadsheet(url):
    """
        This function tries to decode a file from an url
    """
    try:
        response = get_file_from_url(url)
        if response.content:
            decoded_content = response.content.decode('utf-8')
            return decoded_content
    except Exception:
        logging.exception("Something wrong happen with the url")


def consume_csv_spreadsheet():
    response = get_spreadsheet(URL)
    if response:
        data = parse_spreadsheet(response)
        return data
