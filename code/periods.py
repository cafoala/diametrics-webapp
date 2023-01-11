import pandas as pd


def get_day_night_breakdown(df, day_start, day_end, night_start, night_end):
    df_dt = df.set_index('time')
    day = df_dt.between_time(day_start, day_end).reset_index()
    night = df_dt.between_time(night_start, night_end).reset_index()
    return day, night

'''def get_day_night_breakdown(df):
    df_dt = df.set_index('time')
    day = df_dt.between_time('06:00','23:59')
    night = df_dt[~df_dt.index.isin(day.index)].reset_index()
    day = day.reset_index()
    return day, night'''

'''def daily_breakdown(df):
    df.groupby(df['time'].dt.date).apply()'''