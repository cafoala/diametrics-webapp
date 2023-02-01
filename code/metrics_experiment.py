import pandas as pd
import metrics_helper
import numpy as np

def calculate_all_metrics(df, units='mmol/L', additional_tirs=None, lv1_hypo=3.9, lv2_hypo=3.0, lv1_hyper=10, lv2_hyper=13.9,  event_mins=15, event_long_mins=120):
    factor = 0.0557
    if metrics_helper.check_df(df):
        # create a list to add the results to
        results = {}#{'ID': ID}
        results_mg = {}#{'ID': ID}
        df = df.dropna(subset=['glc']).reset_index(drop=True)
        # Convert to mmol/L
        if units == 'mg/dL':
            df['glc'] = df['glc']*factor
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
        glyc_var_mg =  {}
        for i in glyc_var:
            glyc_var_mg[i] = glyc_var[i]/factor         
        results_mg.update(glyc_var_mg)

        # LBGI and HBGI
        bgi = metrics_helper.helper_bgi(df['glc'], 'mmol/L')
        results.update(bgi)
        #bgi_mg = metrics_helper.helper_bgi(df['glc'], 'mg/dL')
        results_mg.update(bgi)
        
        # MAGE
        mage_results = metrics_helper.mage_helper(df)
        results.update(mage_results)
        mage_mg = {'MAGE':mage_results['MAGE']/factor}
        results_mg.update(mage_mg)

        # Time in ranges
        ranges = metrics_helper.tir_helper(df.glc)
        results.update(ranges)
        results_mg.update(ranges)

        unique_ranges = metrics_helper.calculate_unique_tirs(df.glc, additional_tirs, units)
        results.update(unique_ranges)
        results_mg.update(unique_ranges)
        
        # New method
        hypos = metrics_helper.calculate_glycemic_episodes(df, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, event_mins, event_long_mins)
        results.update(hypos)
        results_mg.update(hypos)
        
        # Old method
        #old_hypos, breakdown = metrics_helper.helper_hypo_episodes(df, gap_size=interval, lv1_threshold=lv1_hypo, lv2_threshold=lv2_hypo)
        #results.update(old_hypos)
        #results_mg.update(old_hypos)
        
        # Amount of data available
        #data_sufficiency = metrics_helper.helper_missing(df,  gap_size=interval)
        #results.update(data_sufficiency)   
        # Convert to df
        results = pd.DataFrame.from_dict([results])
        results_mg = pd.DataFrame.from_dict([results_mg])

        return results, results_mg
    
    else:
        print('EXPLODE THE PROGRAM')


