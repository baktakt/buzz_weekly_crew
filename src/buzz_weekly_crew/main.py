#!/usr/bin/env python
import sys, os
from buzz_weekly_crew.crew import BuzzWeeklyCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        "rss-feeds": os.getenv('RSS_FEEDS'),
        "number-of-articles-from-each-feed": os.getenv('ARTICLES_PER_FEED'),
        "number-of-articles-in-blog-post": os.getenv('ARTICLES_IN_BLOG'),
        "topics": os.getenv('TOPICS'),
        "blog-name": os.getenv('BLOG_NAME'),
              }
    BuzzWeeklyCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "rss-feeds": os.getenv('RSS_FEEDS'),
        "number-of-articles-from-each-feed": os.getenv('ARTICLES_PER_FEED'),
        "number-of-articles-in-blog-post": os.getenv('ARTICLES_IN_BLOG'),
        "topics": os.getenv('TOPICS'),
        "blog-name": os.getenv('BLOG_NAME'),
              }
    try:
        BuzzWeeklyCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
