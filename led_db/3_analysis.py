import pandas as pd
df = pd.read_csv('data/listening_enriched_FULL.csv')
print(df.head())

# Count experiences with non-empty evidence_text
described = df['evidence_text'].notna() & (df['evidence_text'].str.strip() != '')
num_with_description = described.sum()
num_without_description = len(df) - num_with_description

print(f"Total experiences: {len(df)}")
print(f"Experiences with a description: {num_with_description}")
print(f"Experiences with empty or missing description: {num_without_description}")


# Filter complete records
complete = df[(df['has_listener'] == 1) & 
              (df['has_music'] == 1) & 
              (df['has_evidence_text'] == 1)]

print(complete.head())

complete.columns
complete.evidence_text

# Example: Find Beethoven listening experiences
beethoven = df[df['composer_name'].str.contains('Beethoven', na=False)]
print(beethoven[['listener_name', 'music_title', 'date', 'place_name']])

