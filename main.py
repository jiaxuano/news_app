import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

# Sample data
data = pd.DataFrame({
    'topic': ['Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae'],
    'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'quarter': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'article_count': [10, 15, 12, 18, 14, 20, 16, 22, 18, 25, 20, 28],
    'sentiment': [0.7, 0.6, 0.8, 0.5, 0.6, 0.7, 0.8, 0.6, 0.7, 0.8, 0.9, 0.7],
    'positive_sentences': ['Great technology!', 'Exciting sports event!', 'Amazing innovation!', 'Thrilling match!', 'Cutting-edge tech!', 'Impressive performance!', 'Groundbreaking invention!', 'Spectacular game!', 'Revolutionary product!', 'Unforgettable moment!', 'Future is here!', 'Incredible athlete!'],
    'negative_sentences': ['Technical issue', 'Poor sportsmanship', 'Buggy software', 'Disappointing result', 'Compatibility problems', 'Controversial decision', 'Security breach', 'Unsportsmanlike conduct', 'System failure', 'Injury concerns', 'Outdated technology', 'Doping allegations']
})

# Define the topics and time periods
topics = ['Federal Home Loan Bank of San Francisco', 'Fannie Mae']
time_periods = ['Week', 'Month', 'Quarter']

# Set page layout to wide
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("SwiftNews")

# Main page for user inputs
selected_section = st.sidebar.radio("Go to", ["Home", "Topic News", "Analysis"])

if selected_section == "Home":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>Trending News</h1>", unsafe_allow_html=True)
    # Define the path for the datasets
    dataset_path = 'results/'

    # Define topics and corresponding file names
    topics = {
        'Fannie Mae': 'fannie mae.csv',
        'Federal Home Loan Bank of San Francisco': 'Federal Home Loan Bank of San Francisco.csv',
        'First Republic Bank': 'First Republic Bank.csv'
    }

    # Load and sort data function
    def load_data(topic_name):
        df = pd.read_csv(dataset_path + topics[topic_name])
        df = df.sort_values(by='publish_date', ascending=False)
        df = df[df['summaries']!='Not-related content']
        df = df[df['summaries']!='Not-related content.']
        return df

    # Load initial dataset
    initial_topic = 'First Republic Bank'
    df = load_data(initial_topic)

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

elif selected_section == "Topic News":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>Topic News</h1>", unsafe_allow_html=True)
    # Add code for Topic News

elif selected_section == "Analysis":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>Analysis</h1>", unsafe_allow_html=True)
    # Add code for Analysis

    # Sample code for Analysis section
    col1, col2 = st.columns(2)

    with col1:
        selected_topic = st.selectbox('Select the Member', topics)

    with col2:
        selected_time_period = st.selectbox('Select time period', time_periods)

    st.markdown("---", unsafe_allow_html=True)  # Horizontal line

    col1, col2, col3 = st.columns(3)

    # First section: Number of articles over time and positive sentences
    with col1:
        filtered_data = data[data['topic'] == selected_topic]

        if selected_time_period == 'Week':
            x_axis = 'week'
            title = 'Number of Articles per Week'
        elif selected_time_period == 'Month':
            x_axis = 'month'
            title = 'Number of Articles per Month'
        else:
            x_axis = 'quarter'
            title = 'Number of Articles per Quarter'

        article_count_plot = px.line(filtered_data, x=x_axis, y='article_count', title=title)
        article_count_plot.update_layout(xaxis_title=f'{selected_time_period}', yaxis_title='Number of Articles', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
        article_count_plot.update_layout(title={'x':0.5, 'xanchor': 'center'})
        st.plotly_chart(article_count_plot, use_container_width=True)

        positive_sentences = filtered_data['positive_sentences'].tolist()
        # Add custom CSS to highlight selectbox
        st.markdown(
            """
            <style>
            .stSelectbox div[data-baseweb='select'] {
                border: 2px solid #005A8D !important;
                border-radius: 5px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.subheader('Positive News')
        st.markdown("<ul style='list-style-type: disc; padding-left: 20px; text-align: center;'>", unsafe_allow_html=True)
        for sentence in positive_sentences:
            st.markdown(f"<li style='color: #006E8D;'>{sentence}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

    # Second section: Sentiment over time and negative sentences
    with col2:
        sentiment_plot = px.line(filtered_data, x=x_axis, y='sentiment', title=f'Sentiment over {selected_time_period}')
        sentiment_plot.update_layout(xaxis_title=f'{selected_time_period}', yaxis_title='Sentiment Score', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
        sentiment_plot.update_layout(title={'x':0.5, 'xanchor': 'center'})
        sentiment_plot.update_traces(line_color='#FF5733')  # Change the line color to red
        st.plotly_chart(sentiment_plot, use_container_width=True)


        negative_sentences = filtered_data['negative_sentences'].tolist()
        st.subheader('Negative News')
        st.markdown("<ul style='list-style-type: disc; padding-left: 20px; text-align: center;'>", unsafe_allow_html=True)
        for sentence in negative_sentences:
            st.markdown(f"<li style='color: #FF5733;'>{sentence}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

    # Third section: Image, today's sentiment, number of articles today
    with col3:

        fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=60,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Reputation score"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': 'rgb(0, 128, 0)', 'thickness': 0.75},
            'bgcolor': "#F4F6F9",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgb(255, 0, 0)'},
                {'range': [50, 100], 'color': 'rgb(0, 255, 0)'}  # Corrected the range
            ],
        }
    ))

        fig.update_layout(plot_bgcolor="#F0F2F6")  # Set background color for the graph
        fig.update_layout(paper_bgcolor="#F0F2F6")  # Set background color for the plot area

        if selected_topic == 'Federal Home Loan Bank of San Francisco':
            image = Image.open('images/Federal Home Loan Bank of San Francisco/Federal Home Loan Bank of San Francisco Announces 2023 Director Election Results - GlobeNewswire.jpg')  # Replace with actual path
        elif selected_topic == 'Fannie Mae':
            image = Image.open('images/fannie mae/Fannie-Mae-Logo.png')  # Replace with actual path

        today_data = filtered_data[filtered_data[x_axis] == filtered_data[x_axis].max()]
        articles_today = today_data['article_count'].sum()
        sentiment_today = today_data['sentiment'].mean()

        st.markdown(f'<p style="color: #005A8D; font-size: 18px; text-align: center;">Number of news articles released today: {articles_today}</p>', unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)

        st.image(image, caption=f'Image for {selected_topic}', use_column_width=True)

    # Set background color for the Streamlit app container
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F0F2F6; /* Light gray */
        }
        .stImage > img {
            background-color: #F0F2F6; /* Light gray */
            border-radius: 10px; /* Optional: Add rounded corners */
        }
        .stPlot > div {
            background-color: #F0F2F6; /* Light gray */
            border-radius: 10px; /* Optional: Add rounded corners */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

