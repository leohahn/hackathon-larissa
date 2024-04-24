import pandas as pd
import pydot

df = pd.read_csv("Baseparateste.csv", delimiter=";")

todas_pastas = set()
todas_conexoes = {}

def normalizar_pasta(f):
    if pd.isnull(f):
        return None
    return f.replace("\\", "_").replace(":", "")

for _, row in df.iterrows():
    nome = row["Nome"]
    id = row["ID"]
    origem = normalizar_pasta(row["PastaOrigem"])
    destino = normalizar_pasta(row["PastaDestino"])
    backup = normalizar_pasta(row["PastaBackup"])

    for f in [origem, destino, backup]:
        if pd.isnull(f) or f.strip() == "":
            continue
        todas_pastas.add(f)

    for p in [destino, backup]:
        if pd.isnull(p) or p.strip() == "":
            continue

        if origem not in todas_conexoes:
            todas_conexoes[origem] = set()

        todas_conexoes[origem].add((p, nome))

grafico = pydot.Dot(graph_type='digraph', bgcolor="white")

# Add nodes
for pasta in todas_pastas:
    node = pydot.Node(pasta, label=pasta)
    grafico.add_node(node)

# Add edges
for orig, conex in todas_conexoes.items():
    for c in conex:
        grafico.add_edge(pydot.Edge(orig, c[0], color="blue", label=c[1]))

grafico.write_png("resultado.png")
