from collections import deque


def bfs(residual_graph, parent, source, sink):
    """Finds any path from source to sink that still has spare pipe capacity."""
    visited = {source}
    queue = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor, remaining_capacity in residual_graph[current].items():
            if neighbor not in visited and remaining_capacity > 0:
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False


def analyze_water_flow(nodes, pipes):
    """
    Runs Edmonds-Karp Max Flow to find community shortfalls and bottleneck pipes.
    
    nodes: list of dicts matching the database 'nodes' table
    pipes: list of dicts matching the database 'pipes' table
    """
    SUPER_SOURCE = "SUPER_SOURCE"
    SUPER_SINK = "SUPER_SINK"

    # 1. Create an empty network map for all nodes + Super Source & Super Sink
    residual = {SUPER_SOURCE: {}, SUPER_SINK: {}}
    node_lookup = {}
    for n in nodes:
        residual[n["id"]] = {}
        node_lookup[n["id"]] = n

    # 2. Add real pipes (burst pipes get 0 capacity so water cannot pass)
    for p in pipes:
        cap = 0 if p["status"] == "burst" else p["capacity"]
        u, v = p["from_node"], p["to_node"]
        residual[u][v] = residual[u].get(v, 0) + cap
        residual[v].setdefault(u, 0)  # Reverse path needed by Edmonds-Karp

    # 3. Connect Super Source to sources, and communities to Super Sink
    for n in nodes:
        if n["type"] == "source":
            # Use 'supply' if provided, otherwise allow pipes to set the limit
            supply = n.get("supply", 999999)
            residual[SUPER_SOURCE][n["id"]] = supply
            residual[n["id"]][SUPER_SOURCE] = 0
        elif n["type"] == "community":
            residual[n["id"]][SUPER_SINK] = n["demand"]
            residual[SUPER_SINK][n["id"]] = 0

    # 4. Push water through available paths until no paths remain
    parent = {}
    total_water_delivered = 0

    while bfs(residual, parent, SUPER_SOURCE, SUPER_SINK):
        # Find the narrowest pipe along the path just found
        path_flow = float("inf")
        step = SUPER_SINK
        while step != SUPER_SOURCE:
            prev = parent[step]
            path_flow = min(path_flow, residual[prev][step])
            step = prev

        # Subtract that water from forward pipes and add to reverse paths
        step = SUPER_SINK
        while step != SUPER_SOURCE:
            prev = parent[step]
            residual[prev][step] -= path_flow
            residual[step][prev] += path_flow
            step = prev

        total_water_delivered += path_flow
        parent = {}

    # 5. Check which communities did not get enough water
    shortfalls = []
    for n in nodes:
        if n["type"] == "community":
            unmet_demand = residual[n["id"]][SUPER_SINK]
            received = n["demand"] - unmet_demand
            if unmet_demand > 0:
                shortfalls.append({
                    "id": n["id"],
                    "name": n["name"],
                    "demand": n["demand"],
                    "received": received,
                    "shortfall": unmet_demand
                })

    # 6. Find bottleneck pipes (working pipes with 0 spare capacity left)
    bottlenecks = []
    for p in pipes:
        if p["status"] == "ok" and p["capacity"] > 0:
            if residual[p["from_node"]][p["to_node"]] == 0:
                from_name = node_lookup[p["from_node"]]["name"]
                to_name = node_lookup[p["to_node"]]["name"]
                bottlenecks.append({
                    "pipe_id": p["id"],
                    "from": from_name,
                    "to": to_name,
                    "capacity": p["capacity"]
                })

    return {
        "total_water_delivered": total_water_delivered,
        "shortfalls": shortfalls,
        "bottlenecks": bottlenecks
    }