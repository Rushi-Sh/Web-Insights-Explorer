import streamlit as st
import re
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content
)
from LLM import get_ai_response

# Page config
st.set_page_config(
    page_title="WebInsight Explorer",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        color: #1E88E5;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 500 !important;
        color: #424242;
        margin-bottom: 1rem !important;
    }
    .url-input {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with icon
st.markdown("<h1 class='main-header'>🔍 AI Web Scraper</h1>", unsafe_allow_html=True)

# Create two columns for the description
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<p style='font-size: 1.2em; color: #666;'>Extract and analyze web content intelligently using AI</p>", 
                unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align: right;'><span style='background-color: #E3F2FD; padding: 5px 10px; border-radius: 15px; color: #1E88E5;'>Beta Version</span></div>", 
                unsafe_allow_html=True)

# URL input section
st.markdown("<h2 class='subheader'>📝 Enter Website URL</h2>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='url-input'>", unsafe_allow_html=True)
    url_pattern = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    url = st.text_input("", 
                        placeholder="https://example.com",
                        help="Enter the complete URL including http:// or https://")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        scrape_button = st.button("🚀 Start Scraping", use_container_width=True)

# Processing section
if scrape_button:
    if re.match(url_pattern, url):
        with st.spinner("🔄 Scraping website content..."):
            try:
                result = scrape_website(url)
                body = extract_body_content(result)
                cleaned_content = clean_body_content(body)
                st.session_state.dom_content = cleaned_content
                st.success("✅ Website content scraped successfully!")
            except Exception as e:
                st.error(f"❌ Error occurred while scraping: {str(e)}")
    else:
        st.error("❌ Invalid URL. Please enter a valid website URL.")

# Analysis section
if "dom_content" in st.session_state:
    st.markdown("""---""")
    st.markdown("<h2 class='subheader'>🔍 Analyze Content</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style='background-color: #f8f9fa; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
        """, unsafe_allow_html=True)
        
        parse_description = st.text_area(
            "What would you like to find?",
            placeholder="Example: Find all product prices and their descriptions",
            help="Describe what information you want to extract from the website",
            height=100
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            analyze_button = st.button("🔍 Analyze Content", use_container_width=True)

        if analyze_button and parse_description:
            with st.spinner("🤖 AI is analyzing the content..."):
                try:
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = get_ai_response(parse_description, dom_chunks)
                    
                    # Display results in a nice format
                    st.markdown("""
                    <div style='background-color: white; border-radius: 10px; padding: 20px; margin-top: 20px; border: 1px solid #e0e0e0;'>
                        <h3 style='color: #1E88E5; margin-bottom: 15px;'>📊 Analysis Results</h3>
                    """, unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

# Footer
st.markdown("""---""")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Made with ❤️ by Rushi Shah</p>
    </div>
""", unsafe_allow_html=True)