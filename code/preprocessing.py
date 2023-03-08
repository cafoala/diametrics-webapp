from datetime import datetime
import pandas as pd
import autoprocessing
import transformData
import metrics_helper

def calculate_time_interval(df):
    df = df.dropna(subset=['time','glc'])
    diff = df.time.diff().mode()
    diff_mins = int(diff[0].total_seconds()/60)
    return diff_mins

# let's assume we're getting 1 file in and it's already been confirmed that it's a df
def preprocess_df(df, filename, dt_format, device, units):
    data_dictionary = {}
    # Replace high and low values for different devices 
    # ?DOUBLE CHECK THESE VALUES?
    #df.replace({'High': 22.2, 'Low': 2.2, 'HI':22.2, 'LO':2.2, 'hi':22.2, 'lo':2.2}, inplace=True)
    df_transformed = transformData.transformData(df, device)
    if df_transformed.usable:        
        try:
            df_transformed.data = df_transformed.data.dropna(subset=['time', 'glc'])
            # Convert to the correct dt format and sort
            if dt_format=='euro':
                df_transformed.data['time'] = pd.to_datetime(df_transformed.data['time'], dayfirst=True)
            else:
                df_transformed.data['time'] = pd.to_datetime(df_transformed.data['time'], dayfirst=False)
            df_transformed.data = df_transformed.data.sort_values(['time'])
            # Replace low high values
            '''if (device=='dexcom') or (dt_format=='eur'):            
                df = df.replace({'high': 22.3, 'low': 2.1,'High': 22.3, 'Low': 2.1, 'HI':22.3, 'LO':2.1, 'hi':22.3, 'lo':2.1})
            else:
                df = df.replace({'high': 27.9, 'low': 2.1,'High': 27.9, 'Low': 2.1, 'HI':27.9, 'LO':2.1, 'hi':27.9, 'lo':2.1})
            # Convert glucose to numeric and check for , instead of .
            try:
                df_transformed.data['glc'] = pd.to_numeric(df_transformed.data['glc'])
            except:
                df_transformed.data['glc'] = df_transformed.data['glc'].replace(',', '.')
                df_transformed.data['glc'] = pd.to_numeric(df_transformed.data['glc'])
            if 'scan_glc' in df_transformed.data.columns:
                df_transformed.data['scan_glc'] = pd.to_numeric(df_transformed.data['scan_glc'])'''
            # Calculate if mmol/L or mg/dL
            #data_dictionary['Units'] = autoprocessing.assert_units(df_transformed.data['glc'])

            # Check if there's an id
            if df_transformed.id is None:
                df_transformed.id = filename.rsplit('.', 1)[0] ## had .name previously
            # Check if there's an interval
            if df_transformed.interval is None:
                df_transformed.interval = calculate_time_interval(df_transformed.data)
            
            data_stats = metrics_helper.helper_missing(df_transformed.data, df_transformed.interval)
            days = str(pd.to_datetime(data_stats['End DateTime']) - pd.to_datetime(data_stats['Start DateTime']))
            
            data_dictionary['Usable'] = df_transformed.usable
            data_dictionary['Filename'] = filename
            data_dictionary['Device'] = df_transformed.device
            data_dictionary['Interval'] = df_transformed.interval
            data_dictionary['Units'] = units
            data_dictionary['data'] = df_transformed.data.to_dict('records')
            data_dictionary['ID'] = df_transformed.id
            data_dictionary.update(data_stats)
            data_dictionary['Days'] = days

            return data_dictionary
        except Exception as ex:
            # log that there is a non-dt item in the col
            data_dictionary = {'Usable': False, 'Filename': filename, 'Device':'N/A',
                'ID': 'N/A', 'Start DateTime': 'N/A', 'End DateTime': 'N/A',
                'Days': 'N/A', 'Data Sufficiency (%)':'N/A'}
            return data_dictionary
    else:
        # Log the errors?
        data_dictionary = {'Usable': False, 'Filename': filename, 'Device':'N/A',
            'ID': 'N/A', 'Start DateTime': 'N/A', 'End DateTime': 'N/A',
            'Days': 'N/A', 'Data Sufficiency (%)':'N/A'}
        return data_dictionary
    