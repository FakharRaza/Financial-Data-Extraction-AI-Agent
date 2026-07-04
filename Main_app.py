import streamlit as st
import pandas as pd
from Financial_data import extract_financial_info  # Yeh aapki function file hai

st.set_page_config(layout="wide")
st.title("Financial Data Extraction Tool")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Input News Article")
    article_text = st.text_area("Paste your article here...", height=400)
    extract_button = st.button("Extract Data")

with right_col:
    st.subheader("Extracted Financial Details")
    # app.py mein yeh change karein
if extract_button:
    result_df = extract_financial_info(article_text)
    if result_df is not None:
        st.success("Data Extracted Successfully!")
        st.dataframe(result_df)
    else:
        st.error("AI se data fetch karne mein problem hui. Please check the terminal.")