import numpy as np
import pandas as pd

#from ipysheet import from_dataframe, to_dataframe, cell, row, column, cell_range

import qgrid

COL_COUNT = 'count'
COL_KEEP = 'keep'

MEMBER_ID = 'member_id'
MEMBERSHIP_ITEM = 'membership_item'

KEEP_LIST_MEMBERSHIP_ITEMS = [
    "Affinity Membership",
    "Corporate Membership",
    "Corporate Membership-three month extention",
    "Global Online Comp Membership - 1 Month",
    "Global Online Comp Membership - 3 Month",
    "Global Online Comp Membership - 6 Month",
    "Global Online Membership",
    "Global Online Membership - 2 Year",
    "Global Online Membership - 3 Year",
    "Professional Comp Membership - 1 Month",
    "Professional Comp Membership - 3 Month",
    "Professional Comp Membership - 6 Month",
    "Professional Membership",
    "Professional Membership - 2 Year",
    "Professional Membership - 3 Year",
    "Professional Membership - 6 Month",
    "SHRM Complimentary Membership - 1 year",
    "SHRM Life Membership",
    "SHRM Life Membership Renewal"
    ]

def keep_grid_show_filter(df, column_to_group_by, column_to_count, keep_array):
    df_possible = df.groupby(column_to_group_by)[column_to_count].nunique()
    df_possible = df_possible.reset_index()
    df_possible = df_possible.rename(columns={column_to_count: COL_COUNT})

    if keep_array is None:
        df_possible = df_possible.sort_values([column_to_group_by], ascending = (True))
    else:
        df_possible[COL_KEEP] = False               # set default value to False
        df_possible.astype({COL_KEEP: 'bool'}).dtypes
        # update 'keep' column based on presence of MEMBERSHIP_ITEM in keep list
        for i, row in df_possible.iterrows():
            bKeep = False
            if row[column_to_group_by] in keep_array:
                bKeep = True
            df_possible.at[i,COL_KEEP] = bKeep

        df_possible = df_possible.sort_values([COL_KEEP, column_to_group_by], ascending = (True, True))

    #sheet_keep = from_dataframe(df_possible)
    #return sheet_keep

    qgrid_widget = qgrid.show_grid(df_possible, show_toolbar=False)
    return qgrid_widget

def keep_grid_apply_filter(qgrid_sheet_to_keep, col_name, df):
    ### Apply filtering
    ### qgrid method to convert sheet to df
    df_filter_by = qgrid_sheet_to_keep.get_changed_df()
    df_filter_by = df_filter_by[df_filter_by[COL_KEEP] == True]

    arr_keep = df_filter_by[col_name].tolist()

    len_before_filter = len(df)
    df_filtered_list = df[df[col_name].isin(arr_keep)] 
    len_after_filter = len(df_filtered_list)
    print('There are {} out of {} email addresses available for use.'.format(len_after_filter, len_before_filter))
    
    return df_filtered_list

def convert_keep_sheet_to_df(sheet):
    return to_dataframe(sheet)

def get_keep_possibilites_df(df, column_to_group_by, column_to_count, keep_array):
    df_possible = df.groupby(column_to_group_by)[column_to_count].nunique()
    df_possible = df_possible.reset_index()
    df_possible = df_possible.rename(columns={column_to_count: COL_COUNT})
    
    if keep_array is None:
        df_possible = df_possible.sort_values([column_to_group_by], ascending = (True))
    else:
        df_possible[COL_KEEP] = False               # set default value to False
        df_possible.astype({COL_KEEP: 'bool'}).dtypes
        # update 'keep' column based on presence of MEMBERSHIP_ITEM in keep list
        for i, row in df_possible.iterrows():
            bKeep = False
            if row[column_to_group_by] in keep_array:
                bKeep = True
            df_possible.at[i,COL_KEEP] = bKeep

        df_possible = df_possible.sort_values([COL_KEEP, column_to_group_by], ascending = (True, True))

    return df_possible

if __name__ == "__main__":
    pass