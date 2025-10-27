import pandas as pd
import autoprocessing
import datetime
import numpy as np

class transformData:
    def __init__(self, df, device):
        self.usable = False
        self.device = 'Unknown'
        self.interval = None
        self.data = None
        self.id = None

        if device == 'FreeStyle Libre':
            #if self.assert_flash_libre(df):
             #   print('it\'s a libre')
            try:
                self.convert_flash_libre(df)
            except Exception as e:
                print(e)
        elif device =='Dexcom': #self.assert_dexcom(df):
            print('it\'s a dexcom')
            try:
                self.convert_dexcom(df)
            except Exception as ex:
                print(ex)
        else:
            print('it\'s a medtronic')
            try:
                self.convert_medtronic(df)
            except Exception as e:
                print(e)

    def convert_flash_libre(self, df):
        # Drop top rows
        df = df.iloc[1:]
        # Set first row as column headers
        df.columns = df.iloc[0]
        df.drop(index=[1], inplace=True)
        df.reset_index(inplace=True, drop=True)
        # Keep important columns
        if 'Historic Glucose(mmol/L)' in df.columns:
            df = df.loc[:,('Meter Timestamp', 'Historic Glucose(mmol/L)', 'Scan Glucose(mmol/L)')]
        elif 'Historic Glucose(mg/dL)' in df.columns:
            df = df.loc[:,('Meter Timestamp', 'Historic Glucose(mg/dL)', 'Scan Glucose(mg/dL)')]
        elif 'Historic Glucose mmol/L' in df.columns:
            df = df.loc[:,('Device Timestamp', 'Historic Glucose mmol/L', 'Scan Glucose mmol/L')]
        else:
            df = df = df.loc[:,('Device Timestamp', 'Historic Glucose mg/dL', 'Scan Glucose mg/dL')]

        # Rename cols
        df.columns = ['time', 'glc', 'scan_glc']
        # only keep time and glc for now
        self.data = df[['time', 'glc']]
        self.interval = 15
        self.usable = True
        #self.device = 'FreeStyle Libre'


    def convert_dexcom(self, df):
        # Set first row as column headers
        #df.columns = df.iloc[0]
        # Drop top rows
        #df = df.iloc[1:]
        filter_col = [col for col in df if col.startswith('Timestamp')]
        #df.drop(index=[2], inplace=True)
        df.reset_index(inplace=True, drop=True)
        if 'GlucoseValue' in df.columns:
            # Keep important columns
            df = df.loc[:,('GlucoseDisplayTime', 'GlucoseValue')]
        elif 'Glucose Value (mmol/L)' in df.columns:
            df = df.loc[:,(filter_col[0], 'Glucose Value (mmol/L)')]
            df = df.dropna(subset=[filter_col[0]])

        elif 'Glucose Value (mg/dL)' in df.columns:
            df = df.loc[:,(filter_col[0], 'Glucose Value (mg/dL)')]
            df = df.dropna(subset=[filter_col[0]])
        
        # Rename cols
        df.columns = ['time', 'glc']

        # Replace low high values
        #df = df.replace({'High': 22.3, 'Low': 2.1, 'HI':22.3, 'LO':2.1, 'hi':22.3, 'lo':2.1})
        self.data = df
        self.usable = True
        # Set device name
        #self.device = 'Dexcom'
        # set time interval to 5mins
        self.interval = 5

    
    def convert_medtronic(self, df):
        print('Converting medtronic')
        print(df.head())
        # Set first row as column headers
        df.columns = df.iloc[10]
        print(df.columns)
        # Drop top rows
        df = df.iloc[11:]
        print(df.head())
        df.reset_index(inplace=True, drop=True)
        if 'Sensor Glucose (mmol/L)' in df.columns:
            # Keep important columns
            df = df.loc[:,('Timestamp', 'Sensor Glucose (mmol/L)')]
        elif 'Sensor Glucose (mg/dL)' in df.columns:
            df = df.loc[:,('Timestamp', 'Sensor Glucose (mg/dL)')]

        print(df.head())
        df.columns = ['time', 'glc']
        df = df.dropna()
        # Rename cols
        # Replace low high values
        #df = df.replace({'High': 22.3, 'Low': 2.1, 'HI':22.3, 'LO':2.1, 'hi':22.3, 'lo':2.1})
        self.data = df
        self.usable = True
        # Set device name
        #self.device = 'Dexcom'
        # set time interval to 5mins
        self.interval = 5


def combine_datetime(date, time):
    dt = f'{date} {time}'
    try:
        dt = pd.to_datetime(dt)
    except:
        dt = np.nan
    return dt
