import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.models import Category, Image

@pytest.fixture
def category(db):
    return Category.objects.create(name='TestCat')

@pytest.fixture
def image(db, category):
    # minimal dummy-файл для ImageField
    img_file = SimpleUploadedFile(
        name='test.jpg',
        content=b'\x47\x49\x46\x38\x39\x61',
        content_type='image/jpeg'
    )
    img = Image.objects.create(
        title='My Image',
        image=img_file,
        created_date='2025-01-01',
        age_limit=0
    )
    img.categories.add(category)
    return img

@pytest.mark.django_db
def test_gallery_view_status_and_context(client, category, image):
    url = reverse('main')
    resp = client.get(url)
    assert resp.status_code == 200
    # переконуємося, що в контексті є категорії
    assert 'categories' in resp.context
    cats = list(resp.context['categories'])
    assert category in cats

@pytest.mark.django_db
def test_gallery_view_shows_images_in_category(client, category, image):
    url = reverse('main')
    resp = client.get(url)
    # знайдемо нашу категорію в контексті
    cats = resp.context['categories']
    cat = next(c for c in cats if c == category)
    imgs = list(cat.image_set.all())
    assert image in imgs

@pytest.mark.django_db
def test_image_detail_view_success(client, image):
    url = reverse('image_detail', args=[image.pk])
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.context['image'] == image

@pytest.mark.django_db
def test_image_detail_view_404(client):
    url = reverse('image_detail', args=[9999])
    resp = client.get(url)
    assert resp.status_code == 404