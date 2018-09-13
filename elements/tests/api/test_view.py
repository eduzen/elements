import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Image


@pytest.mark.django_db(transaction=True)
def test_api_can_create_image():
    """Test the api can create a image."""
    client = APIClient()
    data = {'title': 'my picture', 'description': 'my description', }
    response = client.post('/api/image/', data, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_api_can_get_image():
    """Test the api can get a image."""
    client = APIClient()
    image1 = Image.objects.create(title='my picture', description='my description',)

    images = Image.objects.get()

    response = client.get('/api/image/', kwargs={'pk': image1.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['id'] == images.id


@pytest.mark.django_db(transaction=True)
def test_api_can_delete_bucketlist():
    """Test the api can delete a image."""
    client = APIClient()
    image1 = Image.objects.create(title='my picture', description='my description',)
    image = Image.objects.get()
    response = client.delete(
        reverse('image_details', kwargs={'pk': image1.id}),
        format='json',
        follow=True)


@pytest.mark.django_db(transaction=True)
def test_api_can_get_image_list():
    """Test the api can get a list of image."""
    client = APIClient()
    image1 = Image.objects.create(title='my picture', description='my description',)
    image2 = Image.objects.create(title='my picture', description='my description',)

    images = Image.objects.all()

    response = client.get('/api/image/', format="json")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(images)


def test_api_get_data_ok(mocker):
    client = APIClient()
    mocker.patch('api.views.consume_csv_spreadsheet', return_value="Something")
    response = client.get('/api/load_data/', format="json")

    assert response.status_code == status.HTTP_200_OK
