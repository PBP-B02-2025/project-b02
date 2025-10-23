from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_forum_list, name='show_forum'),
    path('json-forum/', show_json_forum, name='show_json'),
    path('<uuid:id>', show_forum, name='show_forum'),
    path('json-forum/<uuid:id>', show_json_forum_by_id, name='show_json_forum_by_id'),
    path('json-comment/<uuid:id>', show_json_comment, name='show_json_comment'),
    path('create-forum-ajax/', create_forum_ajax, name='create_forum_ajax'),
    path('create-comment-ajax/', create_comment_ajax, name='create_comment_ajax'),
    path('delete-forum-ajax/', delete_forum_ajax, name='delete_forum_ajax'),
]