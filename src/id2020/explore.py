# %%
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib


# %%
edges = pd.read_csv('edges.csv', names=['fg_batch', 'component_batch', 'component', 'quantity'])
edges.head()

fg_batches = pd.read_json('fg_batches.json').T
component_batches = pd.read_json('component_lots.json').T


# %%
G = nx.Graph()
G.add_nodes_from(fg_batches.to_dict(orient='index').items(), label='fg_batch')
G.add_nodes_from(component_batches.to_dict(orient='index').items(), label='component_batch')

edge_vals = edges.groupby(['fg_batch', 'component_batch'], as_index=False)['quantity'].sum().values
G.add_edges_from([(u, v, {'quantiy': d}) for u,v,d in edge_vals], label='component_supplies')


# %% 
subnodes = set(['027887e6-0ccb-11eb-9794-ac675dc8de75'])
subnodes.update(list(G.neighbors('027887e6-0ccb-11eb-9794-ac675dc8de75')))

for node in list(subnodes):
    subnodes.update(list(G.neighbors(node)))
sub = G.subgraph(subnodes)
colors = ['blue' if data['label'] == 'fg_batch' else 'red' for n,data in sub.nodes(data=True)]


# %%
nx.draw(sub, node_color=colors, node_size=2, dpi=300, figsize=(15,15))
# %%
