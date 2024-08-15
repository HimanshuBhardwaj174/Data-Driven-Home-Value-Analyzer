
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Property Price Predictor", layout="wide")

# Load data
@st.cache_resource
def load_data():
    with open('./pages/pipeline.pkl', 'rb') as f:
        pipe = pickle.load(f)
    with open('./pages/df.pkl', 'rb') as f:
        df = pickle.load(f)
    return pipe, df

pipe, df = load_data()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .st-emotion-cache-16idsys p {
        font-size: 20px;
    }
    .prediction-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/000000/real-estate.png", width=100)
st.sidebar.title("About")
st.sidebar.info("This app predicts luxury property prices based on various features. Use the inputs below to get an estimated price range for your property.")

# Main content
st.title("🏰 Property Price Predictor")
st.markdown("Discover the value of your high-end property with our advanced prediction model.")

# Create two main columns
left_column, right_column = st.columns([2, 1])

with left_column:
    st.subheader("Property Details")
    
    with st.container():
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-title'>Basic Information</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        property_type = col1.selectbox('Property Type', df['property_type'].unique().tolist(), help="Select the type of property")
        sector = col2.selectbox('Sector', df['sector'].sort_values().unique(), help="Select the sector of the property")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-title'>Size and Age</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        built_up_area = col1.number_input(label='Built-up Area (sq ft)', min_value=0, help="Enter the built-up area in square feet")
        agePossession = col2.selectbox('Age of Property', df['agePossession'].unique(), help="Select the age category of the property")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-title'>Room Configuration</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        bedRoom = col1.selectbox('Bedrooms', df['bedRoom'].sort_values().unique(), help="Select the number of bedrooms")
        bathroom = col2.selectbox('Bathrooms', df['bathroom'].sort_values().unique(), help="Select the number of bathrooms")
        balcony = col3.selectbox('Balconies', ['0', '1', '2', '3', '3+'], help="Select the number of balconies")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-title'>Additional Features</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        furnishing_type = col1.selectbox('Furnishing Type', df['furnishing_type'].sort_values().unique(), help="Select the furnishing type")
        floor_category = col2.selectbox('Floor Category', df['floor_category'].sort_values().unique(), help="Select the floor category")
        
        col1, col2, col3 = st.columns(3)
        servant = col1.selectbox('Servant Room', df['servant room'].sort_values().unique(), help="Select if servant room is available")
        store = col2.selectbox('Store Room', df['store room'].sort_values().unique(), help="Select if store room is available")
        luxury_category = col3.selectbox('Luxury Category', df['luxury_category'].sort_values().unique(), help="Select the luxury category")
        st.markdown("</div>", unsafe_allow_html=True)

with right_column:
    st.subheader("Prediction")
    prediction_box = st.empty()
    
    if st.button('Predict Price', key='predict'):
        val = [[property_type, sector, bedRoom, bathroom, balcony,
                agePossession, built_up_area, servant, store,
                furnishing_type, luxury_category, floor_category]]
        one_df = pd.DataFrame(val, columns=df.columns)
        price = np.round(pipe.predict(one_df), 2)
        lower_price = np.round(price - 0.22, 2)[0]
        upper_price = np.round(price + 0.22, 2)[0]
        
        with prediction_box.container():
            st.markdown(f"""
            <div class="prediction-box">
                <h3 style='text-align: center; color: #2c3e50;'>Estimated Price Range</h3>
                <p style='text-align: center; font-size: 28px; font-weight: bold; color: #27ae60;'>
                    ₹{lower_price} Cr - ₹{upper_price} Cr
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = price[0],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Predicted Price (Cr)", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, max(upper_price, 10)]},
                    'bar': {'color': "#27ae60"},
                    'steps': [
                        {'range': [0, lower_price], 'color': "lightgray"},
                        {'range': [lower_price, upper_price], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': price[0]}}))
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("Note: This is an estimated range. Actual prices may vary based on market conditions and specific property features.")
# Add a footer
st.markdown("---")
st.markdown("", unsafe_allow_html=True)

