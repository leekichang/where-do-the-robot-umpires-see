import pandas as pd

files = ['./data/2021.csv', './data/2022.csv', './data/2023.csv', './data/MLB.csv']

chunk_size = 50000
for file in files:
    data = pd.read_csv(file, encoding='cp949')
    for i in range(len(data) // chunk_size + 1):
        data[i * chunk_size:(i + 1) * chunk_size].to_csv(file.replace('.csv', f'_{i}.csv'), index=False, encoding='cp949')
        