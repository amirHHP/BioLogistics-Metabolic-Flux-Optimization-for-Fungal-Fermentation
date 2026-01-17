import numpy as np
from scipy.optimize import linprog

def solve_bio_logistics():
    """
    A Toy Model demonstrating Metabolic Flux Analysis using Linear Programming.
    
    CONCEPT:
    We treat the fungal cell as a 'Factory'.
    - Input Logistics: Glucose (Sugar) and Oxygen.
    - Production Line: Metabolic reactions converting inputs to energy.
    - Output Target: Biomass (Growth).
    
    MATHEMATICS:
    Maximize Z = c * v
    Subject to S * v = 0 (Steady State Constraint)
    Subject to LB <= v <= UB (Capacity Constraints)
    """

    # --- 1. Define the 'Production Line' (The Reactions) ---
    # We have 5 logical steps in our supply chain (Fluxes v0 to v4):
    # v0: Import Glucose (Supply In)
    # v1: Import Oxygen (Supply In)
    # v2: Metabolism (Process: Glucose + Oxygen -> Energy + Building Blocks)
    # v3: Growth (Manufacturing: Energy + Blocks -> Biomass)
    # v4: Waste Secretion (CO2 output)
    
    reaction_names = ["v0_Glucose_In", "v1_Oxygen_In", "v2_Metabolism", "v3_Growth", "v4_Waste_CO2"]

    # --- 2. Define the 'Hubs' (The Metabolites) ---
    # These are the internal storage nodes where resources are held temporarily.
    # Row 0: Internal Glucose
    # Row 1: Internal Oxygen
    # Row 2: Energy (ATP)
    # Row 3: Building Blocks (Precursors)
    
    # --- 3. The Stoichiometric Matrix (S) ---
    # This acts as the 'Routing Map'. 
    # Positive (+) means production/arrival at a hub.
    # Negative (-) means consumption/departure from a hub.
    
    # Rows = Metabolites (4 internal hubs)
    # Cols = Reactions (5 supply chain steps)
    
    S = np.array([
        # v0,  v1,  v2,  v3,  v4
        [ 1,   0,  -1,   0,   0],  # Internal Glucose balance
        [ 0,   1,  -1,   0,   0],  # Internal Oxygen balance
        [ 0,   0,   2,  -1,   0],  # Energy Balance (1 unit metab -> 2 energy units)
        [ 0,   0,   1,  -1,   0]   # Building Block Balance
    ])

    # --- 4. Define Constraints (Capacity Limits) ---
    # In logistics, trucks have max capacity. In cells, enzymes have max rates.
    
    # Bounds for each reaction (Min Flux, Max Flux)
    # We limit Glucose intake to simulate a specific environment (e.g., specific tank conditions)
    bounds = [
        (0, 10),    # v0: Max Glucose intake = 10 units/hr
        (0, 100),   # v1: Oxygen is abundant
        (0, 1000),  # v2: Internal metabolism is fast
        (0, 1000),  # v3: Growth capability
        (0, 1000)   # v4: Waste removal
    ]

    # --- 5. Define Objective (KPI) ---
    # Our Goal: Maximize v3 (Growth).
    # Note: linprog minimizes by default, so we use a negative coefficient for v3 to maximize it.
    c = [0, 0, 0, -1, 0] 

    # --- 6. The Optimization Engine (Solver) ---
    print("running optimization algorithm...")
    result = linprog(c, A_eq=S, b_eq=np.zeros(4), bounds=bounds, method='highs')

    # --- 7. Reporting Results ---
    if result.success:
        print("\n--- OPTIMAL FLUX DISTRIBUTION FOUND ---")
        print(f"Objective (Max Growth Rate): {round(result.x[3] * -1, 4)} units/hr") # Multiply by -1 to reverse minimization
        print("\nLogistics Breakdown:")
        for name, flux in zip(reaction_names, result.x):
            print(f"  {name}: {round(flux, 4)}")
            
        print("\nAnalysis:")
        print("To achieve maximum growth, the system automatically routed resources")
        print("efficiently through v2 to satisfy the demand at v3.")
    else:
        print("Optimization failed.")

if __name__ == "__main__":
    solve_bio_logistics()
