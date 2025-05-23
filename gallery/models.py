from django.shortcuts import render, get_object_or_404
from .models import Image, Category

def gallery_view(request):
    # зчитуємо назву категорії з GET-параметра
    category_name = request.GET.get('category')
    if category_name:
        # фільтруємо по ManyToManyField
        images = Image.objects.filter(categories__name=category_name).distinct()
    else:
        images = Image.objects.all()

    categories = Category.objects.all()
    return render(request, 'gallery/gallery.html', {
        'images': images,
        'categories': categories,
        'selected_category': category_name
    })

def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request, 'gallery/image_detail.html', {
        'image': image
    })
