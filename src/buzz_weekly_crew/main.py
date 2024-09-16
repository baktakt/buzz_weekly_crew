#!/usr/bin/env python
import sys
import os
from buzz_weekly_crew.crew import BuzzWeeklyCrew

def get_inputs():
    """Get common inputs from environment variables."""
    return {
        "rss-feeds": os.getenv('RSS_FEEDS'),
        "number-of-articles-from-each-feed": os.getenv('ARTICLES_PER_FEED'),
        "number-of-articles-in-blog-post": os.getenv('ARTICLES_IN_BLOG'),
        "topics": os.getenv('TOPICS'),
        "blog-name": os.getenv('BLOG_NAME'),
    }

def run():
    BuzzWeeklyCrew().crew().kickoff(inputs=get_inputs())

def train():
    """Train the crew for a given number of iterations."""
    try:
        n_iterations = int(sys.argv[1])
        filename = sys.argv[2]  # Add this line to get the filename from command-line arguments
        BuzzWeeklyCrew().crew().train(n_iterations=n_iterations, inputs=get_inputs(), filename=filename)  # Add filename here
    except (IndexError, ValueError):
        print("Usage: train <number_of_iterations> <filename>")  # Update usage message
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Add command-line argument parsing here if needed
    pass
