from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS
import pandas as pd

# Load graph
g = Graph()
g.parse("The_Listening_Experience_Database.nt", format="nt")

# Namespaces
LED = Namespace("http://led.kmi.open.ac.uk/term/")
EVENT = Namespace("http://purl.org/NET/c4dm/event.owl#")
RO = Namespace("http://www.co-ode.org/roberts/upper.owl#")
SCHEMA = Namespace("http://schema.org/")

records = []

for excerpt in g.subjects(None, None):  
    # Filter alle excerpt URIs
    if "/excerpt/" not in str(excerpt):
        continue

    data = {"uri": str(excerpt)}

    # 1️⃣ Tekst ophalen
    text = None
    for _, _, o in g.triples((excerpt, LED.hasEvidenceText, None)):
        text = str(o)
    if not text:  # fallback: HTML content
        for _, _, o in g.triples((excerpt, None, None)):
            if isinstance(o, Literal) and "<p>" in str(o):
                text = str(o)
    if not text:
        continue
    data["text"] = text

    # 2️⃣ Vind de bijbehorende EXPERIENCE-node
    experience = None
    for exp, _, ex in g.triples((None, LED.hasExcerpt, excerpt)):
        experience = exp
    if not experience:
        continue

    # 3️⃣ Metadata ophalen van EXPERIENCE
    # Agent
    agents = []
    for _, _, agent in g.triples((experience, EVENT.agent, None)):
        label = next((str(o) for _, _, o in g.triples((agent, RDFS.label, None))), str(agent))
        agents.append(label)
    data["agent"] = "; ".join(agents) if agents else None

    # Date
    date = next((str(o) for _, _, o in g.triples((experience, DCTERMS.date, None))), None)
    data["date"] = date

    # Locations
    for loc_pred, col in [
        (RO.has_initial_physical_location, "location_initial"),
        (RO.has_final_physical_location, "location_final"),
    ]:
        loc = next((str(o) for _, _, o in g.triples((experience, loc_pred, None))), None)
        data[col] = loc

    # 4️⃣ Source koppelen via isPartOf
    source_uri = next((str(o) for _, _, o in g.triples((excerpt, DCTERMS.isPartOf, None))), None)
    data["source_uri"] = source_uri

    # 5️⃣ Titel & sourcetype ophalen van Source
    if source_uri:
        title = next((str(o) for _, _, o in g.triples((URIRef(source_uri), DCTERMS.title, None))), None)
        data["source_title"] = title
        
        source_type = next((str(o) for _, _, o in g.triples((URIRef(source_uri), LED.hasSourceType, None))), None)
        data["source_type"] = source_type

    records.append(data)

    if len(records) >= 500:
        break

df = pd.DataFrame(records)
df.to_csv("listening_enriched_FULL.csv", index=False)
print(f"🎉 {len(df)} enriched excerpts opgeslagen!")
