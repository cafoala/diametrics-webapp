import copy
import pandas as pd
import numpy as np
#import scipy
from scipy import signal
import warnings
from datetime import timedelta
import statistics
from sklearn.metrics import auc
import glycemic_events_helper
from pandarallel import pandarallel
pandarallel.initialize()

fift_mins = timedelta(minutes=15)
thirt_mins = timedelta(minutes=30)


def check_df(df):
    '''
    Check if the file given is a valid dataframe
    '''
    if not isinstance(df, pd.DataFrame):
        # I want to return this info to user somehow??
        warnings.warn('Not a dataframe')
        return False
    else:
        # drop any null values in the glc column
        df = df.dropna(subset=['time', 'glc'])
        if df.empty:
            warnings.warn('Empty dataframe')
            return False
        else:
            return True
            
def calculate_auc(df):
    if df.shape[0]>1:
        start_time = df.time.iloc[0]
        mins_from_start = df.time.parallel_apply(lambda x: x-start_time)
        df['hours_from_start'] = mins_from_start.parallel_apply(lambda x: (x.total_seconds()/60)/60)
        avg_auc = auc(df['hours_from_start'], df['glc'])#/24
        return avg_auc
    else:
        return np.nan

def auc_helper(df):
    df['date'] = df['time'].dt.date
    df['hour'] = df['time'].dt.hour
    hourly_breakdown = df.groupby([df.date, df.hour]).parallel_apply(lambda group: calculate_auc(group)).reset_index()
    hourly_breakdown.columns = ['date', 'hour', 'auc']
    daily_breakdown = hourly_breakdown.groupby('date').auc.mean()
    hourly_avg = hourly_breakdown.auc.mean()
    #daily_auc = df.groupby(df['time'].dt.date).apply(lambda group: calculate_auc(group))/24 # .reset_index()
    #daily_avg = daily_auc.mean()
    return  hourly_avg, daily_breakdown, hourly_breakdown 
    
def mage_helper(df):
    '''
    Calculates the mage using Scipy's signal class
    '''
    # Find peaks and troughs using scipy signal
    peaks, properties = signal.find_peaks(df['glc'], prominence=df['glc'].std())
    troughs, properties = signal.find_peaks(-df['glc'], prominence=df['glc'].std())
    # Create dataframe with peaks and troughs in order
    single_indexes = df.iloc[np.concatenate((peaks, troughs, [0, -1]))]
    single_indexes.sort_values('time', inplace=True)
    # Make a difference column between the peaks and troughs
    single_indexes['diff'] = single_indexes['glc'].diff()
    # Calculate the positive and negative mage and mean
    mage_positive = single_indexes[single_indexes['diff'] > 0]['diff'].mean()
    mage_negative = single_indexes[single_indexes['diff'] < 0]['diff'].mean()
    if pd.notnull(mage_positive) & pd.notnull(mage_negative):
        mage_mean = statistics.mean([mage_positive, abs(mage_negative)])
    elif pd.notnull(mage_positive):
        mage_mean = mage_positive
    elif pd.notnull(mage_negative):
        mage_mean = abs(mage_negative)
    else:
        mage_mean = 0  # np.nan
    return {'MAGE':mage_mean}

def convert_to_rounded_percent(value, length):
    return round(value * 100 / length, 2)

def tir_helper(series):
    """
    Helper function for time in range calculation with normal thresholds. Calculates the percentage of readings within
    each threshold by divSiding number of readings within range by total length of series
    """
    df_len = series.size
    tir_hypo = convert_to_rounded_percent(series.loc[series < 3.9].size, df_len)

    tir_lv1_hypo = convert_to_rounded_percent(series.loc[(series < 3.9) & (series >= 3)].size, df_len)

    tir_lv2_hypo = convert_to_rounded_percent(series.loc[series < 3].size, df_len)

    tir_norm = convert_to_rounded_percent(series.loc[(series >= 3.9) & (series <= 10)].size, df_len)
    
    tir_hyper = convert_to_rounded_percent(series.loc[series > 10].size, df_len)

    tir_lv1_hyper = convert_to_rounded_percent(series.loc[(series <= 13.9) & (series > 10)].size, df_len)

    tir_lv2_hyper = convert_to_rounded_percent(series.loc[series > 13.9].size, df_len)
    
    #tir_norm_1 = convert_to_rounded_percent((series.loc[(series >= 3.9) & (series < 7.8)]).size, df_len)

    #tir_norm_2 = convert_to_rounded_percent((series.loc[(series >= 7.8) & (series <= 10)]).size, df_len)
    '''
    tir_hypo_ex = series.loc[series < 5].size, df_len)

    tir_norm_ex = (series.loc[(series >= 5) & (series <= 15)]).size, df_len)

    tir_hyper_ex = series.loc[series > 15].size, df_len)
    '''
    return {'TIR normal': tir_norm, 'TIR hypoglycemia':tir_hypo, 'TIR level 1 hypoglycemia':tir_lv1_hypo, 'TIR level 2 hypoglycemia':tir_lv2_hypo, #'TIR normal (3.9-7.8)': tir_norm_1, 'TIR normal (7.8-10)': tir_norm_2, 
            'TIR hyperglycemia':tir_hyper, 'TIR level 1 hyperglycemia':tir_lv1_hyper, 'TIR level 2 hyperglycemia':tir_lv2_hyper}

