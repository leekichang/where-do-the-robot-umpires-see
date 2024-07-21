import pandas as pd

files = ['./data/2021',
         './data/2022',
         './data/2023']
lens = [5,5,5,6]
for file in files:
    merged_data = pd.DataFrame()
    for i in range(lens):
        f_name = f'{file}_{i}.csv'
        data = pd.read_csv(f_name, encoding='cp949')
        merged_data = pd.concat([merged_data, data])
    merged_data.to_csv(f'{file}.csv', index=False, encoding='cp949')