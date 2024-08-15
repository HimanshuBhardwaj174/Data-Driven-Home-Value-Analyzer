# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle
# import plotly.graph_objects as go

# # Page configuration
# st.set_page_config(page_title="Recommend Appartments", layout="wide")


# with open('../10. Recommender System/location_appartments.pkl','rb') as f:
#     df = pickle.load(f)

# with open('../10. Recommender System/cosine_sim1.pkl','rb') as f:
#     cosine_sim1 = pickle.load(f)
# with open('../10. Recommender System/cosine_sim2.pkl','rb') as f:
#     cosine_sim2 = pickle.load(f)
# with open('../10. Recommender System/cosine_sim3.pkl','rb') as f:
#     cosine_sim3 = pickle.load(f)

# def recommend_properties_with_scores(property_name, top_n=247):
    
#     cosine_sim_matrix = 30*cosine_sim1 + 20*cosine_sim2 + 8*cosine_sim3
#     # cosine_sim_matrix = cosine_sim3
    
#     # Get the similarity scores for the property using its name as the index
#     sim_scores = list(enumerate(cosine_sim_matrix[df.index.get_loc(property_name)]))
    
#     # Sort properties based on the similarity scores
#     sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
#     # Get the indices and scores of the top_n most similar properties
#     top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
#     top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
#     # Retrieve the names of the top properties using the indices
#     top_properties = df.index[top_indices].tolist()
    
#     # Create a dataframe with the results
#     recommendations_df = pd.DataFrame({
#         'PropertyName': top_properties,
#         'SimilarityScore': top_scores
#     })
    
#     return recommendations_df



# ##Part 1 
# location = st.selectbox('Location',sorted(df.columns.to_list()))
# radius = st.number_input('Radius in Kms')

# if st.button('Find'):
#     frame = df[df[location].sort_values() < radius*1000][location]
#     app = []
#     dis = []
#     for i,j in frame.items():
#         app.append(i)
#         dis.append(str(round(j/1000)) + ' Kms')
#         #st.text(str(i) + ' ' + '->' + str(round(j/1000)) +'Kms')

#     genre = st.radio(
#         "What's your favorite movie genre",
#         app,
#         captions = dis)
    
# ##Part 2
# appartment = st.selectbox('Appartments',sorted(df.index.to_list()))

# if st.button('Predict'):
#     st.dataframe(recommend_properties_with_scores(appartment).head())




import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Gurugram Property Recommender", layout="wide")

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
    h1, h2, h3 {
        color: #2c3e50;
    }
    .result-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_resource
def load_data():
    with open('../10. Recommender System/location_appartments.pkl', 'rb') as f:
        df = pickle.load(f)
    with open('../10. Recommender System/cosine_sim1.pkl', 'rb') as f:
        cosine_sim1 = pickle.load(f)
    with open('../10. Recommender System/cosine_sim2.pkl', 'rb') as f:
        cosine_sim2 = pickle.load(f)
    with open('../10. Recommender System/cosine_sim3.pkl', 'rb') as f:
        cosine_sim3 = pickle.load(f)
    return df, cosine_sim1, cosine_sim2, cosine_sim3

df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

# Recommendation function
def recommend_properties_with_scores(property_name, top_n=247):
    cosine_sim_matrix = 30*cosine_sim1 + 20*cosine_sim2 + 8*cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    top_properties = df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    return recommendations_df

# Title
st.title("🏡 Gurugram Property Recommender")
st.markdown("Discover your ideal property in Gurugram with our advanced recommendation system.")

# Create tabs
tab1, tab2 = st.tabs(["Location-based Search", "Similar Property Finder"])

with tab1:
    st.header("🗺️ Find Properties by Location")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox('Select a Location', sorted(df.columns.to_list()))
    with col2:
        radius = st.number_input('Search Radius (in km)', min_value=0.1, max_value=50.0, value=5.0, step=0.1)
    
    if st.button('Find Properties', key='find_location'):
        frame = df[df[location].sort_values() < radius*1000][location]
        if frame.empty:
            st.warning(f"No properties found within {radius} km of {location}.")
        else:
            st.success(f"Found {len(frame)} properties within {radius} km of {location}.")
            
            # Create a dataframe for display
            result_df = pd.DataFrame({
                'Property': frame.index,
                'Distance (km)': frame.values / 1000
            }).sort_values('Distance (km)')
            
            # Display results in an interactive table
            st.dataframe(result_df, height=400)
            
            # Visualize on a scatter plot
            fig = px.scatter(result_df, x='Distance (km)', y='Property', 
                             title=f'Properties near {location}',
                             labels={'Property': 'Property Name', 'Distance (km)': 'Distance (km)'},
                             hover_data=['Distance (km)'])
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🏘️ Find Similar Properties")
    
    appartment = st.selectbox('Select a Property', sorted(df.index.to_list()))
    
    if st.button('Find Similar Properties', key='find_similar'):
        recommendations = recommend_properties_with_scores(appartment).head(10)
        
        st.success(f"Here are the top 10 properties similar to {appartment}:")
        
        # Display results in an interactive table
        st.dataframe(recommendations, height=400)
        
        # Visualize on a bar chart
        fig = px.bar(recommendations, x='PropertyName', y='SimilarityScore', 
                     title=f'Top 10 Properties Similar to {appartment}',
                     labels={'PropertyName': 'Property Name', 'SimilarityScore': 'Similarity Score'},
                     hover_data=['SimilarityScore'])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
