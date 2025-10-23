from django.shortcuts import render
from review.forms import ProductForm
from review.models import Review
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from shop.models import Product
from django.core import serializers

from django.utils.html import strip_tags
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


# Create your views here.

@login_required
def add_review(request, product_id):
    comment = strip_tags(request.POST.get("comment"))
    star = request.POST.get("star")
    user = request.user
    product = get_object_or_404(Product, id=product_id)

    new_review = Review(
        user=user,
        comment=comment,
        star=star,
        product=product
    )

    new_review.save()

    return HttpResponse(b"CREATED", status=201)


def edit_review(request, id): #cek apakah ini ajax

    review = get_object_or_404(Review, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=review)
        
        # Debug logging
        print(f"POST data: {request.POST}")
        print(f"Form errors: {form.errors}")
        print(f"Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            form.save()
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Review updated successfully!'
                })
            else:
                return redirect('main:show_main')
        
        # For AJAX requests with form errors
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    else:
        form = ProductForm(instance=review)

    context = {
        'form': form,
        'review': review
    }

    return render(request, "edit_jersey.html", context) 


def read_review_by_json(request, id):
    try:
        review = Review.objects.select_related('user').get(pk=id)
        data = {
            'id': str(review.id),
            'comment': review.comment,
            'star': review.star,
            'user': str(review.user),
            'product': str(review.product)
        }
        return JsonResponse(data)
    except Review.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def delete_review(request, id):
    if request.method == 'DELETE' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        review = get_object_or_404(Review, pk=id)
        review.delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def average_star(product_id):
    try:
        product = Product.objects.get(id=product_id)
        avg = 0
        size = 0

        

        for review in product.review_set.all():
            avg += review.star
            size += 1

        if size == 0:
            return JsonResponse(0)
        
        return JsonResponse(avg / size)
    except:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
def show_all_review_from_one_product(product_id):
    try:
        product = Product.objects.get(id=product_id)

        review_list = []

        for review in product.review_set.all():
            review_list.append(review)

        return JsonResponse(review_list)
    except:
        return JsonResponse({'detail': 'Not found'}, status=404)   
    

def base_page(request):
    review_list = Review.objects.all()
    
    return render(request, 'dasar.html', {'review_list': review_list})

