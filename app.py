import streamlit as st
import pandas as pd
import os

def common_message():
  st.write('''
  Jai Shree Mataji!

  For any queries or feedback, you may reach out to me at +91 7774035501 or [advaitkisar2509@gmail.com](mailto:advaitkisar2509@gmail.com). 

  Thank you for using this web app!
  ''')

# Custom CSS injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Roboto+Mono&display=swap');

/* Main title styling */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #2a3f5f !important;
    border-bottom: 2px solid #2a3f5f;
    padding-bottom: 10px;
}

/* Stotra title styling */
.stotra-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    color: #2a3f5f !important;
    margin: 1rem 0 !important;
}

/* Script content styling */
.script-content {
    font-family: 'Roboto Mono', monospace !important;
    font-size: 1.1rem;
    line-height: 1.6;
    white-space: pre-wrap;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 5px;
    margin-top: 15px;
}

/* Dropdown styling */
.stSelectbox > div > div {
    font-family: 'Playfair Display', serif !important;
}
</style>
""", unsafe_allow_html=True)

# Load data from Excel
@st.cache_data
def load_data():
    data = {}
    data['SA'] = pd.read_excel('Data.xlsx', sheet_name='SA')
    data['MR'] = pd.read_excel('Data.xlsx', sheet_name='MR')
    data['HI'] = pd.read_excel('Data.xlsx', sheet_name='HI')
    data['EN'] = pd.read_excel('Data.xlsx', sheet_name='EN')

    return data

data = load_data()

# App layout
st.title('Sahajayoga Stotra Sangraha')

st.markdown('<div style="font-size: 14px; color: #000;">Designed and developed by Advait Amit Kisar</div>', unsafe_allow_html=True)

# Language selection
language = st.selectbox('Select Language', ['Sanskrit / संस्कृतम् (SA)', 'Marathi / मराठी (MR)', 'Hindi / हिन्दी (HI)', 'English (EN)'])
lang_code = language[-3:-1]  # Extracts SA/MR/HI/EN

# Stotra selection
df = data[lang_code]
if lang_code == 'EN':
   stotra_options = [
    f"{row['Name (Roman)']}"
    for _, row in df.iterrows()
   ]
else:
   stotra_options = [
       f"{idx+1}. {row['Name (Roman)']} / {row['Name (Original)']}"
       for idx, (_, row) in enumerate(df.iterrows())
   ]
selected_stotra = st.selectbox('Select Stotra', stotra_options)

# Script selection
if lang_code == 'SA':
   script_map = {
       'Devanagari (Marathi/Hindi)': 'DN',
       'Roman (English)': 'EN',
       'IAST': 'IA'
   }
elif lang_code != 'EN':
   script_map = {
       'Devanagari (Marathi/Hindi)': 'DN',
       'Roman (English)': 'EN',
       'ISO 15919 Indic': 'ISO'
   }
else:
   script_map = {'Roman (English)': 'EN'}
script = st.selectbox('Select Script', list(script_map.keys()), index=0)


# Get selected stotra details
selected_index = stotra_options.index(selected_stotra)
stotra_code = df.iloc[selected_index]['Code']
name_roman = df.iloc[selected_index]['Name (Roman)']
if lang_code != 'EN':
   name_orig = df.iloc[selected_index]['Name (Original)']

# Display combined title
st.divider()
if lang_code != 'EN':
    st.markdown(f"<div class='stotra-title'>{name_roman} / {name_orig}</div>", 
            unsafe_allow_html=True)
else:
    st.markdown(f"<div class='stotra-title'>{name_roman}</div>", 
            unsafe_allow_html=True)


# Construct file path
file_suffix = script_map[script]
file_path = f"Scripts/{lang_code}/{stotra_code}-{file_suffix}.txt"

# Display content
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    st.text(content)
else:
    st.error("File not found. Please check the file structure.")
st.divider()

st.markdown('<div style="margin-top: 16px;">Check out Sahajayoga Bhajan Sangraha for getting lyrics of Bhajans:</div>', unsafe_allow_html=True)
st.link_button("Sahajayoga Bhajan Sangraha", "https://sahajayogabhajansangraha.streamlit.app/", type="primary")
common_message()
