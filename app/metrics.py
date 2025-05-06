import networkx as nx
import pandas as pd
import os
from app.logger import logger

def analyze_network(arrow_df, node_df):
    G = nx.DiGraph()

    # Reading nodes of the graph
    for _, row in node_df.iterrows():
        G.add_node(row["Id"], label=row["Label"], size=row.get("Size", 1))

    # Reading edges of the graph
    for _, row in arrow_df.iterrows():
        G.add_edge(row["Source"], row["Target"])

    S = G.number_of_nodes()
    L = G.number_of_edges()
    
    # Calculating connectance
    C = L / (S * S) if S > 0 else 0
    
    # Calculating average degree of the nodes of the graph
    avg_degree = sum(dict(G.degree()).values()) / S if S > 0 else 0
    
    # Calculating the number of isolated components of the graph
    components = nx.number_weakly_connected_components(G)
    
    # Calculating longest path length of the graph (If there are any acyclic components)
    longest_path = nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else "Cyclic"

    return {
        "Nodes": S,
        "Links": L,
        "Connectance": round(C, 4),
        "Average degree": round(avg_degree, 2),
        "Connected components": components,
        "Longest path": longest_path
    }

def save_metrics(metrics, output_path):
    df = pd.DataFrame([metrics])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Metrics file generated")
