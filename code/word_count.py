'''
Counts the word occurrences. Made for the DIRE project research group
'''
from nltk.corpus import stopwords

# List of punctuation to be excluded from analysis
punctuation_lst = [".", "!", "'s", "?", ",", ":", "*", "-", '’', '``', '”', '“', '#', '...',
                   '>', '‘', '—', ';', ']', '[', '–']

# Additional words to be excluded from analysis
other_removed_words = ["the", "'", "a", "&", '"', "https", "''", "(", ")", "@", "was", "would", "as",
                       " the", "the ", " the "]

def word_count_analysis(data):
    """
    Counts the occurrences of words in the given data, excluding stop words, punctuation, and specified words.
    Returns a dictionary with words as keys and their frequencies as values.
    """
    word_dict = {}

    for message_list in data:
        for message in message_list:
            for word in message.split():
                # Increment the count if the word already exists in the dictionary
                if word in word_dict:
                    word_dict[word] += 1
                # Add the word if it is not in the dictionary and not in the excluded lists
                if word not in word_dict and word not in other_removed_words and word not in punctuation_lst and word not in stopwords.words('english'):
                    word_dict[word] = 1

    return word_dict