def unique_tir(glc_series, lower_thresh, upper_thresh):
    df_len = glc_series.size
    if lower_thresh==2.2:
        tir = convert_to_rounded_percent(glc_series.loc[glc_series <= upper_thresh].size, df_len)
    elif upper_thresh==22.2:
        tir = convert_to_rounded_percent(glc_series.loc[glc_series >= lower_thresh].size, df_len)
    else:
        tir = convert_to_rounded_percent(glc_series.loc[(glc_series <= upper_thresh) & (glc_series >= lower_thresh)].size, df_len)
    return tir

def calculate_unique_tirs(glc_series, thresholds, units):
    if thresholds is None:
        return {}
    results_dict = {}
    for i in thresholds:
        name = f'TIR {i[0]}-{i[1]}{units}'
        tir = unique_tir(glc_series, i[0], i[1])
        results_dict[name] = tir
    return results_dict
        
def calculate_glycemic_episodes(df, hypo_lv1_thresh=3.9, hypo_lv2_thresh=3, hyper_lv1_thresh=10, hyper_lv2_thresh=13.9, mins=15, long_mins=120):
    total_hypos, lv1_hypos, lv2_hypos, prolonged_hypos, avg_length_hypos, total_time_hypos = glycemic_events_helper.calculate_episodes(df, True, hypo_lv1_thresh, hypo_lv2_thresh, mins, long_mins)
    total_hypers, lv1_hypers, lv2_hypers, prolonged_hypers, avg_length_hypers, total_time_hypers = glycemic_events_helper.calculate_episodes(df, False, hyper_lv1_thresh, hyper_lv2_thresh, mins, long_mins)
    results = {'Total hypos': total_hypos, 'LV1 hypos': lv1_hypos, 'LV2 hypos':lv2_hypos, 
                    'Prolonged hypos':prolonged_hypos, 'Avg. length hypos': avg_length_hypos, 
                    'Total length hypos':total_time_hypos, 'Total hypers':total_hypers, 
                    'LV1 hypers':lv1_hypers, 'LV2 hypers':lv2_hypers, 'Prolonged hypers':prolonged_hypers, 
                    'Avg. length hypers':avg_length_hypers, 'Total length hypers':total_time_hypers}
    return results

