import requests
import pandas as pd

# Your Facebook access token
access_token = 'EAAOKF5vwULwBO3cZBfEoy1t9P7rlI1fgyIDZBmTOpbChhgaSIcnFLuA9EKkTiVZBAKA5bP2MTsYRDB0UW1jfXO2JC082pvQq666ZB38jKg3CC70yQrkiYGmMrOkMvrG7fzIfNR12vcYJeqyHV8WZA5VOU4cZAgMqKvn6jMfNgQiJgQkRHSZBBE3LMrVuRsbs3GvYsFtdZBEyZAlUKlPmIYjgOAtNk'

# The ID of the Facebook page or profile
page_id = '	346030858590567'

# Facebook Graph API URL to fetch posts along with likes
url = f'https://graph.facebook.com/v12.0/{page_id}/posts?fields=id,message,created_time,likes.summary(true)&access_token={access_token}'

# Make the request to fetch data
response = requests.get(url)
data = response.json()

# Check if data is successfully fetched
if 'data' in data:
    posts = data['data']
else:
    print("Failed to fetch data")
    posts = []

# Prepare data for saving to CSV
posts_data = []
for post in posts:
    posts_data.append({
        'post_id': post.get('id'),
        'message': post.get('message', ''),
        'created_time': post.get('created_time', ''),
        'likes': post.get('likes', {}).get('summary', {}).get('total_count', 0),
        # Add more fields as needed
    })

# Convert to a DataFrame
df = pd.DataFrame(posts_data)

# Save to CSV
df.to_csv('facebook_posts.csv', index=False, encoding='utf-8')

print("Data saved to facebook_posts.csv")


import pandas as pd
import re
from collections import Counter

# Load the data from the CSV file
df = pd.read_csv('facebook_posts.csv')

# Display the first few rows to verify the data
print(df.head())

# Check for missing values in each column
print(df.isnull().sum())
# Convert 'created_time' to datetime format if not already in that format
df['created_time'] = pd.to_datetime(df['created_time'])
# Extract date and hour from 'created_time'
df['date'] = df['created_time'].dt.date
df['hour'] = df['created_time'].dt.hour
# Summary statistics for numerical columns
print(df.describe())
import matplotlib.pyplot as plt

# Plot the distribution of likes
df['likes'].plot(kind='hist', bins=20, title='Distribution of Likes')
plt.xlabel('Number of Likes')
plt.ylabel('Frequency')
plt.show()

# Plot the number of posts over time
df['date'].value_counts().sort_index().plot(kind='line', title='Posts Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.show()

# Function to extract hashtags and keywords
def extract_hashtags_and_keywords(text):
    hashtags = re.findall(r'#\w+', text.lower())  # Extract hashtags
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words (keywords)
    return hashtags, words

# Lists to store all hashtags and keywords
all_hashtags = []
all_keywords = []

# Iterate over each message and extract hashtags and keywords
for message in df['message']:
    hashtags, keywords = extract_hashtags_and_keywords(message)
    all_hashtags.extend(hashtags)
    all_keywords.extend(keywords)

# Display some of the extracted hashtags and keywords
print("Sample Hashtags:", all_hashtags[:10])
print("Sample Keywords:", all_keywords[:10])
# Count the frequency of hashtags and keywords
hashtag_counts = Counter(all_hashtags)
keyword_counts = Counter(all_keywords)

# Display the 10 most common hashtags and keywords
print("Most common hashtags:")
print(hashtag_counts.most_common(10))

print("\nMost common keywords:")
print(keyword_counts.most_common(10))

# Convert 'created_time' to datetime format if not already
df['created_time'] = pd.to_datetime(df['created_time'])

# Extract date from 'created_time'
df['date'] = df['created_time'].dt.date

# Analyze hashtag trends over time
hashtag_trends = {}
for date, group in df.groupby('date'):
    hashtags_on_date = []
    for message in group['message']:
        hashtags, _ = extract_hashtags_and_keywords(message)
        hashtags_on_date.extend(hashtags)
    hashtag_trends[date] = Counter(hashtags_on_date)

# Example: Display trend of a specific hashtag
specific_hashtag = '#eminem'
trend_data = {date: counts[specific_hashtag] for date, counts in hashtag_trends.items() if specific_hashtag in counts}

# Convert to a DataFrame for easier plotting
trend_df = pd.DataFrame(list(trend_data.items()), columns=['Date', 'Count'])

# Plot the trend
trend_df.plot(x='Date', y='Count', kind='line', title=f"Trend of {specific_hashtag}")
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.show()

# Plot trends for multiple hashtags
hashtags_to_plot = ['#eminem', '#nolie']
for hashtag in hashtags_to_plot:
    trend_data = {date: counts[hashtag] for date, counts in hashtag_trends.items() if hashtag in counts}
    trend_df = pd.DataFrame(list(trend_data.items()), columns=['Date', 'Count'])
    trend_df.plot(x='Date', y='Count', kind='line', title=f"Trend of {hashtag}")
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.show()

