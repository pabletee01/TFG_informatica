import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from app.logger import logger

def generate_graph_png(node_csv, edge_csv, output_path="graph_output.png"):

    # Loading nodes (Implementation pending)
    df_nodes = pd.read_csv(node_csv)
    labels = dict(zip(df_nodes["Id"], df_nodes["Label"]))
    sizes = dict(zip(df_nodes["Id"], df_nodes["Size"]))
    
    # Creating graph and adding nodes
    G = nx.DiGraph()
    G.add_nodes_from(df_nodes["Id"])
    
    # Adding edges
    df_edges = pd.read_csv(edge_csv)
    G.add_edges_from(zip(df_edges["Source"], df_edges["Target"]))

    # Calculating layout for nodes
    # pos = nx.spring_layout(G, k=0.15, iterations=50)
    pos = nx.kamada_kawai_layout(G, scale=15)

    # Get sizes with fallback
    node_sizes = [sizes.get(n, 10) * 10 for n in G.nodes()] 

    # Draw
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos,
            with_labels=False,
            node_size=node_sizes,
            arrows=True,
            edge_color="gray",
            node_color="skyblue",
            linewidths=0.5)

    # Drawing labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=6)

    plt.title("habitat", fontsize=16)
    # plt.tight_layout()
    plt.savefig(output_path, format="png", dpi=300)
    
    plt.close()
    logger.info("PNG generated")
