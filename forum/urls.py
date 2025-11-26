from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_forum_list, name='show_forum_list'),
    path('json-forum/', show_json_forum, name='show_json'),
    path('<uuid:id>', show_forum, name='show_forum'),
    path('json-forum/<uuid:id>', show_json_forum_by_id, name='show_json_forum_by_id'),
    path('json-comment/<uuid:id>', show_json_comment, name='show_json_comment'),
    path('create-forum-ajax/', create_forum_ajax, name='create_forum_ajax'),
    path('create-comment-ajax/', create_comment_ajax, name='create_comment_ajax'),
    path('delete-forum-ajax/', delete_forum_ajax, name='delete_forum_ajax'),
    path('edit-forum-ajax/', edit_forum_ajax, name='edit_forum_ajax'),
    path('delete-comment-ajax/', delete_comment_ajax, name='delete_comment_ajax'),
    path('edit-comment-ajax/', edit_comment_ajax, name='edit_comment_ajax'),
    path('json-forum-sort/', show_json_forum_sort, name='json_forum_sort'),
    path('create-forum-flutter/', create_forum_flutter, name='create_forum_flutter'),
    path('edit-forum-flutter/', edit_forum_flutter, name='edit_forum_flutter'),
    path('delete-forum-flutter/', delete_forum_flutter, name='delete-forum-flutter'),
    path('create-comment-flutter/', add_comment_flutter, name='create_comment_flutter'),
    path('edit-comment-flutter/', edit_comment_flutter, name='edit_comment_flutter'),
    path('delete-comment-flutter/', delete_comment_flutter, name='delete-comment-flutter'),
]