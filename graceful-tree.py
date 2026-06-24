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
# Basic Setup
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
    nodes = node_list[:]
    random.shuffle(nodes)

    edges = []
    connected = [nodes[0]]

    for n in nodes[1:]:
        attach = random.choice(connected)
        edges.append((attach, n))
        connected.append(n)

    return edges

# -----------------------------
# New Puzzle Button
# -----------------------------

if st.button("🔄 New Puzzle"):
    st.session_state.edges = generate_random_tree(nodes)
    st.rerun()

if not st.session_state.edges:
    st.session_state.edges = generate_random_tree(nodes)

edges = st.session_state.edges

# -----------------------------
# Layout
# -----------------------------

graph_col, control_col = st.columns([2, 1])

# -----------------------------
# Controls (right side)
# -----------------------------

with control_col:
    st.subheader("Node Labels")

    for node in nodes:
        st.session_state.labels[node] = st.selectbox(
            f"Node {node}",
            available_labels,
            key=node
        )

# -----------------------------
# Edge calculations
# -----------------------------

edge_labels = {}

for u, v in edges:
    edge_labels[(u, v)] = abs(
        st.session_state.labels[u] - st.session_state.labels[v]
    )

edge_values = list(edge_labels.values())

duplicates = {
    v for v in edge_values
    if edge_values.count(v) > 1
}

# -----------------------------
# Graph layout (fixed + contained)
# -----------------------------

G = nx.Graph()
G.add_edges_from(edges)

pos = nx.spring_layout(G, seed=42, scale=0.8)

# shrink inward so nothing hits border
for k in pos:
    x, y = pos[k]
    pos[k] = (x * 0.9, y * 0.9)

display_labels = {
    n: f"{n}\n{st.session_state.labels[n]}"
    for n in nodes
}

# -----------------------------
# Draw graph (small + contained)
# -----------------------------

with graph_col:

    fig, ax = plt.subplots(figsize=(3.8, 3.5))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2000,
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
        font_size=9,
        ax=ax
    )

    for (u, v), val in edge_labels.items():
        color = "red" if val in duplicates else "black"

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): val},
            font_color=color,
            font_size=9,
            ax=ax
        )

    ax.set_axis_off()
    ax.margins(0.15)
    plt.tight_layout()

    st.pyplot(fig, use_container_width=False)

# -----------------------------
# Results panel
# -----------------------------

st.subheader("Edge Differences")

for (u, v), val in edge_labels.items():
    if val in duplicates:
        st.write(f"🔴 {u}-{v}: {val}")
    else:
        st.write(f"⚫ {u}-{v}: {val}")

# -----------------------------
# Win condition
# -----------------------------

node_ok = len(set(st.session_state.labels.values())) == 5
edge_ok = len(set(edge_values)) == len(edge_values)

if not node_ok:
    st.error("Each node must have a different odd number.")

elif edge_ok:
    st.success("🎉 Graceful labeling found!")
    st.balloons()

else:
    st.warning("Node labels are unique, but some edge differences repeat.")
