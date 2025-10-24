from django.test import TestCase, SimpleTestCase, Client
from django.contrib import admin
from forum.models import Forum, Comment
from django.urls import reverse, resolve
from forum import views
import uuid
from django.apps import apps
from forum.apps import ForumConfig
from django.contrib.auth.models import User

# Create your tests here.

class AdminRegistrationTest(TestCase):
    def test_forum_registered_in_admin(self):
        self.assertIn(Forum, admin.site._registry)
    
    def test_comment_registered_in_admin(self):
        self.assertIn(Comment, admin.site._registry)

class TestUrls(SimpleTestCase):
    def test_show_forum_list_url_resolves(self):
        url = reverse('forum:show_forum_list')
        self.assertEqual(resolve(url).func, views.show_forum_list)

    def test_show_json_forum_url_resolves(self):
        url = reverse('forum:show_json')
        self.assertEqual(resolve(url).func, views.show_json_forum)

    def test_show_forum_url_resolves(self):
        fake_id = uuid.uuid4()
        url = reverse('forum:show_forum', args=[fake_id])
        self.assertEqual(resolve(url).func, views.show_forum)

    def test_show_json_forum_by_id_url_resolves(self):
        fake_id = uuid.uuid4()
        url = reverse('forum:show_json_forum_by_id', args=[fake_id])
        self.assertEqual(resolve(url).func, views.show_json_forum_by_id)

    def test_show_json_comment_url_resolves(self):
        fake_id = uuid.uuid4()
        url = reverse('forum:show_json_comment', args=[fake_id])
        self.assertEqual(resolve(url).func, views.show_json_comment)

    def test_create_forum_ajax_url_resolves(self):
        url = reverse('forum:create_forum_ajax')
        self.assertEqual(resolve(url).func, views.create_forum_ajax)

    def test_create_comment_ajax_url_resolves(self):
        url = reverse('forum:create_comment_ajax')
        self.assertEqual(resolve(url).func, views.create_comment_ajax)

    def test_delete_forum_ajax_url_resolves(self):
        url = reverse('forum:delete_forum_ajax')
        self.assertEqual(resolve(url).func, views.delete_forum_ajax)

    def test_edit_forum_ajax_url_resolves(self):
        url = reverse('forum:edit_forum_ajax')
        self.assertEqual(resolve(url).func, views.edit_forum_ajax)

    def test_delete_comment_ajax_url_resolves(self):
        url = reverse('forum:delete_comment_ajax')
        self.assertEqual(resolve(url).func, views.delete_comment_ajax)

    def test_edit_comment_ajax_url_resolves(self):
        url = reverse('forum:edit_comment_ajax')
        self.assertEqual(resolve(url).func, views.edit_comment_ajax)

    def test_json_forum_sort_url_resolves(self):
        url = reverse('forum:json_forum_sort')
        self.assertEqual(resolve(url).func, views.show_json_forum_sort)

class ForumConfigTest(SimpleTestCase):
    def test_app_name(self):
        self.assertEqual(ForumConfig.name, 'forum')

    def test_app_is_registered(self):
        app_config = apps.get_app_config('forum')
        self.assertEqual(app_config.name, 'forum')
        self.assertIsInstance(app_config, ForumConfig)

class ForumModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='12345')
        self.forum = Forum.objects.create(
            author=self.user,
            title='Test Forum',
            content='This is a test forum content.'
        )

    def test_forum_str_returns_title(self):
        self.assertEqual(str(self.forum), 'Test Forum')

    def test_increment_views_increases_view_count(self):
        initial_views = self.forum.forum_views
        self.forum.increment_views()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forum_views, initial_views + 1)

    def test_forum_fields_exist(self):
        self.assertEqual(self.forum.author, self.user)
        self.assertEqual(self.forum.title, 'Test Forum')
        self.assertEqual(self.forum.content, 'This is a test forum content.')
        self.assertIsNotNone(self.forum.created_at)
        self.assertIsNotNone(self.forum.updated_at)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='12345')
        self.forum = Forum.objects.create(
            author=self.user,
            title='Another Forum',
            content='Forum for testing comment.'
        )
        self.comment = Comment.objects.create(
            author=self.user,
            forum=self.forum,
            content='This is a comment.'
        )

    def test_comment_str_returns_empty_string(self):
        self.assertEqual(str(self.comment), "")

    def test_comment_fields_exist(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.forum, self.forum)
        self.assertEqual(self.comment.content, 'This is a comment.')
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)

class ForumViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='12345')
        self.other_user = User.objects.create_user(username='other', password='12345')
        self.forum = Forum.objects.create(author=self.user, title='Test Forum', content='Forum content')
        self.comment = Comment.objects.create(author=self.user, forum=self.forum, content='Comment content')

    def test_show_forum_list(self):
        response = self.client.get(reverse('forum:show_forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum.html')

    def test_show_forum_detail(self):
        response = self.client.get(reverse('forum:show_forum', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_detail.html')

    def test_show_json_forum(self):
        response = self.client.get(reverse('forum:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_show_json_forum_sort_newest_oldest_popular(self):
        url = reverse('forum:json_forum_sort')
        for sort in ['newest', 'oldest', 'popular', 'none']:
            response = self.client.get(url, {'sort': sort})
            self.assertEqual(response.status_code, 200)

    def test_show_json_forum_by_id_found_and_not_found(self):
        url = reverse('forum:show_json_forum_by_id', args=[self.forum.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        bad_url = reverse('forum:show_json_forum_by_id', args=[uuid.uuid4()])
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_show_json_comment(self):
        url = reverse('forum:show_json_comment', args=[self.forum.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_create_forum_ajax_requires_login(self):
        url = reverse('forum:create_forum_ajax')
        response = self.client.post(url, {'title': 'New', 'content': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_create_forum_ajax_success(self):
        self.client.login(username='tester', password='12345')
        url = reverse('forum:create_forum_ajax')
        response = self.client.post(url, {'title': 'New Forum', 'content': 'test'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Forum.objects.filter(title='New Forum').exists())

    def test_create_comment_ajax_success(self):
        self.client.login(username='tester', password='12345')
        url = reverse('forum:create_comment_ajax')
        response = self.client.post(url, {'forum_id': self.forum.id, 'content': 'New comment'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Comment.objects.filter(content='New comment').exists())

    def test_delete_forum_ajax_unauthorized_and_authorized(self):
        self.client.login(username='other', password='12345')
        url = reverse('forum:delete_forum_ajax')
        response = self.client.post(url, {'forum_id': self.forum.id})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='tester', password='12345')
        response = self.client.post(url, {'forum_id': self.forum.id})
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_ajax_unauthorized_and_authorized(self):
        self.client.login(username='other', password='12345')
        url = reverse('forum:delete_comment_ajax')
        response = self.client.post(url, {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='tester', password='12345')
        response = self.client.post(url, {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)

    def test_edit_forum_ajax_unauthorized_and_authorized(self):
        self.client.login(username='other', password='12345')
        url = reverse('forum:edit_forum_ajax')
        response = self.client.post(url, {'forum_id': self.forum.id, 'title': 'X', 'content': 'Y'})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='tester', password='12345')
        response = self.client.post(url, {'forum_id': self.forum.id, 'title': 'Edited', 'content': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.title, 'Edited')

    def test_edit_comment_ajax_unauthorized_and_authorized(self):
        self.client.login(username='other', password='12345')
        url = reverse('forum:edit_comment_ajax')
        response = self.client.post(url, {'comment_id': self.comment.id, 'content': 'Hack'})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='tester', password='12345')
        response = self.client.post(url, {'comment_id': self.comment.id, 'content': 'Edited comment'})
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Edited comment')
