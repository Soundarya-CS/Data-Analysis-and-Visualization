from googleapiclient.discovery import build
import pandas as pd
import json # import json for pretty printing

# Replace with your API key
api_key = "AIzaSyCwDQnVnlos-W86mdSEc41QphSn0lLCEOM"

# Function to fetch trending videos
def get_trending_videos(regioncode = "IN", maxResults = 20):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part = "snippet, statistics",
        chart = "mostPopular",
        regionCode = regioncode,
        maxResults = maxResults
    )

    response = request.execute()

# To know the JSON structure (OPTIONAL)
#     print(json.dumps(response, indent=4))
#     return response
# get_trending_videos(regioncode="IN", maxResults = 1)

# Fetch trending videod data
    video_data = []
    for item in response["items"]:
        video_info = {
            "Title" : item["snippet"]["title"],
            "ChannelName" : item["snippet"]["channelTitle"],
            "Published_date" : item["snippet"]["publishedAt"],
            "Views" : item["statistics"].get("viewCount", 0),
            "Likes" : item["statistics"].get("likeCount", 0),
            "Comments" : item["statistics"].get("commentCount", 0),
            "Video_url" : f"https://www.youtube.com/watch?v={item['id']}"
                }
        video_data.append(video_info)

    return pd.DataFrame(video_data)

df = get_trending_videos(regioncode='IN', maxResults=10)

# To save as CSV
df.to_csv('youtube_trending_videos.csv', index= False)

print("Trending videos data saved to youtube_trending_videos.csv")

#------------------------------------------------------------------------------#

# Data Analysis using the Youtube_trending _Videos

#Load the CSV file
df = pd.read_csv("youtube_trending_videos.csv")

#Display basic info
print(df.info())

#Show the first 5 rows
print(df.head())

# Most viewed video
most_viewed_video = df.loc[df["Views"].idxmax()]
print("Most viewed video:\n", most_viewed_video)
# Most Liked Video
most_liked_video = df.loc[df["Likes"].idxmax()]
print("Most liked video:\n", most_liked_video)
# The channel with most trending videos
most_trending_videos = df["ChannelName"].value_counts().idxmax()
print("The channel with most trending videos:\n", most_trending_videos)


# Correlation between Views, likes and comments
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(6,4))
sns.heatmap(df[["Views", "Likes", "Comments"]].corr(), annot= True, cmap = "coolwarm", fmt = ".2f")
plt.title("Correlation between Views, Likes and Comments")
plt.show()

# Most viewed videos bar chart

top_5 = df.nlargest(5, "Views")

plt.figure(figsize=(10,5))
sns.barplot(x=top_5["Views"], y=top_5["Title"], hue= None, palette="viridis", legend = False)
plt.xlabel("Views")
plt.ylabel("Video title")
plt.title("Top 5 most trending videos")
plt.show()
