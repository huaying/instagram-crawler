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
  -n NUMBER, --number NUMBER
                        number of returned posts
  -u USERNAME, --username USERNAME
                        instagram's username
  -t TAG, --tag TAG     instagram's tag name
  -o OUTPUT, --output OUTPUT
                        output file name(json format)

  --debug               see how the program automates the browser

  --fetch_comments      fetch comments
  # Turning on the flag might take forever to fetch data if there are too many commnets.

  --fetch_likes_plays   fetch like/play number

  --fetch_likers        fetch all likers
  # Instagram might have rate limit for fetching likers. Turning on the flag might take forever to fetch data if there are too many likes.

  --fetch_mentions      fetch users who are mentioned in the caption/comments (startwith @)

  --fetch_hashtags      fetch hashtags in the caption/comments (startwith #)

  --fetch_details       fetch username and photo caption
  # only available for "hashtag" search

```


### Example
```
python crawler.py posts_full -u cal_foodie -n 100 -o ./output
python crawler.py posts_full -u cal_foodie -n 10 --fetch_likers --fetch_likes_plays
python crawler.py posts_full -u cal_foodie -n 10 --fetch_comments
python crawler.py profile -u cal_foodie -o ./output
python crawler.py hashtag -t taiwan -o ./output
python crawler.py hashtag -t taiwan -o ./output --fetch_details
python crawler.py posts -u cal_foodie -n 100 -o ./output # deprecated
```
1. Choose mode `posts`, you will get url, caption, first photo for each post; choose mode `posts_full`, you will get url, caption, all photos, time, comments, number of likes and views for each posts. Mode `posts_full` will take way longer than mode `posts`. **[`posts` is deprecated. For the recent posts, there is no quick way to get the post caption]**
2. Return default 100 hashtag posts(mode: hashtag) and all user's posts(mode: posts) if not specifying the number of post `-n`, `--number`.
3. Print the result to the console if not specifying the output path of post `-o`, `--output`.
4. It takes much longer to get data if the post number is over about 1000 since Instagram has set up the rate limit for data request.
5. Don't use this repo crawler Instagram if the user has more than 10000 posts.

The data format of `posts`:
![screen shot 2018-10-11 at 2 33 09 pm](https://user-images.githubusercontent.com/3991678/46835356-cd521d80-cd62-11e8-9bb1-888bc32af484.png)

The data format of `posts_full`:
<img width="1123" alt="Screen Shot 2019-03-17 at 11 02 24 PM" src="https://user-images.githubusercontent.com/3991678/54510055-1c4f4080-4909-11e9-8d06-8c35a08fb74e.png">

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
