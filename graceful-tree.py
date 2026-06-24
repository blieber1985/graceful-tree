import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Graceful Tree Puzzle")

st.markdown("""
Assign the odd numbers **1, 3, 5, 7, 9** to the nodes.

**Goal:** Make every edge difference unique.
""")

# -----------------------------
# Tree Structure
# -----------------------------

edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E")
]

nodes = ["A", "B", "C", "D", "E"]
available_labels = [1, 3, 5, 7, 9]

# -----------------------------
# Layout
# -----------------------------

graph_col, control_col = st.columns([3, 1])

# -----------------------------
# Controls
# -----------------------------

labels = {}

with control_col:

    st.subheader("Node Labels")

    for node in nodes:
        labels[node] = st.selectbox(
            f"Node {node}",
            available_labels,
            key=node
        )

# -----------------------------
# Edge Differences
# -----------------------------

edge_labels = {}

for u, v in edges:
    edge_labels[(u, v)] = abs(labels[u] - labels[v])

# Detect duplicate edge values
edge_values = list(edge_labels.values())
duplicates = {
    value
    for value in edge_values
    if edge_values.count(value) > 1
}

# -----------------------------
# Build Graph
# -----------------------------

G = nx.Graph()
G.add_edges_from(edges)

pos = {
    "A": (0, 1),
    "B": (-0.5, 0),
    "C": (0.5, 0),
    "D": (-1, -1),
    "E": (0, -1)
}

display_labels = {}

for node in nodes:
    display_labels[node] = f"{node}\n{labels[node]}"

# -----------------------------
# Draw Graph
# -----------------------------

with graph_col:

    fig, ax = plt.subplots(figsize=(7, 6))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=3500,
        ax=ax
    )

    nx.draw_networkx_edges(
        G,
        pos,
        width=2,
        ax=ax
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels=display_labels,
        font_size=12,
        ax=ax
    )

    # Draw edge labels individually so duplicates can be red
    for edge, value in edge_labels.items():

        color = "red" if value in duplicates else "black"

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={edge: value},
            font_color=color,
            font_size=12,
            ax=ax
        )

    ax.set_axis_off()

    st.pyplot(fig)

# -----------------------------
# Results
# -----------------------------

st.subheader("Edge Differences")

for (u, v), value in edge_labels.items():

    if value in duplicates:
        st.write(f"🔴 {u}-{v}: {value}")
    else:
        st.write(f"⚫ {u}-{v}: {value}")

# -----------------------------
# Check Solution
# -----------------------------

unique_node_labels = len(set(labels.values())) == len(nodes)
unique_edge_labels = len(set(edge_values)) == len(edge_values)

if not unique_node_labels:
    st.error("Each node must have a different odd number.")

elif unique_edge_labels:
    st.success("🎉 Graceful labeling found!")
    st.balloons()

    st.write("Edge labels:", sorted(edge_values))

else:
    st.warning("Node labels are unique, but some edge differences repeat.")
