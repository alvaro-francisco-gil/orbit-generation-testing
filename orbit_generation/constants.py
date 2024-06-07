# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_constants.ipynb.

# %% auto 0
__all__ = ['MU', 'EM_POINTS', 'EM_ORBIT_TYPES', 'orbit_classification', 'ORBIT_CLASS_DF']

# %% ../nbs/00_constants.ipynb 2
import pandas as pd

# %% ../nbs/00_constants.ipynb 3
MU = 0.0122

# %% ../nbs/00_constants.ipynb 4
EM_POINTS={
    'Moon': (1-MU,0,0),
    'Earth': (-MU,0,0),
    'Lagrange 1': (0.8369,0,0),
    'Lagrange 2': (1.1557,0,0),
    'Lagrange 3': (-1.0051,0,0),
    'Lagrange 4': (0.4879,0.8660,0),
    'Lagrange 5': (0.4879,-0.8660,0)
}

# %% ../nbs/00_constants.ipynb 5
EM_ORBIT_TYPES = {
    1: "S_BN",
    2: "S_BS",
    3: "S_DN",
    4: "S_DPO",
    5: "S_DRO",
    6: "S_DS",
    7: "S_L1_A",
    8: "S_L1_HN",
    9: "S_L1_HS",
    10: "S_L1_L",
    11: "S_L1_V",
    12: "S_L2_A",
    13: "S_L2_HN",
    14: "S_L2_HS",
    15: "S_L2_L",
    16: "S_L2_V",
    17: "S_L3_A",
    18: "S_L3_HN",
    19: "S_L3_HS",
    20: "S_L3_L",
    21: "S_L3_V",
    22: "S_L4_A",
    23: "S_L4_LP",
    24: "S_L4_SP",
    25: "S_L4_V",
    26: "S_L5_A",
    27: "S_L5_LP",
    28: "S_L5_SP",
    29: "S_L5_V",
    30: "S_LPOE",
    31: "S_LPOW"
}

# %% ../nbs/00_constants.ipynb 6
orbit_classification = {
    "Id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    "Label": ["S_BN", "S_BS", "S_DN", "S_DPO", "S_DRO", "S_DS", "S_L1_A", "S_L1_HN", "S_L1_HS", "S_L1_L", "S_L1_V", "S_L2_A", "S_L2_HN", "S_L2_HS", "S_L2_L", "S_L2_V", "S_L3_A", "S_L3_HN", "S_L3_HS", "S_L3_L", "S_L3_V", "S_L4_A", "S_L4_LP", "S_L4_SP", "S_L4_V", "S_L5_A", "S_L5_LP", "S_L5_SP", "S_L5_V", "S_LPOE", "S_LPOW", "S_R11", "S_R12", "S_R13", "S_R14", "S_R21", "S_R23", "S_R31", "S_R32", "S_R34", "S_R41", "S_R43"],
    "Type": ["System-wide", "System-wide", "System-wide", "System-wide", "System-wide", "System-wide", "L1", "L1", "L1", "L1", "L1", "L2", "L2", "L2", "L2", "L2", "L3", "L3", "L3", "L3", "L3", "L4", "L4", "L4", "L4", "L5", "L5", "L5", "L5", "System-wide", "System-wide", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant", "Resonant"],
    "Subtype": ["Butterfly", "Butterfly", "Dragonfly", "Distant Prograde", "Distant Retrograde", "Dragonfly", "Axial", "Halo", "Halo", "Lyapunov", "Vertical", "Axial", "Halo", "Halo", "Lyapunov", "Vertical", "Axial", "Halo", "Halo", "Lyapunov", "Vertical", "Axial", "Long Period", "Long Period", "Vertical", "Axial", "Long Period", "Long Period", "Vertical", "Long Period", "Long Period", "Resonant 1,1", "Resonant 1,2", "Resonant 1,3", "Resonant 1,4", "Resonant 2,1", "Resonant 2,3", "Resonant 3,1", "Resonant 3,2", "Resonant 3,4", "Resonant 4,1", "Resonant 4,3"],
    "Direction": ["North", "South", "North", "Planar", "Planar", "South", "No specification", "North", "South", "Planar", "No specification", "No specification", "North", "South", "Planar", "No specification", "No specification", "North", "South", "Planar", "No specification", "No specification", "East", "West", "No specification", "No specification", "North", "South", "No specification", "North", "South", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar", "Planar"]
}

ORBIT_CLASS_DF = pd.DataFrame(orbit_classification)
