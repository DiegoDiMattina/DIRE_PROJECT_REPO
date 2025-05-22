'''
Python file concerned with extracting telegram messages based on the dates provided.
Made for the DIRE project research group
'''
import datetime

def extract_dates(json_data, start_date, end_date):
    '''
    takes in json data and given two start and end dates will give all the messages between them
    '''
    start_date_obj = validate_date(start_date)
    end_date_obj = validate_date(end_date)

    if start_date_obj > end_date_obj:
        raise ValueError(f'Start date: {start_date_obj} cannot come after end date: {end_date_obj}')

    filtered_data = [
            item for item in json_data
            if start_date_obj <= datetime.datetime.strptime(item['Date'][0:10], '%Y-%m-%d') <= end_date_obj #Make sure to get all the messages are between the two dates
        ]
    return filtered_data


def validate_date(date_string):
    '''
    Makes sure the dates are valid (Can't have June 38)
    '''
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_string}'. Expected format: 'YYYY-MM-DD'.")
