import os
import numpy as np
import pandas as pd
import qgrid
import datetime

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from ipywidgets import *
from IPython.core.display import display, HTML

dict_filter_by = {}     # Used by keep_grid_show_filter

CSV_SEPARATOR = ','     # '\t'

FLDR_SAMPLING = '../sampling'
FLDR_NOTEBOOKS = '../notebooks'

COL_COUNT = 'count'
COL_KEEP = 'keep'

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

KEEP_LIST_JOB_TITLES = [
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

def __assign_assign_pub_private_sector(str_org_type, str_industry, str_email_domain):

    value = 'Private'
    try:
        if len(str_org_type) == 0 and len(str_industry) == 0:
            value = 'Private'
        elif len(str_org_type) == 0 and (str_industry == "Education" or str_industry == "Government"):
            value = 'pub_ed'
        elif len(str_org_type) == 0 and str_industry != "Education" and str_industry != "Government":
            value = 'Private'
        elif len(str_industry) == 0 and (str_org_type == "Govt Sector - Federal" or str_org_type == "Govt Sector - State/Local"):
            value = 'pub_ed'
        elif len(str_industry) == 0 and str_org_type != "Govt Sector - Federal" and str_org_type != "Govt Sector - State/Local":
            value = 'Private'
        elif str_email_domain[-4:] == '.gov':
            value = 'pub_ed'
        elif str_org_type == "Govt Sector - Federal" or str_org_type == "Govt Sector - State/Local" or str_industry == "Education" or str_industry == "Government":
            value = 'pub_ed'
        else:
            value = 'Private'
    except:
        raise Exception('Houston, we have a problem')    
    
    #print('OrgType = {}, Indus = {}, Domain = {}, value = {}, '.format(str_org_type, str_industry, str_email_domain[-4:], value))
    return value

def assign_pub_private_sector(df):
    #Determine who is public/private based off of org_type, industry and domain
    df[COL_EMAIL_DOMAIN] = df[COL_EMAIL_DOMAIN].fillna('')
    df[COL_INDUSTRY] = df[COL_INDUSTRY].fillna('')
    df[COL_ORG_TYPE] = df[COL_ORG_TYPE].fillna('')

    df[COL_PUB_PRIVATE_CALCULATED] = df.apply(lambda x: __assign_assign_pub_private_sector(x[COL_ORG_TYPE].strip(), x[COL_INDUSTRY].strip(), x[COL_EMAIL_DOMAIN].strip()), axis=1)
    
    print('Assigned Pub/Private Sector.')
    
    return df

def __assign_title(str_job_title, str_boss_title, str_num_overseen, mgmt_titles):

    title = 'Worker'
    try:
        """
        if str_job_title.lower() in mgmt_titles:
            title = 'Manager'
        elif str_job_title == "Manager, Generalist" and str_boss_title.lower() != "administrator" and str_boss_title.lower() != "hr manager" and str_num_overseen != "0":
            title = 'Manager'
        """
        if len(str_job_title) == 0:
            title = 'Worker'
        elif str_job_title.lower() in mgmt_titles:
            title = 'Manager'
        elif len(str_boss_title) == 0 or len(str_num_overseen) == 0:
            title = 'Worker'
        elif str_job_title == "Manager, Generalist" and (str_boss_title.lower() == "administrator" or str_boss_title.lower() == "hr manager" or str_num_overseen == "0"):
            title = 'Worker'
        elif str_job_title == "Manager, Generalist" and str_boss_title.lower() != "administrator" and str_boss_title.lower() != "hr manager" and str_num_overseen != "0":
            title = 'Manager'
        else:
            title = 'Worker'
    except:
        raise Exception('Houston, we have a problem')

    return title

def assign_title(df):
    #Who is a manager vs. a worker> To align with BLS, if they have a manager job title, Manager, otherwise worker. 
    #Our category "Manager, Generalist" is ambiguous, so if they report to a manager or administrator, or have no direct reports we treat them as worker
            
    mgmt_titles = ["Partner, Principal","President, CEO, Chairman","CHRO, CHCO","VP or Asst/Assoc VP","Asst. or Assoc. Vice Pres","Director or Asst/Assoc Director","Supervisor"]
    mgmt_titles = [title.lower() for title in mgmt_titles]

    #nonmgmtTitles = ["Consultant","Coordinator","Legal Counsel","Representative, Associate","Specialist","Other","Administrative Assistant","Administrator"]
    #nonmgmtTitles = [title.lower() for title in nonmgmtTitles]

    df[COL_JOB_TITLE] = df[COL_JOB_TITLE].fillna('')
    df[COL_BOSS_TITLE] = df[COL_BOSS_TITLE].fillna('')
    df[COL_NUM_OVERSEEN] = df[COL_NUM_OVERSEEN].fillna('')

    df[COL_TITLE_CALCULATED] = df.apply(lambda x: __assign_title(x[COL_JOB_TITLE].strip(), x[COL_BOSS_TITLE].strip(), x[COL_NUM_OVERSEEN].strip(), mgmt_titles), axis=1)
    
    print('Assigned Manager/Worker Title.')
    
    return df

def __assign_expiration_range(str_expiry_date):
    str_expires_in = 'unkown'
    try:
        if str_expiry_date < datetime.datetime.now():
            if str_expiry_date >= (datetime.datetime.now() - datetime.timedelta(days=30)):
                str_expires_in = EXPIRED_WITHIN_30
            elif str_expiry_date >= (datetime.datetime.now() - datetime.timedelta(days=90)):
                str_expires_in = EXPIRED_WITHIN_90
            elif str_expiry_date >= (datetime.datetime.now() - datetime.timedelta(days=180)):
                str_expires_in = EXPIRED_WITHIN_180
            else:
                str_expires_in = EXPIRED_IN_MORE_THAN_180
        if str_expiry_date >= datetime.datetime.now():
            if str_expiry_date <= (datetime.datetime.now() + datetime.timedelta(days=30)):
                str_expires_in = EXPIRES_WITHIN_30
            elif str_expiry_date <= (datetime.datetime.now() + datetime.timedelta(days=90)):
                str_expires_in = EXPIRES_WITHIN_90
            elif str_expiry_date <= (datetime.datetime.now() + datetime.timedelta(days=180)):
                str_expires_in = EXPIRES_WITHIN_180
            else:
                str_expires_in = EXPIRES_IN_MORE_THAN_180
    except:
        raise Exception('Houston, we have a problem')
    if str_expires_in == 'unkown':
        print('Date= {}, expires_in= {}'.format(str_expiry_date, str_expires_in))
    return str_expires_in

def assign_expiration_range(df):
    #EXPIRY_DATE = 'expiration_date'
    #EXPIRY_RANGE_CALCULATED = 'expiration_range_calculated'

    df[COL_EXPIRY_DATE] = df[COL_EXPIRY_DATE].fillna('')

    df[COL_EXPIRY_RANGE_CALCULATED] = df.apply(lambda x: __assign_expiration_range(x[COL_EXPIRY_DATE]), axis=1)
    
    print('Assigned expiration range.')
    
    return df

def keep_grid_show_filter(df, column_to_group_by, column_to_count, keep_array, bkeep_all = False):
    action_name  = column_to_group_by + '_'

    #dict_filter_by = {}
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
    msg_html = '<h1>Important:</h1></br><b>Please examine the list below and check/uncheck any record types you do not wish to use.</br></br>NOTE: </b><span>The default list has already been pre-selected.</span>'
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
        
    #sheet_keep = from_dataframe(df_possible)
    #return sheet_keep

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

def load_csv(file_name):
    df = pd.read_csv (file_name , sep=CSV_SEPARATOR)
    df.columns= df.columns.str.lower()
    # convert column to datetime
    df[COL_EXPIRY_DATE] = pd.to_datetime(df[COL_EXPIRY_DATE])

    return df
    
    print('There are {} email addresses available for use.'.format(len(df_all_active_roster)))
