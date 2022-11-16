import pandas as pd
import metrics_helper
import numpy as np

def calculate_all_metrics(df, ID, interval, unit='mmol'):
    if metrics_helper.check_df(df):
        
        # create a list to add the results to
        results = {'ID': ID}
        df = df.dropna(subset=['glc']).reset_index(drop=True)

        # Basic metrics
        avg_glc = df.glc.mean()
        sd = df.glc.std()
        cv = (sd * 100 / avg_glc)
        min_glc = df.glc.min() # not necessary... but useful maybe?
        max_glc = df.glc.max() # same
        ea1c = (avg_glc + 2.59) / 1.59 # mmol right?
        auc, daily_breakdown, hourly_breakdown = metrics_helper.auc_helper(df)
        
        glyc_var = {'Average glucose':avg_glc, 'SD':sd, 'CV':cv, 'eA1c':ea1c, 
                    'Min. glucose':min_glc, 'Max. glucose':max_glc, 'AUC': auc}
        results.update(glyc_var)

        # LBGI and HBGI
        bgi = metrics_helper.helper_bgi(df)
        results.update(bgi)
        
        # MAGE
        mage_results = metrics_helper.mage_helper(df)
        results.update(mage_results)

        # Time in ranges
        ranges = metrics_helper.tir_helper(df.glc)
        results.update(ranges)

        # New method
        #hypos = metrics_helper.number_of_hypos(df)
        #results.update(hypos)

        # Old method 
        old_hypos, breakdown = metrics_helper.helper_hypo_episodes(df, gap_size=interval)
        results.update(old_hypos)
        
        # Amount of data available
        data_sufficiency = metrics_helper.helper_missing(df,  gap_size=interval)
        results.update(data_sufficiency)                        

        return results
    
        
        
    else:
        print('EXPLODE THE PROGRAM')


