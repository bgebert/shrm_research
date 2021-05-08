####    This can be removed once the SHRM Helper Utility library is written
import enum
from logging import Filter
import sys
sys.path.insert(0, '/Users/bgebert/Scripts/SHRM/shrm_utilities/')
import shrm_utilities

from numpy.lib.utils import source

####    Import Libraries
import sqlite3 as sl
import csv
import os
import os.path
from os import path
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import glob
import time
import re
from datetime import datetime
from enum import Enum

class RESEARCH_TYPE(Enum):
    RESEARCH = 0
    RESEARCH_MARKET = 1

CSV_SEPARATOR = ','     # '\t'

RESEARCH_TYPE_BENEFITS = 'benefits'

TBL_SURVEYS = 'SURVEYS'
TBL_MEMBERS = 'MEMBERS'
TBL_MEMBERS_TO_SURVEYS = 'MEMBERS_TO_SURVEYS'

SURVEYS_COL_SURVEY_ID = 'survey_id'
SURVEYS_COL_NAME = 'name'
SURVEYS_COL_DATE = 'date'

MEMBERS_COL_SURVEY_ID = 'member_id'
MEMBERS_COL_FNAME = 'first_name'
MEMBERS_COL_LNAME = 'last_name'
MEMBERS_COL_EMAIL = 'email'
MEMBERS_COL_LAST_SURVEY_DATE = 'last_survey_date'

def get_date_name (row):
    new_val = str(row['date']) + '___' + str(row['name'])
    return new_val

def get_unprocessed_survey_dirs(conn):
    # get list of processed survey dirs
    SQL_Query = pd.read_sql_query(
        '''select
        name,
        date
        from SURVEYS''', conn)
    df_saved_surveys = pd.DataFrame(SQL_Query, columns=['name', 'date'])
    surveys_dict = {}
    for index, row in df_saved_surveys.iterrows(): 
        surveys_dict[row['name']] = row['date']


    # find potential unprocessed survey dirs by iterating over folder names in s_drive and, 
    # comparing names to previously processed list
    df = pd.DataFrame(columns=['name','date'])
    for filename in glob.iglob('/Volumes/share/Departments/Research & Insights/Sampling/**/*.csv', recursive=True):
        if 'qualtrics' in filename.lower():
            match = re.search(r'\d{4}-\d{2}-\d{2}', filename.split('/')[-1])
            if match != None:
                survey_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            else:
                t = os.path.getmtime(filename)
                survey_date = datetime.fromtimestamp(t)

            survey_name = filename.split('/')[-2]

            # verify survey_name starts with a year
            match = re.match(r'.*([1-3][0-9]{3})', survey_name[:4])
            strts_with_year = False
            if match is not None:
                strts_with_year = True

            # verify survey_name starts with a year AND hasn't already been processed
            if survey_name not in surveys_dict and strts_with_year:
                surveys_dict[survey_name] = survey_date
                print('{}, on {}'.format(survey_name, survey_date.strftime('%Y-%m-%d')))
                new_row = {'name':survey_name, 'date': survey_date.strftime('%Y-%m-%d')}
                df = df.append(new_row, ignore_index=True)

    if len(df) > 0: # found new records, append to db
        return df
        #df.to_sql('SURVEYS', conn, if_exists='append', index = False)
        #conn.commit()
    else:
        return None

def get_old_survey_name_and_date():
    #import os.path, time
    
    #conn = sl.connect('./research_surveys.db')

    # get list of surveys previous processed
    SQL_Query = pd.read_sql_query(
        '''select
        name,
        date
        from SURVEYS''', conn)
    df_saved_surveys = pd.DataFrame(SQL_Query, columns=['name', 'date'])
    surveys_dict = {}
    for index, row in df_saved_surveys.iterrows(): 
        surveys_dict[row['name']] = row['date']
    
    # iterate over folder names in s_drive
    df = pd.DataFrame(columns=['name','date'])
    for filename in glob.iglob('/Volumes/share/Departments/Research & Insights/Sampling/**/*.csv', recursive=True):
        if 'qualtrics' in filename.lower():
            match = re.search(r'\d{4}-\d{2}-\d{2}', filename.split('/')[-1])
            if match != None:
                survey_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            else:
                t = os.path.getmtime(filename)
                survey_date = datetime.fromtimestamp(t)

            survey_name = filename.split('/')[-2]

            # verify survey_name starts with a year
            match = re.match(r'.*([1-3][0-9]{3})', survey_name[:4])
            strts_with_year = False
            if match is not None:
                strts_with_year = True

            # verify survey_name starts with a year AND hasn't already been processed
            if survey_name not in surveys_dict and strts_with_year:
                surveys_dict[survey_name] = survey_date
                print('{}, on {}'.format(survey_name, survey_date.strftime('%Y-%m-%d')))
                new_row = {'name':survey_name, 'date': survey_date.strftime('%Y-%m-%d')}
                df = df.append(new_row, ignore_index=True)

    if len(df) > 0: # found new records, append to db
        #conn = sl.connect('./research_surveys.db')
        #c = conn.cursor()
        df.to_sql('SURVEYS', conn, if_exists='append', index = False)
        conn.commit()

