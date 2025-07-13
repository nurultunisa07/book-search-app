import streamlit as st
import pandas as pd
import json
import os

# Page configuration
st.set_page_config(
    page_title="Books Search App",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 Books to Scrape - Search App")
st.markdown("Search and explore books from Books to Scrape website")

# Load data
@st.cache_data
def load_data():
    try:
        with open('data/books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
        return pd.DataFrame(books)
    except FileNotFoundError:
        st.error("Data file not found. Please run the scraper first.")
        return pd.DataFrame()

# Load the data
df = load_data()

if not df.empty:
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Search by title
    search_query = st.sidebar.text_input("Search by title:", "")
    
    # Filter by category
    categories = ['All'] + sorted(df['category'].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Category:", categories)
    
    # Filter by rating
    ratings = ['All'] + sorted(df['rating'].dropna().unique().tolist())
    selected_rating = st.sidebar.selectbox("Rating:", ratings)
    
    # Filter by availability
    availability_options = ['All'] + sorted(df['availability'].dropna().unique().tolist())
    selected_availability = st.sidebar.selectbox("Availability:", availability_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_query, case=False, na=False)]
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_rating != 'All':
        filtered_df = filtered_df[filtered_df['rating'] == selected_rating]
    
    if selected_availability != 'All':
        filtered_df = filtered_df[filtered_df['availability'] == selected_availability]
    
    # Display results
    st.header(f"📖 Found {len(filtered_df)} books")
    
    # Display books in cards
    for idx, book in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if book['image_url']:
                    st.image(book['image_url'], width=150)
            
            with col2:
                st.subheader(book['title'])
                st.write(f"**Price:** {book['price']}")
                st.write(f"**Category:** {book['category']}")
                st.write(f"**Rating:** {book['rating']}")
                st.write(f"**Availability:** {book['availability']}")
                
                if book['description']:
                    st.write(f"**Description:** {book['description'][:200]}...")
                
                st.write(f"**URL:** [{book['url']}]({book['url']})")
            
            st.divider()
    
    # Statistics
    st.sidebar.header("📊 Statistics")
    st.sidebar.write(f"Total books: {len(df)}")
    st.sidebar.write(f"Filtered books: {len(filtered_df)}")
    st.sidebar.write(f"Categories: {df['category'].nunique()}")
    st.sidebar.write(f"Average rating: {df['rating'].mode().iloc[0] if not df['rating'].empty else 'N/A'}")

else:
    st.error("No data available. Please run the scraper first.")