'''
Does the emoji Analysis by counting the emojis and ordering it in descending order.
Made for the DIRE project research group
'''

import emoji

def is_emoji(character):
    """
    Check if a character is an emoji.
    """
    return character in emoji.EMOJI_DATA


def get_top_emojis(data):
    """
    Extract the top emojis from the given data and their counts.
    :param data: List of strings
    :return: Dictionary with emojis as keys and their counts as values
    """
    emoji_dict = {}
    for value in data:
        for char in value:
            if is_emoji(char):
                emoji_dict[char] = emoji_dict.get(char, 0) + 1

    if not emoji_dict:
        return {}

    sorted_dict = dict(sorted(emoji_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict