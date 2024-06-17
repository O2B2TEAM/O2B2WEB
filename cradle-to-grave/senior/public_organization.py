import base64
import os

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="노세老世",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.subheader("노세老世 | 복지관", divider='orange')
st.markdown("노인 복지와 구직 사이트를 제공합니다.")
st.markdown(" ")

# Load the CSV file
file_path = 'dir/site.csv'  # Update this path if necessary
df = pd.read_csv(file_path)

# Streamlit app
def main():
    # Multiselector for 'divde' column
    divde_options = df['DIVIDE'].unique()
    selected_divdes = st.multiselect('Select divde', divde_options)

    if selected_divdes:
        # Filter dataframe based on selected divde
        filtered_df = df[df['DIVIDE'].isin(selected_divdes)]

        # Display the filtered dataframe
        cols = st.columns(5)  # Create 5 columns for each row
        col_index = 0

        for index, row in filtered_df.iterrows():
            with cols[col_index]:
                with st.container(border=True):
                    image_path = f"images/{index}.png"
                    st.image(image_path)
                    st.markdown(f"##### {row['APP_NAME']}")
                    st.markdown(f"[Link to app]({row['APP_LINK']})")
            col_index = (col_index + 1) % 5  # Move to the next column

if __name__ == "__main__":
    main()
