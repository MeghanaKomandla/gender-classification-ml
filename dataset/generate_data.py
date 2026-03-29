import csv
import random
import os

# Create dataset folder if not exists
os.makedirs("dataset", exist_ok=True)

# Define ranges
male_ranges = {
    'forehead_width': (11.5, 14.0),
    'forehead_height': (5.0, 6.5),
    'nose_width': (3.5, 4.8),
    'nose_height': (4.0, 5.2),
}

female_ranges = {
    'forehead_width': (10.0, 12.5),
    'forehead_height': (4.5, 6.0),
    'nose_width': (2.8, 3.8),
    'nose_height': (3.5, 4.5),
}

data = []
random.seed(42)

# Generate Male samples (~250)
for _ in range(250):
    row = {k: round(random.uniform(v[0], v[1]), 2) for k, v in male_ranges.items()}
    row['gender'] = "Male"
    data.append(row)

# Generate Female samples (~250)
for _ in range(250):
    row = {k: round(random.uniform(v[0], v[1]), 2) for k, v in female_ranges.items()}
    row['gender'] = "Female"
    data.append(row)

# Shuffle data
random.shuffle(data)

# Write to CSV
with open('dataset/gender_data.csv', mode='w', newline='') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            'forehead_width',
            'forehead_height',
            'nose_width',
            'nose_height',
            'gender'
        ]
    )
    
    writer.writeheader()
    
    for r in data:
        writer.writerow(r)

print("Dataset generated successfully!")
