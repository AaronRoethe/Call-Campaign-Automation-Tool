import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

today = date.today()
tomorrow = (today + timedelta(days = 1))
yesterday = (today + timedelta(days = -1))

def formate_col(df, col, type):
    if type == 'date':
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    elif type == 'num':
        df[col] = pd.to_numeric(df[col], errors='coerce', downcast="integer")
    else:
        print('add new type')
    return df

def format(df):
    df.columns = df.columns.str.replace('/ ','')
    df = df.rename(columns=lambda x: x.replace(' ', "_"))
    df = formate_col(df, 'PhoneNumber', 'num')
    df = formate_col(df, 'Site_Clean_Id', 'num')
    df = formate_col(df, 'Last_Call', 'date')
    df = formate_col(df, 'Project_Due_Date', 'date')
    df = formate_col(df, 'Recommended_Schedule_Date', 'date')
    return df

def clean_num(df):
    filter1 = df['PhoneNumber'] < 1111111111
    filter2 = df['PhoneNumber'].isna()
    df['PhoneNumber'] = np.where(filter1 | filter2, 9999999999,df['PhoneNumber'])
    return df

def Last_Call(df):
    df.drop('Age', axis=1, inplace=True)
    df['age'] = (tomorrow - df['Last_Call']).dt.days

    f1 = df.Last_Call.isna()
    df.age = np.where(f1, df.DaysSinceCreation, df.age)
    
    f1 = df.age < df.DaysSinceCreation
    df.age = np.where(f1, df.age, df.DaysSinceCreation)

    return df

def check_load(df, today):
    df['Last Call'] = pd.to_datetime(df['Last Call'], errors='coerce')#.dt.date
    test_results = 'Pass' if any(df['Last Call'] == today.strftime('%Y-%m-%d')) else 'Fail'
    return df, test_results

### Covert fire flag with specific client project to a 5 day cycle _> add to RADV
def fire_flag(df, skill_name):
    filer1 = df['Score'].str[:1].isin(1,2,3)
    df['Outreach_Status'] = np.where(filer1, skill_name, df['Outreach_Status'])
    return df

def add_columns(df, tomorrow_str):
    ### init columns
    df['Load_Date'] = tomorrow_str
    ### score columns
    ### age
    # cut_bins = [0, 5, 10, 15, 20, 10000]
    # label_bins = [5, 10, 15, 20, 21]
    # df['age_category'] = pd.cut(df['age'], bins=cut_bins, labels=label_bins, include_lowest=True)
    # age_sort    = {21:0, 20:1, 15:2, 10:3, 5:4}
    # df['age_sort'] = df['age_category'].map(age_sort)
    ### map
    audit_sort  = {'RADV':1, 'Medicaid Risk':1, 'HEDIS':2, 'Specialty':3,  'ACA':6, 'Medicare Risk':5}
    df['audit_sort'] = df['Audit_Type'].map(audit_sort)
    ### use map 
    f1 = df.audit_sort <=2
    df['sla'] = np.where(f1, 5, 10)
    df['target_sla'] = np.where(f1, 4, 8)
    f1 = df.sla >= df.age
    df['meet_sla'] = np.where(f1, 1,0)
    df['meet_target_sla'] = np.where(f1, 1,0)
    ### togo charts
    bucket_amount = 100
    labels = list(([x for x in range(bucket_amount)]))
    df['togo_bin'] = pd.cut(df.ToGoCharts, bins=bucket_amount, labels=labels)
    df.togo_bin = df.togo_bin.astype(int)
    # no call flag
    f1 = df.Last_Call.isna()
    df['no_call'] = np.where(f1, 1, 0)
    # needed for merge
    df['PhoneNumber'] = df['PhoneNumber'].astype(str)
    return df

def clean(df, tomorrow_str):
    df = Last_Call(clean_num(format(df))).reset_index(drop=True)
    new_col = add_columns(df, tomorrow_str)
    return new_col

if __name__ == "__main__":
    print('test')
