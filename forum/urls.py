from django.urls import path
from forum.views import show_forum_list, show_json_forum, show_json_comment, show_json_forum_by_id, show_forum, create_forum_ajax

app_name = 'forum'

urlpatterns = [
    path('', show_forum_list, name='show_forum'),
    path('json-forum/', show_json_forum, name='show_json'),
    path('create-ajax/', create_forum_ajax, name='create_forum_ajax'),
    path('<uuid:id>', show_forum, name='show_forum'),
    path('json-forum/<uuid:id>', show_json_forum_by_id, name='show_json_forum_by_id'),
    path('json-comment/<uuid:id>', show_json_comment, name='show_json_comment'),
]