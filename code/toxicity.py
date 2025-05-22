'''
Does all the toxicity analysis for the telegram messages. Made for the DIRE project research group
'''
import os
from detoxify import Detoxify
import ssl
import urllib.request

# Set up SSL context to bypass HTTPS verification
ssl._create_default_https_context = ssl._create_unverified_context

# Define paths and download the checkpoint file
SAVE_DIR = os.path.expanduser("~/ckpt_files")
SAVE_PATH = os.path.join(SAVE_DIR, "toxic_original-c1212f89.ckpt")

os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure the directory exists

urllib.request.urlretrieve(
    "https://github.com/unitaryai/detoxify/releases/download/v0.1-alpha/toxic_original-c1212f89.ckpt",
    SAVE_PATH
)

def sentiment_analysis(data):
    """
    Perform sentiment analysis on a list of messages using Detoxify
     and returns a list of dictionaries containing toxicity analysis results.
    """
    model = Detoxify('original')  # Load the model once for efficiency
    return [model.predict(message) for message in data]

def average_toxicity(toxicity_list):
    """
    Calculate average toxicity metrics from a list of toxicity results by taking in
    toxicity_list and returning a Dictionary containing average percentages for each toxicity metric.
    """
    if not toxicity_list:
        return {}

    # Initialize totals for each metric
    totals = {
        "toxicity": 0,
        "severe_toxicity": 0,
        "obscene": 0,
        "threat": 0,
        "insult": 0,
        "identity_attack": 0
    }

    # Accumulate values
    for toxicity in toxicity_list:
        for key in totals:
            totals[key] += toxicity.get(key, 0)

    # Calculate averages and convert to percentages
    toxicity_count = len(toxicity_list)
    return {
        key: round((value / toxicity_count) * 100, 3)
        for key, value in totals.items()
    }