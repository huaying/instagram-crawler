from datetime import datetime
from unittest import TestCase, mock
from inscrawler.fetch import fetch_datetime, fetch_hashtags, \
    fetch_mentions, fetch_imgs


class TestFetchMentions(TestCase):

    @mock.patch("inscrawler.fetch.settings")
    def test_fetch_mentions(self, mock_settings):
        mock_settings.fetch_mentions = True

        post = {}
        fetch_mentions("""
            This is my new robot, called @inscrawler
        """, post)

        self.assertIn("mentions", post)
        self.assertIn("inscrawler", post["mentions"])

    @mock.patch("inscrawler.fetch.settings")
    def test_fetch_mentions_if_not_enabled_by_settings(self, mock_settings):
        mock_settings.fetch_mentions = False

        post = {}
        fetch_mentions("""
            This is my new robot, called @inscrawler
        """, post)

        self.assertNotIn("mentions", post)


class TestFetchHashtags(TestCase):

    @mock.patch("inscrawler.fetch.settings")
    def test_fetch_hashtags(self, mock_settings):
        mock_settings.fetch_hashtags = True

        post = {}
        fetch_hashtags("""
            This is my new robot, called #inscrawler
        """, post)

        self.assertIn("hashtags", post)
        self.assertIn("inscrawler", post["hashtags"])

    @mock.patch("inscrawler.fetch.settings")
    def test_fetch_hashtags_if_not_enabled_by_settings(self, mock_settings):
        mock_settings.fetch_hashtags = False

        post = {}
        fetch_hashtags("""
            This is my new robot, called #inscrawler
        """, post)

        self.assertNotIn("hashtags", post)


class TestFetchDatetime(TestCase):

    def test_fetch_datetime(self):
        mock_browser = mock.Mock()
        mock_browser.find_one.return_value \
            .get_attribute.return_value = datetime.now()

        post = {}
        fetch_datetime(mock_browser, post)

        self.assertIn("datetime", post)


class TestFetchImgs(TestCase):

    def test_fetch_imgs(self):
        mock_element = mock.Mock()
        mock_element.get_attribute.return_value = "image_path"

        mock_browser = mock.Mock()
        mock_browser.find.return_value = [mock_element]
        mock_browser.find_one.return_value = None

        post = {}
        fetch_imgs(mock_browser, post)
        
        self.assertIn("img_urls", post)
        self.assertListEqual(post.get("img_urls"), [
            "image_path"
        ])

    def test_fetch_imgs_in_carroussel(self):
        def mock_get_next_photo_btn(html_class):
            if mock_get_next_photo_btn.loop > 2:
                return None

            mock_get_next_photo_btn.loop += 1
            return mock.Mock()
        mock_get_next_photo_btn.loop = 0

        mock_element = mock.Mock()
        mock_element.get_attribute.return_value = "image_path"

        mock_browser = mock.Mock()
        mock_browser.find.return_value = [mock_element]
        mock_browser.find_one = mock_get_next_photo_btn

        post = {}
        fetch_imgs(mock_browser, post)
        
        self.assertIn("img_urls", post)
        self.assertListEqual(post.get("img_urls"), [
            "image_path"
        ])

    def test_fetch_imgs_if_find_is_not_a_list(self):
        mock_browser = mock.Mock()
        mock_browser.find.return_value = None

        post = {}
        fetch_imgs(mock_browser, post)
        
        self.assertIn("img_urls", post)
        self.assertListEqual(post.get("img_urls"), [])
