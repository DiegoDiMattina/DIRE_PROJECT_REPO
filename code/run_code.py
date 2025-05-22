from graphs import *
from data_processing import *
from url_analysis import *
from toxicity import *
from date_extractor import *
from word_count import *
from emoji_analysis import *

# TODO: Fix repository structure and clean codebase
# Plan:
# 1. Track a fake news story to analyze repetition and origin
# 2. Map content to the groups that initiated it

TOPIC_LIST = ["January", "February", "March", "Election",
              "China", "Voting", "Russia", "Crypto"]

JSON_FILES = ["Telegram_Messages_English_January.json", "Telegram_Messages_English_February.json",
              "Telegram_Messages_English_March.json", "Election_Cycle.json",
              "Telegram_Messages_China.json", "Telegram_Message_Voting.json",
              "Telegram_Messages_Russia.json", "Telegram_Messages_Crypto.json"]

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

def analyze_and_plot(json_file_list, topic_list, base_save_dir="plots"):
    """
    Analyzes JSON files for specified topics and generates plots.

    Args:
        json_file_list (list): List of JSON file paths.
        topic_list (list): List of topics corresponding to the JSON files.
        base_save_dir (str): Directory to save the generated plots.

    Returns:
        None
    """
    os.makedirs(base_save_dir, exist_ok=True)

    for json_file, topic in zip(json_file_list, topic_list):
        data = extract_json(json_file)
        cleaned_data = combine_compressed_urls(data, "Youtube.com", "youtu.be")

        video_dict = video_url_analysis(cleaned_data)
        domain_dict = website_domain_analysis(cleaned_data)

        # Generate plots for domain analysis
        plot_top_usage_values(domain_dict, save_path=f"{base_save_dir}/top_domain_usage_values_{topic}.png", topic=topic)
        plot_top_views_values(domain_dict, save_path=f"{base_save_dir}/top_domain_views_values_{topic}.png", topic=topic)
        plot_top_forwards_values(domain_dict, save_path=f"{base_save_dir}/top_domain_forward_values_{topic}.png", topic=topic)

        # Generate plots for video analysis
        plot_top_usage_values(video_dict, save_path=f"{base_save_dir}/top_video_usage_values_{topic}.png", topic=topic, url_analysis_graph=True)
        plot_top_views_values(video_dict, save_path=f"{base_save_dir}/top_video_views_values_{topic}.png", topic=topic, url_analysis_graph=True)
        plot_top_forwards_values(video_dict, save_path=f"{base_save_dir}/top_video_forward_values_{topic}.png", topic=topic, url_analysis_graph=True)

def do_word_analysis(data):
    """
    Analyzes word frequency in the provided data.

    Args:
        data (list): Data to analyze.

    Returns:
        dict: Word frequencies sorted in descending order.
    """
    return sort_dict_by_value_descending(word_count_analysis(process_data(data)))

def do_analysis(data, topic):
    """
    Performs analysis on data for a specific topic across multiple time ranges.

    Args:
        data (list): Input data for analysis.
        topic (str): Topic name for the analysis.

    Returns:
        None
    """
    for month in year_list:
        month_data = extract_dates(data, month[0], month[1])
        cleaned_data = process_data(month_data)
        sentiment_dict = sentiment_analysis(cleaned_data)
        word_count_dict = do_word_analysis(month_data)
        emoji_dictionary = get_top_emojis(word_count_dict)
        avg_toxicity_dict = average_toxicity(sentiment_dict)

        if not emoji_dictionary:
            print(f"No emojis found for {topic} from {month[0]} to {month[1]}")
            continue

        # Generate and save plots
        plot_and_save_top_occurrences(word_count_dict, 10, topic=f'Word Occurrences for {topic} between {month[0]}-{month[1]}', type="Words")
        plot_and_save_top_occurrences(emoji_dictionary, 10, topic=f'Emoji Occurrences for {topic} between {month[0]}-{month[1]}', type="Emojis")
        make_bar_graph_toxic(avg_toxicity_dict, name=f"Average Toxicity for {topic} between {month[0]}-{month[1]}")

# Perform analysis for specific datasets
FEMA_DATA = extract_json("../JSONs/Telegram_Messages_FEMA.json")
do_analysis(FEMA_DATA, "FEMA")

HARP_DATA = extract_json("../JSONs/Telegram_Messages_HAARP.json")
do_analysis(HARP_DATA, "HARP")

CLIMATE_DATA = extract_json("../JSONs/Telegram_Message_Climate_Change.json")
do_analysis(CLIMATE_DATA, "Climate_Change")