import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime, timedelta
import plotly.graph_objects as go
import io
import requests

# Set page configuration
st.set_page_config(layout="wide", page_title="SwiftNews Analysis Dashboard")

# Sidebar for navigation
st.sidebar.title("SwiftNews")

# Define the path for the datasets
dataset_path = 'results/'

# Define topics and corresponding file names
# Because keys are defined kind of inconsistently lower case key definitions exist :/
topics_dict = {
    'Fannie Mae': 'fannie mae.csv',
    'fannie mae': 'fannie mae.csv',

    # 'Tesla' : 'tesla.csv',
    'Meta' : 'meta.csv',
    'meta' : 'meta.csv',
    'Apple' : 'apple company.csv',
    'apple company' : 'apple company.csv',

    # 'Google' : 'google.csv',
    'Federal Home Loan Bank of San Francisco': 'Federal Home Loan Bank of San Francisco.csv',
    'First Republic Bank': 'First Republic Bank.csv'
}

analysis_data = pd.DataFrame({
    'topic': ['Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Meta', 'Apple'] * 3,
    'week' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'month' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'quarter' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'week_count': [9, 10, 10, 7, 9, 7, 6, 8, 5, 9, 11, 8],
    'month_count': [36, 25, 40, 42, 17, 18, 12, 20, 15, 17, 9, 7],
    'quarter_count': [114, 123, 131, 167, 200, 144, 176, 139, 110, 135, 108, 90],
    'article_count': [10, 15, 12, 18, 14, 20, 16, 22, 18, 25, 20, 28],
    'week_sentiment': [0.72,0.82,0.10,-0.34,0.78,-0.42,-0.86,0.79,0.33,0.12,-0.93,-0.28],
    'month_sentiment': [0.30, -0.44,-0.37,0.81,0.88,0.79,-0.27,0.64,0.91,0.67,0.58,-0.24], 
    'quarter_sentiment' : [0.70,-0.54,0.30,-0.35,0.39,0.97,-0.27,0.01,-0.34,0.41,-0.89,-0.83],
    'positive_sentences': ['Great technology!', 'Exciting sports event!', 'Amazing innovation!', 'Thrilling match!', 'Cutting-edge tech!', 'Impressive performance!', 'Groundbreaking invention!', 'Spectacular game!', 'Revolutionary product!', 'Unforgettable moment!', 'Future is here!', 'Incredible athlete!'],
    'negative_sentences': ['Technical issue', 'Poor sportsmanship', 'Buggy software', 'Disappointing result', 'Compatibility problems', 'Controversial decision', 'Security breach', 'Unsportsmanlike conduct', 'System failure', 'Injury concerns', 'Outdated technology', 'Doping allegations']
})


bulletpoints = pd.read_csv('results/bullets.csv')

# Function to load and sort data
def load_data(topic_name):
    df = pd.read_csv(dataset_path + topics_dict[topic_name])
    df['publish_date'] = pd.to_datetime(df['publish_date'])
    df = df.sort_values(by='publish_date', ascending=False)
    df = df[df['summaries'] != 'Not-related content']
    df = df[df['summaries'] != 'Not-related content.']
    return df


def load_aggregated_data(topic_name, days):
    df = pd.read_csv(dataset_path + topics_dict[topic_name])
    df['publish_date'] = pd.to_datetime(df['publish_date']).dt.date

    # Aggregate data by day
    daily_summary = df.groupby('publish_date').agg({
        'default_sentiment': 'mean',  # Average sentiment per day
        'title': 'count'  # Count of entries per day, assuming 'title' as a proxy for entries
    }).rename(columns={'default_sentiment': 'average_sentiment', 'title': 'count_per_day'})

    # Create a date range for the last 'days' days, normalized to dates
    end_date = pd.to_datetime("today").normalize()
    start_date = end_date - pd.Timedelta(days=days - 1)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D').date

    # Reindex the DataFrame to include all days in the last 'days' days, filling missing days with NaN
    full_summary = daily_summary.reindex(date_range).fillna({
        'average_sentiment': 0,  # Fill missing sentiment averages with 0
        'count_per_day': 0       # Fill missing counts with 0
    })

    return full_summary

# Initialize session state for current news index
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Main page logic based on navigation selection
selected_section = st.sidebar.radio("Go to", ["Home", "News by Topics", "Analysis"])

if selected_section == "Home":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>SwiftNews Trending</h1>", unsafe_allow_html=True)
    latest_date = datetime.now() - timedelta(days=3)
    recent_news_list = []

    for topic in topics_dict:
        df = load_data(topic)
        last_three_dates = df['publish_date'].drop_duplicates().nlargest(3)
        recent_news = df[df['publish_date'].isin(last_three_dates)]
        recent_news_list.append(recent_news)

    if recent_news_list:
        df = pd.concat(recent_news_list)
        if df.empty:
            st.write("No recent news available.")
        else:
            # Ensure current index is within the bounds
            max_index = len(df) - 1
            if st.session_state.current_index > max_index:
                st.session_state.current_index = max_index

            def show_news(index):
                if index >= 0 and index <= max_index:
                    with st.container():
                        col1, col2, col3 = st.columns([1, 4, 1])
                        with col1:
                            if st.button('Previous Story'):
                                st.session_state.current_index = max(0, index - 1)
                        with col2:
                            row = df.iloc[index]
                            # Get sentiment value and determine color
                            sentiment_value = row.get('default_sentiment', 0)  # Use get for safe access
                            sentiment_color = "#000000"  # Default black color
                            if sentiment_value > 0:
                                sentiment_color = "#008000"  # Green color
                            elif sentiment_value < 0:
                                sentiment_color = "#FF0000"  # Red color

                            st.image(row['image'], use_column_width=True)
                            st.markdown(f"<h1 style='font-size: 36px;'>{row['title']}</h1>", unsafe_allow_html=True)
                            
                            # Format the published date to exclude the time and align publisher to the right
                            published_date = row['publish_date'].strftime('%Y-%m-%d')
                            date_publisher_html = f"""
                                <div style='display: flex; justify-content: space-between; align-items: center;'>
                                    <span><b>Published Date:</b> {published_date}</span>
                                    <span><b>Publisher:</b> {row['publisher']}</span>
                                </div>
                                """
                            st.markdown(date_publisher_html, unsafe_allow_html=True)

                            st.text_area("Summary", row['summaries'], height=150)
                            st.markdown(f"<p style='color: {sentiment_color};'>**Article Sentiment:** {sentiment_value}</p>", unsafe_allow_html=True)
                            st.markdown(f"[Read full article]({row['url']})", unsafe_allow_html=True)
                        with col3:
                            if st.button('Next Story'):
                                st.session_state.current_index = min(max_index, index + 1)

            # Display the current news item
            show_news(st.session_state.current_index)
    else:
        st.write("No recent news available.")


if selected_section == "News by Topics":
    topic_selection = st.sidebar.selectbox('Choose a topic', options=list(topics_dict.keys()))
    df = load_data(topic_selection)

    def show_news(index):
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])  # Adjust the ratio as needed
            with col1:
                if st.button('Previous Story'):
                    if st.session_state.current_index > 0:
                        st.session_state.current_index -= 1  # Correct the decrement logic
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
                
                # Format the published date to exclude the time
                published_date = df.iloc[index]['publish_date'].strftime('%Y-%m-%d')
                
                # Create a markdown string for published date and publisher
                date_publisher_html = f"""
                    <div>
                        <span><b>Published Date:</b> {published_date}</span>
                        <span style="float: right;"><b>Publisher:</b> {df.iloc[index]['publisher']}</span>
                    </div>
                    """
                st.markdown(date_publisher_html, unsafe_allow_html=True)

                summary = df.iloc[index]['summaries']
                st.text_area("Summary", summary, height=150)
                
                st.markdown(f"<p style='color: {sentiment_color};'>**Article Sentiment:** {sentiment_value}</p>", unsafe_allow_html=True)

                link = df.iloc[index]['url']
                st.markdown(f"[Read full article]({link})", unsafe_allow_html=True)

            with col3:
                if st.button('Next Story'):
                    if st.session_state.current_index < len(df) - 1:
                        st.session_state.current_index += 1
    # Display the current news item or the first item by default
    show_news(st.session_state.current_index)

# elif selected_section == "Analysis":
#     st.markdown("<h1 style='text-align: center; color: #005A8D;'>Analysis</h1>", unsafe_allow_html=True)

#     # Sample code for Analysis section
#     col1, col2 = st.columns(2)

#     with col1:
#         selected_topic = st.selectbox('Select the Topic', topics_dict.keys())

#     with col2:
#         selected_time_period = st.selectbox('Select time period', ['Week', 'Month', 'Quarter'])

#     st.markdown("---", unsafe_allow_html=True)  # Horizontal line

#     col1, col2, col3 = st.columns(3)

