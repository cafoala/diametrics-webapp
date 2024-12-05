import pandas as pd
import sys
from webapp_code import metrics_helper

# test the 3 different outcomes of check_df function
def test_check_df1():
    assert metrics_helper.check_df(pd.read_csv("tests/metrics/example1.csv")) == True

def test_check_df2():s
    assert metrics_helper.check_df(pd.read_csv("tests/metrics/example2.csv")) == False

def test_check_df3():
    assert metrics_helper.check_df(10) == False