import pandas as pd
import sys
'''import sys, os
print(sys.path)'''
print(sys.path)
#example1 = pd.read_csv('example1.csv')  #'../test-data/example1.csv')
#example2 = pd.read_csv('../test-data/example2.csv')
'''
sys.path.append('c:\\Users\\cr591\\OneDrive - University of Exeter\\Desktop\\PhD\\Projects\\diametrics-webapp-dash\\code\\')
print(sys.path)
import metrics_helper'''
# test the 3 different outcomes of check_df function
def test_check_df1():
    assert metrics_helper.check_df(example1) == True

def test_check_df2():
    assert metrics_helper.check_df(example2) == False

def test_check_df3():
    assert metrics_helper.check_df(10) == False