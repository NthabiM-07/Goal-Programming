

from pulp import LpProblem, LpVariable, LpMinimize, LpStatus

def solve_concrete_mix_problem():
    """
    Concrete Mix Optimization using Pre-emptive Goal Programming
    ----------------------------------------------------------------
    This script determines the optimal quantities of cement, sand, and stone
    for a concrete mix, satisfying multiple goals with different priorities.
    
    Priority 1: Achieve at least 18,000 kg of total mix.
    Priority 2: Keep total cost ≤ R12,000.
    Technical constraints are also enforced.
    """
    print("\n=== Concrete Mix Optimization using Pre-emptive Goal Programming ===")
    print("Author: <Your Name> | For educational and demonstration purposes\n")
    print("Problem: Find optimal cement, sand, and stone mix for concrete,\n"
          "while satisfying prioritized goals and technical constraints.\n")
    print("--- Step 1: Priority 1 (Total mix ≥ 18,000 kg) ---")

    # --- Step 1: Priority 1 (Total mix ≥ 18,000 kg) ---
    model1 = LpProblem(name="Concrete_Mix_Priority1", sense=LpMinimize)

    # Decision variables (amounts in kg)
    xc = LpVariable(name="xc", lowBound=0)  # Cement
    xs = LpVariable(name="xs", lowBound=0)  # Sand
    xt = LpVariable(name="xt", lowBound=0)  # Stone

    # Deviation variables for Priority 1 goal
    d1_minus = LpVariable(name="d1_minus", lowBound=0)  # Underachievement
    d1_plus = LpVariable(name="d1_plus", lowBound=0)    # Overachievement

    # Objective: Minimize underachievement of total mix
    model1 += d1_minus, "Minimize_Underachievement_of_Total_Mix"

    # Goal constraint for Priority 1
    model1 += xc + xs + xt + d1_minus - d1_plus == 18000, "Total_Mix_Goal"

    # Technical constraints
    model1 += xc - 0.21*xs - 0.21*xt >= 0, "Cement_Proportion (≥21%)"
    model1 += xt - 1.3*xs <= 0, "Stone_to_Sand_Ratio (≤1.3)"
    model1 += xs <= 6500, "Sand_Availability (≤6500 kg)"

    # Solve for Priority 1
    model1.solve()

    print(f"Status: {LpStatus[model1.status]}")
    
    if model1.status == 1:  # If the model is optimal
        print("\nOptimal solution for Priority 1:")
        print(f"  Cement (xc):   {xc.value():.2f} kg")
        print(f"  Sand (xs):     {xs.value():.2f} kg")
        print(f"  Stone (xt):    {xt.value():.2f} kg")
        print(f"  Total mix:     {xc.value() + xs.value() + xt.value():.2f} kg")
        print(f"  d1_minus:      {d1_minus.value():.2f}")
        print(f"  d1_plus:       {d1_plus.value():.2f}")
        print(f"  Total cost:    R{1.75*xc.value() + 0.8*xt.value():.2f}")

        # Check if Priority 1 is fully satisfied
        if d1_minus.value() == 0:
            print("  ✔ Priority 1 is fully satisfied!")
        else:
            print("  ✖ Priority 1 cannot be fully satisfied. Using the best possible achievement.")

        # --- Step 2: Priority 2 (Cost ≤ R12,000) ---
        print("\n--- Step 2: Priority 2 (Cost ≤ R12,000) while maintaining Priority 1 achievement ---")

        model2 = LpProblem(name="Concrete_Mix_Priority2", sense=LpMinimize)

        # Decision variables for phase 2
        xc2 = LpVariable(name="xc2", lowBound=0)  # Cement
        xs2 = LpVariable(name="xs2", lowBound=0)  # Sand
        xt2 = LpVariable(name="xt2", lowBound=0)  # Stone

        # Deviation variables for Priority 2 goal
        d2_minus = LpVariable(name="d2_minus", lowBound=0)  # Underachievement of cost goal
        d2_plus = LpVariable(name="d2_plus", lowBound=0)    # Overachievement of cost goal

        # Deviation variables for Priority 1 goal in phase 2
        d1_minus2 = LpVariable(name="d1_minus2", lowBound=0)  # Underachievement of total mix goal
        d1_plus2 = LpVariable(name="d1_plus2", lowBound=0)    # Overachievement of total mix goal

        # Objective: Minimize overachievement of cost
        model2 += d2_plus, "Minimize_Overachievement_of_Cost"

        # Goal constraint for Priority 1 in phase 2
        model2 += xc2 + xs2 + xt2 + d1_minus2 - d1_plus2 == 18000, "Total_Mix_Goal_Phase2"
        model2 += d1_minus2 == d1_minus.value(), "Fix_Priority1_Achievement"

        # Goal constraint for Priority 2
        model2 += 1.75*xc2 + 0.8*xt2 + d2_minus - d2_plus == 12000, "Cost_Goal"

        # Technical constraints
        model2 += xc2 - 0.21*xs2 - 0.21*xt2 >= 0, "Cement_Proportion (≥21%)"
        model2 += xt2 - 1.3*xs2 <= 0, "Stone_to_Sand_Ratio (≤1.3)"
        model2 += xs2 <= 6500, "Sand_Availability (≤6500 kg)"

        # Solve for Priority 2
        model2.solve()

        print(f"Status: {LpStatus[model2.status]}")

        if model2.status == 1:
            print("\nOptimal solution for Priority 2 (final solution):")
            print(f"  Cement (xc):   {xc2.value():.2f} kg")
            print(f"  Sand (xs):     {xs2.value():.2f} kg")
            print(f"  Stone (xt):    {xt2.value():.2f} kg")
            print(f"  Total mix:     {xc2.value() + xs2.value() + xt2.value():.2f} kg")
            print(f"  Total cost:    R{1.75*xc2.value() + 0.8*xt2.value():.2f}")
            print(f"  d1_minus2:     {d1_minus2.value():.2f}")
            print(f"  d1_plus2:      {d1_plus2.value():.2f}")
            print(f"  d2_minus:      {d2_minus.value():.2f}")
            print(f"  d2_plus:       {d2_plus.value():.2f}")

            # Check if Priority 2 is fully satisfied
            if d2_plus.value() == 0:
                print("  ✔ Priority 2 is fully satisfied!")
            else:
                print(f"  ✖ Priority 2 cannot be fully satisfied. Cost exceeds budget by R{d2_plus.value():.2f}")
        else:
            print("✖ Failed to find optimal solution for Priority 2.")
    else:
        print("✖ Failed to find optimal solution for Priority 1.")

    # --- Final Results Summary ---
    print("\n=== Final Recommendation for Concrete Mix ===")
    if model1.status == 1 and ('model2' in locals() and model2.status == 1):
        print(f"  Cement:    {xc2.value():.2f} kg")
        print(f"  Sand:      {xs2.value():.2f} kg")
        print(f"  Stone:     {xt2.value():.2f} kg")
        print(f"  Total mix: {xc2.value() + xs2.value() + xt2.value():.2f} kg")
        print(f"  Total cost: R{1.75*xc2.value() + 0.8*xt2.value():.2f}")

        # Verify constraints
        cement_proportion = xc2.value() / (xs2.value() + xt2.value()) * 100 if (xs2.value() + xt2.value()) > 0 else 0
        stone_sand_ratio = xt2.value() / xs2.value() if xs2.value() > 0 else float('inf')

        print("\n  --- Verification of Constraints ---")
        print(f"  Cement proportion: {cement_proportion:.2f}% (must be ≥ 21%)")
        print(f"  Stone to sand ratio: {stone_sand_ratio:.2f} (must be ≤ 1.3)")
        print(f"  Sand used: {xs2.value():.2f} kg (limit: 6500 kg)")
    else:
        print("  No feasible recommendation found for all priorities.")

if __name__ == "__main__":
    solve_concrete_mix_problem()
