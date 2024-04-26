import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go


# Sample data
data = pd.DataFrame({
    'topic': ['Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae', 'Federal Home Loan Bank of San Francisco', 'Fannie Mae'],
    'week': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
    'month': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'quarter': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

# Main page for user inputs
st.markdown("<h1 style='text-align: center; color: #005A8D;'>Member Reputation Analysis</h1>", unsafe_allow_html=True)

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
