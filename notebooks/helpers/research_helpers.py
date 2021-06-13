import os
import numpy as np
import pandas as pd
import qgrid
import datetime
import glob

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from ipywidgets import *
from IPython.core.display import display, HTML

from collections import OrderedDict

ARRAY_FOLDERS_TO_IGNORE = ['.ipynb_checkpoints', 
                           'About the Member Population', 
                           'Archive', 
                           'AllActive', 
                           'Brad', 
                           'Member Lists', 
                           'notebooks', 
                           'Opt Out Lists', 
                           'Sampling R Code']

#OPTIONS_CSV_COLUMNS = []
#OPTIONS_EXISTING_PROJECTS = []
#OPTIONS_LOCATIONS = []
#OPTIONS_YES_NO = ['Yes','No']
#OPTIONS_NEW_PROJECT = ['<New Project>']
#OPTIONS_PREV_DATAFRAMES = ['<Revert to previous state (dataframe)>']

dict_keep_lists = {}    # Used to keep dictionary of arrays used to pre-select items used in qgrid filtering
dict_dataframes = {}    # Used to keep track of order of changes to the active roster list 
dict_filter_by = {}     # Used by keep_grid_show_filter

#grid_work_do = None

CSV_SEPARATOR = ','     # '\t'

FLDR_MEMBER_LISTS = 'Member Lists'
FLDR_SAMPLING = '../sampling'
FLDR_NOTEBOOKS = '../notebooks'

FNAME_ACTIVE_ROSTER_CSV = 'all_active.csv'

COL_COUNT = 'count'
COL_KEEP = 'keep'
COL_REMOVE = 'remove'

"""
COL_EMAIL = 'email'
COL_EXPIRY_DATE = 'expiration_date'
COL_EXPIRY_RANGE_CALCULATED = 'expiration_range_calculated'
COL_MEMBER_ID = 'member_id'
COL_MEMBERSHIP_ITEM = 'membership_item'

COL_EMAIL_DOMAIN = 'email_domain'
COL_INDUSTRY = 'industry'
COL_ORG_TYPE = 'organization_type'
COL_PUB_PRIVATE_CALCULATED = 'pub_private_calculated'

COL_JOB_TITLE = 'job_title'
COL_BOSS_TITLE = 'supervisor_title'
COL_NUM_OVERSEEN = 'employee_oversee'
COL_TITLE_CALCULATED = 'title_calculated'

COL_REGION_CALCULATED = 'region_calculated'
COL_LOCATION_CALCULATED = 'location_calculated'

EXPIRED_IN_MORE_THAN_180 = '(1) Expired more than 180 days'
EXPIRED_WITHIN_180 = '(2) Expired within 180 days'
EXPIRED_WITHIN_90 = '(3) Expired within 90 days'
EXPIRED_WITHIN_30 = '(4) Expired within 30 days'
EXPIRES_WITHIN_30 = '(5) Expires within 30 days'
EXPIRES_WITHIN_90 = '(6) Expires within 90 days'
EXPIRES_WITHIN_180 = '(7) Expires within 180 days'
EXPIRES_IN_MORE_THAN_180 = '(8) Expires in more than 180'


KEEP_LIST_SURVEY_DIRS = []

KEEP_LIST_EXPIRES_IN = [
    EXPIRES_WITHIN_30,
    EXPIRES_WITHIN_90,
    EXPIRES_WITHIN_180,
    EXPIRES_IN_MORE_THAN_180
    ]
"""

COL_EMAIL = 'email'
COL_EXPIRY_DATE = 'expiration_date'
COL_JOB_TITLE = 'job_title'
COL_LOCATION_CALCULATED = 'location_calculated'
COL_MEMBER_ID = 'member_id'
COL_MEMBERSHIP_ITEM = 'membership_item'
COL_REGION_CALCULATED = 'region_calculated'

dict_keep_lists[COL_LOCATION_CALCULATED] = [
    "US"
    ]

dict_keep_lists[COL_JOB_TITLE] = [
    "",
    "Administrative Assistant ",
    "Administrator",
    "Asst. or Assoc. Vice Pres",
    "CHRO, CHCO",
    "Coordinator",
    "Director or Asst/Assoc Director",
    "Legal Counsel",
    "Manager, Generalist",
    "Other",
    "Partner, Principal",
    "President, CEO, Chairman",
    "Representative, Associate",
    "Specialist",
    "Supervisor",
    "VP or Asst/Assoc VP"
    ]

