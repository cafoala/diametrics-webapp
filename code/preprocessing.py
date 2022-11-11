from datetime import datetime
import pandas as pd
import autoprocessing
import transformData
import metrics_helper

def calculate_time_interval(df):
    diff = df.dropna(subset=['time','glc'])
    diff = df.time.diff().mode()
    diff_mins = int(diff[0].total_seconds()/60)
    return diff_mins



# let's assume we're getting 1 file in and it's already been confirmed that it's a df
def preprocess_df(df, filename):
    data_dictionary = {}
    # Replace high and low values for different devices 
    # ?DOUBLE CHECK THESE VALUES?
    df.replace({'High': 22.2, 'Low': 2.2, 'HI':22.2, 'LO':2.2, 'hi':22.2, 'lo':2.2}, inplace=True)
    df_transformed = transformData.transformData(df)
    if df_transformed.data.empty:
        df_transformed.usable = False

    if df_transformed.usable:
        # Check that the whole datetime works
        try:
            df_transformed.data['time'] = pd.to_datetime(df_transformed.data['time'])
            df_transformed.data['glc'] = pd.to_numeric(df_transformed.data['glc'])
            if 'scan_glc' in df_transformed.data.columns:
                df_transformed.data['scan_glc'] = pd.to_numeric(df_transformed.data['scan_glc'])
        except Exception as ex:
            # log that there is a non-dt item in the col
            print(ex)
            return None


        # Calculate if mmol/L or mg/dL
        data_dictionary['Units'] = autoprocessing.assert_units(df_transformed.data['glc'])

        # Check if there's an id
        if df_transformed.id is None:
            df_transformed.id = filename.rsplit('.', 1)[0] ## had .name previously
        # Check if there's an interval
        if df_transformed.interval is None:
            df_transformed.interval = calculate_time_interval(df_transformed.data)
        
        data_stats = metrics_helper.helper_missing(df_transformed.data, df_transformed.interval)

        
        data_dictionary['Usable'] = df_transformed.usable
        data_dictionary['Filename'] = filename
        data_dictionary['Device'] = df_transformed.device
        data_dictionary['Interval'] = df_transformed.interval
        data_dictionary['data'] = df_transformed.data
        data_dictionary['ID'] = df_transformed.id
        data_dictionary.update(data_stats)
        print(data_dictionary)
        return data_dictionary
    else:
        # Log the errors?
        return None
    