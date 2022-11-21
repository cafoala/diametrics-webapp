import pandas as pd
import sys # added!

#sys.path.append("../..")
#import os
#dirname = os.path.dirname(__file__)
#filename = os.path.join(dirname, '../../code')
#from code.metrics_helper import tir_helper
from code.metrics_helper import tir_helper

example1 = [2.9, 3, 3.8, 3.9, 4, 9.9, 10, 10.1, 13.8, 13.9, 14]
test_data = pd.Series(example1)
results = tir_helper(test_data)



def test_tir_keys():
    # maybe here i could assert it's not empty
    expected_keys = set(['TIR normal', 'TIR hypoglycemia',
    'TIR level 1 hypoglycemia',
    'TIR level 2 hypoglycemia',
    'TIR hyperglycemia',
    'TIR level 1 hyperglycemia',
    'TIR level 2 hyperglycemia'])

    actual_keys = set(results.keys())

    assert expected_keys.issubset(actual_keys) & actual_keys.issubset(expected_keys)


def test_tir_normal():
     assert results['TIR normal'] == 36.36

def test_tir_hypo():
     assert results['TIR hypoglycemia'] == 27.27

def test_tir_hypo_lv1():
     assert results['TIR level 1 hypoglycemia'] == 18.18

def test_tir_hypo_lv2():
     assert results['TIR level 2 hypoglycemia'] == 9.09

def test_tir_hyper():
     assert results['TIR hyperglycemia'] == 36.36

def test_tir_hyper_lv1():
     assert results['TIR level 1 hyperglycemia'] == 27.27

def test_tir_hyper_lv2():
     assert results['TIR level 2 hyperglycemia'] == 9.09