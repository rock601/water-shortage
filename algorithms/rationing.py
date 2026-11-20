def allocate_water(available_water, communities):
    """
    Divides limited water fairly among communities using a Greedy algorithm.
    
    available_water: total liters of water that can reach the communities
    communities: a list of dictionaries matching your database 'nodes' table
    """
    # 1. Set priority rules: hospitals first (1), schools second (2), homes third (3)
    priority_order = {
        "hospital": 1,
        "school": 2,
        "residential": 3
    }

    # 2. Sort communities so the highest priority and highest demand come first
    sorted_communities = sorted(
        communities,
        key=lambda c: (priority_order.get(c["priority_type"], 4), -c["demand"])
    )

    remaining_water = available_water
    allocation_plan = []

    # 3. Hand out water one community at a time until it runs out
    for community in sorted_communities:
        needed = community["demand"]
        
        # Give them everything they need, OR whatever water is left
        water_given = min(remaining_water, needed)
        remaining_water -= water_given

        allocation_plan.append({
            "id": community["id"],
            "name": community["name"],
            "priority_type": community["priority_type"],
            "demand": needed,
            "allocated": water_given,
            "shortfall": needed - water_given
        })

    return allocation_plan
