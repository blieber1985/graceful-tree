import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("Graceful Tree Puzzle")

# Tree structure
edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E")
]

nodes = ["A", "B", "C", "D", "E"]
available_labels = [1, 3, 5, 7, 9]

st.header("Assign labels")

labels = {}

for node in nodes:
    labels[node] = st.selectbox(
        f"Label for {node}",
        available_labels,
        key=node
    )

# Check uniqueness of node labels
node_labels_unique = len(set(labels.values())) == len(nodes)

# Draw graph
G = nx.Graph()
G.add_edges_from(edges)

pos = {
    "A": (0, 1),
    "B": (-0.5, 0),
    "C": (0.5, 0),
    "D": (-1, -1),
    "E": (0, -1)
}

fig, ax = plt.subplots()

nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=False,
    node_size=2000,
)

nx.draw_networkx_labels(
    G,
    pos,
    labels={n: str(labels[n]) for n in nodes},
    ax=ax,
)

st.pyplot(fig)

# Compute edge differences
st.header("Edge Differences")

edge_diffs = []

for u, v in edges:
    diff = abs(labels[u] - labels[v])
    edge_diffs.append(diff)
    st.write(f"{u}-{v}: {diff}")

# Winning condition
if node_labels_unique:
    if len(set(edge_diffs)) == len(edge_diffs):
        st.success("You found a graceful labeling!")
    else:
        st.warning("Node labels are unique, but edge labels repeat.")
else:
    st.error("Each node must have a different odd number.")
