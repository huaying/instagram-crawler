# Instagram Crawler [![Build Status](https://travis-ci.org/huaying/ins-crawler.svg?branch=master)](https://travis-ci.org/huaying/ins-crawler)
1. Get Instagram posts/profile/hashtag data without using Instagram API. `crawler.py`
2. Like posts automatically. `liker.py`

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
  mode                  options: [posts, profile, hashtag]

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
python crawler.py profile -u cal_foodie -o ./output
python crawler.py hashtag -t taiwan -o ./output
```
1. Return default 100 hashtag posts(mode: hashtag) and all user's posts(mode: posts) if not specifying the number of post `-n`, `--number`.
2. Print the result to the console if not specifying the output path of post `-o`, `--output`.
3. It takes much longer to get data if the post number is over about 1000 since Instagram has set up the rate limit for data request.
4. Don't use this repo crawler Instagram if the user has more than 10000 posts.

## Liker
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
