import streamlit as st
import pandas as pd

# URLs for the raw CSV files on GitHub
csv_urls = {
    'Fannie Mae': 'https://raw.githubusercontent.com/vineethgupthab/news_app/fcce4c71e57b9a943281c4de8d15be2babd1342b/results/fannie%20mae.csv',
    'Federal Home Loan Bank of San Francisco': 'https://raw.githubusercontent.com/vineethgupthab/news_app/fcce4c71e57b9a943281c4de8d15be2babd1342b/results/Federal%20Home%20Loan%20Bank%20of%20San%20Francisco.csv',
    'First Republic Bank': 'https://raw.githubusercontent.com/vineethgupthab/news_app/fcce4c71e57b9a943281c4de8d15be2babd1342b/results/First%20Republic%20Bank.csv'
}

# Function to load data from a GitHub URL
def load_data_from_github(csv_url):
    return pd.read_csv(csv_url)

# Define the initial topic
initial_topic = 'Fannie Mae'

# Sidebar navigation and topic selection
st.sidebar.title("Navigation")
if st.sidebar.button('Home'):
    st.sidebar.write("You are at the Home view.")
    # Define the home action

# Use the initial topic to set the default selection in the selectbox
topic_selection = st.sidebar.selectbox('Choose a topic', options=list(csv_urls.keys()), index=list(csv_urls.keys()).index(initial_topic))

if st.sidebar.button('Analysis'):
    st.sidebar.write("You are at the Analysis view.")
    # Define the analysis action

if st.sidebar.button('Learn'):
    company_name = topic_selection.replace(' ', '_')
    st.sidebar.markdown(f"[Learn about {topic_selection}](https://en.wikipedia.org/wiki/{company_name})", unsafe_allow_html=True)

# Load the data for the selected topic
df = load_data_from_github(csv_urls[topic_selection])
df = df.sort_values(by='publish_date', ascending=False)

# Main Page Display Function
def show_news(index):
    with st.container():
        col1, col2 = st.columns([1, 4])  # Adjust the ratio as needed
        with col1:
            st.write("")  # For vertical spacing
        with col2:
            # Get sentiment value and determine color
            sentiment_value = df.iloc[index]['default_sentiment']
            sentiment_color = "#000000"  # Default black color
            if sentiment_value > 0:
                sentiment_color = "#008000"  # Green color
            elif sentiment_value < 0:
                sentiment_color = "#FF0000"  # Red color

            # Display image
            image = df.iloc[index]['image']
            st.image(image, use_column_width=True)

            # Display title, published date, link, summary, and sentiment
            title = df.iloc[index]['title']
            st.markdown(f"<h1 style='font-size: 36px;'>{title}</h1>", unsafe_allow_html=True)
            
            published_date = df.iloc[index]['publish_date']
            st.markdown(f"**Published Date:** {published_date}", unsafe_allow_html=True)
            
            summary = df.iloc[index]['summaries']
            st.text_area("Summary", summary, height=150)
            
            st.markdown(f"<p style='color: {sentiment_color};'>**Sentiment:** {sentiment_value}</p>", unsafe_allow_html=True)
            
            link = df.iloc[index]['url']
            st.markdown(f"[Read full article]({link})", unsafe_allow_html=True)

# Navigation buttons for stories
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button('Previous Story'):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

with col3:
    if st.button('Next Story'):
        if st.session_state.current_index < len(df) - 1:
            st.session_state.current_index += 1

# Show the current news item or the first item by default
show_news(st.session_state.current_index)