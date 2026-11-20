import sys
import os

# Allows this test file to find the 'algorithms' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.rationing import allocate_water

# Fake test communities around Achimota (using your database fields)
sample_communities = [
    {
        "id": 4,
        "name": "Dome Houses",
        "type": "community",
        "population": 300,
        "demand": 60,
        "priority_type": "residential"
    },
    {
        "id": 5,
        "name": "Achimota Clinic",
        "type": "community",
        "population": 150,
        "demand": 60,
        "priority_type": "hospital"
    }
]

# Suppose only 80 liters of water are available (even though total demand is 120)
results = allocate_water(available_water=80, communities=sample_communities)

print("--- FAIR RATIONING RESULTS ---")
for item in results:
    print(f"{item['name']} ({item['priority_type']}): Needed {item['demand']}L | Got {item['allocated']}L | Shortfall: {item['shortfall']}L")