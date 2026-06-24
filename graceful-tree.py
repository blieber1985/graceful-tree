import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("Graceful Tree Puzzle")

edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E")
]

nodes = ["A", "B", "C", "D", "E"]
available_labels = [1, 3, 5, 7, 9]

graph_col, control_col = st.columns([3, 1])

labels = {}

with control_col:
    st.subheader("Labels")

    for node in nodes:
        labels[node] = st.selectbox(
            f"Node {node}",
            available_labels,
            key=node
        )

# Build edge labels
edge_labels = {}

for u, v in edges:
    edge_labels[(u, v)] = abs(labels[u] - labels[v])

with graph_col:

    G = nx.Graph()
    G.add_edges_from(edges)

    pos = {
        "A": (0, 1),
        "B": (-0.5, 0),
        "C": (0.5, 0),
        "D": (-1, -1),
        "E": (0, -1)
    }

    fig, ax = plt.subplots(figsize=(6, 5))

    nx.draw(
        G,
        pos,
        ax=ax,
        node_size=2500,
        with_labels=False
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels={n: str(labels[n]) for n in nodes},
        font_size=14,
        ax=ax
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=12,
        ax=ax
    )

    st.pyplot(fig)
