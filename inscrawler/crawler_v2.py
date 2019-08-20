from time import sleep

import requests
from tqdm import tqdm

from .crawler import InsCrawler


class InsCrawlerV2(InsCrawler):
    def _fetch_urls(self, num):
        TIMEOUT = 600
        browser = self.browser
        url_set = set()
        urls = []
        pre_post_num = 0
        wait_time = 1

        pbar = tqdm(total=num)

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(".v1Nh3 a")
            for ele in ele_posts:
                url = ele.get_attribute("href")
                if url not in url_set:
                    url_set.add(url)
                    urls.append(url)
            if pre_post_num == len(urls):
                pbar.set_description("Wait for %s sec" % (wait_time))
                sleep(wait_time)
                pbar.set_description("fetching url list")

                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(urls)
            browser.scroll_down()

            return pre_post_num, wait_time

        pbar.set_description("fetching")
        while len(urls) < num and wait_time < TIMEOUT:
            post_num, wait_time = start_fetching(pre_post_num, wait_time)
            pbar.update(post_num - pre_post_num)
            pre_post_num = post_num

            loading = browser.find_one(".W1Bne")
            if not loading and wait_time > TIMEOUT / 2:
                break

        pbar.close()
        print("Fetched %s urls." % (min(len(urls), num)))
        return urls[:num]

    def _get_json_data(self, url):
        json_url = f"{url}?__a=1"
        res = requests.get(json_url)

        if res.status_code == 200:
            json_res = res.json()
            return json_res

    def _get_posts_full(self, num):
        def get_caption(json_data):
            try:
                caption = json_data["graphql"]["shortcode_media"][
                    "edge_media_to_caption"
                ]["edges"][0]["node"]["text"]
            except Exception:
                try:
                    caption = json_data["graphql"]["shortcode_media"][
                        "edge_media_to_parent_comment"
                    ]["edges"][0]["node"]["text"]
                except Exception:
                    return ""

            return caption

        def get_img_urls(json_data):
            try:
                img_urls = [
                    node["node"]["display_url"]
                    for node in json_data["graphql"]["shortcode_media"][
                        "edge_sidecar_to_children"
                    ]["edges"]
                ]
            except Exception:
                img_urls = [json_data["graphql"]["shortcode_media"]["display_url"]]
            return img_urls

        urls = self._fetch_urls(num)
        posts = []
        for url in urls:
            json_data = self._get_json_data(url)
            print(url)

            post = {
                "url": url,
                "author": json_data["graphql"]["shortcode_media"]["owner"]["username"],
                "caption": get_caption(json_data),
                "likes": json_data["graphql"]["shortcode_media"][
                    "edge_media_preview_like"
                ]["count"],
                "img_urls": get_img_urls(json_data),
                "timestamp": json_data["graphql"]["shortcode_media"][
                    "taken_at_timestamp"
                ],
            }

            posts.append(post)

        return posts
