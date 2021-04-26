import numpy as np
import pandas as pd

#from ipysheet import from_dataframe, to_dataframe, cell, row, column, cell_range

import qgrid

COL_COUNT = 'count'
COL_KEEP = 'keep'

def show_keep_grid(df, column_to_group_by, column_to_count, keep_array):
    df_possible = df.groupby(column_to_group_by)[column_to_count].nunique()
    df_possible = df_possible.reset_index()
    df_possible = df_possible.rename(columns={column_to_count: COL_COUNT})

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

def convert_keep_sheet_to_df(sheet):
    return to_dataframe(sheet)

def get_keep_possibilites_df(df, column_to_group_by, column_to_count, keep_array):
    df_possible = df.groupby(column_to_group_by)[column_to_count].nunique()
    df_possible = df_possible.reset_index()
    df_possible = df_possible.rename(columns={column_to_count: COL_COUNT})

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