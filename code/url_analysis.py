'''
Extract all the information like forwards based on URLS and such. Made for the DIRE project research group
'''
import re
from util_functions import *

def website_domain_analysis(telegram_data):
    """
    Analyze website domain occurrences in Telegram messages.
    Extracts domain names from messages containing URLs and calculates the total
    occurrences, views, and forwards for each domain by analyzing json data
     containing Telegram message data. Each dictionary should have a "Message", "Views", and "Forwards" key.
     Returns a dictionary where keys are domain names and values are lists of [count, total views, total forwards].
    """
    url_pattern = r'https?://(?:www\.)?([^/]+)'  # Regex pattern to extract domain names
    url_dict = {}  # Dictionary to store domain statistics

    for data in telegram_data:
        # Check if message contains a URL
        if data["Message"] is not None and "https:" in data["Message"]:
            # Extract domain names from the message
            url_list = re.findall(url_pattern, data["Message"])
            for url in url_list:
                if url not in url_dict:
                    # Initialize statistics for a new domain
                    count = 1
                    views = safe_int(data["Views"])
                    forwards = safe_int(data["Forwards"])
                    url_dict[url] = [count, views, forwards]
                else:
                    # Update statistics for an existing domain
                    count = url_dict[url][0] + 1
                    views = url_dict[url][1] + safe_int(data['Views'])
                    forwards = url_dict[url][2] + safe_int(data['Forwards'])
                    url_dict[url] = [count, views, forwards]
    return url_dict

def video_url_analysis(telegram_data):
    """
    Analyze video URL occurrences in Telegram messages. Extracts full URLs from messages and calculates the total occurrences,
    views, and forwards for each URL.List of dictionaries containing Telegram message data.
    Each dictionary should have a "Message", "Views", and "Forwards" key. A dictionary where keys are URLs and values are lists of
    [count, total views, total forwards].
    """
    url_pattern = r'https?:\/\/[^\s"]+'  # Regex pattern to extract full URLs
    url_dict = {}  # Dictionary to store URL statistics

    for data in telegram_data:
        # Check if message contains a URL
        if data["Message"] is not None and "https:" in data["Message"]:
            # Extract URLs from the message
            url_list = re.findall(url_pattern, data["Message"])
            for url in url_list:
                if url not in url_dict:
                    # Initialize statistics for a new URL
                    count = 1
                    views = safe_int(data["Views"])
                    forwards = safe_int(data["Forwards"])
                    url_dict[url] = [count, views, forwards]
                else:
                    # Update statistics for an existing URL
                    count = url_dict[url][0] + 1
                    views = url_dict[url][1] + safe_int(data['Views'])
                    forwards = url_dict[url][2] + safe_int(data['Forwards'])
                    url_dict[url] = [count, views, forwards]
    return url_dict