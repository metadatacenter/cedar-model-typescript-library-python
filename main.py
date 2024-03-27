import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Step 1: Load JSON Data
with open('../roundtrip/summary.json') as f:  # Ensure the path to your JSON file is correct
    data = json.load(f)

# Convert data to a pandas DataFrame for easier manipulation
df = pd.DataFrame(data)

# Step 2: Separate Data by Type
elements = df[df['type'] == 'element']
templates = df[df['type'] == 'template']
fields = df[df['type'] == 'field']


# Function to create histograms with adjustments
def create_histograms(dataframe, column, title):
    plt.figure(figsize=(10, 6))

    # Adjusting the bin size for readability
    max_error = max(dataframe[column])
    bins = np.arange(0, max_error + 1, max(1, max_error // 50))  # Ensure at least 1 to avoid zero division error

    plt.hist(dataframe[column], bins=bins, alpha=0.7, log=True)

    # Highlight the 0 column
    zero_errors = dataframe[dataframe[column] == 0]
    if not zero_errors.empty:
        plt.hist(zero_errors[column], bins=[-0.5, 0.5], color='red', alpha=0.7, log=True)

    plt.title(title)
    plt.xlabel('Number of Errors')
    plt.ylabel('Number of Artifacts')
    plt.xticks(bins[::max(1, len(bins) // 15)])
    plt.yticks([1, 2, 3, 4, 6, 8, 10, 100, 1000, 10000],
               ['1', '2', '3', '4', '6', '8', '10', '100', '1k', '10k'])  # Explicit y-ticks for clarity

    plt.grid(axis='y', alpha=0.75)

    plt.savefig(f"graphs/{title.replace(':', '').replace(' ', '_').lower()}.png")  # Save the figure with a filename derived from the title


# Step 3: Create Diagrams for Compare Error Counts
create_histograms(elements, 'compareErrorCount', 'Elements: Comparison Error Counts')
create_histograms(templates, 'compareErrorCount', 'Templates: Comparison Error Counts')
create_histograms(fields, 'compareErrorCount', 'Fields: Comparison Error Counts')

# Step 4: Create Diagrams for Parsing Error Counts
create_histograms(elements, 'parsingErrorCount', 'Elements: Parsing Error Counts')
create_histograms(templates, 'parsingErrorCount', 'Templates: Parsing Error Counts')
create_histograms(fields, 'parsingErrorCount', 'Fields: Parsing Error Counts')
