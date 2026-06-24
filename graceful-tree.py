import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")

st.title("Graceful Tree Puzzle (Randomized)")

st.markdown("""
Assign the odd numbers **1, 3, 5, 7, 9** to the nodes.

**Goal:** Make every edge difference unique.
""")

# -----------------------------
# Session State Initialization
# -----------------------------

nodes = ["A", "B", "C", "D", "E"]
available_labels = [1, 3, 5, 7, 9]

if "labels" not in st.session_state:
    st.session_state.labels = {n: available_labels[0] for n in nodes}

if "edges" not in st.session_state:
    st.session_state.edges = []

# -----------------------------
# Random Tree Generator
# -----------------------------

def generate_random_tree(node_list):
    """Generate a random tree using Prüfer-like attachment."""
    nodes = node_list[:]
    random.shuffle(nodes)

    edges = []
    connected = [nodes[0]]

    for n in nodes[1:]:
        attach_to = random.choice(connected)
        edges.append((attach_to, n))
        connected.append(n)

    return edges

# -----------------------------
# New Puzzle Button
# -----------------------------

if st.button("🔄 New Puzzle"):
    st.session_state.edges = generate_random_tree(nodes)
    st.rerun()

# Generate initial tree if empty
if not st.session_state.edges:
    st.session_state.edges = generate_random_tree(nodes)

edges = st.session_state.edges

# -----------------------------
# Layout
# -----------------------------

graph_col, control_col = st.columns([2, 1])

# -----------------------------
# Controls
# -----------------------------

with control_col:
    st.subheader("Node Labels")

    for node in nodes:
        st.session_state.labels[node] = st.selectbox(
            f"Node {node}",
            available_labels,
            key=node,
        )

# -----------------------------
# Edge Values
# -----------------------------

edge_labels = {}

for u, v in edges:
    edge_labels[(u, v)] = abs(
        st.session_state.labels[u] - st.session_state.labels[v]
    )

edge_values = list(edge_labels.values())

duplicates = {
    val for val in edge_values
    if edge_values.count(val) > 1
}

# -----------------------------
# Build Graph
# -----------------------------

G = nx.Graph()
G.add_edges_from(edges)

# Compact layout (works for random trees)
pos = nx.spring_layout(G, seed=42)

display_labels = {
    n: f"{n}\n{st.session_state.labels[n]}"
    for n in nodes
}

# -----------------------------
# Draw Graph
# -----------------------------

with graph_col:

    fig, ax = plt.subplots(figsize=(4.5, 4))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2200,
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
        font_size=10,
        ax=ax
    )

    for (u, v), val in edge_labels.items():
        color = "red" if val in duplicates else "black"

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): val},
            font_color=color,
            font_size=10,
            ax=ax
        )

    ax.set_axis_off()
    st.pyplot(fig, use_container_width=False)

# -----------------------------
# Results
# -----------------------------

st.subheader("Edge Differences")

for (u, v), val in edge_labels.items():
    if val in duplicates:
        st.write(f"🔴 {u}-{v}: {val}")
    else:
        st.write(f"⚫ {u}-{v}: {val}")

# -----------------------------
# Win Check
# -----------------------------

node_ok = len(set(st.session_state.labels.values())) == 5
edge_ok = len(set(edge_values)) == len(edge_values)

if not node_ok:
    st.error("Each node must have a different odd number.")

elif edge_ok:
    st.success("🎉 Graceful labeling found!")
    st.balloons()

else:
    st.warning("Node labels are unique, but edge differences repeat.")
