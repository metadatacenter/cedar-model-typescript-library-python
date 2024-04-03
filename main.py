import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open('../roundtrip/summary.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)

df['createdOnDay'] = df['createdOn'].astype(str).str[:10]

df['createdOnDatetime'] = pd.to_datetime(df['createdOnDay'], errors='coerce')
# df = df.dropna(subset=['createdOnDatetime'])
df['createdOnYearMonth'] = df['createdOnDatetime'].dt.to_period('M')

elements = df[df['type'] == 'element']
templates = df[df['type'] == 'template']
fields = df[df['type'] == 'field']


def create_histograms(dataframe, column, title, file_prefix):
    plt.figure(figsize=(19.2, 10.8))

    max_error = max(dataframe[column])
    bins = np.arange(0, max_error + 1, max(1, max_error // 50))

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

    plt.savefig(f"graphs/{file_prefix+'_'+title.replace(':', '').replace(' ', '_').lower()}.png")


def create_histograms_by_creation_date(dataframe, title):
    plt.figure(figsize=(19.2, 10.8))

    month_counts = dataframe['createdOnYearMonth'].value_counts().sort_index()

    month_counts.index = month_counts.index.astype(str)

    plt.bar(month_counts.index, month_counts.values, color='skyblue')

    plt.title(title)
    plt.xlabel('Creation Months')
    plt.ylabel('Number of Artifacts')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"graphs/03_{title.replace(':', '').replace(' ', '_').lower()}.png")


create_histograms(elements, 'compareErrorCount', 'Elements: Roundtrip Error Counts', '02')
create_histograms(templates, 'compareErrorCount', 'Templates: Roundtrip Error Counts', '02')
create_histograms(fields, 'compareErrorCount', 'Fields: Roundtrip Error Counts', '02')

create_histograms(elements, 'parsingErrorCount', 'Elements: Parsing Error Counts', '01')
create_histograms(templates, 'parsingErrorCount', 'Templates: Parsing Error Counts', '01')
create_histograms(fields, 'parsingErrorCount', 'Fields: Parsing Error Counts', '01')

create_histograms_by_creation_date(elements, 'Elements: Creation Dates')
create_histograms_by_creation_date(templates, 'Templates: Creation Dates')
create_histograms_by_creation_date(fields, 'Fields: Creation Dates')
