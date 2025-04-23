import pandas as pd
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect
import matplotlib.pyplot as plt
import re
import os
from datetime import datetime
from detoxify import Detoxify
import ssl
import urllib.request
import emoji


from pandas.io.sas.sas_constants import dataset_length

ssl._create_default_https_context = ssl._create_unverified_context
save_path = "/ckpt_files/toxic_original-c1212f89.ckpt"
urllib.request.urlretrieve(
    "https://github.com/unitaryai/detoxify/releases/download/v0.1-alpha/toxic_original-c1212f89.ckpt",
    save_path
)



#Date these topics first appear (Look for HAARP/fema)
#Bad sentiment begins and continues
#Emoji Usage per month/word
#toxigen and detoxify
# Clean code and document


#Look how harp where it came from when it came in and when it began and Fema


# Download stopwords if you haven't already
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt')

punctuation_lst = [".","!","'s","?",",",":","*","-",'’', '``', '”', '“', '#', '...',
                   '>', '‘', '—', ';', ']', '[' , '–']
other_removed_words = ["the", "'", "a", "&", '"', "https", "''", "(", ")", "@", "was", "would", "as" , " the", "the ", " the "]
url_links = []


TOPIC_LIST = ["January", "February", "March", "Election",
              "China", "Voting", "Russia", "Crypto"]

JSON_FILES = ["Telegram_Messages_English_January.json", "Telegram_Messages_English_February.json",
              "Telegram_Messages_English_March.json", "Election_Cycle.json",
              "Telegram_Messages_China.json","Telegram_Message_Voting.json",
              "Telegram_Messages_Russia.json", "Telegram_Messages_Crypto.json"
             ]


def extract_json(json_file_name):
    '''
    Takes JSON mes
    :param month_year:
    :return: Processed Data
    '''
    filename = json_file_name
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data



def clean_data(data):
    cleaned_messages = []
    for message in data:
        if not message["Message"] or isinstance(message, str):
            continue
        try:
            if detect(message["Message"]) == "pt":
                continue
            elif detect(message["Message"]) == "en":
                message_tokenize = word_tokenize(message["Message"])
                cleaned_messages.append(stop_words_cleaning(message_tokenize))
        except Exception as e:
            url_links.append(message["Message"])
    return cleaned_messages



def stop_words_cleaning(message_tokens):
    messages = []
    for word in message_tokens:
        if word.lower() in stopwords.words('english'):
            message_tokens.remove(word)
        if word.lower() in punctuation_lst:
            message_tokens.remove(word)
        if word.lower() in other_removed_words:
            message_tokens.remove(word)
    message = ' '.join(message_tokens)
    messages.append(message.lower())
    return messages


def save_panda_dataframe(data):
    df = pd.DataFrame({'Message': data})
    drop_duplicates = df.drop_duplicates(subset='Message')

    styled_df = drop_duplicates.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('background-color', 'lightblue')]}]
    )

    html = styled_df.render()
    with open("cleaned_messages.html", "w") as file:
        file.write(html)



def website_domain_analysis(telegram_data):

    url_pattern = r'https?://(?:www\.)?([^/]+)'
    url_dict = {}

    for data in telegram_data:
        if data["Message"] is not None and "https:" in data["Message"]:
            url_list = re.findall(url_pattern, data["Message"])
            for url in url_list:
                if url not in url_dict:
                    count = 1
                    views = safe_int(data["Views"])
                    forwards = safe_int(data["Forwards"])
                    url_dict[url] = [count, views, forwards]
                else:
                    count = url_dict[url][0] + 1
                    views = url_dict[url][1] + safe_int(data['Views'])
                    forwards = url_dict[url][2] + safe_int(data['Forwards'])
                    url_dict[url] = [count, views, forwards]
    return url_dict



def video_url_analysis(telegram_data):

    url_pattern = r'https?:\/\/[^\s"]+'
    url_dict = {}

    for data in telegram_data:
        if data["Message"] is not None and "https:" in data["Message"]:
            url_list = re.findall(url_pattern, data["Message"])
            for url in url_list:
                if url not in url_dict:
                    count = 1
                    views = safe_int(data["Views"])
                    forwards = safe_int(data["Forwards"])
                    url_dict[url] = [count, views, forwards]
                else:
                    count = url_dict[url][0] + 1
                    views = url_dict[url][1] + safe_int(data['Views'])
                    forwards = url_dict[url][2] + safe_int(data['Forwards'])
                    url_dict[url] = [count, views, forwards]
    return url_dict




def safe_int(values):
    try:
        return int(values)
    except (ValueError, TypeError):
        return 0


