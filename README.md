# Youtube-dashboard

## Overview
  This is a simple dashboard data collected from youtube scrape using the youtube-api-v3. With the data you'll see all the channel related details like; subsribers, view count, comment count, duration, comment previews, like count, dislike count, favorites. There are a total of 3 notebooks. Data scrape, analysis, and training model.
  
### Data scraping
  There are six functions used to scrape data from getting channel ids using the search function, getting playlist ids using the channels function, getting video ids using the playlistItems function, getting the video statistics from the videos function and last getting the comments using the commentThreads function. With the search function I have searched for all the channels with a region code of 'MN'. Although it didn't return only mongolian channels, it was close.
  
### Data Analysis
  Using the channel statistics data, I've looked at the top ten channels.
  With the video statistics data, I've formatted the dates, changed formats to numerics and added an engagement column summing the comment count and like count. Created a month column from the published_date column and created a total seconds column from the duration column. Using the month column I could see how much vidoes are upload per month. The results didn't show much of a difference. 

### Data preprocessing and training
  With the video statistics data I've wanted to do a youtube views predictor by the video title. First thought I had was to groupbythe views into bins and have it be a categorical classifier. But with training it kind of failed so I just used the views as it is. Then cleaning the title column, I got rid of the stop words, took out the special characters, lemmatized the words and tokenized them. 
  For the training I used a pretrained model 'distilber-base-uncased'.

### The model
  In the second tab of the dashboard you have can input any kind of title and it will give back a predicted number of views you video may likely have.

Link to the streamlit application https://sarazoloo-youtube-dashboard-youtube-app-bhvrso.streamlit.app/
