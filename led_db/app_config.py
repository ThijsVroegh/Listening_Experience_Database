"""
Configuration file for the Listening Experience Database Explorer

This file contains all configurable settings for the Streamlit app.
Modify these values to customize the app behavior.
"""

# ============================================================================
# FILE PATHS
# ============================================================================

DATA_FILE = "data/listening_enriched_FULL.csv"

# ============================================================================
# APP SETTINGS
# ============================================================================

APP_TITLE = "🎵 Listening Experience Database Explorer"
APP_ICON = "🎵"
APP_LAYOUT = "wide"  # "centered" or "wide"
SIDEBAR_STATE = "expanded"  # "expanded" or "collapsed"

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================

# Maximum text length to display before truncating (set to None for no limit)
MAX_TEXT_LENGTH = None

# Number of experiences to show per page (for future pagination feature)
EXPERIENCES_PER_PAGE = 1

# Show debug information
DEBUG_MODE = False

# ============================================================================
# FILTER DEFAULTS
# ============================================================================

# Default filter values
DEFAULT_ONLY_WITH_TEXT = True  # Start with only text-containing experiences
DEFAULT_YEAR_MIN = 1377  # Will be overridden by actual data min
DEFAULT_YEAR_MAX = 2034  # Will be overridden by actual data max

# ============================================================================
# CACHE SETTINGS
# ============================================================================

# Time to live for cached data (in seconds)
# Set to None to cache indefinitely
CACHE_TTL = None

# ============================================================================
# UI CUSTOMIZATION
# ============================================================================

# Color scheme (for future theming)
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#f0f2f6"

# Text display styling
TEXT_BOX_STYLE = """
    background-color: #f0f2f6; 
    padding: 20px; 
    border-radius: 10px; 
    border-left: 5px solid #1f77b4; 
    margin: 10px 0;
"""

# ============================================================================
# COLUMN DISPLAY NAMES
# ============================================================================

# Map internal column names to display names
COLUMN_DISPLAY_NAMES = {
    'experience_id': 'Experience ID',
    'listener_name': 'Listener',
    'listener_gender': 'Gender',
    'listener_birth_date': 'Born',
    'listener_death_date': 'Died',
    'listener_nationality': 'Nationality',
    'listener_religion': 'Religion',
    'music_title': 'Music',
    'composer_name': 'Composer',
    'place_name': 'Place',
    'date': 'Date',
    'evidence_text': 'Description',
    'source_title': 'Source',
}

# ============================================================================
# FILTER OPTIONS
# ============================================================================

# Which filters to show in the sidebar
ENABLED_FILTERS = {
    'only_with_text': True,
    'year_range': True,
    'listener': True,
    'gender': True,
    'religion': True,
    'composer': True,
    'place': True,
    'environment': True,
    'medium': True,
}

# Predefined filter options
ENVIRONMENT_OPTIONS = ["All", "Indoor", "Outdoor", "Public", "Domestic", "Solitary", "Accompanied"]
MEDIUM_OPTIONS = ["All", "Live", "Playback", "Broadcast"]

# ============================================================================
# STATISTICS
# ============================================================================

# Which statistics to show at the top
ENABLED_STATISTICS = {
    'total_experiences': True,
    'with_descriptions': True,
    'unique_listeners': True,
    'unique_composers': True,
}

# ============================================================================
# EXPORT SETTINGS (for future export feature)
# ============================================================================

EXPORT_FORMATS = ['CSV', 'JSON', 'Excel']
DEFAULT_EXPORT_FORMAT = 'CSV'

# ============================================================================
# SEARCH SETTINGS (for future search feature)
# ============================================================================

# Enable full-text search
ENABLE_SEARCH = False

# Minimum search query length
MIN_SEARCH_LENGTH = 3

# ============================================================================
# ADVANCED FEATURES (for future development)
# ============================================================================

# Enable visualization features
ENABLE_VISUALIZATIONS = False

# Enable comparison mode
ENABLE_COMPARISON = False

# Enable bookmarking
ENABLE_BOOKMARKS = False

# Enable annotations
ENABLE_ANNOTATIONS = False
