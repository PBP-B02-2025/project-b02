from django.shortcuts import render
from review.forms import ReviewForm
from review.models import Review
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm    
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
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Review added successfully!'
                }, status=201)
            else:
                # For non-AJAX requests, redirect to product detail
                return redirect('shop:product-detail', product_id=product_id)
        else:
            # Return form with errors for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'add_review.html', context)



def edit_review(request, id): #cek apakah ini ajax

    review = get_object_or_404(Review, pk=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        
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
                return redirect(reverse('shop:product-detail', args=[review.product.id]))
        
        # For AJAX requests with form errors
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review
    }

    return render(request, "update_review.html", context) 


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

def show_product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')
    form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'review_of_product.html', context)

@login_required
def delete_review(request, id):
    if request.method == 'DELETE' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        review = get_object_or_404(Review, pk=id)
        
        # Check if user owns the review
        if review.user != request.user:
            return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
        
        review.delete()
        return JsonResponse({'success': True, 'message': 'Review deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    
# def average_star(product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         avg = 0
#         size = 0

        

#         for review in product.review_set.all():
#             avg += review.star
#             size += 1

#         if size == 0:
#             return JsonResponse(0)
        
#         return JsonResponse(avg / size)
#     except:
#         return JsonResponse({'detail': 'Not found'}, status=404)
    
# def show_all_review_from_one_product(product_id):
#     try:
#         product = Product.objects.get(id=product_id)

#         review_list = []

#         for review in product.review_set.all():
#             review_list.append(review)

#         return JsonResponse(review_list)
#     except:
#         return JsonResponse({'detail': 'Not found'}, status=404)   
    

# def base_page(request):
#     review_list = Review.objects.all()
    
#     return render(request, 'dasar.html', {'review_list': review_list})

