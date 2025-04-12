import streamlit as st
import pandas as pd
from PIL import Image

# Load the data
df_RFM = pd.read_csv('df_RFM.csv')  # Has RFM scores
df_now = pd.read_csv('df_now.csv')  # Has cluster labels

# Merge the cluster info into the RFM DataFrame
df_combined = pd.merge(df_RFM, df_now[['Member_number', 'Cluster']], on='Member_number', how='left')

# App config
st.set_page_config(page_title="RFM KMeans Segmentation", layout="centered")
st.title("🎯 Customer Segmentation with RFM + KMeans (k=3)")

# 1. Show image
st.header("📈 Unsupervised Customer Segments")
image = Image.open("Unsupervised Segments.png")
st.image(image, use_column_width=True)

# 2. Show 10 random customers with cluster
st.header("👥 Sample of 10 Random Customers")
st.dataframe(df_combined.sample(10)[['Member_number', 'R', 'F', 'M', 'RFM_Score', 'Cluster']])

# 3. User input
st.header("🔍 Customer Lookup")
option = st.radio("Choose a search option:", ["Search by Member Number", "Search by RFM Scores"])

if option == "Search by Member Number":
    member_id = st.text_input("Enter Member_number (e.g., 2193):")
    if member_id:
        try:
            member_id = int(member_id)
            result = df_combined[df_combined['Member_number'] == member_id]
            if not result.empty:
                st.success(f"Cluster for Member {member_id}: Cluster {result['Cluster'].values[0]}")
                st.dataframe(result)
            else:
                st.error("Member_number not found.")
        except ValueError:
            st.error("Please enter a valid integer Member_number.")
else:
    r = st.selectbox("R Score", [1, 2, 3, 4])
    f = st.selectbox("F Score", [1, 2, 3, 4])
    m = st.selectbox("M Score", [1, 2, 3, 4])
    filtered = df_combined[(df_combined['R'] == r) & 
                           (df_combined['F'] == f) & 
                           (df_combined['M'] == m)]
    st.success(f"Found {len(filtered)} customers matching RFM={r}{f}{m}")
    st.dataframe(filtered[['Member_number', 'R', 'F', 'M', 'RFM_Score', 'Cluster']])
