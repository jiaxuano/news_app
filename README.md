**SwiftNews**
SwiftNews is an application designed to streamline the consumption of news content from various sources. 
It utilizes natural language processing (NLP) techniques to classify the sentiment of news articles, automatically summarize their content, and provide insightful analytics.

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

**Data**
Add your topic of interests in the news lines of the topics.txt file.

**Schedule the Data Collection process**
- Through Cronjobs, We could automate the data collection process.
We have scheduled the collection on 2 datas. One for News collection and the other is for Image collection.
You could automate the process by adding the following command in crontab -e
```0 * * * * python_environment_location google_news.py_location >> log_file```
```0 * * * * python_environment_location download_images.py_location >> image_log_file```