def combine_compressed_urls(data, key1, key2):
    if key1 in data and key2 in data:
        data[key1] = [a + b for a, b in zip(data[key1], data[key2])]
        del data[key2]
        return data
    else:
        return data


def plot_top_usage_values(data, top_n=10, save_path="top_websites_usage_values.png", topic = "Telegram Data", url_analysis_graph = False):

    sorted_data = sorted(data.items(), key=lambda x: x[1][0], reverse=True)

    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][0] for site in top_sites]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Usage")
    if url_analysis_graph:
        plt.title(f"Top {top_n} URL by Usage Value for {topic}")
    else:
        plt.title(f"Top {top_n} Websites by Usage Value for {topic}")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path



def plot_top_views_values(data, top_n=10, save_path="top_websites_views_values.png", topic = "Telegram Data", url_analysis_graph = False):

    sorted_data = sorted(data.items(), key=lambda x: x[1][1], reverse=True)


    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][1] for site in top_sites]


    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Views")
    if url_analysis_graph:
        plt.title(f"Top {top_n} URL by Usage Value for {topic}")
    else:
        plt.title(f"Top {top_n} Websites by Usage Value for {topic}")

    plt.xticks(rotation=45, ha='right')


    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path



def plot_top_forwards_values(data, top_n=10, save_path="top_websites_forward_values.png", topic = "Telegram Data", url_analysis_graph = False):

    sorted_data = sorted(data.items(), key=lambda x: x[1][2], reverse=True)

    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][2] for site in top_sites]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Forward")
    if url_analysis_graph:
        plt.title(f"Top {top_n} URL by Usage Value for {topic}")
    else:
        plt.title(f"Top {top_n} Websites by Usage Value for {topic}")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path



def analyze_and_plot(json_file_list, topic_list, base_save_dir="plots"):
    os.makedirs(base_save_dir, exist_ok=True)

    for json_file, topic in zip(json_file_list, topic_list):

        data = extract_json(json_file)
        cleaned_data = combine_compressed_urls(data, "Youtube.com", "youtu.be")

        video_dict = video_url_analysis(cleaned_data)
        domain_dict = website_domain_analysis(cleaned_data)

        plot_top_usage_values(domain_dict, save_path=f"{base_save_dir}/top_domain_usage_values_{topic}.png", topic=topic)
        plot_top_views_values(domain_dict, save_path=f"{base_save_dir}/top_domain_views_values_{topic}.png", topic=topic)
        plot_top_forwards_values(domain_dict, save_path=f"{base_save_dir}/top_domain_forward_values_{topic}.png", topic=topic)

        plot_top_usage_values(video_dict, save_path=f"{base_save_dir}/top_video_usage_values_{topic}.png", topic=topic, url_analysis_graph=True)
        plot_top_views_values(video_dict, save_path=f"{base_save_dir}/top_video_views_values_{topic}.png", topic=topic, url_analysis_graph=True)
        plot_top_forwards_values(video_dict, save_path=f"{base_save_dir}/top_video_forward_values_{topic}.png", topic=topic, url_analysis_graph=True)


def plot_and_save_top_occurrences(sort_dict, top_n = 10, topic = "" ,type = "" ):
    """
    Plots and saves a bar graph of the top occurrences from a sorted frequency dictionary.

    Parameters:
        sorted_frequencies (dict): A sorted dictionary of word frequencies in descending order.
        top_n (int): The number of top occurrences to display. Default is 10.
    """
    save_dir = "../occurrence_graphs"
    os.makedirs(save_dir, exist_ok=True)



    if len(sort_dict) < 10:
        top_n = len(sort_dict)

    top_items = list(sort_dict.items())[:top_n]

    labels, values = zip(*top_items)

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel(type)
    plt.ylabel('Occurrences')
    plt.title(f'Top {top_n} Occurrences {topic}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot to the directory
    save_path = os.path.join(save_dir, f'top_occurrences_{topic}_.png')
    plt.savefig(save_path)
    plt.close()



def word_count_analysis(data):
    word_dict = {}
    for message_list in data:
        for message in message_list:
            for word in message.split():
                if word in word_dict:
                    word_dict[word] += 1
                if word not in word_dict and word not in other_removed_words and word not in punctuation_lst and word not in stopwords.words('english'):
                    word_dict[word] = 1

    return word_dict


def extract_dates(json_data, start_date, end_date):

    start_date_obj = validate_date(start_date)
    end_date_obj = validate_date(end_date)

    if start_date_obj > end_date_obj:
        raise ValueError(f'Start date: {start_date_obj} cannot come after end date: {end_date_obj}')

    filtered_data = [
            item for item in json_data
            if start_date_obj <= datetime.strptime(item['Date'][0:10], '%Y-%m-%d') <= end_date_obj
        ]
    return filtered_data


def validate_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_string}'. Expected format: 'YYYY-MM-DD'.")


