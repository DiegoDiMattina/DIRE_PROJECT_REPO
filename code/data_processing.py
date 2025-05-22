'''
This is the data processing file that is used to extract the json data and preform basic cleaning
of the data. Made for the Dire research group
'''
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect

punctuation_lst = [".","!","'s","?",",",":","*","-",'’', '``', '”', '“', '#', '...',
                   '>', '‘', '—', ';', ']', '[' , '–']

other_removed_words = ["the", "'", "a", "&", '"', "https", "''", "(", ")", "@", "was", "would", "as" , " the", "the ", " the "]
url_links = []




def extract_json(json_file_name):
    '''
    Takes in a path/name of the json file and returns the data
    '''
    with open(json_file_name, 'r') as json_file:
        data = json.load(json_file)
        return data


def process_data(data):
    '''
    Takes in Json data and pushes english messages through to the data pipeline.
    If it is a link then it will save that link into url messages
    This function both populates the url links and pushes data to be cleaned
    '''
    cleaned_messages = []
    for message in data:
        if not message["Message"] or isinstance(message, str): #Making sure the messages are string
            continue
        try:
            if detect(message["Message"]) == "pt":
                continue
            elif detect(message["Message"]) == "en": #Ensuring that the messages are English
                message_tokenize = word_tokenize(message["Message"]) # Splits the messages into a word list
                cleaned_messages.append(stop_words_cleaning(message_tokenize)) #Sends messages to clean
        except Exception as e:
            url_links.append(message["Message"]) # Adds URL link to use
    return cleaned_messages



def stop_words_cleaning(message_tokens):
    messages = []
    for word in message_tokens:
        if word.lower() in stopwords.words('english'): # Removes stop words that are not important to the overall meaning
            message_tokens.remove(word)
        if word.lower() in punctuation_lst: # Removes unneeded punctuation
            message_tokens.remove(word)
        if word.lower() in other_removed_words: #Remove other words
            message_tokens.remove(word)
    message = ' '.join(message_tokens) #conjoins all the world together
    messages.append(message.lower())
    return messages
