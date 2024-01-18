from django.urls import reverse
from microblogs.models import Post


class LogInTester():
    def is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
    

    
    
    
    
    
    
    
    
def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

def create_posts(author, from_count, to_count):
    """Create unique numbered posts for testing purposes."""
    for count in range(from_count, to_count):
        text = f'Post__{count}'
        post = Post(author=author, text=text)
        post.save()


# class MenuTesterMixin(AssertHTMLMixin):
#     menu_urls = [
#         reverse('user_list'), reverse('feed'), reverse('password'),
#         reverse('profile'), reverse('log_out')
#     ]

#     def assert_menu(self, response):
#         for url in self.menu_urls:
#             with self.assertHTML(response, f'a[href="{url}"]'):
#                 pass

#     def assert_no_menu(self, response):
#         for url in self.menu_urls:
#             self.assertNotHTML(response, f'a[href="{url}"]')
