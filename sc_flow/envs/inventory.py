import gymnasium as gym
from dataclasses import dataclass
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class Item:
    '''Object for tracking items in an inventory system'''
    id: int
    unit_manufacturing_cost: float
    unit_retail_price: float
    quantity: int

@dataclass
class Store:
    id: int 
    lat: float
    long: float
    cap: int
    items: List[int]
    inv: List[int]

@dataclass
class DC:
    id: int
    lat: float
    long: float
    cap: int
    

def generate_random_items(
        rng, 
        n_items, 
        umc_gamma_shape=2, 
        umc_gamma_scale=0.5,
        urp_gamma_shape=6,
        urp_gamma_scale=6
    ):

    '''

    '''

    ids = rng.choice(np.arange(start=1000000, stop=9999999), size=n_items, replace=False)
    umcs = rng.gamma(shape=umc_gamma_shape, scale=umc_gamma_scale, size=n_items).round(decimals=2)
    urps = rng.gamma(shape=urp_gamma_shape, scale=urp_gamma_scale, size=n_items).round(decimals=2)

    return [Item(ids[i], umcs[i], urps[i]) 
            for i in range(n_items)]

def generate_random_stores(
        rng, 
        n_stores,
        items,
        min_lat=38.591114,
        max_lat=41.343825,
        min_long=-84.858398,
        max_long=-80.485840,
        mean_item_ratio = 0.75,
        std_item_ratio = 0.1,
        mean_cap = 3000,
        std_cap = 1500
    ):
    '''

    '''

    ids = rng.choice(np.arange(start=100000, stop=999999), size=n_stores, replace=False)
    lats = rng.uniform(low=min_lat, high=max_lat, size=n_stores).round(decimals=6)
    longs = rng.uniform(low=min_long, high=max_long, size=n_stores).round(decimals=6)
    caps = rng.normal(loc=mean_cap, scale=std_cap, size=n_stores).round(decimals=0).astype(int)
    
    # List of all items
    item_master_list = [item.id for item in items]
    # Number of all items
    n_items_master = len(item_master_list)
    # Ratio of items in each store
    item_ratios = rng.normal(loc=mean_item_ratio, scale=std_item_ratio, size=n_stores).clip(min=0.25, max=1.0)
    # Number of items in each store
    n_items_store = [int(round(ratio*n_items_master, 0)) for ratio in item_ratios]
    store_item_ids = [list(rng.choice(item_master_list, size=n_items)) for n_items in n_items_store]
    # Item inventory in each store
    store_inv = [[0]*len(items) for items in store_item_ids]
    # Iterate through each store, adding 10 to the inventory of a single,
    # randomly selected item, until the total store inventory is greater
    # than the store capacity
    for s in range(n_stores):
        cap = caps[s]
        n_items = n_items_store[s]
        total_inv = 0
        while total_inv < cap:
            store_inv[s][rng.integers(low=0, high=n_items)] += 10
            total_inv += 10
            
            

    return [Store(ids[i], lats[i], longs[i], caps[i], store_item_ids[i], store_inv[i])
            for i in range(n_stores)]

class Inventory(gym.env):
    '''
    '''
    def __init__(self, n_items, n_stores, n_dcs):
        self.graph = nx.Graph()
        self.graph.add_nodes_from([0]) # Demand
        self.graph.add_nodes_from([1],)