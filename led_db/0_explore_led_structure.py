from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
import pandas as pd

# Load the RDF data
g = Graph()
print("📥 Loading dataset...")
g.parse("The_Listening_Experience_Database.nt", format="nt")
print(f"📦 Loaded {len(g)} triples.\n")

# Define namespaces
LED = Namespace("http://led.kmi.open.ac.uk/term/")
MO = Namespace("http://purl.org/ontology/mo/")
EVENT = Namespace("http://purl.org/NET/c4dm/event.owl#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DCT = Namespace("http://purl.org/dc/terms/")

# Find a sample listening experience
print("🔎 Finding sample listening experience...")
experiences = list(g.subjects(RDF.type, LED.ListeningExperience))
print(f"Total listening experiences: {len(experiences)}\n")

if experiences:
    sample_exp = experiences[0]
    print(f"Sample experience URI: {sample_exp}\n")
    print("Properties of this experience:")
    for p, o in g.predicate_objects(sample_exp):
        print(f"  {p} -> {o}")
    
    print("\n" + "="*80 + "\n")
    
    # Check for event:agent (listener)
    agent = g.value(sample_exp, EVENT.agent)
    if agent:
        print(f"Listener: {agent}")
        for p, o in g.predicate_objects(agent):
            print(f"  {p} -> {o}")
    
    print("\n" + "="*80 + "\n")
    
    # Check for music performance
    performance = g.value(sample_exp, MO.performance_of)
    if performance:
        print(f"Performance: {performance}")
        for p, o in g.predicate_objects(performance):
            print(f"  {p} -> {o}")
    
    print("\n" + "="*80 + "\n")
    
    # Check for location
    location = g.value(sample_exp, EVENT.place)
    if location:
        print(f"Location: {location}")
        for p, o in g.predicate_objects(location):
            print(f"  {p} -> {o}")
    
    print("\n" + "="*80 + "\n")
    
    # Check for time
    time = g.value(sample_exp, EVENT.time)
    if time:
        print(f"Time: {time}")
        for p, o in g.predicate_objects(time):
            print(f"  {p} -> {o}")
    
    print("\n" + "="*80 + "\n")
    
    # Check for source (bibo:Excerpt)
    source = g.value(sample_exp, LED.is_reported_in)
    if source:
        print(f"Source: {source}")
        for p, o in g.predicate_objects(source):
            print(f"  {p} -> {o}")
