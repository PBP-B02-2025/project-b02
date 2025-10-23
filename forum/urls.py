from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_forum_list, name='show_forum'),
    path('json-forum/', show_json_forum, name='show_json'),
    path('<uuid:id>', show_forum, name='show_forum'),
    path('json-forum/<uuid:id>', show_json_forum_by_id, name='show_json_forum_by_id'),
    path('json-comment/<uuid:id>', show_json_comment, name='show_json_comment'),
    path('create-forum-ajax/', create_forum_ajax, name='create_forum_ajax')
]