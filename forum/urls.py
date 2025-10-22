from django.urls import path
from forum.views import show_forum, show_json_forum, show_json_comment

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show_forum'),
    path('json-forum/', show_json_forum, name='show_json'),
    path('json-comment/<uuid:id>', show_json_comment, name='show_json_comment'),
]