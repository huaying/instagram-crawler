# Instagram Crawler [![Build Status](https://travis-ci.org/huaying/ins-crawler.svg?branch=master)](https://travis-ci.org/huaying/ins-crawler)
Get Instagram posts/profile/hashtag data without using Instagram API.

## Install
1. Download chromedriver and put it into bin folder: `./inscrawler/bin/chromedriver`
2. Install Selenium: `pip install -r requirement.txt`

## Usage
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


## Example
```
python crawler.py posts -u cal_foodie -n 100 -o ./output
python crawler.py profile -u cal_foodie -o ./output
python crawler.py hashtag taiwan -o ./output
```
1. Return default 100 hashtag posts(mode: hashtag) and all user's posts(mode: posts) if not specifying the number of post `-n`, `--number`.
2. Print the result to the console if not specifying the output path of post `-o`, `--output`.
3. It takes much longer to get data if the post number is over about 1000 since Instagram has set up the rate limit for data request.
4. Don't use this repo crawler Instagram if the user has more than 10000 posts.
