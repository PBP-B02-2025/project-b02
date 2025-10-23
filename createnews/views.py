from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from createnews.models import News

def show_news_list(request): 
    # 🟩 Filter kategori dari dropdown (?category=event)
    category = request.GET.get('category')
    if category:
        news_list = News.objects.filter(category=category).order_by('-created_at')
    else:
        news_list = News.objects.all().order_by('-created_at')

    # 🟨 Sidebar Populer: berita dengan is_featured=True
    popular = News.objects.filter(is_featured=True).order_by('-news_views')[:5]

    # 🟢 Kalau request dari AJAX (fetch updatePopularList)
    if request.GET.get("ajax") == "1":
        return JsonResponse({
            "popular_list": [
                {
                    "id": str(p.id),
                    "title": p.title,
                    "author": p.author,
                    "thumbnail": p.thumbnail,
                }
                for p in popular
            ]
        })

    # 🟦 Kalau bukan AJAX, render template biasa
    context = {
        'news_list': news_list,
        'popular_list': popular,
        'categories': News.CATEGORY_CHOICES,
    }
    return render(request, "createnews/news_list.html", context)


def show_news_detail(request, id):
    news = get_object_or_404(News, pk=id)
    news.news_views += 1
    news.save()
    return render(request, "createnews/news_detail.html", {"news": news})

# Helper check admin
def _is_admin(request):
    return request.user.is_authenticated and request.user.is_staff

@csrf_exempt
def create_news_ajax(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    if not _is_admin(request):
        return JsonResponse({"error": "Not allowed"}, status=403)

    title = strip_tags(request.POST.get("title", ""))
    author = request.user.username if request.user.is_authenticated else "Anonymous"
    content = strip_tags(request.POST.get("content", ""))
    category = request.POST.get("category", "sports_news")
    thumbnail = request.POST.get("thumbnail", "")
    is_featured = request.POST.get("is_featured") in ("true", "on", "1")

    news = News.objects.create(
        title=title, author=author, content=content,
        category=category, thumbnail=thumbnail, is_featured=is_featured
    )

    return JsonResponse({
        "id": news.id,
        "title": news.title,
        "author": news.author,
        "content": news.content[:100],
        "category": news.get_category_display(),
        "thumbnail": news.thumbnail,
        "is_featured": news.is_featured,
    })

@csrf_exempt
def edit_news_ajax(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    if not _is_admin(request):
        return HttpResponseForbidden("Not allowed")
    news = get_object_or_404(News, pk=id)
    news.title = strip_tags(request.POST.get("title", news.title))
    news.author = strip_tags(request.POST.get("author", news.author))
    news.content = strip_tags(request.POST.get("content", news.content))
    news.category = request.POST.get("category", news.category)
    news.thumbnail = request.POST.get("thumbnail", news.thumbnail)
    news.is_featured = request.POST.get("is_featured") in ("true", "on", "1")
    news.save()
    return JsonResponse({
    "id": str(news.id),
    "title": news.title,
    "author": news.author,
    "content": news.content,  # ✅ kirim konten penuh
    "category": news.category,
    "thumbnail": news.thumbnail,
    "is_featured": news.is_featured,
})

    

@csrf_exempt
def delete_news_ajax(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    if not _is_admin(request):
        return HttpResponseForbidden("Not allowed")
    news = get_object_or_404(News, pk=id)
    news.delete()
    return JsonResponse({"status": "deleted"})
