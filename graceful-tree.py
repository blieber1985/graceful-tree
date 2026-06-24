import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide")

st.title("Graceful Tree Puzzle")

# ----------------------------
# Initialize state
# ----------------------------

if "labels" not in st.session_state:
    st.session_state.labels = {
        "A": None,
        "B": None,
        "C": None,
        "D": None,
        "E": None,
    }

if "selected_node" not in st.session_state:
    st.session_state.selected_node = None

# ----------------------------
# Tree structure
# ----------------------------

tree_edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E"),
]

# ----------------------------
# Build edge labels
# ----------------------------

edge_values = []

for u, v in tree_edges:
    lu = st.session_state.labels[u]
    lv = st.session_state.labels[v]

    if lu is not None and lv is not None:
        edge_values.append(abs(lu - lv))

duplicates = set()

for val in edge_values:
    if edge_values.count(val) > 1:
        duplicates.add(val)

# ----------------------------
# Build graph
# ----------------------------

nodes = []

for node in ["A", "B", "C", "D", "E"]:

    label = st.session_state.labels[node]

    if label is None:
        text = node
    else:
        text = str(label)

    nodes.append(
        Node(
            id=node,
            label=text,
            size=30,
        )
    )

edges = []

for u, v in tree_edges:

    lu = st.session_state.labels[u]
    lv = st.session_state.labels[v]

    edge_label = ""

    color = "gray"

    if lu is not None and lv is not None:

        diff = abs(lu - lv)
        edge_label = str(diff)

        if diff in duplicates:
            color = "red"

    edges.append(
        Edge(
            source=u,
            target=v,
            label=edge_label,
            color=color,
        )
    )

config = Config(
    width=900,
    height=600,
    directed=False,
    physics=False,
    hierarchical=True,
)

selected = agraph(
    nodes=nodes,
    edges=edges,
    config=config,
)

# ----------------------------
# Node clicked
# ----------------------------

if selected:
    st.session_state.selected_node = selected

# ----------------------------
# Label assignment
# ----------------------------

if st.session_state.selected_node:

    node = st.session_state.selected_node

    st.subheader(f"Selected Node: {node}")

    current = st.session_state.labels[node]

    available = [1, 3, 5, 7, 9]

    choice = st.selectbox(
        "Assign Label",
        available,
        index=0 if current is None else available.index(current),
    )

    if st.button("Apply Label"):
        st.session_state.labels[node] = choice
        st.rerun()

# ----------------------------
# Check solution
# ----------------------------

labels = list(st.session_state.labels.values())

if None not in labels:

    unique_nodes = len(set(labels)) == 5

    edge_values = []

    for u, v in tree_edges:
        edge_values.append(
            abs(
                st.session_state.labels[u]
                - st.session_state.labels[v]
            )
        )

    unique_edges = len(set(edge_values)) == len(edge_values)

    if unique_nodes and unique_edges:
        st.balloons()
        st.success("Graceful labeling found!")
