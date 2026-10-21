from rdflib import Graph, Literal
from rdflib.namespace import RDF

bestand = "The_Listening_Experience_Database.nt"
g = Graph()
g.parse(bestand, format="nt")

print("🔎 Predicaten met tekst (eerste 30):")
preds = set()

for s, p, o in g.triples((None, None, None)):
    if isinstance(o, Literal) and len(str(o)) > 40:  # filter korte strings weg
        preds.add(p)
    if len(preds) > 30:
        break

for p in preds:
    print("-", p)


#####################

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

bestand = "The_Listening_Experience_Database.nt"
g = Graph()
g.parse(bestand, format="nt")

BIBO = Namespace("http://purl.org/ontology/bibo/")

print("🔎 Predicaten met tekst voor bibo:Excerpt:")
preds = set()

for s, p, o in g.triples((None, RDF.type, BIBO.Excerpt)):
    for _, p2, o2 in g.triples((s, None, None)):
        if isinstance(o2, Literal) and len(str(o2)) > 40:
            preds.add(p2)

for p in preds:
    print("-", p)


######################

from rdflib import Graph

g = Graph()
g.parse("The_Listening_Experience_Database.nt", format="nt")

# Zoek naar relaties met 'text'
text_predicates = set(p for s,p,o in g if "text" in str(p).lower())
print("Predicaten met mogelijke 'tekst':", text_predicates)

# Zoek naar properties voor agent, work, source
for label in ["agent", "work", "source", "date", "location"]:
    preds = set(p for s,p,o in g if label in str(p).lower())
    print(f"🔎 Predicaten voor {label}:", preds)



######


from rdflib import Graph, Namespace, Literal
import pandas as pd
from rdflib.namespace import RDF, RDFS

# RDF laden
bestand = "The_Listening_Experience_Database.nt"
g = Graph()
print("📥 Dataset inladen...")
g.parse(bestand, format="nt")
print(f"📦 Geladen met {len(g)} triples.\n")

# Namespaces
BIBO = Namespace("http://purl.org/ontology/bibo/")
LED = Namespace("http://led.kmi.open.ac.uk/term/")

TEXT_PREDICATES = {
    LED.has_evidence_text,
    RDFS.label,
    RDF.value
}

print("🔎 Teksten verzamelen...")
records = []

for s, _, _ in g.triples((None, RDF.type, BIBO.Excerpt)):
    text_fragments = []

    for p, o in g.predicate_objects(s):
        if p in TEXT_PREDICATES and isinstance(o, Literal):
            val = str(o).strip()
            if len(val) > 100:  # filter korte labels metadata weg
                text_fragments.append(val)

    if text_fragments:
        combined_text = "\n\n".join(text_fragments)
        records.append({
            "uri": str(s),
            "text": combined_text
        })

    if len(records) >= 1000:
        break

# Dataframe
df = pd.DataFrame(records)

# Exporteren
if not df.empty:
    df.to_csv("listening_experiences_1000.csv", index=False)
    print(f"🎉 Klaar! {len(df)} teksten opgeslagen in 'listening_experiences_1000.csv'")
else:
    print("⚠ Geen teksten gevonden met de gebruikte predicaten.")
