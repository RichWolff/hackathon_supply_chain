# %%
import pandas as pd
import tqdm
import numpy as np
from collections import Counter
import random
from collections import defaultdict
import uuid
np.random.seed(42)


# %%
def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]


# %%
# Product Names
product_names = [
    'condor',
    'eagle',
    'goldfinch',
    'raven',
    'hawk',
    'cardinal',
    'falcon',
    'osprey',
    'robin'
]

component_names = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'p'
]

# %%
# Seed fg_components with supplier components and random % of sales, and batch counts
np.random.seed(42)
fg_components = defaultdict(dict)
num_of_batches = 10000
random_pct_sales = constrained_sum_sample_pos(len(product_names), 100)
fg_batches = defaultdict(dict)
for i, product in enumerate(product_names):
    components = sorted(np.random.choice(component_names, np.random.uniform(3, 7, 1).astype(int)[0], replace=False))
    fg_components[product]['components'] = components
    fg_components[product]['pct_of_sales'] = random_pct_sales[i]/100
    fg_components[product]['batch_count'] = fg_components[product]['pct_of_sales'] * num_of_batches
    
    quantities = np.random.normal(200, 11, int(fg_components[product]['batch_count'])).astype(int)
    batch_defects = ((1 - np.random.power(8, 1000)) * 5).astype(int)
    for quantity, defect in zip(quantities, batch_defects):
        uid = str(uuid.uuid1())
        fg_batches[uid]['product'] = product
        fg_batches[uid]['quantity'] = int(quantity)
        fg_batches[uid]['defects'] = int(defect)


# %%
with open('fg_batches.json', 'w') as f:
    json.dump(dict(fg_batches), f, indent=4)


# %%
# Assume 200 units per fg batch
# assume each component generates 1000 units per batch
# for every 5 batches, generate 1 components
component_counts = Counter()
for row in np.array(list(fg_components.items()))[:, 1]:
    for component in row['components']:
        component_counts[component] += int(row['batch_count'] * .2)

print(component_counts)

# %%
# Join a component batch to fg batches
component_lots = defaultdict(dict)
for component, num_of_batches in component_counts.items():
    quantities = np.random.normal(1000, 10, num_of_batches).astype(int)
    for quantity in quantities:
        uid = str(uuid.uuid1())
        component_lots[uid]['component'] = component
        component_lots[uid]['quantity'] = int(quantity)

# %%
with open('component_lots.json', 'w') as f:
    json.dump(dict(component_lots), f, indent=4)
# %%
edges = []
for batch in tqdm.tqdm(list(fg_batches.items())):
    # Get a list of components to match to component batches 
    components = fg_components[batch[1]['product']]['components']
    quantity = batch[1]['quantity']
    
    # loop through each component in product
    for component in components:
        # Get quantity needed for batch
        current_batch_qty = quantity

        # If current_batch_qty > 0 , pull units from a component lot
        while current_batch_qty > 0:
            # Get list of potentail componenet batches
            potential_component_batches = list(filter(lambda x: x[1]['component'] == component, list(component_lots.items())))
            if len(potential_component_batches) == 0:
                uid = str(uuid.uuid1())
                quantity = np.random.normal(1000, 15)
                component_lots[uid]['component'] = component
                component_lots[uid]['quantity'] = int(quantity)
            
                potential_component_batches = list(filter(lambda x: x[1]['component'] == component, list(component_lots.items())))

            take_from = min([
                current_batch_qty,
                int(np.random.normal(25, 3))
            ])

            # Get batch
            compBatch = random.choice(potential_component_batches)
            compLot = component_lots[compBatch[0]]
            compLot['quantity'] -= take_from


            if compLot['quantity'] <= 0:
                component_lots.pop(compBatch[0])

            edges.append((batch[0], compBatch[0], component, take_from))
            current_batch_qty -= take_from

# %%
edges2 = [', '.join([str(e) for e in edge]) + str('\n') for edge in edges]
with open('edges.csv', 'w') as f:
    f.writelines(edges2)

# %%
