'''
A bunch of python utils file used throughout the project. Made for the DIRE project research group
'''

def safe_int(values):
    """
    Converts a value to an integer, returning 0 if the conversion fails.
    Handles ValueError and TypeError gracefully.
    """
    try:
        return int(values)
    except (ValueError, TypeError):
        return 0

def combine_compressed_urls(data, key1, key2):
    """
    Combines values from two keys in a dictionary by adding them element-wise.
    Removes the second key after combining if both keys exist.
    """
    if key1 in data and key2 in data:
        data[key1] = [a + b for a, b in zip(data[key1], data[key2])]
        del data[key2]
        return data
    else:
        return data

def sort_dict_by_value_descending(input_dict):
    """
    Sorts a dictionary by its values in descending order.
    Returns a new dictionary with sorted items.
    """
    sorted_items = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_items)