#     # First section: Number of articles over time and positive sentences
#     with col1:
#         filtered_data = analysis_data[analysis_data['topic'] == selected_topic]

#         if selected_time_period == 'Week':
#             x_axis = 'week'
#             y_axis = 'week_count'
#             y_sentiment = 'week_sentiment'
#             title = 'Number of Articles per Week'

#         elif selected_time_period == 'Month':
#             x_axis = 'month'
#             y_axis = 'month_count'
#             y_sentiment = 'month_sentiment'
#             title = 'Number of Articles per Month'
#         else:
#             x_axis = 'quarter'
#             y_axis = 'quarter_count'
#             y_sentiment = 'quarter_sentiment'
#             title = 'Number of Articles per Quarter'

#         # article_count_plot = px.line(filtered_data, x=x_axis, y='article_count', title=title)
#         article_count_plot = px.line(filtered_data, x=x_axis, y=y_axis, title=title)
#         article_count_plot.update_layout(xaxis_title=f'{selected_time_period}', yaxis_title='Number of Articles', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
#         article_count_plot.update_layout(title={'x':0.5, 'xanchor': 'center'})
#         st.plotly_chart(article_count_plot, use_container_width=True)

#         positive_sentences = filtered_data['positive_sentences'].tolist()
#         st.subheader('Positive News')
#         st.markdown("<ul style='list-style-type: disc; padding-left: 20px; text-align: center;'>", unsafe_allow_html=True)
#         for sentence in positive_sentences:
#             st.markdown(f"<li style='color: #006E8D;'>{sentence}</li>", unsafe_allow_html=True)
#         st.markdown("</ul>", unsafe_allow_html=True)

#     # Second section: Sentiment over time and negative sentences
#     with col2:
#         sentiment_plot = px.line(filtered_data, x=x_axis, y=y_sentiment, title=f'Sentiment over {selected_time_period}')
#         # sentiment_plot = px.line(filtered_data, x=x_axis, y='sentiment', title=f'Sentiment over {selected_time_period}')
#         sentiment_plot.update_layout(xaxis_title=f'{selected_time_period}', yaxis_title='Sentiment Score', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
#         sentiment_plot.update_layout(title={'x':0.5, 'xanchor': 'center'})
#         sentiment_plot.update_traces(line_color='#FF5733')  # Change the line color to red
#         st.plotly_chart(sentiment_plot, use_container_width=True)

#         negative_sentences = filtered_data['negative_sentences'].tolist()
#         st.subheader('Negative News')
#         st.markdown("<ul style='list-style-type: disc; padding-left: 20px; text-align: center;'>", unsafe_allow_html=True)
#         for sentence in negative_sentences:
#             st.markdown(f"<li style='color: #FF5733;'>{sentence}</li>", unsafe_allow_html=True)
#         st.markdown("</ul>", unsafe_allow_html=True)



