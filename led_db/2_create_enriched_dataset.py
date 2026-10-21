"""
Create an enriched, clean version of the LED dataset with:
- Better column names
- Cleaned data (removed URIs from text fields where possible)
- Additional derived fields
- Proper date formatting
"""

import pandas as pd
import re

print("📥 Loading the full dataset...")
df = pd.read_csv("listening_experiences_FULL.csv")

print(f"📦 Loaded {len(df)} listening experiences\n")

# Create enriched version
df_enriched = pd.DataFrame()

# Experience ID
df_enriched['experience_id'] = df['experience_uri'].str.split('/').str[-1]
df_enriched['experience_uri'] = df['experience_uri']

# LISTENER INFORMATION
df_enriched['listener_name'] = df['listener_name']
df_enriched['listener_gender'] = df['listener_gender']

# Clean birth/death dates
def extract_date(date_uri):
    if pd.isna(date_uri) or date_uri == '':
        return ''
    # Extract date from URI like http://reference.data.gov.uk/id/day/1891-04-27
    match = re.search(r'/day/(\d{4}-\d{2}-\d{2})', str(date_uri))
    if match:
        return match.group(1)
    return ''

df_enriched['listener_birth_date'] = df['listener_birth_date'].apply(extract_date)
df_enriched['listener_death_date'] = df['listener_death_date'].apply(extract_date)

# Clean nationality and places
def extract_label(uri):
    if pd.isna(uri) or uri == '':
        return ''
    # Extract last part of URI
    return str(uri).split('/')[-1].replace('_', ' ')

df_enriched['listener_nationality'] = df['listener_nationality'].apply(extract_label)
df_enriched['listener_birth_place'] = df['listener_birth_place'].apply(extract_label)
df_enriched['listener_death_place'] = df['listener_death_place'].apply(extract_label)

# Clean occupations
def clean_occupations(occ_str):
    if pd.isna(occ_str) or occ_str == '':
        return ''
    # Extract labels from URIs
    occupations = str(occ_str).split(';')
    cleaned = [o.strip().split('/')[-1].replace('_', ' ') for o in occupations]
    return '; '.join(cleaned)

df_enriched['listener_occupations'] = df['listener_occupations'].apply(clean_occupations)
df_enriched['listener_religion'] = df['listener_religion'].apply(extract_label)
df_enriched['listener_social_status'] = df['listener_social_status'].apply(extract_label)

# MUSIC INFORMATION
df_enriched['music_title'] = df['music_title']
df_enriched['composer_name'] = df['composer_name']
df_enriched['music_genre'] = df['music_genre']
df_enriched['performers'] = df['performers']
df_enriched['instruments'] = df['instruments']

# LOCATION INFORMATION
df_enriched['place_name'] = df['place_name']
df_enriched['place_description'] = df['place_description']

# TIME INFORMATION
df_enriched['date'] = df['time_label']

# Extract year for analysis
def extract_year(time_label):
    if pd.isna(time_label) or time_label == '':
        return None
    # Try to extract 4-digit year
    match = re.search(r'\b(1\d{3}|20\d{2})\b', str(time_label))
    if match:
        return int(match.group(1))
    return None

df_enriched['year'] = df['time_label'].apply(extract_year)

# ENVIRONMENT & MEDIUM
def clean_environment(env_str):
    if pd.isna(env_str) or env_str == '':
        return ''
    # Remove prefix, just keep the category
    parts = str(env_str).split(';')
    cleaned = [p.strip().replace('ListeningEnvironment.', '') for p in parts]
    return '; '.join(cleaned)

def clean_medium(med_str):
    if pd.isna(med_str) or med_str == '':
        return ''
    return str(med_str).replace('Medium.', '').strip()

df_enriched['environment'] = df['environment'].apply(clean_environment)
df_enriched['medium'] = df['medium'].apply(clean_medium)

# EVIDENCE TEXT & SOURCE
df_enriched['evidence_text'] = df['evidence_text']

# Calculate text length
df_enriched['evidence_text_length'] = df['evidence_text'].str.len().fillna(0).astype(int)