def get_old_survey_respondents():
    #import sqlalchemy

    SQL_Query = pd.read_sql_query(
        '''select
        survey_id,
        name,
        date
        from SURVEYS''', conn)
    df_saved_surveys = pd.DataFrame(SQL_Query, columns=['survey_id', 'name', 'date'])
    df_saved_surveys = df_saved_surveys.sort_values(by='date')

    # get list of members previous processed
    SQL_Query = pd.read_sql_query(
        '''select
        member_id,
        email
        from MEMBER''', conn)
    df_saved_members = pd.DataFrame(SQL_Query, columns=['member_id', 'email'])
    members_dict = {}
    for index, row in df_saved_members.iterrows(): 
        members_dict[row['member_id']] = row['email']
    
    # iterate over folder names in s_drive
    df = pd.DataFrame(columns=['member_id','first_name', 'last_name', 'email'])
    for filename in glob.iglob('/Volumes/share/Departments/Research & Insights/Sampling/**/*.csv', recursive=True):
        if 'qualtrics' in filename.lower():
            match = re.search(r'\d{4}-\d{2}-\d{2}', filename.split('/')[-1])
            if match != None:
                survey_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            else:
                t = os.path.getmtime(filename)
                survey_date = datetime.fromtimestamp(t)

            survey_name = filename.split('/')[-2]

            # verify survey_name starts with a year
            match = re.match(r'.*([1-3][0-9]{3})', survey_name[:4])
            strts_with_year = False
            if match is not None:
                strts_with_year = True

            # verify survey_name starts with a year AND hasn't already been processed
            if survey_name not in members_dict and strts_with_year:
                members_dict[survey_name] = survey_date
                print('{}, on {}'.format(survey_name, survey_date.strftime('%Y-%m-%d')))
                new_row = {'name':survey_name, 'date': survey_date.strftime('%Y-%m-%d')}
                df = df.append(new_row, ignore_index=True)

    if len(df) > 0: # found new records, append to db
        #conn = sl.connect('./research_surveys.db')
        #c = conn.cursor()
        df.to_sql('SURVEY', conn, if_exists='append', index = False)
        conn.commit()

def _callback_process(research_type):
    try:
        conn = sl.connect('/Volumes/share/Departments/Research & Insights/Sampling/research_surveys.db')
        cursor = conn.cursor()
        
        df_unprocessed_survey_dirs = get_unprocessed_survey_dirs(conn)
        if df_unprocessed_survey_dirs is None:
            print('There are no new survey directories to process :)')
        else:
            df_unprocessed_survey_dirs['date_name'] = df_unprocessed_survey_dirs.apply (lambda row: get_date_name(row), axis=1)
            df_unprocessed_survey_dirs.head()

        #get_old_survey_name_and_date() #Scans path for new survey folders and add them to the DB
        get_old_survey_respondents()

        conn.close()

    except:
        shrm_mailer.send_email('Error: Failed inside research_database','Error\n\nFailed inside research_database - _callback_process\n\n error:\n\n', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
        #outputFile.write(primary_key + '\n')
        pass

try:
    start_time = time.time()
    print('Started SCRIPT at ' + str(datetime.now()))

    ####    Initialize SHRM helper objects
    shrm_config = shrm_utilities.Config(os.path.dirname(os.path.realpath(__file__)))
    shrm_logger = shrm_utilities.Logger(shrm_config.cwd)
    shrm_mailer = shrm_utilities.mailer
    #shrm_webdriver = shrm_utilities.WebDriver(shrm_config.cwdtemp)
    
    ####    Do work
    _callback_process(RESEARCH_TYPE.RESEARCH)
    
    ####    Send email stating that the script is finished
    shrm_logger.logger.info('Terminated')
    shrm_mailer.send_email('Terminated: membership_roster_prep','', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_info'), shrm_logger, shrm_config)

    end_time = time.time()
    print('\tCompleted SCRIPT at ' + str(datetime.now()))
    print('\tCompleted SCRIPT in {} seconds.'.format(str(end_time-start_time)))

except Exception as e:
    #shrm_webdriver.cleanup_drivers()
    shrm_logger.logger.error("Error\n\nFailed inside membership_roster_prep\n\nwith error: ", exc_info=True)
    shrm_mailer.send_email('Error: membership_roster_prep (type=Exception)','', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
    pass
except SystemExit:
    #shrm_webdriver.cleanup_drivers()
    shrm_logger.logger.error ("Script ended prematurely.  Please check the log file.")
    shrm_mailer.send_email('Error: membership_roster_prep (type=Exception)','', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
    pass
except:
    #shrm_webdriver.cleanup_drivers()
    shrm_logger.logger.error("Error\n\nFailed inside membership_roster_prep\n\nwith error: ", exc_info=True)
    shrm_mailer.send_email('Error: membership_roster_prep (type=Exception)','', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
    pass
