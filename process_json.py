import pandas as pd
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect
import matplotlib.pyplot as plt
import re


# Do it by topics/themes
#Check the election time period
#Check what specific post
#Try it by type
# Download stopwords if you haven't already
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt')

punctuation_lst = [".","!","'s","?",",",":","*","-"]
url_links = []
messages = []

def extract_by_month_year(month_year):
    '''
    Takes JSON mes
    :param month_year:
    :return: Processed Data
    '''
    filename = f'Telegram Messages({month_year}).json'
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data


def clean_data(data):
    for message in data:
        if not message["Message"] or isinstance(message, str):
            continue
        try:
            if detect(message["Message"]) == "pt":
                continue
            elif detect(message["Message"]) == "en":
                message_tokenize = word_tokenize(message["Message"])
                stop_words_cleaning(message_tokenize)
        except Exception as e:
            url_links.append(message["Message"])


def stop_words_cleaning(message_tokens):

    for word in message_tokens:
        if word.lower() in stopwords.words('english'):
            message_tokens.remove(word)
        if word.lower() in punctuation_lst:
            message_tokens.remove(word)
    print(message_tokens)
    message = ' '.join(message_tokens)
    messages.append(message)


def save_panda_dataframe(data):
    df = pd.DataFrame({'Message': data})
    drop_duplicates = df.drop_duplicates(subset='Message')

    styled_df = drop_duplicates.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('background-color', 'lightblue')]}]
    )

    html = styled_df.render()
    with open("cleaned_messages.html", "w") as file:
        file.write(html)



def url_analysis(telegram_data):

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
        raise KeyError("One or both keys not found in dictionary")


def plot_top_usage_values(data, top_n=10, save_path="top_websites_usage_values.png"):

    sorted_data = sorted(data.items(), key=lambda x: x[1][0], reverse=True)

    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][0] for site in top_sites]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Usage")
    plt.title(f"Top {top_n} Websites by Usage Value")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


def plot_top_views_values(data, top_n=10, save_path="top_websites_views_values.png"):

    sorted_data = sorted(data.items(), key=lambda x: x[1][1], reverse=True)


    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][1] for site in top_sites]


    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Views")
    plt.title(f"Top {top_n} Websites by View Value")
    plt.xticks(rotation=45, ha='right')


    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


def plot_top_forwards_values(data, top_n=10, save_path="top_websites_forward_values.png"):

    sorted_data = sorted(data.items(), key=lambda x: x[1][2], reverse=True)

    top_sites = sorted_data[:top_n]

    labels = [site[0] for site in top_sites]
    middle_values = [site[1][2] for site in top_sites]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, middle_values, color='skyblue')
    plt.xlabel("Website")
    plt.ylabel("Forward")
    plt.title(f"Top {top_n} Websites by Forward Value")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


data = extract_by_month_year("Mar 2025")
data_dict = url_analysis(data)
cleaned_dict = combine_compressed_urls(data_dict, "youtube.com", "youtu.be")
print(cleaned_dict)
plot_top_usage_values(cleaned_dict)
plot_top_views_values(cleaned_dict)
plot_top_forwards_values(cleaned_dict)

