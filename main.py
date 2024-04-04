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
instances = df[df['type'] == 'instance']

import numpy as np
import matplotlib.pyplot as plt


def create_histograms(dataframe, column, title, file_prefix):
    plt.figure(figsize=(19.2, 10.8))

    conditions = []
    labels = []
    colors = ['#226C7B', '#0000ff']

    false_condition = dataframe[dataframe['isCSV2CEDAR'] == False][column]
    if not false_condition.empty:
        conditions.append(false_condition)
        labels.append('CSV2CEDAR False')

    true_condition = dataframe[dataframe['isCSV2CEDAR'] == True][column]
    if not true_condition.empty:
        conditions.append(true_condition)
        labels.append('CSV2CEDAR True')

    if conditions:
        selected_colors = colors[:len(conditions)]

        max_error = max(cond.max() for cond in conditions)
        bins = np.arange(0, max_error + 1, max(1, max_error // 50))

        plt.hist(conditions, bins=bins, color=selected_colors, alpha=0.7, stacked=True, label=labels, log=True)

        if labels:
            plt.legend()

    plt.title(title)
    plt.xlabel('Number of Errors')
    plt.ylabel('Number of Artifacts')
    plt.grid(axis='y', alpha=0.75)

    plt.savefig(f"graphs/{file_prefix + '_' + title.replace(',', '').replace(':', '').replace(' ', '_').lower()}.png")
    plt.close()


def create_histograms_by_creation_date(dataframe, title, file_prefix, skip_csv_2_cedar=False):
    plt.figure(figsize=(19.2, 10.8))

    if skip_csv_2_cedar:
        dataframe = dataframe[dataframe['isCSV2CEDAR'] == False]

    month_counts = dataframe['createdOnYearMonth'].value_counts().sort_index()

    month_counts.index = month_counts.index.astype(str)

    plt.bar(month_counts.index, month_counts.values, color='#629695', log=True)

    plt.title(title)
    plt.xlabel('Creation Months')
    plt.ylabel('Number of Artifacts')
    plt.xticks(rotation=45)
    plt.yticks([1, 2, 3, 4, 6, 8, 10, 100, 1000, 10000, 100000],
               ['1', '2', '3', '4', '6', '8', '10', '100', '1k', '10k', '100k'])  # Explicit y-ticks for clarity

    plt.grid(axis='y', alpha=0.75)

    plt.savefig(f"graphs/{file_prefix+'_'+title.replace(',', '').replace(':', '').replace(' ', '_').lower()}.png")
    plt.close()

create_histograms(fields, 'parsingErrorCount', 'Fields: Parsing Error Counts', '01_01')
create_histograms(elements, 'parsingErrorCount', 'Elements: Parsing Error Counts', '01_02')
create_histograms(templates, 'parsingErrorCount', 'Templates: Parsing Error Counts', '01_03')
create_histograms(instances, 'parsingErrorCount', 'Instances: Parsing Error Counts', '01_04')

create_histograms(fields, 'compareErrorCount', 'Fields: Roundtrip Error Counts', '02_01')
create_histograms(elements, 'compareErrorCount', 'Elements: Roundtrip Error Counts', '02_02')
create_histograms(templates, 'compareErrorCount', 'Templates: Roundtrip Error Counts', '02_03')

create_histograms(fields, 'compareWarningCount', 'Fields: Roundtrip Warning Counts', '03_01')
create_histograms(elements, 'compareWarningCount', 'Elements: Roundtrip Warning Counts', '03_02')
create_histograms(templates, 'compareWarningCount', 'Templates: Roundtrip Warning Counts', '03_03')

create_histograms_by_creation_date(fields, 'Fields: Creation Dates', '04_01')
create_histograms_by_creation_date(elements, 'Elements: Creation Dates', '04_02')
create_histograms_by_creation_date(templates, 'Templates: Creation Dates', '04_03')
create_histograms_by_creation_date(instances, 'Instances: Creation Dates', '04_04')