def helper_hypo_episodes(df, gap_size, interpolate=False, interp_method='pchip', lv1_threshold=3.9, lv2_threshold=3):
    """
    Helper function for hypoglycemic_episodes.
    """
    # Setting a copy so the df isn't altered in the following forloop
    df = copy.copy(df)
    # Convert time column to datetime and sort by time then reset index
    df['time'] = pd.to_datetime(df['time'])
    df.sort_values('time', inplace=True)
    df.reset_index(drop=True)

    # Calls the interpolate function if interpolate==True
    if interpolate:
        df.set_index('time', inplace=True)
        df = df.resample(rule='min', origin='start').asfreq()
        df['glc'] = df['glc'].interpolate(method=interp_method, limit_area='inside',
                                      limit_direction='forward', limit=gap_size)
        df.reset_index(inplace=True)
        gap_size = 1

    # set a boolean array where glc goes below 3.9, unless exercise thresholds are set then it's 7
    ### HERE ###
    bool_array = df['glc'] < lv1_threshold
    # gives a consecutive unique number to every bout below 3.9
    unique_consec_number = bool_array.ne(bool_array.shift()).cumsum()
    # the number of consecutive readings below 3.9
    number_consec_readings = unique_consec_number.map(unique_consec_number.value_counts()).where(bool_array)
    # set up a df using these values to identify each bout of hypogylcaemia
    df_full = pd.DataFrame({'time_rep': df['time'], 'glc_rep': df['glc'],
                            'unique_number': unique_consec_number,
                            'consec_readings': number_consec_readings})
    # drop nulls and reset index to only get bouts below 3.9 in df
    df_full.dropna(inplace=True)
    df_full.reset_index(inplace=True, drop=True)
    # create 2 new columns which will be used to identify the lowest reading in the bout (low)
    # and lv2 to identify whether the bout was a lv2 hypo
    df_full['low'] = np.nan
    df_full['lv2'] = np.nan
    # loop through all of the unique numbers that signify the bouts to calculate the low value
    # and whether it was a lv2 hypo
    for num in set(df_full.unique_number.values):
        # set the values of low at the unique number equal to the min glc for that bout
        df_full['low'].iloc[df_full[df_full['unique_number'] == num].index] = df_full[
            df_full['unique_number'] == num]['glc_rep'].min()
        # calculate whether the bout was a lv_2 hypo by calling the lv2_calc function
        lv2 = lv2_calc(df_full[df_full['unique_number'] == num], 'time_rep', 'glc_rep', lv2_threshold)
        # set the lv2 column equal to the boolean value
        df_full['lv2'].iloc[df_full[df_full['unique_number'] == num].index] = lv2

    list_results = []
    for num in set(df_full['unique_number'].values):
        # print(num)
        sub_df = df_full[df_full['unique_number'] == num]
        sub_df.sort_values('time_rep', inplace=True)
        sub_df.reset_index(inplace=True)

        start_time = sub_df['time_rep'].iloc[0]
        end_time = sub_df['time_rep'].iloc[-1]
        low = sub_df['low'].iloc[0]
        lv2 = sub_df['lv2'].iloc[0]

        list_results.append([start_time, end_time, low, lv2])

    df_start_end = pd.DataFrame(list_results, columns=['start', 'end', 'low', 'lv2'])
    df_start_end.sort_values('start', inplace=True)
    df_start_end.reset_index(inplace=True, drop=True)

    # this section confirms whether the episode is actually a hypo and joins other
    # hypos that are less than 15 mins apart
    hypos_list = []
    i = 0
    # use a while loop to go through every hypo
    while i < df_start_end.shape[0]:
        row = df_start_end.iloc[i]
        diff = row.end - row.start
        # only considered a hypo if the duration of hypo is >= 15 mins
        # if it's longer than 15 mins, allocate the variables to equal the row
        if (diff >= timedelta(minutes=15)) & (diff > timedelta(0)):
            start = row.start
            end = row.end
            low = row.low
            lv2 = row.lv2

            # before entering this section, check that there's at least 2 entries left to compare
            if i < df_start_end.shape[0] - 1:
                # loops through remaining hypos, connecting it to the current hypo if they are less than 15 min apart
                for n in range(1, df_start_end.shape[0] - i):
                    nxt_row = df_start_end.iloc[i + n]
                    # the difference between hypos is less than 15 mins + 2 * time interval between readings
                    # end of the hypo is changed to end of next row, low is made lowest of both
                    # and lv2 is true if either one is true
                    if nxt_row.start - end < timedelta(minutes=(6 - gap_size / 5) * gap_size):  #
                        end = nxt_row.end
                        if low > nxt_row.low:
                            low = nxt_row.low
                        if nxt_row.lv2:
                            lv2 = True
                        # if it's the last entry, there'll be nothing to compare to so add the results to the list here
                        # before the while loop is stopped with the n+1 line
                        if n + i == df_start_end.shape[0] - 1:
                            hypos_list.append([start, end, low, lv2])
                            i += n + 1

                    else:
                        # if there isn't a hypo within 15 mins of this hypo, add the results to the list
                        # increase i by as many iterations (n) of the forloop that have run
                        # break the forloop to move on to next hypo
                        hypos_list.append([start, end, low, lv2])
                        i += n
                        break
            # this is the last hypo in the df, so no need to check if there's another hypo 15 mins apart
            # but hypo is over 15 mins so gets added to the results list
            else:
                hypos_list.append([start, end, low, lv2])
                i += 1
        # hypo is shorter than 15 mins so it doesn't get added to the results list
        else:
            i += 1

    # convert the results list into a dataframe
    results = pd.DataFrame(hypos_list, columns=['start_time', 'end_time', 'low', 'lv2']).reset_index(drop=True)

    # calculate overview statistics, number of hypos, avg length of hypos, number lv2 hypos
    duration = results.end_time - results.start_time
    number_hypos = results.shape[0]
    avg_length = duration.mean()
    total_time_hypo = duration.sum()
    #print(duration)
    #print(timedelta(minutes=120))
    #number_long_hypos = duration[duration>timedelta(minutes=120)].shape[0]
    if pd.notnull(avg_length):
        avg_length = str(avg_length.round('1s')) # .total_seconds() / 60
        total_time_hypo = str(total_time_hypo.round('1s')) #.total_seconds() / 60
    elif number_hypos == 0:
        avg_length = 0
        total_time_hypo = 0
    else:
        avg_length = np.nan
        total_time_hypo = np.nan

    number_lv2_hypos = results[results['lv2']].shape[0]
    number_lv1_hypos = number_hypos - number_lv2_hypos

    overview = {'Total hypoglycemic episodes':number_hypos, 'Level 1 hypoglycemic episodes':number_lv1_hypos, 'Level 2 hypoglycemic episodes':number_lv2_hypos,
                    'Average length of hypoglycemic episodes':avg_length, 'Total time in hypoglycemia':total_time_hypo}

    return overview, results


