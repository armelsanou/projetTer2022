from Bio import Entrez

Entrez.email = "Your.Name.Here@example.org"
handle = Entrez.elink(db="pubmed", id="26998445", cmd="neighbor_score", rettype="xml")
records = Entrez.read(handle)

scores = sorted(records[0]['LinkSetDb'][0]['Link'], key=lambda k: int(k['Score']))
#show the top 5 results
for i in range(1, 6):
    handle = Entrez.efetch(db="pubmed", id=scores[-i]['Id'], rettype="xml")
    record = Entrez.read(handle)
    print(record)