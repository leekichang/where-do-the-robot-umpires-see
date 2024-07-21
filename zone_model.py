import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit

def loss_function(params, x_data, y_data, r_data):
        alpha, beta, lambda_, r, x0, y0 = params
        d = (np.abs(x_data - x0)**r + np.abs((y_data - y0) / lambda_)**r)**(1/r)
        strike_prob = expit(-beta * (d - alpha))
        
        log_likelihood = 0.0
        for i in range(len(x_data)):
            if r_data[i] == 1: 
                log_likelihood += np.log(strike_prob[i])
            else:  
                log_likelihood += np.log(1 - strike_prob[i])
        return -log_likelihood

class ZoneModel:
    def __init__(self, name:'str'):
        self.name = name
        self.params = np.array([1.0, 10.0, 0.8, 3.0, 0.0, 2.5])  # [alpha, beta, lambda, r, x0, y0]
    
            
    def logit_inv(self, x):
        return np.log(x / (1 - x))

    def infer(self, x_data, y_data):
        alpha, beta, lambda_, r, x0, y0 = self.params
        x_term = r * np.log(np.abs(x_data - x0))
        y_term = r * np.log(np.abs((y_data - y0) / lambda_))
        
        d = (np.abs(x_data - x0)**r + np.abs((y_data - y0) / lambda_)**r)**(1/r)
        strike_prob = expit(-beta * (d - alpha))
        return strike_prob
    
    def fit(self, x_data, y_data, r_data):
        result = minimize(loss_function, self.params, args=(x_data, y_data, r_data), method='Nelder-Mead')
        self.best_params = result.x

    def print_best_params(self):
        print(f"Optimized Parameter of {self.name}:")
        print(f"alpha  = {self.best_params[0]}")
        print(f"beta   = {self.best_params[1]}")
        print(f"lambda = {self.best_params[2]}")
        print(f"r      = {self.best_params[3]}")
        print(f"x0     = {self.best_params[4]}")
        print(f"y0     = {self.best_params[5]}")

if __name__ == '__main__':
    year = 2024
    data = pd.read_csv(f'./data/{year}.csv', encoding='cp949')
    filtered_df = data[(data['result']=='Strike')|(data['result']=='Ball')]
    x_data = filtered_df['x'].to_numpy()
    y_data = filtered_df['y'].to_numpy()
    results = filtered_df['result'].to_numpy()
    r_data = []
    for result in results:
        if result == 'Strike':
            r_data.append(1)
        else:
            r_data.append(0)
    r_data = np.array(r_data)
    
    model = ZoneModel(name=f'{year}')
    model.fit(x_data[:100], y_data[:100], r_data[:100])
    model.print_best_params()