def sort_dict_by_value_descending(input_dict):
    sorted_items = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_items)


def do_word_analysis(data):
    return sort_dict_by_value_descending(word_count_analysis(clean_data(data)))


def sentiment_analysis(data):
    toxicity_list = []
    for message in data:
        results = Detoxify('original').predict(message)
        toxicity_list.append(results)
    return toxicity_list


def average_toxicity(toxicity_list):
    toxicity_number = len(toxicity_list)
    general_toxicity = 0
    severe_toxicity = 0
    obscene = 0
    threat = 0
    insult = 0
    identity_attack = 0


    for toxicity in toxicity_list:
        general_toxicity += toxicity["toxicity"][0]
        severe_toxicity += toxicity["severe_toxicity"][0]
        obscene += toxicity["obscene"][0]
        threat += toxicity["threat"][0]
        insult += toxicity["insult"][0]
        identity_attack += toxicity["identity_attack"][0]

    average_toxicity_dict = {
        "general_toxicity": round((general_toxicity / toxicity_number) * 100, 3),
        "severe_toxicity": round((severe_toxicity / toxicity_number) * 100, 3),
        "obscene": round((obscene / toxicity_number) * 100, 3),
        "threat": round((threat / toxicity_number) * 100, 3),
        "insult": round((insult / toxicity_number) * 100, 3),
        "identity_attack": round((identity_attack / toxicity_number) * 100, 3)
    }
    return average_toxicity_dict

def is_emoji(character):
    return character in emoji.EMOJI_DATA


def get_top_emojis(data):
    emoji_dict = {}
    for value in data:
        for char in value:
            if is_emoji(char):
                if char in emoji_dict:
                    emoji_dict[char] += 1
                else:
                    emoji_dict[char] = 1

    if len(emoji_dict) == 0:
        return {}

    sorted_dict = dict(sorted(emoji_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


def make_bar_graph_toxic(data, name):

    save_dir = "../occurrence_graphs"
    os.makedirs(save_dir, exist_ok=True)

    # Create the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue', edgecolor='black')
    plt.title(f"Toxicity Levels {name}", fontsize=16)
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Scores", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    # Save the graph to the specified file path
    plt.savefig(save_dir + "/" + name + ".png")
    plt.close()






year_list = [
 ('2024-01-01', '2024-01-31'),
 ('2024-02-01', '2024-02-29'),
 ('2024-03-01', '2024-03-31'),
 ('2024-04-01', '2024-04-30'),
 ('2024-05-01', '2024-05-31'),
 ('2024-06-01', '2024-06-30'),
 ('2024-07-01', '2024-07-31'),
 ('2024-08-01', '2024-08-31'),
 ('2024-09-01', '2024-09-30'),
 ('2024-10-01', '2024-10-31'),
 ('2024-11-01', '2024-11-30'),
 ('2024-12-01', '2024-12-31')
]


def do_analysis(data, topic):
    for month in year_list:
        month_data = extract_dates(data, month[0], month[1])
        cleaned_data = clean_data(month_data)
        sentiment_dict = sentiment_analysis(cleaned_data)
        word_count_dict = do_word_analysis(month_data)
        emoji_dictionary = get_top_emojis(word_count_dict)
        avg_toxicity_dict = average_toxicity(sentiment_dict)

        if not emoji_dictionary:
            print(f"Empty Emoji Dictionary from {month[0]}-{month[1]}")
            continue


        plot_and_save_top_occurrences(word_count_dict, 10, topic= f'Word Occurrences for {topic} between {month[0]}-{month[1]}', type="Words")
        plot_and_save_top_occurrences(emoji_dictionary, 10, topic= f'Emoji Occurrences for {topic} between {month[0]}-{month[1]}', type="Emojis")
        make_bar_graph_toxic(avg_toxicity_dict, name= f"Average Toxicity from {month[0]}-{month[1]}")




FEMA_DATA = extract_json("../JSONs/Telegram_Messages_FEMA.json")
do_analysis(FEMA_DATA, "FEMA")

HARP_DATA = extract_json("Telegram_Messages_HARP.json")
do_analysis(HARP_DATA, "HARP")

ClIMATE_DATA = extract_json("../JSONs/Telegram_Message_Climate_Change.json")
do_analysis(ClIMATE_DATA, "Climate_Change")
