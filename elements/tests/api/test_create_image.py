import pytest
from api.models import Image


@pytest.mark.django_db
def test_save_image_without_pic():
    image = Image(
        title='my picture', description='my description',
    )
    image.save()

    assert image.title == 'my picture'
    assert image.description == 'my description'