elif selected_section == "Analysis":
    st.markdown("<h1 style='text-align: center; color: #005A8D;'>Analysis</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_topic = st.selectbox('Select the Topic', bulletpoints['topic'].unique())
    with col2:
        selected_time_period = st.selectbox('Select time period', ['Week', 'Month', 'Quarter'])
        timeframe_days = {'Week': 7, 'Month': 30, 'Quarter': 90}
        days = timeframe_days[selected_time_period]

    st.markdown("---", unsafe_allow_html=True)  # Horizontal line

    col1, col2, col3 = st.columns(3)

    filtered_data = load_aggregated_data(selected_topic, days)

    # First section: Number of articles over time and displaying bullet points for positive sentences
    with col1:
        # Plotting the number of articles
        article_count_plot = px.line(filtered_data, y='count_per_day', labels={'index': 'Date', 'count_per_day': 'Article Count'},
                                     title=f'Number of Articles per {selected_time_period}')
        article_count_plot.update_layout(xaxis_title='Date', yaxis_title='Number of Articles', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
        article_count_plot.update_layout(title={'x':0.5, 'xanchor': 'center'})
        st.plotly_chart(article_count_plot, use_container_width=True)

        # Display bullet points for positive news
        topic_bullets = bulletpoints[(bulletpoints['topic'] == selected_topic) & (bulletpoints['timeframe'] == f'{selected_time_period.lower()}ly')]
        positive_sentences = [sentence.strip('- ').strip() for sentence in topic_bullets['positive'].iloc[0].split('\n') if sentence]
        st.subheader('Positive News')
        st.markdown("<ul style='list-style-type: disc; padding-left: 20px; text-align: center;'>", unsafe_allow_html=True)
        for sentence in positive_sentences:
            st.markdown(f"<li style='color: #006E8D;'>{sentence}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

    # Second section: Sentiment over time and displaying bullet points for negative sentences
    with col2:
        # Plotting sentiment over time
        sentiment_plot = px.line(filtered_data, y='average_sentiment', labels={'index': 'Date', 'average_sentiment': 'Average Sentiment'},
                                 title=f'Sentiment over {selected_time_period}')
        sentiment_plot.update_layout(xaxis_title='Date', yaxis_title='Sentiment Score', plot_bgcolor='#F4F6F9', paper_bgcolor='#F4F6F9')
        sentiment_plot.update_traces(line_color='#FF5733')
        st.plotly_chart(sentiment_plot, use_container_width=True)

        # Display bullet points for negative news
        negative_sentences = [sentence.strip('- ').strip() for sentence in topic_bullets['negative'].iloc[0].split('\n') if sentence]
        st.subheader('Negative News')
        st.markdown("<ul style='list-style-type: disc; padding_left: 20px; text-align: center;'>", unsafe_allow_html=True)
        for sentence in negative_sentences:
            st.markdown(f"<li style='color: #FF5733;'>{sentence}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

    # Optionally, you can add additional visualizations or data summaries in col3 or elsewhere as needed



    # Third section: Image, today's sentiment, number of articles today
    articles_in_time = filtered_data['count_per_day'].sum()

    # Third section: Image, today's sentiment, number of articles today
    articles_in_time = filtered_data['count_per_day'].sum()

    with col3:
        # Calculate the average sentiment
        average_sentiment = filtered_data['average_sentiment'].mean() * 100

        # Determine sentiment text
        sentiment_text = ""
        if -10 <= average_sentiment <= 10:
            sentiment_text = "Neutral"
        elif -30 <= average_sentiment < -10:
            sentiment_text = "Slightly Negative"
        elif -60 <= average_sentiment < -30:
            sentiment_text = "Moderately Negative"
        elif average_sentiment < -60:
            sentiment_text = "Very Negative"
        elif 10 < average_sentiment <= 30:
            sentiment_text = "Slightly Positive"
        elif 30 < average_sentiment <= 60:
            sentiment_text = "Moderately Positive"
        elif average_sentiment > 60:
            sentiment_text = "Very Positive"

        # Convert average sentiment to percentage and add percentage sign
        average_sentiment_percentage = f"{average_sentiment:.2f}%"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=average_sentiment,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Sentiment"},
            gauge={
                'axis': {'range': [-100, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': 'rgb(0, 128, 0)', 'thickness': 0.75},
                'bgcolor': "#F4F6F9",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [-100, -50], 'color': 'rgb(255, 0, 0)'},
                    {'range': [-50, 50], 'color': 'rgb(255, 255, 255)'},
                    {'range': [50, 100], 'color': 'rgb(0, 255, 0)'}
                ],
            }
        ))

        # Add percentage sign and sentiment text
        fig.update_layout(
            annotations=[
                dict(
                    text=f"{sentiment_text}",
                    x=0.5,
                    y=0.5,
                    font=dict(size=24),
                    showarrow=False,
                    align="center"
                )
            ]
        )

        fig.update_layout(plot_bgcolor="#F0F2F6")  # Set background color for the graph
        fig.update_layout(paper_bgcolor="#F0F2F6")  # Set background color for the plot area

        # Define image_path with a default image
        default_image_path = 'Default-Logo.png'  # Adjust to a valid default image path
        image_path = {
            'Federal Home Loan Bank of San Francisco': 'Federal-Home-Loan-Bank-Logo.png',
            'fannie mae': 'Fannie-Mae-Logo.png',
            'First Republic Bank': 'First-Republic-Bank-Logo.png',
            'apple company': 'Apple-Logo.png',
            'Google': 'Google-Logo.png',  # Uncommented and assuming you have an image
            'meta': 'Meta-Logo.png',
            'Tesla': 'Tesla-Logo.png'  # Uncommented and assuming you have an image
        }.get(selected_topic, default_image_path)

        try:
            image = Image.open(image_path)
            st.image(image, caption=f'Image for {selected_topic}', use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

        st.markdown(f'<p style="color: #005A8D; font-size: 18px; text-align: center;">Number of news articles released this {selected_time_period}: {articles_in_time}</p>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