dict_keep_lists[COL_MEMBERSHIP_ITEM] = [
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

dict_keep_lists[COL_REGION_CALCULATED] = [
    "",
    "Northeast",
    "South",
    "Midwest",
    "West"
    ]

def get_keep_list(column_name):
    if column_name in dict_keep_lists.keys():
        return dict_keep_lists[column_name]
    else:
        return []

def load_existing_projects(OPTIONS_ARRAY):
    if len(OPTIONS_ARRAY) == 0:
        OPTIONS_ARRAY = np.array([])
        dirs = os.scandir(path = FLDR_SAMPLING)
        for entry in dirs :
            if entry.is_dir() and entry.name not in ARRAY_FOLDERS_TO_IGNORE:
                OPTIONS_ARRAY = np.append (OPTIONS_ARRAY, [entry.name])
    
    return OPTIONS_ARRAY

def build_dropdown(option_array, option_selected = None, label = 'Please Select'):
    #if new_option:
    #    option_array = np.insert (option_array, 0, new_option)
    #    #option_array = np.append (option_array, new_option)
    
    if label is None:
        label = 'Please Select'
    
    if option_selected:
        dd = widgets.Dropdown(
            options=option_array,
            value=option_selected,
            description=label,
            disabled=False,
            layout=widgets.Layout(width="500px")
        )
    else:
        dd = widgets.Dropdown(
            options=option_array,
            description=label,
            disabled=False,
            layout=widgets.Layout(width="50%")
        )
    
    return dd

def load_csv(file_name):
    df = pd.read_csv (file_name , sep=CSV_SEPARATOR)
    df.columns= df.columns.str.lower()
    # convert column to datetime
    if COL_EXPIRY_DATE in df.columns:
        df[COL_EXPIRY_DATE] = pd.to_datetime(df[COL_EXPIRY_DATE])

    return df
    
    #print('There are {} email addresses available for use.'.format(len(df_all_active_roster)))


def keep_grid_show_filter(df, column_to_group_by, column_to_count, keep_array, bkeep_all = False):
    action_name  = column_to_group_by + '_'

    dict_filter_by[action_name + 'label'] = widgets.HTML()
    dict_filter_by[action_name + 'label'].value = '<center><h3>Your current record count is <u>{}</u></h3></center>'.format(len(df))
    dict_filter_by[action_name + 'results_widgets'] = widgets.HBox([dict_filter_by[action_name + 'label']])

    def handle_all_events(event, qgrid_widget):
        df_testing = keep_grid_apply_filter(dict_filter_by[action_name + 'qgrid_sheet_to_keep'], column_to_group_by, df)
        dict_filter_by[qgrid_widget.action_name + 'label'].value = '<h3>Your possible record count is <b><u>{}</u></b> out of <u>{}</u></h3>'.format(len(df_testing), len(df))

    # Allow user's to select which groups, if any, they want to keep
    dict_filter_by[action_name + 'qgrid_sheet_to_keep'] = __keep_grid_show_filter(df, column_to_group_by, column_to_count, keep_array)
    setattr(dict_filter_by[action_name + 'qgrid_sheet_to_keep'], 'action_name', action_name)
    handle_all_events(None, dict_filter_by[action_name + 'qgrid_sheet_to_keep'])

    dict_filter_by[action_name + 'qgrid_sheet_to_keep'].on('cell_edited', handle_all_events)
    dict_filter_by[action_name + 'dashboard'] = widgets.VBox([dict_filter_by[action_name + 'results_widgets'], dict_filter_by[action_name + 'qgrid_sheet_to_keep']])
    display(dict_filter_by[action_name + 'dashboard'])

    return dict_filter_by[action_name + 'qgrid_sheet_to_keep']

def __keep_grid_show_filter(df, column_to_group_by, column_to_count, keep_array, bkeep_all = False):
    msg_html = '<h1>Important:</h1></br><b>Please examine the list below and check/uncheck any record types you do not wish to use.</br></br>NOTE: </b><span>The default keep list has already been pre-selected.</span>'
    display(HTML(msg_html))
    
    if column_to_count is None:
        df_possible = df
        df_possible = df_possible.reset_index()
    else:
        df[column_to_group_by] = df[column_to_group_by].fillna('')
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
            if bkeep_all:
                bKeep = True
            df_possible.at[i,COL_KEEP] = bKeep

        df_possible = df_possible.sort_values([COL_KEEP, column_to_group_by], ascending = (True, True))
        
    qgrid_widget = qgrid.show_grid(df_possible, show_toolbar=False, grid_options={"maxVisibleRows": 10})
    return qgrid_widget

def keep_grid_apply_filter(qgrid_sheet_to_keep, col_name, df, bShowUpdate=False):
    ### Apply filtering
    ### qgrid method to convert sheet to df
    df_filter_by = qgrid_sheet_to_keep.get_changed_df()
    df_filter_by = df_filter_by[df_filter_by[COL_KEEP] == True]

    arr_keep = df_filter_by[col_name].tolist()
    
    len_before_filter = len(df)
    df_filtered_list = df[df[col_name].isin(arr_keep)] 
    len_after_filter = len(df_filtered_list)

    if bShowUpdate:
        print('The filter was successfully applied to the data frame.')
        print('There are now {} out of {} items available for use.'.format(len_after_filter, len_before_filter))

    if bShowUpdate:
        return df_filtered_list, arr_keep
    else:
        return df_filtered_list