def lv2_calc(df, time, glc, lv2_threshold):
    """
    Determines whether a hypoglycaemic episode is a level 2 hypoglycaemic
    episode. Lv2 is when glc drops below 3.0mmol/L for at least 15 consecutive 
    mins
   
    """
    # lv2 is false unless proven otherwise
    lv2 = False
    # gives a unique number to all episodes where glc drops below 3
    
    ### HERE ###
    bool_array = df[glc] < lv2_threshold
    unique_consec_number = bool_array.ne(bool_array.shift()).cumsum()
    number_consec_values = unique_consec_number.map(unique_consec_number.value_counts()).where(bool_array)
    df_comb = pd.DataFrame({'time_rep': df[time], 'unique_lv2': unique_consec_number,
                            'consec_readings': number_consec_values, 'glc_rep': df[glc]})
    df_comb.dropna(inplace=True)

    # loop through all of these bouts below 3 and see if any last at least 15 mins, if so lv2 = True
    for num in set(df_comb['unique_lv2'].values):
        sub_df = df_comb[df_comb['unique_lv2'] == num]
        sub_df.sort_values('time_rep', inplace=True)
        sub_df.reset_index(inplace=True)

        start_time = sub_df[time].iloc[0]
        end_time = sub_df[time].iloc[-1]
        if end_time - start_time >= timedelta(minutes=15):
            lv2 = True

    return lv2


def helper_missing(df, gap_size, start_time=None, end_time=None):
    """
    Helper for percent_missing function
    """
    # Calculate start and end time from dataframe
    if start_time is None:
        start_time = df['time'].iloc[0]
    if end_time is None:
        end_time = df['time'].iloc[-1]
    
    # Subsection of df with start and end times provided
    df = df.loc[(df['time']>=start_time)&(df['time']<=end_time)]

    if gap_size == 5:
        freq = '5min'
    elif gap_size==15:
        freq = '15min'
    else:
        return print('EXPLODE THE PROGRAM')
    
    # calculate the number of non-null values
    number_readings = sum(df.set_index('time').groupby(pd.Grouper(freq=freq)).count()['glc'] > 0)
    # calculate the missing data based on start and end of df
    total_readings = ((end_time - start_time)+timedelta(minutes=gap_size))/+timedelta(minutes=gap_size)


    if number_readings >= total_readings:
        data_sufficiency = 100
    else:
        data_sufficiency = number_readings*100/total_readings
    
    return {'Start DateTime': str(start_time.round('min')), 'End DateTime':str(end_time.round('min')), 'Data Sufficiency':np.round(data_sufficiency, 1)}

# LBGI and HBGI
def calc_bgi(glucose, units):
    if units=='mmol/L':
        num1=1.794
        num2=1.026
        num3=1.861
    else:
        num1=1.509
        num2=1.084
        num3=5.381
    bgi = num1*(np.log(glucose)**num2 - num3)
    return bgi
    
def calc_lbgi(glucose, units):
    bgi = calc_bgi(glucose, units)
    lbgi = 10*(min(bgi, 0)**2)
    return lbgi

def calc_hbgi(glucose, units):
    bgi = calc_bgi(glucose, units)
    hbgi = 10*(max(bgi, 0)**2)
    return hbgi

def helper_bgi(glc_series, units):
    lbgi = glc_series.parallel_apply(lambda x: calc_lbgi(x, units)).mean()
    hbgi = glc_series.parallel_apply(lambda x: calc_hbgi(x, units)).mean()
    return {'LBGI': lbgi, 'HBGI':hbgi}