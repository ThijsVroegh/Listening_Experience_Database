"""
Listening Experience Database Explorer
A Streamlit app for exploring historical music listening experiences

This app allows users to browse, filter, and analyze listening experiences
from the Listening Experience Database (LED).
"""

import streamlit as st
import pandas as pd
from typing import Optional
import numpy as np


# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_FILE = "data/listening_enriched_FULL.csv"
APP_TITLE = "🎵 Listening Experience Database Explorer"
APP_ICON = "🎵"


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Load the listening experience database.
    
    Returns:
        pd.DataFrame: The complete listening experience dataset
    """
    df = pd.read_csv(DATA_FILE)
    
    # Convert date columns to datetime for better filtering
    df['date_submitted'] = pd.to_datetime(df['date_submitted'], errors='coerce')
    df['date_approved'] = pd.to_datetime(df['date_approved'], errors='coerce')
    
    return df


# ============================================================================
# FILTERING FUNCTIONS
# ============================================================================

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Apply user-selected filters to the dataframe.
    
    Args:
        df: The complete dataframe
        filters: Dictionary of filter parameters
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()
    
    # Filter by year range (include records with missing years)
    if filters.get('year_range'):
        year_min, year_max = filters['year_range']
        filtered_df = filtered_df[
            (filtered_df['year'].isna()) |  # Include records without a year
            ((filtered_df['year'] >= year_min) & (filtered_df['year'] <= year_max))
        ]
    
    # Filter by listener
    if filters.get('listener') and filters['listener'] != "All":
        filtered_df = filtered_df[filtered_df['listener_name'] == filters['listener']]
    
    # Filter by composer
    if filters.get('composer') and filters['composer'] != "All":
        filtered_df = filtered_df[filtered_df['composer_name'] == filters['composer']]
    
    # Filter by place
    if filters.get('place') and filters['place'] != "All":
        filtered_df = filtered_df[filtered_df['place_name'] == filters['place']]
    
    # Filter by environment
    if filters.get('environment') and filters['environment'] != "All":
        filtered_df = filtered_df[
            filtered_df['environment'].str.contains(filters['environment'], na=False)
        ]
    
    # Filter by medium
    if filters.get('medium') and filters['medium'] != "All":
        filtered_df = filtered_df[
            filtered_df['medium'].str.contains(filters['medium'], na=False)
        ]
    
    # Filter by gender
    if filters.get('gender') and filters['gender'] != "All":
        filtered_df = filtered_df[filtered_df['listener_gender'] == filters['gender']]
    
    # Filter by religion
    if filters.get('religion') and filters['religion'] != "All":
        filtered_df = filtered_df[
            filtered_df['listener_religion'].str.contains(filters['religion'], na=False)
        ]
    
    # Only show records with evidence text
    if filters.get('only_with_text'):
        filtered_df = filtered_df[filtered_df['has_evidence_text'] == 1]
    
    return filtered_df


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar_filters(df: pd.DataFrame) -> dict:
    """
    Render the sidebar with all filter options.
    
    Args:
        df: The complete dataframe
        
    Returns:
        dict: Dictionary of selected filter values
    """
    st.sidebar.header("📊 Filter Options")
    
    filters = {}
    
    # Only show records with text
    filters['only_with_text'] = st.sidebar.checkbox(
        "Only show experiences with descriptions",
        value=True,
        help="Filter to only show records that have evidence text"
    )
    
    # Year range filter
    st.sidebar.subheader("📅 Time Period")
    year_min = int(df['year'].min())
    year_max = int(df['year'].max())
    filters['year_range'] = st.sidebar.slider(
        "Year range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        help="Filter experiences by year"
    )
    
    # Listener filter
    st.sidebar.subheader("👤 Listener")
    listeners = ["All"] + sorted(df['listener_name'].dropna().unique().tolist())
    filters['listener'] = st.sidebar.selectbox(
        "Select listener",
        options=listeners,
        help="Filter by specific listener"
    )
    
    # Gender filter
    genders = ["All"] + sorted(df['listener_gender'].dropna().unique().tolist())
    filters['gender'] = st.sidebar.selectbox(
        "Listener gender",
        options=genders
    )
    
    # Religion filter
    religions = ["All"] + sorted(df['listener_religion'].dropna().unique().tolist())
    filters['religion'] = st.sidebar.selectbox(
        "Listener religion/worldview",
        options=religions
    )
    
    # Composer filter
    st.sidebar.subheader("🎼 Music")
    composers = ["All"] + sorted(df['composer_name'].dropna().unique().tolist())
    filters['composer'] = st.sidebar.selectbox(
        "Select composer",
        options=composers,
        help="Filter by composer"
    )
    
    # Location filter
    st.sidebar.subheader("📍 Location")
    places = ["All"] + sorted(df['place_name'].dropna().unique().tolist())
    filters['place'] = st.sidebar.selectbox(
        "Select place",
        options=places,
        help="Filter by location"
    )
    
    # Environment filter
    st.sidebar.subheader("🏛️ Context")
    environments = ["All", "Indoor", "Outdoor", "Public", "Domestic", "Solitary", "Accompanied"]
    filters['environment'] = st.sidebar.selectbox(
        "Environment",
        options=environments,
        help="Filter by listening environment"
    )
    
    # Medium filter
    mediums = ["All", "Live", "Playback", "Broadcast"]
    filters['medium'] = st.sidebar.selectbox(
        "Medium",
        options=mediums,
        help="Filter by how music was delivered"
    )
    
    return filters


def render_experience_card(row: pd.Series, index: int, total: int):
    """
    Render a detailed card for a single listening experience.
    
    Args:
        row: The dataframe row containing the experience data
        index: Current index (1-based)
        total: Total number of experiences
    """
    st.markdown(f"### Experience {index} of {total}")
    
    # Create columns for metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👤 Listener**")
        st.write(row['listener_name'] if pd.notna(row['listener_name']) else "Unknown")
        if pd.notna(row['listener_birth_date']) or pd.notna(row['listener_death_date']):
            birth = row['listener_birth_date'] if pd.notna(row['listener_birth_date']) else "?"
            death = row['listener_death_date'] if pd.notna(row['listener_death_date']) else "?"
            st.caption(f"({birth} - {death})")
        if pd.notna(row['listener_gender']):
            st.caption(f"Gender: {row['listener_gender']}")
        if pd.notna(row['listener_nationality']):
            st.caption(f"Nationality: {row['listener_nationality']}")
        if pd.notna(row['listener_occupations']):
            st.caption(f"Occupation: {row['listener_occupations']}")
        if pd.notna(row['listener_religion']):
            st.caption(f"Religion: {row['listener_religion']}")
    
    with col2:
        st.markdown("**🎵 Music**")
        st.write(row['music_title'] if pd.notna(row['music_title']) else "Unknown")
        if pd.notna(row['composer_name']):
            st.caption(f"Composer: {row['composer_name']}")
        if pd.notna(row['performers']):
            st.caption(f"Performers: {row['performers']}")
        if pd.notna(row['instruments']):
            st.caption(f"Instruments: {row['instruments']}")
        if pd.notna(row['music_genre']):
            st.caption(f"Genre: {row['music_genre']}")
    
    with col3:
        st.markdown("**📍 When & Where**")
        if pd.notna(row['date']):
            st.write(f"📅 {row['date']}")
        if pd.notna(row['time_of_day']):
            st.caption(f"🕐 {row['time_of_day']}")
        if pd.notna(row['place_name']):
            st.write(f"📍 {row['place_name']}")
        if pd.notna(row['environment']):
            st.caption(f"Environment: {row['environment']}")
        if pd.notna(row['medium']):
            st.caption(f"Medium: {row['medium']}")
    
    # Evidence text
    st.markdown("---")
    st.markdown("**📝 Listening Experience Description**")
    
    if pd.notna(row['evidence_text']) and row['evidence_text'].strip():
        # Display the evidence text in a nice box with dark text
        st.markdown(
            f"""<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; 
            border-left: 5px solid #1f77b4; margin: 10px 0; color: #000000;">
            {row['evidence_text']}
            </div>""",
            unsafe_allow_html=True
        )
        st.caption(f"Text length: {row['evidence_text_length']} characters")
    else:
        st.info("📭 No description available for this experience")
    
    # Source information
    with st.expander("📚 Source Information"):
        if pd.notna(row['source_title']):
            st.write(f"**Title:** {row['source_title']}")
        if pd.notna(row['source_author']):
            st.write(f"**Author:** {row['source_author']}")
        if pd.notna(row['source_publisher']):
            st.write(f"**Publisher:** {row['source_publisher']}")
        if pd.notna(row['source_pages']):
            st.write(f"**Pages:** {row['source_pages']}")
        if pd.notna(row['source_language']):
            st.write(f"**Language:** {row['source_language']}")
        if pd.notna(row['source_type']):
            st.write(f"**Type:** {row['source_type']}")
    
    # Additional metadata
    with st.expander("ℹ️ Additional Information"):
        st.write(f"**Experience ID:** {row['experience_id']}")
        if pd.notna(row['date_submitted']):
            st.write(f"**Date Submitted:** {row['date_submitted']}")
        if pd.notna(row['date_approved']):
            st.write(f"**Date Approved:** {row['date_approved']}")
        if pd.notna(row['comment']) and row['comment'].strip():
            st.write(f"**Comments:** {row['comment']}")
        if pd.notna(row['experience_uri']):
            st.write(f"**URI:** {row['experience_uri']}")


def render_statistics(df: pd.DataFrame):
    """
    Render statistics about the filtered dataset.
    
    Args:
        df: The filtered dataframe
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Experiences", len(df))
    
    with col2:
        st.metric("With Descriptions", df['has_evidence_text'].sum())
    
    with col3:
        st.metric("Unique Listeners", df['listener_name'].nunique())
    
    with col4:
        st.metric("Unique Composers", df['composer_name'].nunique())


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="LED Explorer",
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title
    st.title(APP_TITLE)
    st.markdown("""
    Explore over 12,000 documented experiences of listening to music throughout history.
    Use the sidebar to filter by time period, listener, composer, location, and more.
    """)
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {DATA_FILE}")
        st.info("Please ensure the data file is in the correct location.")
        return
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return
    
    # Render filters in sidebar
    filters = render_sidebar_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Show statistics
    render_statistics(filtered_df)
    
    # Check if we have results
    if len(filtered_df) == 0:
        st.warning("⚠️ No experiences match the selected filters. Try adjusting your criteria.")
        return
    
    st.markdown("---")
    
    # Initialize session state for navigation
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    
    # Ensure current_index is within bounds
    if st.session_state.current_index >= len(filtered_df):
        st.session_state.current_index = 0
    
    # Navigation controls
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮️ First", use_container_width=True):
            st.session_state.current_index = 0
    
    with col2:
        if st.button("◀️ Previous", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
    
    with col3:
        # Jump to specific experience
        selected_index = st.selectbox(
            "Jump to experience:",
            options=range(len(filtered_df)),
            index=st.session_state.current_index,
            format_func=lambda x: f"Experience {x+1} of {len(filtered_df)}"
        )
        if selected_index != st.session_state.current_index:
            st.session_state.current_index = selected_index
    
    with col4:
        if st.button("Next ▶️", use_container_width=True):
            if st.session_state.current_index < len(filtered_df) - 1:
                st.session_state.current_index += 1
    
    with col5:
        if st.button("Last ⏭️", use_container_width=True):
            st.session_state.current_index = len(filtered_df) - 1
    
    # Display current experience
    st.markdown("---")
    current_row = filtered_df.iloc[st.session_state.current_index]
    render_experience_card(
        current_row, 
        st.session_state.current_index + 1, 
        len(filtered_df)
    )
    
    # Footer
    st.markdown("---")
    st.caption("""
    **About this database:** The Listening Experience Database (LED) contains documented 
    experiences of listening to music throughout history, drawn from diaries, letters, 
    memoirs, and other historical sources.
    """)


if __name__ == "__main__":
    main()
