import json
import os
from collections import defaultdict
from datetime import datetime

# Constants
DIRECTORY = './'  # Update this path
SECONDS_IN_DAY = 86400
SECONDS_IN_YEAR = 31536000  # Assuming a non-leap year
MONTHS_IN_YEAR = 12
TOP_PLACES_LIMIT = 20  # Limit to top 20 places
SORT_BY = 'frequency'  # Options: 'time' or 'frequency'
CIRCLED_NUMBERS = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']

def parse_timestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

def calculate_duration(start, end):
    return (parse_timestamp(end) - parse_timestamp(start)).total_seconds()

def get_place_id_info(place_visit):
    location = place_visit.get('location', {})
    place_id = location.get('placeId')
    address = location.get('address', '')
    name = location.get('name', '')
    full_address = f"{name}, {address}" if name else address
    return place_id, full_address

# Main Script
visit_details = defaultdict(lambda: {'count': 0, 'duration': 0, 'address': ''})

# Read and combine all JSON files
for filename in os.listdir(DIRECTORY):
    if filename.endswith('.json'):
        with open(os.path.join(DIRECTORY, filename), 'r') as file:
            data = json.load(file)
            timeline_objects = data.get('timelineObjects', [])
            for obj in timeline_objects:
                if 'placeVisit' in obj:
                    place_id, full_address = get_place_id_info(obj['placeVisit'])
                    if place_id:
                        duration = calculate_duration(obj['placeVisit']['duration']['startTimestamp'], obj['placeVisit']['duration']['endTimestamp'])
                        visit_details[place_id]['count'] += 1
                        visit_details[place_id]['duration'] += duration
                        visit_details[place_id]['address'] = full_address

# Sort the list of places
if SORT_BY == 'time':
    sorted_visits = sorted(visit_details.items(), key=lambda x: x[1]['duration'], reverse=True)[:TOP_PLACES_LIMIT]
else:  # Default to sorting by frequency
    sorted_visits = sorted(visit_details.items(), key=lambda x: x[1]['count'], reverse=True)[:TOP_PLACES_LIMIT]

print("Top 20 places visited, ordered by number of visits:")
for index, (place_id, details) in enumerate(sorted_visits):
    total_hours = round(details['duration'] / 3600, 2)
    total_days = round(details['duration'] / SECONDS_IN_DAY, 2)
    percentage_of_year = (details['duration'] / SECONDS_IN_YEAR) * 100
    average_percentage_per_month = percentage_of_year / MONTHS_IN_YEAR

    circle_number = CIRCLED_NUMBERS[index] if index < len(CIRCLED_NUMBERS) else str(index + 1)
    print(f'{circle_number.center(93)}')
    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━•❃°•°❀°•°❃•━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print(f'{details["address"]} ({details["count"]} visits)'.center(80))
    print(f'Time spent: {total_hours} hours ({total_days} days, {percentage_of_year:.2f}% of the year, {average_percentage_per_month:.2f}% per month)'.center(80))
    print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━•❃°•°❀°•°❃•━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')