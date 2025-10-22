from django.urls import path
from review.views import *
app_name = 'review'

urlpatterns = [
    path('review/add-review', add_review, name='add_review'),
    path('review/edit-review', edit_review, name='edit_review'),
    path('review/delete-review', delete_review, name='delete_review'),
    path('review/read-review', read_review_by_json, name='read_review_by_json'),
]