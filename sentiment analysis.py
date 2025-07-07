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

from textblob import TextBlob

# Apply sentiment analysis to the messages
df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Plot the sentiment distribution
df['sentiment'].plot(kind='hist', bins=20, title='Sentiment Distribution')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Frequency')
plt.show()

