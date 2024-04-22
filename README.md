-- Developing Stage --

<a href="https://newsapp-kf4izafuxgmhgdtpbpz5hx.streamlit.app/" target="_blank">**SwiftNews** (Try Here)</a>


**SwiftNews** is an application designed to streamline the consumption of news content from various sources. 
It utilizes Large Language models (LLMs) to classify the sentiment of news articles, automatically summarize their content, and provide insightful analytics.

**Features**
- **News Aggregation:** Pulls news articles from multiple sources to provide a comprehensive view of current events.
- **Sentiment Analysis:** Classifies the sentiment of each news article as positive, negative, or neutral, allowing users to gauge the overall tone of the news.
- **Automatic Summarization:** Generates concise summaries of news articles to save users time and effort in reading.
- **Analytics:** Provides data-driven insights and visualizations to help users understand trends and patterns in the news.

**Getting Started**

**Installation**

1. Clone the repository:
   ``` git clone https://github.com/your-username/swiftnews.git ```
   
2. Install dependencies:
   ```pip install -r requirements.txt```
   
3. Run the application:
   ```streamlit run main.py```

**Usage**
- Upon launching the application, users can select their preferred news topics and sources.
- The application will fetch news articles from the selected sources and classify their sentiment.
- Users can then view summarized versions of the articles and explore analytics features to gain insights into the news landscape.

**Customization**
- Add your google_gemini_pro key and world_news_api keys (be mindful of the API limits)
- Add your topic of interests in the news lines of the topics.txt file.
- To schedule data collection:
-- Modify the scheduling settings in the code to specify the frequency of data collection.
-- Use tools like cron or Task Scheduler to automate the execution of the data collection script at specified intervals.

- Through Cronjobs, We could automate the data collection process.
We have scheduled the collection on 2 datas. One for News collection and the other is for Image collection.
You could automate the process by adding the following command in crontab -e
- ```0 * * * * python_environment_location google_news.py_location >> log_file_location``` Fetch the news related to the topic for every hour
- ```20 * * * * python_environment_location download_images.py_location >> image_log_file_location``` Download the images for the pulled news at every 20th min of an hour (Giving the news collection module 20 mins)
- Run the model.py file to get the sentiment and summarization results for all the topics into their respective csv files under results folder
  ```python model.py```
https://github.com/vineethgupthab/news_app/assets/138868502/4428d5e1-ec8b-4281-aabc-cd46c5d7db29
