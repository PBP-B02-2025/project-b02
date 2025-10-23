from django.shortcuts import render, get_object_or_404
from forum.models import Forum, Comment
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.utils import timezone
# Create your views here.

def show_forum_list(request):
    return render(request, "forum.html", {})

def show_forum(request, id):
    forum = get_object_or_404(Forum, pk=id)
    forum.increment_views()
    context = {
        'id': id,
        'author_id': str(forum.author_id),
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
            'author_id': forum.author_id,
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
            'comment_count': str(forum.comment_set.count()),
            'author_id': forum.author_id,
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
            'author_id': comment.author_id,
        } for comment in comment_list
    ]
    return JsonResponse(comment_data, safe=False)

@csrf_exempt
@require_POST
def create_forum_ajax(request):
    title = strip_tags(request.POST.get("title"))
    content = strip_tags(request.POST.get("content"))
    author = request.user
    new_forum = Forum(
        title=title,
        content=content,
        author=author,
    )
    new_forum.save()
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def create_comment_ajax(request):
    forum = get_object_or_404(Forum, pk=request.POST.get('forum_id'))
    content = strip_tags(request.POST.get("content"))
    author = request.user
    new_comment = Comment(
        forum=forum,
        content=content,
        author=author,
    )
    new_comment.save()
    forum.updated_at = timezone.now()
    forum.save(update_fields=["updated_at"])
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def delete_forum_ajax(request):
    forum = get_object_or_404(Forum, pk=request.POST.get('forum_id'))
    forum.delete()
    response = JsonResponse({
        'success': True,
        'message': 'Forum deleted succesful!',
        'redirect_url': '/forum/'
    })
    return response

@csrf_exempt
@require_POST
def delete_comment_ajax(request):
    comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
    comment.delete()
    response = JsonResponse({
        'success': True,
        'message': 'Comment deleted succesful!',
    })
    return response

@csrf_exempt
@require_POST
def edit_forum_ajax(request):
    forum = get_object_or_404(Forum, pk=request.POST.get('forum_id'))
    forum.title = strip_tags(request.POST.get("title"))
    forum.content = strip_tags(request.POST.get("content"))
    forum.updated_at = timezone.now()
    forum.save()
    return JsonResponse({
        "success": True,
        "message": "Forum updated successfully!",
        "forum_id": forum.id
    })