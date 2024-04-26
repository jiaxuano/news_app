import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

# Set page config to wide mode for a better layout
st.set_page_config(layout="wide")

# Define the path for the datasets
dataset_path = 'results/'

# Define topics and corresponding file names
topics_dict = {
    'Fannie Mae': 'fannie mae.csv',
    'Federal Home Loan Bank of San Francisco': 'Federal Home Loan Bank of San Francisco.csv',
    'First Republic Bank': 'First Republic Bank.csv'
}

# Sample data for analysis (replace this with your actual data)
analysis_data = pd.DataFrame({
    'topic': ['Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae'],
    'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'quarter': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'article_count': [10, 15, 12, 18, 14, 20, 16, 22, 18, 25, 20, 28],
    'sentiment': [0.7, 0.6, 0.8, 0.5, 0.6, 0.7, 0.8, 0.6, 0.7, 0.8, 0.9, 0.7]
})

# Load and sort data function
def load_data(topic_name):
    df = pd.read_csv(dataset_path + topics_dict[topic_name])
    df = df.sort_values(by='publish_date', ascending=False)
    return df

# Initialize session state for current news index
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Sidebar navigation and topic selection
st.sidebar.title("Navigation")
selected_section = st.sidebar.radio("Go to", ["Home", "Analysis"])

# Main page logic based on navigation selection
if selected_section == "Home":
    topic_selection = st.sidebar.selectbox('Choose a topic', options=list(topics_dict.keys()), index=list(topics_dict.keys()).index('First Republic Bank'))

    # Load the data for the selected topic
    df = load_data(topic_selection)

    # Main Page Display Function
    def show_news(index):
        with st.container():
            # Define column layout for the news item
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button('Previous'):
                    if st.session_state.current_index > 0:
                        st.session_state.current_index -= 1

            with col2:
                # Display image
                image = df.iloc[index]['image']
                st.image(image, use_column_width=True)

                # Display title, published date, link, summary, sentiment, and publisher
                title = df.iloc[index]['title']
                st.markdown(f"<h1 style='font-size: 36px;'>{title}</h1>", unsafe_allow_html=True)

                published_date = df.iloc[index]['publish_date']
                st.markdown(f"**Published Date:** {published_date}", unsafe_allow_html=True)

                publisher = df.iloc[index]['publisher']
                st.markdown(f"**Publisher:** {publisher}", unsafe_allow_html=True)

                summary = df.iloc[index]['summaries']
                st.text_area("Summary", summary, height=150)

                sentiment_value = df.iloc[index]['default_sentiment']
                sentiment_color = "#000000"  # Default black color
                if sentiment_value > 0:
                    sentiment_color = "#008000"  # Green color
                elif sentiment_value < 0:
                    sentiment_color = "#FF0000"  # Red color
                st.markdown(f"<p style='color: {sentiment_color};'>**Sentiment:** {sentiment_value}</p>", unsafe_allow_html=True)

                link = df.iloc[index]['url']
                st.markdown(f"[Read full article]({link})", unsafe_allow_html=True)

            with col3:
                if st.button('Next'):
                    if st.session_state.current_index < len(df) - 1:
                        st.session_state.current_index += 1

    # Display the current news item or the first item by default
    show_news(st.session_state.current_index)

elif selected_section == "Analysis":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>Analysis</h1>", unsafe_allow_html=True)

    # Analysis section using the sample data
    # Here, you should replace 'analysis_data' with your actual analysis data
    selected_topic = st.selectbox('Select the Member', topics_dict.keys())
    selected_time_period = st.selectbox('Select time period', ['Week', 'Month', 'Quarter'])

    filtered_data = analysis_data[analysis_data['topic'] == selected_topic]
    time_period = 'week' if selected_time_period == 'Week' else 'month' if selected_time_period == 'Month' else 'quarter'
    fig = px.line(filtered_data, x=time_period, y='article_count', title=f'Number of Articles over {selected_time_period}')
    st.plotly_chart(fig, use_container_width=True)

    sentiment_fig = px.line(filtered_data, x=time_period, y='sentiment', title=f'Sentiment over {selected_time_period}')
    st.plotly_chart(sentiment_fig, use_container_width=True)