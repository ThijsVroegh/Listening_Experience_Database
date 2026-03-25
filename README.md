# Listening Experience Database (LED) - Complete Extraction

This folder contains scripts and data for extracting the complete Listening Experience Database from the Open University.

## 📊 Dataset Overview

The Listening Experience Database collects data about people's experiences of listening to music throughout history and literature. The complete dataset contains **12,380 listening experiences** with rich metadata about:

- **Listeners**: Who listened to the music (biographical information)
- **Music**: What was listened to (title, composer, genre, performers)
- **Location**: Where the listening took place
- **Time**: When it happened
- **Evidence**: Original text describing the experience
- **Context**: Environment (indoor/outdoor, public/private) and medium (live/recorded)

## 📁 Files in this Folder

### Source Data
**`data/The_Listening_Experience_Database.nt`**
   - Original RDF N-Triples file (621,679 triples)
   - Downloaded from https://ordo.open.ac.uk/articles/dataset/The_Listening_Experience_Database/29890823

### Scripts
**`0_explore_led_structure.py`**
   - Exploratory script to understand data structure
   - Shows sample experiences and relationships
 
**`1_extract_full_led_data.py`**
   - Main extraction script
   - Extracts all listening experiences with complete metadata
   - Uses RDFlib to parse the .nt file
   - Generates `data/listening_experiences_FULL.csv`

**`2_create_enriched_dataset.py`**
   - Post-processing script
   - Cleans and enriches the full dataset
   - Converts URIs to readable labels
   - Adds derived fields and statistics
   - Generates `data/listening_enriched_FULL.csv`

**`3_analysis.py`**
   - Example analysis script
   - Demonstrates how to load and analyze the enriched dataset
   - Provides sample queries and statistics

### Data Files
**`data/listening_experiences_FULL.csv`** (12,380 rows × 47 columns)
   - Complete extraction with all URIs and raw data
   - Contains all relationships and metadata
   - Best for detailed analysis and linking back to source

**`data/listening_enriched_FULL.csv`** (12,380 rows × ~40 columns)
   - Cleaned and enriched version
   - Human-readable data (URIs converted to labels)
   - Better column names
   - Additional derived fields (year, text length, flags)
   - **Recommended for most analyses**

## 📈 Dataset Statistics

### Completeness
- **93.3%** have listener information
- **83.2%** have music information
- **43.7%** have composer information
- **89.9%** have place information
- **96.4%** have date information
- **67.6%** have evidence text
- **13.1%** have time of day information
- **40.4%** have religious affiliation/worldview information

### Coverage
- **1,629** unique listeners
- **5,632** unique compositions
- **994** unique composers
- **2,793** unique places
- **Time span**: 1377 - 2034 (some future dates may be data errors)

### Top Listeners
1. Sergey Prokofiev (758 experiences)
2. Ned Rorem (597)
3. Benjamin Britten (495)
4. Ignatz Moscheles (402)
5. Henry Croswell (390)

### Top Composers
1. Sergey Prokofiev (263 experiences)
2. George Frideric Handel (234)
3. Ludwig van Beethoven (224)
4. Ned Rorem (209)
5. Richard Wagner (174)

### Top Locations
1. London (881 experiences)
2. Royal Festival Hall (594)
3. Paris (586)
4. London, England (228)
5. New York (211)

## 🔧 How to Use

### Option 1: Use the Pre-Generated CSV Files

Simply open `listening_enriched_FULL.csv` in Excel, Python, R, or your preferred tool:

```python
import pandas as pd
df = pd.read_csv('listening_enriched_FULL.csv')
print(df.head())
```

### Option 2: Re-Extract from Source

If you want to modify the extraction or work with the raw RDF data:

```bash
# Activate virtual environment
.\led_env\Scripts\Activate

# Run extraction
python 1_extract_full_led_data.py

# Create enriched version
python 2_create_enriched_dataset.py
```

## 📋 Column Descriptions

### Enriched Dataset (`listening_enriched_FULL.csv`)

**Experience Information**
- `experience_id`: Unique identifier for the experience
- `experience_uri`: Full URI in the database
- `date_submitted`: When this record was submitted
- `date_approved`: When this record was approved
- `comment`: Additional comments about the experience

**Listener Information**
- `listener_name`: Name of the person who listened
- `listener_gender`: Gender of the listener
- `listener_birth_date`: Birth date (YYYY-MM-DD)
- `listener_death_date`: Death date (YYYY-MM-DD)
- `listener_nationality`: Country of nationality
- `listener_birth_place`: Place of birth
- `listener_death_place`: Place of death
- `listener_occupations`: Occupation(s), separated by semicolons
- `listener_religion`: Religious affiliation
- `listener_social_status`: Social status

