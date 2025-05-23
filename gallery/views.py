from django.shortcuts import render, get_object_or_404
from .models import Image, Category

def gallery_view(request):
    category_name = request.GET.get('category')
    if category_name:
        images = Image.objects.filter(category__name=category_name)
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
from django.shortcuts import render, get_object_or_404
