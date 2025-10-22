from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.core import serializers
from createnews.models import News

# ✅ Halaman utama - list berita
def show_news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, "createnews/news_list.html", {"news_list": news_list})

# ✅ Detail berita (lihat isi full)
def show_news_detail(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    return render(request, "createnews/news_detail.html", {"news": news})

# ✅ CREATE (AJAX)
@csrf_exempt
def create_news_ajax(request):
    if request.method == "POST":
        title = strip_tags(request.POST.get("title"))
        author = strip_tags(request.POST.get("author"))
        content = strip_tags(request.POST.get("content"))
        category = request.POST.get("category")
        thumbnail = request.POST.get("thumbnail")

        news = News.objects.create(
            title=title,
            author=author,
            content=content,
            category=category,
            thumbnail=thumbnail,
        )

        return JsonResponse({
            "id": str(news.id),
            "title": news.title,
            "author": news.author,
            "content": news.short_content,
            "category": news.category,
            "thumbnail": news.thumbnail,
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ EDIT (AJAX)
@csrf_exempt
def edit_news_ajax(request, id):
    news = get_object_or_404(News, pk=id)
    if request.method == "POST":
        news.title = strip_tags(request.POST.get("title"))
        news.author = strip_tags(request.POST.get("author"))
        news.content = strip_tags(request.POST.get("content"))
        news.category = request.POST.get("category")
        news.thumbnail = request.POST.get("thumbnail")
        news.save()

        return JsonResponse({
            "id": str(news.id),
            "title": news.title,
            "author": news.author,
            "content": news.short_content,
            "category": news.category,
            "thumbnail": news.thumbnail,
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ DELETE (AJAX)
@csrf_exempt
def delete_news_ajax(request, id):
    if request.method == "POST":
        news = get_object_or_404(News, pk=id)
        news.delete()
        return JsonResponse({"status": "deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ JSON & XML (buat debugging / API)
def show_json(request):
    data = News.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    data = News.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
