# Instagram Crawler [![Build Status](https://travis-ci.org/huaying/instagram-crawler.svg?branch=master)](https://travis-ci.org/huaying/instagram-crawler)

Below is what you can do with this program:
- Get Instagram posts/profile/hashtag data without using Instagram API. `crawler.py`
- Like posts automatically. `liker.py`

This crawler could fail due to updates on instagram’s website. If you encounter any problems, please contact me.

## Install
1. Make sure you have Chrome browser installed.
2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into bin folder: `./inscrawler/bin/chromedriver`
3. Install Selenium: `pip install -r requirements.txt`
4. `cp inscrawler/secret.py.dist inscrawler/secret.py`

## Crawler
### Usage
```
positional arguments:
  mode
    options: [posts, posts_full, profile, hashtag]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of returned posts
  -u USERNAME, --username USERNAME
                        instagram's username
  -t TAG, --tag TAG     instagram's tag name
  -o OUTPUT, --output OUTPUT
                        output file name(json format)
```


### Example
```
python crawler.py posts -u cal_foodie -n 100 -o ./output
python crawler.py posts_full -u cal_foodie -n 100 -o ./output
python crawler.py profile -u cal_foodie -o ./output
python crawler.py hashtag -t taiwan -o ./output
```
1. Choose mode `posts`, you will get url, content, first photo for each post; choose mode `posts_full`, you will get url, content, all photos, time, comments for each posts. Mode `posts_full` will take way longer than mode `posts`.
1. Return default 100 hashtag posts(mode: hashtag) and all user's posts(mode: posts) if not specifying the number of post `-n`, `--number`.
2. Print the result to the console if not specifying the output path of post `-o`, `--output`.
3. It takes much longer to get data if the post number is over about 1000 since Instagram has set up the rate limit for data request.
4. Don't use this repo crawler Instagram if the user has more than 10000 posts.

The data format of `posts`:
![screen shot 2018-10-11 at 2 33 09 pm](https://user-images.githubusercontent.com/3991678/46835356-cd521d80-cd62-11e8-9bb1-888bc32af484.png)

The data format of `posts_full`:
![screen shot 2018-10-11 at 2 34 38 pm](https://user-images.githubusercontent.com/3991678/46835359-cf1be100-cd62-11e8-82cb-89f37a55bb01.png)


## Liker
![Liker Preivew](https://user-images.githubusercontent.com/3991678/41560884-4bbd42d2-72fd-11e8-8d56-84e7cf7187cd.gif)


Set up your username/password in `secret.py` or set them as environment variables.

### Usage
```
positional arguments:
  tag

optional arguments:
  -n NUMBER, --number NUMBER (default 1000)
                        number of posts to like
```

### Example
```
python liker.py foodie
```
