
def get_username_list_from_crawl(crawled_data):
    username_set = set()

    for i in range(len(crawled_data)):
        username_set.add(crawled_data[i].get("username"))

    return list(username_set)
