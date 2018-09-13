import pytest

from api.models import Image
from api.api import (
    parse_text,
    get_file_from_url,
    is_valid_url,
    parse_image,
)


@pytest.mark.parametrize('value, expected', [
    ('Item 1', 'Item 1'),
    ('"Item 6, extra info"', 'Item 6'),
    ('This is a longer description that should wrap arround or broken of with ellipsis',
     'This is a longer description that should wrap arround or broken of with ellipsis'),
    ('"Item 10\nExtra line 1\nExtra line 2\nExtra line 3"', 'Item 10'),
    ('"Item 14, ""extra data"""', 'Item 14'),
    ('"Item 14, ""extra data"""', 'Item 14'),
    ('"Item 14, ""extra data"""', 'Item 14'),
    ('Description 1', 'Description 1'),
    ('"Description 4, <i>extra info</i>"', 'Description 4'),
    ('<b>Description 6</b>', '<b>Description 6</b>'),
])
def test_parse_text(value, expected):
    result = parse_text(value)
    assert expected == result


@pytest.mark.parametrize('url, expected', [
    ('Item 1', False),
    ('', False),
    ('www.google.com', False),
    ('http://www.google.com', True),
])
def test_is_valid_url(url, expected):
    assert is_valid_url(url) == expected


def test_file_from_bad_url():
    url = 'www.google.com'
    response = get_file_from_url(url)
    assert not response


def test_file_from_good_url():
    url = 'http://www.google.com'
    response = get_file_from_url(url)
    assert response.status_code == 200


def test_parse_image_bad_url(mocker):
    mocker.patch('api.api.is_valid_url', return_value=False)
    image_url = 'some url'
    image = Image(
        title='my picture', description='my description',
    )
    result = parse_image(image, image_url)

    assert not result


def test_parse_image_good_url_non_picture(mocker):
    mocker.patch('api.api.is_valid_url', return_value=True)
    mocker.patch('api.api.retrieve_image', return_value=(None, None))
    image_url = 'some url'
    image = Image(
        title='my picture', description='my description',
    )
    result = parse_image(image, image_url)

    assert not result
