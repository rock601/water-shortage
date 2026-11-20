import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.max_flow import analyze_water_flow

# 5-node test network matching your database 'nodes' fields
sample_nodes = [
    {"id": 1, "name": "Achimota Reservoir", "type": "source", "supply": 100, "demand": 0, "priority_type": None},
    {"id": 2, "name": "Junction A", "type": "junction", "demand": 0, "priority_type": None},
    {"id": 3, "name": "Junction B", "type": "junction", "demand": 0, "priority_type": None},
    {"id": 4, "name": "Achimota Clinic", "type": "community", "demand": 60, "priority_type": "hospital"},
    {"id": 5, "name": "Dome Houses", "type": "community", "demand": 60, "priority_type": "residential"},
]

# 4 pipes matching your database 'pipes' fields
sample_pipes = [
    {"id": 1, "from_node": 1, "to_node": 2, "length": 500, "capacity": 80, "status": "ok"},
    {"id": 2, "from_node": 2, "to_node": 4, "length": 300, "capacity": 70, "status": "ok"},
    {"id": 3, "from_node": 2, "to_node": 3, "length": 400, "capacity": 50, "status": "ok"},
    {"id": 4, "from_node": 3, "to_node": 5, "length": 350, "capacity": 60, "status": "ok"},
]

report = analyze_water_flow(sample_nodes, sample_pipes)

print("--- MAX FLOW ANALYSIS RESULTS ---")
print(f"Total Water Delivered: {report['total_water_delivered']}L")

print("\nCommunities with Shortfalls:")
for s in report["shortfalls"]:
    print(f"- {s['name']}: Needed {s['demand']}L | Received {s['received']}L | Shortfall: {s['shortfall']}L")

print("\nBottleneck Pipes (100% Full):")
for b in report["bottlenecks"]:
    print(f"- Pipe #{b['pipe_id']} ({b['from']} -> {b['to']}) max capacity: {b['capacity']}L")

    # --- EDGE CASE TEST: BURST PIPE & DISCONNECTED COMMUNITY ---
print("\n--- EDGE CASE TEST (BURST PIPE + DISCONNECTED NODE) ---")

# Add a disconnected community with no pipes leading to it
edge_nodes = sample_nodes + [
    {"id": 6, "name": "Isolated Area", "type": "community", "demand": 40, "priority_type": "residential"}
]

# Simulate Pipe #3 (Junction A -> Junction B) bursting
edge_pipes = [dict(p) for p in sample_pipes]
edge_pipes[2]["status"] = "burst"

edge_report = analyze_water_flow(edge_nodes, edge_pipes)
print(f"Total Water Delivered After Burst: {edge_report['total_water_delivered']}L")
for s in edge_report["shortfalls"]:
    print(f"- {s['name']}: Needed {s['demand']}L | Received {s['received']}L | Shortfall: {s['shortfall']}L")