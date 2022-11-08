import pandas as pd
import metrics_helper
import numpy as np


def calculate_all_metrics(df, ID, unit, interval):
    if metrics_helper.check_df(df):
        
        # create a list to add the results to
        results = {'ID': ID}
        df = df.dropna(subset=['glc'])

        #print(df.head())
        avg_glc = df.glc.mean()
        sd = df.glc.std()
        cv = (sd * 100 / avg_glc)
        min_glc = df.glc.min() # not necessary... but useful maybe?
        max_glc = df.glc.max() # same
        ea1c = (avg_glc + 2.59) / 1.59 # mmol right?
        #auc = metrics_helper.auc_helper(df)
        for i in [avg_glc, sd, cv, ea1c]:
            i = np.round(i, 2)
        
        glyc_var = {'Average glucose':avg_glc, 'SD':sd, 'CV':cv, 'eA1c':ea1c,}# 'auc':auc}
        results.update(glyc_var)

        ranges = metrics_helper.tir_helper(df.glc)
        results.update(ranges)

        hypos = metrics_helper.number_of_hypos(df)
        results.update(hypos)
        
        mage_results = metrics_helper.mage_helper(df)

        return results
        '''
        perc_missing = percent_missing(df,  interval_size=interval_size,
                                   start_datetime=start_time, end_datetime=end_time)
                                   '''
        
    else:
        print('EXPLODE THE PROGRAM')