"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import PostForm
from ..helpers import create_posts
from microblogs.models import User


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username = "@johndoe")
        self.url = reverse('feed')

    def test_feed_url(self):
        self.assertEqual(self.url,'/feed/')

    def test_get_feed(self):
        self.client.login(username = "@johndoe", password = "Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_feed_shows_users_own_posts(self):
        self.client.login(username="@johndoe", password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertNotContains(response, f'Post__{count}')
        for count in range(200, 203):
            self.assertContains(response, f'Post__{count}')

    def test_feed_shows_users_followees_posts(self):
        self.client.login(username="@johndoe", password='Password123')
        jane = User.objects.get(username='@janedoe')
        petra = User.objects.get(username = '@petrapickles')
        peter = User.objects.get(username = '@peterpickles')
        create_posts(self.user, 100, 103)
        create_posts(jane, 200, 203)
        create_posts(petra, 300, 303)
        create_posts(peter, 400, 403)
        self.user.toggle_follow(jane)
        self.user.toggle_follow(petra)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertContains(response, f'Post__{count}')
        for count in range(200, 203):
            self.assertContains(response, f'Post__{count}')
        for count in range(300,303):
            self.assertContains(response, f'Post__{count}')
        for count in range(400,403):
            self.assertNotContains(response, f'Post__{count}')