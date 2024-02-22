from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Products
from django.utils import timezone


def home(request):
    products = Products.objects
    return render(request, 'products/home.html',{'products':products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        icon_file = request.FILES.get('icon')
        image_file = request.FILES.get('image')

        print("Received title:", title)
        print("Received body:", body)
        print("Received URL:", url)
        print("Received icon file:", icon_file)
        print("Received image file:", image_file)


        if title and body and url and icon_file and image_file:
            product = Products()
            product.title = title
            product.body = body
            if url.startswith('http://') or url.startswith('https://'):
                product.url = url
            else:
                product.url = 'http://' + url
            product.icon = icon_file
            product.image = image_file
            product.pub_date = timezone.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'products/detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        product.votes_total += 1
        product.save()
    return redirect('/products/' + str(product.id))
