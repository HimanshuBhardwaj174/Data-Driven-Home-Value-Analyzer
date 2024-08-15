# import streamlit as st

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

# st.write("# Welcome to Streamlit! 👋")

# st.sidebar.success("Select a demo above.")




import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Gurugram Property Analytics",
    page_icon="🏙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #1E88E5;
    }
    .medium-font {
        font-size:30px !important;
        color: #424242;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="big-font">Welcome to Gurugram Property Analytics! 🏙️</p>', unsafe_allow_html=True)

# Introduction
st.markdown('<p class="medium-font">Explore the dynamic real estate market of Gurugram with our interactive analytics dashboard.</p>', unsafe_allow_html=True)

# Features section
st.markdown("## 🌟 Key Features")

col1, col2, col3,col4 = st.columns(4)

with col1:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 In-depth Analysis")
    st.write("Dive into comprehensive property data, including price trends, sector-wise comparisons, and more.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Interactive Maps")
    st.write("Visualize property distributions across Gurugram with our interactive map feature.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Market Insights")
    st.write("Gain valuable insights into market trends, property types, and pricing factors.")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🏠 Property Recommendations")
    st.write("Get personalized property recommendations based on location and similarity.")
    st.markdown('</div>', unsafe_allow_html=True)

# Sample visualization
st.markdown("## 📊 Sample Visualization")
st.write("Here's a glimpse of what you can explore:")

# Create sample data
import pandas as pd
import numpy as np

sample_data = pd.DataFrame({
    'Sector': ['Sector ' + str(i) for i in range(1, 11)],
    'Average Price': np.random.randint(5000000, 20000000, 10) / 100000
})

fig = px.bar(sample_data, x='Sector', y='Average Price', 
             title='Average Property Prices by Sector (Sample Data)',
             labels={'Average Price': 'Average Price (Crores)'},
             color='Average Price',
             color_continuous_scale=px.colors.sequential.Viridis)

st.plotly_chart(fig, use_container_width=True)



# Recommendation System Overview
st.markdown("## 🔍 Property Recommendation System")
st.write("Our advanced recommendation system helps you find the perfect property in two ways:")

col1, col2 = st.columns(2)

with col1:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📍 Location-based Search")
    st.write("""
    - Select a specific location in Gurugram
    - Set your desired search radius
    - Get a list of properties within that area
    - View results on an interactive map
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🏘️ Similar Property Finder")
    st.write("""
    - Choose a property you like
    - Our system analyzes its features
    - Receive recommendations for similar properties
    - Compare options with similarity scores
    """)
    st.markdown('</div>', unsafe_allow_html=True)














# Call-to-action
st.markdown("## 🚀 Get Started")
st.write("Explore our interactive dashboards to gain insights into Gurugram's property market. Select from the sidebar to begin your journey!")

# Sidebar
st.sidebar.markdown("# Navigation")
st.sidebar.success("Select above to explore different aspects of Gurugram's property market.")

# Footer
st.markdown("---")
