from django.test import TestCase
from createnews.forms import NewsForm
from createnews.models import News
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from createnews.models import News


class NewsFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Berita Baru",
            "content": "Ini adalah isi berita baru tentang latihan fisik.",
            "category": "sports_news",
            "thumbnail": "https://example.com/image.jpg",
            "is_featured": True,
        }

    def test_form_valid_data(self):
        form = NewsForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertEqual(instance.title, "Berita Baru")
        self.assertEqual(instance.category, "sports_news")
        self.assertTrue(instance.is_featured)

    def test_form_missing_title(self):
        data = self.valid_data.copy()
        data["title"] = ""
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_missing_content(self):
        data = self.valid_data.copy()
        data["content"] = ""
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_form_invalid_category_choice(self):
        data = self.valid_data.copy()
        data["category"] = "invalid_category"
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

    def test_form_invalid_thumbnail_url(self):
        data = self.valid_data.copy()
        data["thumbnail"] = "not-a-url"
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail", form.errors)

    def test_form_widgets_have_correct_attributes(self):
        form = NewsForm()
        self.assertEqual(form.fields["title"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["title"].widget.attrs["placeholder"], "Judul berita")
        self.assertEqual(form.fields["content"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["content"].widget.attrs["placeholder"], "Isi berita")
        self.assertEqual(form.fields["category"].widget.attrs["class"], "form-select")
        self.assertEqual(form.fields["thumbnail"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["thumbnail"].widget.attrs["placeholder"], "URL gambar (https://...)")
        self.assertEqual(form.fields["is_featured"].widget.attrs["class"], "form-check-input")



class NewsModelTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title="Judul Test",
            author="penulis",
            content="x" * 150,  
            category="event",
            thumbnail="https://example.com/img.jpg",
            is_featured=False
        )

    def test_str(self):
        self.assertEqual(str(self.news), "Judul Test")

    def test_short_content_truncates(self):
        sc = self.news.short_content
        self.assertTrue(len(sc) > 100)
        self.assertTrue(sc.endswith("..."))

    def test_increment_views(self):
        initial = self.news.news_views
        self.news.increment_views()
        self.news.refresh_from_db()
        self.assertEqual(self.news.news_views, initial + 1)

User = get_user_model()

class NewsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # create admin user
        self.admin = User.objects.create_user(username="admin", password="pass123", is_staff=True)
        # non-admin user
        self.user = User.objects.create_user(username="u", password="pass123", is_staff=False)
        # sample news
        self.news = News.objects.create(
            title="T1",
            author="a",
            content="isi",
            category="sports_news"
        )

    def test_show_news_list_html(self):
        url = reverse('createnews:show_news_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "BALLISTIC NEWS")  # judul pada template

    def test_show_news_list_ajax_popular(self):
        # set one featured item so popular not empty
        self.news.is_featured = True
        self.news.save()
        url = reverse('createnews:show_news_list') + "?ajax=1"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("popular_list", data)
        self.assertIsInstance(data["popular_list"], list)

    def test_show_news_detail_increments_views(self):
        url = reverse('createnews:show_news_detail', args=[str(self.news.id)])
        before = self.news.news_views
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.news.refresh_from_db()
        self.assertEqual(self.news.news_views, before + 1)

    def test_create_news_ajax_admin_allowed(self):
        self.client.login(username="admin", password="pass123")
        url = reverse('createnews:create_news_ajax')
        resp = self.client.post(url, {
            "title": "from ajax",
            "author": "adm",
            "content": "konten",
            "category": "event",
            "thumbnail": "",
            "is_featured": "on"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "from ajax")

    def test_create_news_ajax_non_admin_forbidden(self):
        self.client.login(username="u", password="pass123")
        url = reverse('createnews:create_news_ajax')
        resp = self.client.post(url, {"title": "x", "content": "y"})
        self.assertEqual(resp.status_code, 403)

    def test_edit_news_ajax_admin(self):
        self.client.login(username="admin", password="pass123")
        url = reverse('createnews:edit_news_ajax', args=[str(self.news.id)])
        resp = self.client.post(url, {"title": "Edited", "author": "new", "content": "c"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["title"], "Edited")
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, "Edited")

    def test_delete_news_ajax_admin(self):
        self.client.login(username="admin", password="pass123")
        url = reverse('createnews:delete_news_ajax', args=[str(self.news.id)])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "deleted")
        # ensure deleted
        with self.assertRaises(News.DoesNotExist):
            News.objects.get(pk=self.news.id)