import os
import pickle
import argparse

import pandas as pd
import matplotlib.pyplot as plt

STUFFS = {'직구':'4-Seam',
          '투심':'2-Seam',
          '커터':'Cutter',
          '슬라이더':'Slider',
          '포크':'Fork',
          '커브':'Curve',
          '체인지업':'Change-up',
          '너클볼':'Knuckle',
          '싱커':'Sinker',
          '':'Unknown'}

def parse_args():
    parser = argparse.ArgumentParser(description='ABS PROJECT')
    parser.add_argument('--year', default='2024', type=str)
    args = parser.parse_args()
    return args

class PitchData(object):
    def __init__(self, data):
        self.pitchID  = data['pitchId' ]
        self.location = data['location']
        self.stance   = data['stance'  ]
        self.stuff    = data['stuff'   ]
        self.speed    = data['speed'   ]
        self.result   = data['result'  ]
        self.pitcher  = data['pitcher' ]
        self.batter   = data['batter'  ]

class DataLoader(object):
    def __init__(self, year):
        data_path = f'./data/{year}'
        self.folders = [os.path.join(data_path, f) for f in os.listdir(data_path) \
                        if len(os.listdir(f'{data_path}/{f}'))>0]
        self.innings = 0
        self.pitches = {}
        self.total_pitch = 0
        try:
            self.pitch_df = pd.read_csv(f'./data/{year}.csv', index_col='Unnamed: 0')
            for folder in self.folders:
                for f_ in os.listdir(folder):
                    self.innings += 1
            self.total_pitch = len(self.pitch_df)
        except:
            for folder in self.folders:
                for f_ in os.listdir(folder):
                    with open(f'{folder}/{f_}', 'rb') as f:
                        data = pickle.load(f)
                        self.innings += 1
                    for pitch in data:
                        pitch_ = {}
                        pitch_['location_x'] = pitch['location'][0]
                        pitch_['location_y'] = pitch['location'][1]
                        pitch_['stance'    ] = pitch['stance'    ]
                        pitch_['stuff'     ] = STUFFS[pitch['stuff']]
                        pitch_['speed'     ] = pitch['speed'     ]
                        pitch_['result'    ] = pitch['result'    ]
                        pitch_['pitcher'   ] = pitch['pitcher'   ]
                        pitch_['batter'    ] = pitch['batter'    ]
                        self.pitches[self.total_pitch] = pitch_
                        self.total_pitch += 1
            self.pitch_df = pd.DataFrame.from_dict(self.pitches).transpose()
            self.pitch_df.to_csv(f'./data/{year}.csv', encoding='cp949')
        
    def load_pitches(self):
        return self.pitch_df
    
    def num_pitches(self):
        return self.total_pitch

    def num_innings(self):
        return self.innings
    
    def num_games(self):
        return len(self.folders)
    
class Visualizer(object):
    def __init__(self):
        self.pitches = None
    
    def set_pitches(self, pitches):
        self.pitches = pitches
    
    def visualize_zone(self, conditions:list=[]):
        fig, ax = plt.subplots(figsize=(5,6))
        r_corner = (-0.75, 1.5)
        r_width  = 1.5
        r_height = 2.

        rectangle = plt.Rectangle(r_corner, r_width, r_height, linewidth=2, edgecolor='b', facecolor='none')
        ax.add_patch(rectangle)
        for i in range(2):
            ax.axvline(x=(i+1)*(r_width/3 )+r_corner[0], color='g', linestyle='--', linewidth=1.)  
            ax.axhline(y=(i+1)*(r_height/3)+r_corner[1], color='g', linestyle='--', linewidth=1.)  

        ax.set_xlabel('Width')
        ax.set_ylabel('Height')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-0, 5])
        for condition in conditions:
            r_center = condition['center']
            r_width  = condition['width']
            r_height = condition['height']
            r_corner = (r_center[0]-r_width/2, r_center[1]-r_height/2)
            rectangle = plt.Rectangle(r_corner, r_width, r_height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rectangle)
        plt.show()
    def visualize_distribution(self):
        pass

class PitchFilter(object):
    def __init__(self, pitches:list):
        self.pitches = pitches
    
    def filter_pitches(self, conditions:dict):
        filtered_pitches = []
        conditions = self.filter_condition(conditions)
        for pitch in self.pitches:
            for k, condition in conditions.items():
                pass
        return filtered_pitches

    def filter_condition(self, conditions):
        filtered = {}
        for k, condition in conditions.items():
            if condition is not None:
                filtered[k] = condition
        return filtered

    def filter(self, k:str, condition:list):
        if   k == 'stance':
            pass
        elif k == 'stuff':
            pass
        elif k == 'speed':
            pass
        elif k == 'result':
            pass
        elif k == 'pitcher':
            pass
        elif k == 'batter':
            pass
        elif k == 'location_x':
            pass
        elif k == 'location_y':
            pass
        
        
