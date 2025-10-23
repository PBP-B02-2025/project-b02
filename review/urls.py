from django.urls import path
from review.views import *
app_name = 'review'

urlpatterns = [
    path('review/add-review', add_review, name='add_review'),
    path('review/<uuid:id>/edit', edit_review, name='edit_review'),
    path('review/<uuid:id>/delete', delete_review, name='delete_review'),
    path('review/<uuid"id>/read', read_review_by_json, name='read_review_by_json'),
]