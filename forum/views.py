from django.shortcuts import render
from forum.models import Forum, Comment
from django.http import JsonResponse
# Create your views here.

def show_forum(request):
    return render(request, "forum.html", {})

def show_json_forum(request):
    forum_list = Forum.objects.all()
    forum_data = [
        {
            'id': str(forum.id),
            'title': forum.title,
            'author': forum.author.username,
            'content': forum.content,
            'created_at': forum.created_at.isoformat(),
            'updated_at': forum.updated_at.isoformat(),
            'views': str(forum.forum_views),
        } for forum in forum_list
    ]
    return JsonResponse(forum_data, safe=False)

def show_json_comment(request, id):
    comment_list = Comment.objects.filter(forum_id=id)
    comment_data = [
        {
            'id': str(comment.id),
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat(),
        } for comment in comment_list
    ]
    return JsonResponse(comment_data, safe=False)