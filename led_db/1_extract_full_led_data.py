"""
Extract complete Listening Experience Database with all associated information:
- Experience URI
- Listener (name, birth/death, nationality, etc.)
- Music (title, composer, performer, genre, etc.)
- Location (place name)
- Time (date)
- Evidence text
- Source information
- Environment (indoor/outdoor, public/private, etc.)
- Medium (live/recorded)
"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
import pandas as pd
from datetime import datetime

# Load the RDF data
bestand = "The_Listening_Experience_Database.nt"
g = Graph()
print("📥 Loading Listening Experience Database...")
g.parse(bestand, format="nt")
print(f"📦 Loaded {len(g)} triples.\n")

# Define namespaces
LED = Namespace("http://led.kmi.open.ac.uk/term/")
MO = Namespace("http://purl.org/ontology/mo/")
EVENT = Namespace("http://purl.org/NET/c4dm/event.owl#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DCT = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("http://schema.org/")
DBO = Namespace("http://dbpedia.org/ontology/")

print("🔎 Extracting listening experiences...")

# Get all listening experiences
experiences = list(g.subjects(RDF.type, LED.ListeningExperience))
print(f"Total listening experiences found: {len(experiences)}\n")

records = []

for idx, exp_uri in enumerate(experiences, 1):
    if idx % 1000 == 0:
        print(f"Processing experience {idx}/{len(experiences)}...")
    
    record = {
        'experience_uri': str(exp_uri),
    }
    
    # Basic metadata
    record['date_submitted'] = str(g.value(exp_uri, DCT.dateSubmitted) or '')
    record['date_approved'] = str(g.value(exp_uri, DCT.dateApproved) or '')
    record['comment'] = str(g.value(exp_uri, RDFS.comment) or '')
    record['pages'] = str(g.value(exp_uri, LED.pages) or '')
    
    # LISTENER INFORMATION
    agent_uri = g.value(exp_uri, EVENT.agent)
    if agent_uri:
        record['listener_uri'] = str(agent_uri)
        record['listener_name'] = str(g.value(agent_uri, RDFS.label) or '')
        record['listener_given_name'] = str(g.value(agent_uri, FOAF.givenName) or '')
        record['listener_family_name'] = str(g.value(agent_uri, FOAF.familyName) or '')
        record['listener_gender'] = str(g.value(agent_uri, FOAF.gender) or '')
        record['listener_birth_date'] = str(g.value(agent_uri, SCHEMA.birthDate) or '')
        record['listener_death_date'] = str(g.value(agent_uri, SCHEMA.deathDate) or '')
        record['listener_birth_place'] = str(g.value(agent_uri, SCHEMA.birthPlace) or '')
        record['listener_death_place'] = str(g.value(agent_uri, SCHEMA.deathPlace) or '')
        record['listener_nationality'] = str(g.value(agent_uri, SCHEMA.nationality) or '')
        
        # Get all occupations
        occupations = [str(o) for o in g.objects(agent_uri, DBO.occupation)]
        record['listener_occupations'] = '; '.join(occupations)
        
        record['listener_religion'] = str(g.value(agent_uri, DBO.religion) or '')
        record['listener_social_status'] = str(g.value(agent_uri, LED.has_social_status) or '')
    else:
        record['listener_uri'] = ''
        record['listener_name'] = ''
        record['listener_given_name'] = ''
        record['listener_family_name'] = ''
        record['listener_gender'] = ''
        record['listener_birth_date'] = ''
        record['listener_death_date'] = ''
        record['listener_birth_place'] = ''
        record['listener_death_place'] = ''
        record['listener_nationality'] = ''
        record['listener_occupations'] = ''
        record['listener_religion'] = ''
        record['listener_social_status'] = ''
    
    # MUSIC/PERFORMANCE INFORMATION
    performance_uri = g.value(exp_uri, DCT.subject)
    if performance_uri:
        record['performance_uri'] = str(performance_uri)
        
        # Get musical work information
        musical_expression = g.value(performance_uri, MO.performance_of)
        if musical_expression:
            record['music_uri'] = str(musical_expression)
            record['music_title'] = str(g.value(musical_expression, RDFS.label) or '')
            
            # Composer
            composer_uri = g.value(musical_expression, MO.composer)
            if composer_uri:
                record['composer_uri'] = str(composer_uri)
                record['composer_name'] = str(g.value(composer_uri, RDFS.label) or '')
            else:
                record['composer_uri'] = ''
                record['composer_name'] = ''
            
            # Genre
            genre_uri = g.value(musical_expression, MO.genre)
            if genre_uri:
                record['music_genre'] = str(g.value(genre_uri, RDFS.label) or str(genre_uri))
            else:
                record['music_genre'] = ''
        else:
            record['music_uri'] = ''
            record['music_title'] = ''
            record['composer_uri'] = ''
            record['composer_name'] = ''
            record['music_genre'] = ''
        
        # Performers
        performers = [str(g.value(p, RDFS.label) or p) for p in g.objects(performance_uri, MO.performer)]
        record['performers'] = '; '.join(performers)
        
        # Instruments
        instruments = [str(g.value(i, RDFS.label) or i) for i in g.objects(performance_uri, MO.instrument)]
        record['instruments'] = '; '.join(instruments)
    else:
        record['performance_uri'] = ''
        record['music_uri'] = ''
        record['music_title'] = ''
        record['composer_uri'] = ''
        record['composer_name'] = ''
        record['music_genre'] = ''
        record['performers'] = ''
        record['instruments'] = ''
    
    # LOCATION INFORMATION
    place_uri = g.value(exp_uri, EVENT.place)
    if place_uri:
        record['place_uri'] = str(place_uri)
        record['place_name'] = str(g.value(place_uri, RDFS.label) or '')
        record['place_description'] = str(g.value(place_uri, DCT.description) or '')
    else:
        record['place_uri'] = ''
        record['place_name'] = ''
        record['place_description'] = ''
    
    # TIME INFORMATION
    time_uri = g.value(exp_uri, EVENT.time)
    if time_uri:
        record['time_uri'] = str(time_uri)
        record['time_label'] = str(g.value(time_uri, RDFS.label) or '')
        record['date'] = str(g.value(exp_uri, DCT.date) or '')
    else:
        record['time_uri'] = ''
        record['time_label'] = ''
        record['date'] = ''
    
    # ENVIRONMENT & MEDIUM
    environments = [str(env).split('/')[-1] for env in g.objects(exp_uri, LED.has_environment)]
    record['environment'] = '; '.join(environments)
    
    mediums = [str(med).split('/')[-1] for med in g.objects(exp_uri, LED.has_medium)]
    record['medium'] = '; '.join(mediums)
    
    # SOURCE/EVIDENCE INFORMATION
    source_uri = g.value(exp_uri, LED.is_reported_in)
    if source_uri:
        record['source_uri'] = str(source_uri)
        record['source_label'] = str(g.value(source_uri, RDFS.label) or '')
        record['source_pages'] = str(g.value(source_uri, BIBO.pages) or '')
        record['source_language'] = str(g.value(source_uri, DCT.language) or '')
        
        # Get the evidence text
        evidence_text = g.value(source_uri, RDF.value)
        if evidence_text:
            # Clean HTML tags if present
            text_str = str(evidence_text)
            # Simple HTML tag removal
            import re
            text_str = re.sub('<[^<]+?>', '', text_str)
            record['evidence_text'] = text_str.strip()
        else:
            record['evidence_text'] = ''
        
        # Get parent source information
        parent_source = g.value(source_uri, DCT.isPartOf)
        if parent_source:
            record['parent_source_uri'] = str(parent_source)
            record['parent_source_title'] = str(g.value(parent_source, DCT.title) or '')
            record['parent_source_author'] = str(g.value(parent_source, SCHEMA.author) or '')
            record['parent_source_publisher'] = str(g.value(parent_source, DCT.publisher) or '')
            record['parent_source_date'] = str(g.value(parent_source, DCT.date) or '')
            
            # Get source type (Book, Article, etc.)
            source_types = [str(t).split('/')[-1] for s, p, t in g.triples((parent_source, RDF.type, None))]
            record['parent_source_type'] = '; '.join([t for t in source_types if 'bibo' in str(t).lower() or 'Article' in t or 'Book' in t])
        else:
            record['parent_source_uri'] = ''
            record['parent_source_title'] = ''
            record['parent_source_author'] = ''
            record['parent_source_publisher'] = ''
            record['parent_source_date'] = ''
            record['parent_source_type'] = ''
    else:
        record['source_uri'] = ''
        record['source_label'] = ''
        record['source_pages'] = ''
        record['source_language'] = ''
        record['evidence_text'] = ''
        record['parent_source_uri'] = ''
        record['parent_source_title'] = ''
        record['parent_source_author'] = ''
        record['parent_source_publisher'] = ''
        record['parent_source_date'] = ''
        record['parent_source_type'] = ''
    
    records.append(record)

# Create DataFrame
print("\n📊 Creating DataFrame...")
df = pd.DataFrame(records)

# Save to CSV
output_file = "listening_experiences_FULL.csv"
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n🎉 Complete! Extracted {len(df)} listening experiences")
print(f"📁 Saved to: {output_file}")
print(f"\n📋 Columns included:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print(f"\n📈 Summary statistics:")
print(f"  - Total experiences: {len(df)}")
print(f"  - With listener info: {df['listener_name'].notna().sum()}")
print(f"  - With music info: {df['music_title'].notna().sum()}")
print(f"  - With location info: {df['place_name'].notna().sum()}")
print(f"  - With time info: {df['time_label'].notna().sum()}")
print(f"  - With evidence text: {df['evidence_text'].notna().sum()}")