**Music Information**
- `music_title`: Title of the musical work
- `composer_name`: Name of the composer
- `music_genre`: Genre of the music
- `performers`: Performer(s), separated by semicolons
- `instruments`: Instrument(s) used, separated by semicolons

**Location & Time**
- `place_name`: Name of the place where listening occurred
- `place_description`: Description of the location
- `date`: Date when the listening occurred (human-readable)
- `year`: Extracted year (for analysis)
- `time_of_day`: Time of day when listening occurred (13.1% of experiences have this)

**Context**
- `environment`: Type of environment (e.g., "Indoor; Public; Accompanied")
- `medium`: How the music was delivered (e.g., "Live", "Broadcast", "Playback")

**Evidence & Source**
- `evidence_text`: Original text describing the listening experience
- `evidence_text_length`: Length of the evidence text
- `source_title`: Title of the source document
- `source_author`: Author of the source
- `source_publisher`: Publisher
- `source_type`: Type of source (Book, Article, etc.)
- `source_pages`: Page numbers
- `source_language`: Language code

**Flags (for filtering/analysis)**
- `has_listener`: 1 if listener info exists, 0 otherwise
- `has_music`: 1 if music info exists, 0 otherwise
- `has_composer`: 1 if composer info exists, 0 otherwise
- `has_place`: 1 if place info exists, 0 otherwise
- `has_date`: 1 if date info exists, 0 otherwise
- `has_evidence_text`: 1 if evidence text exists, 0 otherwise

## 🔍 Example Analyses

### Find all experiences by a specific listener
```python
df = pd.read_csv('listening_enriched_FULL.csv')
prokofiev = df[df['listener_name'] == 'Sergey Prokofiev']
print(prokofiev[['date', 'music_title', 'composer_name', 'place_name']])
```

### Find experiences in a specific location
```python
london = df[df['place_name'].str.contains('London', na=False)]
```

### Analyze listening environments
```python
environment_counts = df['environment'].str.split(';').explode().str.strip().value_counts()
print(environment_counts)
```

### Filter by time period
```python
early_20th_century = df[(df['year'] >= 1900) & (df['year'] < 1950)]
```

### Find experiences with evidence text
```python
with_text = df[df['has_evidence_text'] == 1]
print(with_text[['listener_name', 'music_title', 'evidence_text']].head())
```

## 📚 Resources

### Data Source
- **Dataset**: https://ordo.open.ac.uk/articles/dataset/The_Listening_Experience_Database/29890823
- **SPARQL Endpoint**: https://data.open.ac.uk/query
- **Project Website**: https://research-archive.stem.open.ac.uk/led/

### Documentation
- **LED Ontology**: http://led.kmi.open.ac.uk/term/
- **Open University Linked Data**: https://data.open.ac.uk/
- **Example Queries**: https://data.open.ac.uk/queries

### Key Namespaces Used
- `led:` http://led.kmi.open.ac.uk/term/
- `event:` http://purl.org/NET/c4dm/event.owl#
- `mo:` http://purl.org/ontology/mo/ (Music Ontology)
- `bibo:` http://purl.org/ontology/bibo/ (Bibliographic Ontology)
- `foaf:` http://xmlns.com/foaf/0.1/ (Friend of a Friend)
- `dct:` http://purl.org/dc/terms/ (Dublin Core Terms)
- `schema:` http://schema.org/

## 📝 Citation

If you use this data in research, please cite:

Brown, S., Barlow, H., Adamou, A. and d'Aquin, M. (2015) 'The Listening Experience Database Project: Collating the Responses of the 'Ordinary Listener' to Prompt New Insights into Musical Experience', The International Journal of the Humanities: Annual Review, 13, pp. 17-32.

## ⚖️ License

The Listening Experience Database is licensed under **Attribution-NonCommercial-ShareAlike 4.0 International** (CC BY-NC-SA 4.0).

## 🛠️ Technical Requirements

- Python 3.x
- pandas
- rdflib

Install via:
```bash
pip install pandas rdflib
```

## 💡 Tips

1. **For most analyses, use `listening_enriched_FULL.csv`** - it's cleaner and more readable
2. **Use the flags** (`has_listener`, `has_music`, etc.) to filter complete records
3. **The `evidence_text` field** contains the actual historical descriptions - very rich for qualitative analysis
4. **Some dates may be approximate** - the database includes various date formats and precisions
5. **Environment is multi-valued** - use `str.split(';')` to analyze individual environment types

## 🔮 Future Enhancements

Possible extensions to this extraction:
- Sentiment analysis of evidence texts
- Geographic visualization of listening locations
- Network analysis of listener-composer-location relationships

## 📧 Contact

For questions about the data extraction scripts: See this workspace
For questions about the LED project: http://led.kmi.open.ac.uk/
For questions about Open University Linked Data: https://data.open.ac.uk/contact
