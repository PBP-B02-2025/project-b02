from django.shortcuts import render
from forum.models import Forum, Comment
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.

def show_forum_list(request):
    context = {
        'active_page': 'forum'
    }
    return render(request, "forum.html", context)

def show_forum(request, id):
    context = {
        'id': id,
        'active_page': 'forum'
    }
    return render(request, "forum_detail.html", context)

def show_json_forum(request):
    forum_list = Forum.objects.annotate(comment_count=Count('comment'))
    forum_data = [
        {
            'id': str(forum.id),
            'title': forum.title,
            'author': forum.author.username,
            'content': forum.content,
            'created_at': forum.created_at.isoformat(),
            'updated_at': forum.updated_at.isoformat(),
            'views': str(forum.forum_views),
            'comment_count': str(forum.comment_count),
        } for forum in forum_list
    ]
    return JsonResponse(forum_data, safe=False)

def show_json_forum_by_id(request, id):
    try:
        forum = Forum.objects.get(pk=id)
        forum_data = {
            'id': str(forum.id),
            'title': forum.title,
            'author': forum.author.username,
            'content': forum.content,
            'created_at': forum.created_at.isoformat(),
            'updated_at': forum.updated_at.isoformat(),
            'views': str(forum.forum_views),
        } 
        return JsonResponse(forum_data)
    except Forum.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

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

@login_required(login_url='/login/')
@csrf_exempt
@require_POST
def create_forum_ajax(request):
    try:
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if not title or not content:
            return JsonResponse({
                'status': 'error',
                'message': 'Title and content are required!'
            }, status=400)
        
        forum = Forum.objects.create(
            title=title,
            content=content,
            author=request.user,
            forum_views=0
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Forum created successfully!',
            'forum': {
                'id': str(forum.id),
                'title': forum.title,
                'content': forum.content,
                'author': forum.author.username,
                'created_at': forum.created_at.isoformat(),
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)