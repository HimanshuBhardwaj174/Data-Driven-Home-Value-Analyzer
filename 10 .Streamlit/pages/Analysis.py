










import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(page_title="Gurugram Property Analytics", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2 {
        color: #2c3e50;
    }
    .plot-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title('🏙️ Gurugram Property Analytics')
st.markdown("""
This dashboard provides comprehensive analytics on the Gurugram property market. 
Explore various visualizations to gain insights into property prices, types, and distributions across different sectors.
""")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('./Dataset/data_viz1.csv')

new_df = load_data()

# Map of Gurugram
st.header('📍 Map of Gurugram')
with st.container():
    #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    group = new_df.groupby('sector')[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()
    fig = px.scatter_mapbox(group, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                            mapbox_style="open-street-map", text=group.index)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Price Sectorwise
st.header('💰 Price Sectorwise')
with st.container():
    #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    k = new_df.groupby('sector')['price'].mean().sort_values(ascending=False)
    fig = px.bar(k, x=k.index, y=k.values)
    fig.update_layout(xaxis_title="Sectors", yaxis_title="Price (Crore)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Price (Flat vs House)
st.header('🏠 Price (Flat vs House)')
with st.container():
    #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    house_prices = new_df[new_df['property_type'] == 'house']['price']
    flat_prices = new_df[new_df['property_type'] == 'flat']['price']
    fig = ff.create_distplot([house_prices, flat_prices], ['House Prices', 'Flat Prices'], show_hist=True, show_rug=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Area vs Price and BHK Sectorwise
col1, col2 = st.columns(2)

with col1:
    st.header('📊 Area vs Price')
    with st.container():
        #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        property_type = st.selectbox('Select Property type', ['flat', 'house'])
        df_filtered = new_df[new_df['property_type'] == property_type]
        fig = px.scatter(df_filtered, y='price', x='built_up_area', color='bedRoom')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.header('🥧 BHK Sectorwise')
    with st.container():
        #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        sector_options = ['overall'] + sorted(new_df['sector'].unique().tolist())
        selected_sector = st.selectbox('Select Sector', sector_options)
        df_filtered = new_df if selected_sector == 'overall' else new_df[new_df['sector'] == selected_sector]
        fig = px.pie(df_filtered, names='bedRoom')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# BHK Price Comparison
st.header('💲 BHK Price Comparison')
with st.container():
    #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    fig = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Word Cloud
st.header('☁️ Sectorwise Word Cloud')
with st.container():
    #st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    with open('./pages/words.pkl', 'rb') as f:
        words = pickle.load(f)
    sector_ = st.selectbox('Select Sector', sorted(new_df['sector'].unique()))
    if sector_:
        text = words[words['sector'] == sector_]['words'].values[0]
        feature_text = ' '.join(text)
        wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(feature_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown('---')