df_enriched['source_title'] = df['parent_source_title']
df_enriched['source_author'] = df['parent_source_author'].apply(extract_label)
df_enriched['source_publisher'] = df['parent_source_publisher']
df_enriched['source_type'] = df['parent_source_type']
df_enriched['source_pages'] = df['source_pages']
df_enriched['source_language'] = df['source_language'].str.split(':').str[-1]

# METADATA
df_enriched['date_submitted'] = pd.to_datetime(df['date_submitted'], errors='coerce')
df_enriched['date_approved'] = pd.to_datetime(df['date_approved'], errors='coerce')
df_enriched['comment'] = df['comment']

# Create binary flags for analysis
df_enriched['has_listener'] = (df['listener_name'].notna() & (df['listener_name'] != '')).astype(int)
df_enriched['has_music'] = (df['music_title'].notna() & (df['music_title'] != '')).astype(int)
df_enriched['has_composer'] = (df['composer_name'].notna() & (df['composer_name'] != '')).astype(int)
df_enriched['has_place'] = (df['place_name'].notna() & (df['place_name'] != '')).astype(int)
df_enriched['has_date'] = (df['time_label'].notna() & (df['time_label'] != '')).astype(int)
df_enriched['has_evidence_text'] = (df['evidence_text'].notna() & (df['evidence_text'] != '')).astype(int)

# Save enriched version
output_file = "listening_enriched_FULL.csv"
df_enriched.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ Saved enriched dataset to: {output_file}")
print(f"\n📊 Dataset Statistics:")
print(f"   Total experiences: {len(df_enriched)}")
print(f"   Unique listeners: {df_enriched['listener_name'].nunique()}")
print(f"   Unique compositions: {df_enriched['music_title'].nunique()}")
print(f"   Unique composers: {df_enriched['composer_name'].nunique()}")
print(f"   Unique places: {df_enriched['place_name'].nunique()}")
print(f"   Year range: {df_enriched['year'].min():.0f} - {df_enriched['year'].max():.0f}" if df_enriched['year'].notna().any() else "   Year range: N/A")
print(f"\n📋 Completeness:")
print(f"   With listener info: {df_enriched['has_listener'].sum()} ({df_enriched['has_listener'].sum()/len(df_enriched)*100:.1f}%)")
print(f"   With music info: {df_enriched['has_music'].sum()} ({df_enriched['has_music'].sum()/len(df_enriched)*100:.1f}%)")
print(f"   With composer info: {df_enriched['has_composer'].sum()} ({df_enriched['has_composer'].sum()/len(df_enriched)*100:.1f}%)")
print(f"   With place info: {df_enriched['has_place'].sum()} ({df_enriched['has_place'].sum()/len(df_enriched)*100:.1f}%)")
print(f"   With date info: {df_enriched['has_date'].sum()} ({df_enriched['has_date'].sum()/len(df_enriched)*100:.1f}%)")
print(f"   With evidence text: {df_enriched['has_evidence_text'].sum()} ({df_enriched['has_evidence_text'].sum()/len(df_enriched)*100:.1f}%)")

print(f"\n📈 Top 10 Listeners by number of experiences:")
print(df_enriched['listener_name'].value_counts().head(10))

print(f"\n📈 Top 10 Composers:")
print(df_enriched['composer_name'].value_counts().head(10))

print(f"\n📈 Top 10 Places:")
print(df_enriched['place_name'].value_counts().head(10))

print(f"\n📈 Environment distribution:")
env_counts = df_enriched['environment'].str.split(';').explode().str.strip().value_counts()
print(env_counts.head(10))

print(f"\n📈 Medium distribution:")
print(df_enriched['medium'].value_counts())

print(f"\n🎯 Sample row:")
sample = df_enriched[df_enriched['has_evidence_text'] == 1].iloc[0]
print(f"\nExperience: {sample['experience_id']}")
print(f"Listener: {sample['listener_name']} ({sample['listener_birth_date']} - {sample['listener_death_date']})")
print(f"Music: {sample['music_title']} by {sample['composer_name']}")
print(f"Location: {sample['place_name']}")
print(f"Date: {sample['date']}")
print(f"Environment: {sample['environment']}")
print(f"Medium: {sample['medium']}")
print(f"Evidence: {sample['evidence_text'][:200]}...")
