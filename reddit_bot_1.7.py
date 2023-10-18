import praw
import config
import time
import os
import random
import re
#import tweepy


def bot_login():
        print("> Logging in...")
        r = praw.Reddit(
                username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "ffm"
        )
        print("> Logged in!")

        return r


'''
def login_twitter():
        print("> twitter login...")
        t = tweepy.Client(
                consumer_key=config.consumer_key,
                consumer_secret=config.consumer_secret,
                access_token=config.access_token,
                access_token_secret=config.access_token_secret
        )
        print("> logged into twitter!")
        return t
'''


def get_message(post):
        wallet_address = "0x1a297390A688451e4f571041db693FA26F3A0287"
        message = ""
        text = ["Thank you!", "Thank you very much!", "Thanks! 🙏", "Awesome work! 🔥", "Love it!", "Neeeeeed!",
                "Yes please!", "Awesome!", "🔥🔥🔥", "Need this in my collection! 🙏", "Let's go!", "Appreciate it!",
                "Keep it up!", "Fantastic!", "Great!", "🚀🙏💰", "🚀🚀🚀", "🙏🙏🙏", "I gotta win this!", "Thank you 😄",
                "I'm feeling lucky!", "How can I get this?", "Gotta get my hands on this!", "Very cool!", "Cool 😎",
                "what a great opportunity!"]

        message += random.choice(text) + "  \n\n"
        message += wallet_address + "  \n\n"

        return message

def post_search(r, posts_replied_to):
        for post in r.subreddit("NFTsMarketplace+opensea+NFTExchange").new(limit=15):
                title = post.title.lower()
                print(title)
                if (("giveaway" in title) or ("drop" in title) or ("address" in title)) and (post.id not in posts_replied_to):
                        print("> Giveaway found")

                        posts_replied_to.append(post.id)
                        with open("posts_replied_to.txt", "a") as f:
                                f.write(post.id + "\n")

                        comment = get_message(post)
                        post.reply(comment)
                        print(comment)

                        duration = (random.uniform(0.75, 3)) * 60
                        print("> taking a nap for " + str(duration/60) + " mins")
                        time.sleep(duration)
        print("> Post search complete")

def get_saved_posts():
        if not os.path.isfile("posts_replied_to.txt"):
                posts_replied_to = []
        else:
                print("> file open")
                with open("posts_replied_to.txt", "r") as f:
                        posts_replied_to = f.read()
                        posts_replied_to = posts_replied_to.split("\n")
        return posts_replied_to


r = bot_login()
#t = login_twitter()
posts_replied_to = get_saved_posts()
#print(posts_replied_to)
time_duration = 0

while True:
        time_duration = (random.uniform(10, 25)) * 60
        try:
                posts_replied_to = get_saved_posts()
                post_search(r, posts_replied_to)

        except Exception as e: 
                error_message = str(e)
                print(error_message)
                try:
                        timeout = int(re.search(r'\d+', error_message).group())
                        time_duration = ((timeout + 1) * 60)
                except:
                        pass
                
                print("> Something happened, trying again...")

        finally: 
                print("going to sleep for " + str(time_duration / 60) + " mins")
                time.sleep(time_duration)
                print("awake")
