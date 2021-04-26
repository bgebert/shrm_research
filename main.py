####    This can be removed once the SHRM Helper Utility library is written
import enum
from logging import Filter
import sys
sys.path.insert(0, '/Users/bgebert/Scripts/SHRM/shrm_utilities/')
import shrm_utilities

from numpy.lib.utils import source

####    Import Libraries
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

FILENAME_CALCULATED_ROOT = 'calculated_'
FILENAME_MERGED_CALCULATED = 'calculated_merged.csv'
FILENAME_MERGED_PRETTY = 'merged.txt'

KEY_YEAR = "YEAR"
KEY_TOP_LEVEL = "TOP_LEVEL"
KEY_SUB_LEVEL = "SUB_LEVEL"
KEY_CATEGORY = "CATEGORY"
KEY_CUT = "CUT"
KEY_ITEM = "ITEM"
KEY_OFFERED_N = "OFFERED_N"
KEY_OFFERED_PERCENT = "OFFERED_PERCENT"
KEY_NOT_OFFERED_N = "NOT_OFFERED_N"
KEY_NOT_OFFERED_PERCENT = "NOT_OFFERED_PERCENT"
KEY_TOTAL_N = "TOTAL_N"
KEY_TOTAL_PERCENT = "TOTAL_PERCENT"
KEY_SIGNIFICANT = 'SIGNIFICANT'
KEY_P_VALUE = 'P_VALUE'



COLUMN_NAMES = [KEY_YEAR, KEY_TOP_LEVEL, KEY_SUB_LEVEL, KEY_CATEGORY, KEY_CUT, KEY_ITEM, KEY_OFFERED_N, KEY_OFFERED_PERCENT, KEY_NOT_OFFERED_N, KEY_NOT_OFFERED_PERCENT, KEY_TOTAL_N, KEY_TOTAL_PERCENT]
INDEX_NAMES = [KEY_TOP_LEVEL, KEY_SUB_LEVEL, KEY_CATEGORY, KEY_CUT, KEY_ITEM]
MAPPING_QUESTIONS_COLUMN_LOOKUP = 0
MAPPING_QUESTIONS_ITEM = 1
MAPPING_QUESTIONS_CATEGORY = 2
MAPPING_QUESTIONS_TABGROUP = 3

class FILTER_BY(Enum):
    ALL = 0
    ONE = 1
    NONE = 2

class CUT_BY(Enum):
    ALL = 0
    INDUSTRY = 1
    ORGSIZE = 2
    REGION = 3
    STATE = 4

def getSubLevel(toplevel, category):
    bFoundCategory = False
    if toplevel == RESEARCH_TYPE_BENEFITS:
        # SHRM.utils.healthcare
        if category == 'GenHealth':
            bFoundCategory = True
            return 'healthcare'
        elif category == 'HealthSavings':
            bFoundCategory = True
            return 'healthcare'
        elif category == 'PrescriptionDrugPlan':
            bFoundCategory = True
            return 'healthcare'
        elif category == 'Dental_Vision':
            bFoundCategory = True
            return 'healthcare'
        elif category == 'DisabilityAccident':
            bFoundCategory = True
            return 'healthcare'
        elif category == 'Specific_Services':
            bFoundCategory = True
            return 'healthcare'
        
        #SHRM.utils.retirement
        if category == 'Defined Contribution Retirement Savings Plan':
            bFoundCategory = True
            return 'retirement'
        elif category == 'Education and Financial':
            bFoundCategory = True
            return 'retirement'
        elif category == 'Other Retirement':
            bFoundCategory = True
            return 'retirement'
        elif category == 'Retirement':
            bFoundCategory = True
            return 'retirement'
        
        # SHRM.utils.leave
        if category == 'Family and Elder Care Leave':
            bFoundCategory = True
            return 'leave'
        elif category == 'Other Leave':
            bFoundCategory = True
            return 'leave'
        elif category == 'Leave for New Parents':
            bFoundCategory = True
            return 'leave'
        elif category == 'Vacation Sick Personal Leave':
            bFoundCategory = True
            return 'leave'
        
        # SHRM.utils.flexibility
        if category == 'Flexible Work':
            bFoundCategory = True
            return 'flexibility'
        
        # SHRM.utils.family
        if category == 'Family-Friendly':
            bFoundCategory = True
            return 'family'
        
        # SHRM.utils.profdev
        if category == 'Professional Career Development':
            bFoundCategory = True
            return 'profdev'
        
        # SHRM.utils.wellness
        if category == 'Wellness':
            bFoundCategory = True
            return 'wellness'

        if bFoundCategory != True:
            shrm_logger.logger.error ("Unable to find a CATEGORY for: " + toplevel + ' and ' + category)
            return 'NOT_MAPPED'

def loadMappings(sourceDir, year):
    try:
        df_map_questions = None
        if path.exists(sourceDir + 'mappings_questions.csv'):
            df_map_questions = pd.read_csv (sourceDir + 'mappings_questions.csv', sep=CSV_SEPARATOR, header=None)

        df_map_columns = None
        if path.exists(sourceDir + 'mappings_columns.csv'):
            df_map_columns = pd.read_csv (sourceDir + 'mappings_columns.csv', sep=CSV_SEPARATOR, header=None)

        df_map_region = None
        if path.exists(sourceDir + 'mappings_region.csv'):
            df_map_region = pd.read_csv (sourceDir + 'mappings_region.csv', sep=CSV_SEPARATOR, header=None)

        df_map_industry = None
        if path.exists(sourceDir + 'mappings_industry.csv'):
            df_map_industry = pd.read_csv (sourceDir + 'mappings_industry.csv', sep=CSV_SEPARATOR, header=None)

        df_map_orgsize = None
        if path.exists(sourceDir + 'mappings_orgsize.csv'):
            df_map_orgsize = pd.read_csv (sourceDir + 'mappings_orgsize.csv', sep=CSV_SEPARATOR, header=None)

        df_map_state = None
        if path.exists(sourceDir + 'mappings_state.csv'):
            df_map_state = pd.read_csv (sourceDir + 'mappings_state.csv', sep=CSV_SEPARATOR, header=None)

        df_map_all = None
        if path.exists(sourceDir + 'mappings_all.csv'):
            df_map_all = pd.read_csv (sourceDir + 'mappings_all.csv', sep=CSV_SEPARATOR, header=None)
        
        # setup mapping overrides
        if path.exists(sourceDir + year + '_mappings_questions.csv'):
            df_map_questions = pd.read_csv (sourceDir + year + '_mappings_questions.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_columns.csv'):
            df_map_columns = pd.read_csv (sourceDir + year + '_mappings_columns.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_region.csv'):
            df_map_region = pd.read_csv (sourceDir + year + '_mappings_region.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_industry.csv'):
            df_map_industry = pd.read_csv (sourceDir + year + '_mappings_industry.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_orgsize.csv'):
            df_map_orgsize = pd.read_csv (sourceDir + year + '_mappings_orgsize.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_state.csv'):
            df_map_state = pd.read_csv (sourceDir + year + '_mappings_state.csv', sep=CSV_SEPARATOR, header=None)

        if path.exists(sourceDir + year + '_mappings_all.csv'):
            df_map_all = pd.read_csv (sourceDir + year + '_mappings_all.csv', sep=CSV_SEPARATOR, header=None)

        return df_map_questions, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all

    except:
        shrm_mailer.send_email('Error: Failed inside membership_roster_prep','Error\n\nFailed inside membership_roster_prep - loadMappings\n\n error:\n\n', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
        pass

def getCount(df, dfColumn, bOffered):
    if is_numeric_dtype(dfColumn):
        if 1 in dfColumn.values or 2 in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn==1)])   # len(df[(dfColumn.astype(str)=='1')])
            else:
                return len(df[(dfColumn==2)])   # len(df[(dfColumn.astype(str)=='2')])
    elif is_string_dtype(dfColumn):
        if '1' in dfColumn.values or '2' in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn.astype(str)=='1')])
            else:
                return len(df[(dfColumn.astype(str)=='2')])
        elif 'Yes' in dfColumn.values or 'No' in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn.astype(str)=='Yes')])
            else:
                return len(df[(dfColumn.astype(str)=='No')])
        elif 'YES' in dfColumn.values or 'NO' in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn.astype(str)=='YES')])
            else:
                return len(df[(dfColumn.astype(str)=='NO')])
        elif 'yes' in dfColumn.values or 'no' in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn.astype(str)=='yes')])
            else:
                return len(df[(dfColumn.astype(str)=='no')])
        elif 'Offered' in dfColumn.values:
            if bOffered:
                return len(df[(dfColumn.astype(str)=='Offered')])
            else:
                dfColumn = dfColumn.fillna('')
                return len(df[(dfColumn.astype(str)=='')])    
    return 0

def do_calculations(research_type, filter_string, filter_friendly_string, df_calculated, df_raw, cutType, year, df_map_questions):
    for index, row in df_map_questions.iterrows():
        #print('\t\t\t"{}" : {} : {}'.format(filter_friendly_string, index, row[MAPPING_QUESTIONS_ITEM]))
        
        currentFieldName = row[MAPPING_QUESTIONS_COLUMN_LOOKUP]
        currentFieldName = currentFieldName.lower()
        
        rowDict = {}

        rowDict[KEY_YEAR] = year
        #rowDict[KEY_CATEGORY] = df_map_questions[df_map_questions[MAPPING_QUESTIONS_COLUMN_LOOKUP] == row[MAPPING_QUESTIONS_COLUMN_LOOKUP]][MAPPING_QUESTIONS_CATEGORY][index]
        rowDict[KEY_CATEGORY] = row[MAPPING_QUESTIONS_CATEGORY]
        #rowDict[KEY_CUT] = 'all'
        rowDict[KEY_TOP_LEVEL] = research_type
        #rowDict[KEY_SUB_LEVEL] = getSubLevel(rowDict[KEY_TOP_LEVEL], rowDict[KEY_CATEGORY])
        rowDict[KEY_SUB_LEVEL] = row[MAPPING_QUESTIONS_TABGROUP]
        
        #rowDict[KEY_ITEM] = df_map_questions[df_map_questions[MAPPING_QUESTIONS_COLUMN_LOOKUP] == row[MAPPING_QUESTIONS_COLUMN_LOOKUP]][MAPPING_QUESTIONS_ITEM][index]
        rowDict[KEY_ITEM] = row[MAPPING_QUESTIONS_ITEM]
        
        if rowDict[KEY_SUB_LEVEL] == 'NOT_MAPPED':
            shrm_logger.logger.error ("CATEGORY is not defined for: " + rowDict[KEY_TOP_LEVEL] + ' => ' + rowDict[KEY_CATEGORY] + ' => ' + rowDict[KEY_ITEM])

        if filter_string == '':
            filtered_df = df_raw
        else:
            try:
                filtered_df = df_raw.query(filter_string)
            except:
                raise Exception("do_calculations - Error, Could not filter dataset based on {}".format(filter_string))

        if currentFieldName in filtered_df.columns:
            offered_n = getCount(filtered_df, filtered_df[currentFieldName], True)
            not_offered_n = getCount(filtered_df, filtered_df[currentFieldName], False)
        else:
            shrm_logger.logger.error ("COLUMN defined in mappings_questions.csv, not defined in " + year + "_data.csv: " + currentFieldName)
            offered_n = 0
            not_offered_n = 0

        rowDict[KEY_OFFERED_N] = offered_n
        rowDict[KEY_NOT_OFFERED_N] = not_offered_n
        total_n = offered_n + not_offered_n
        rowDict[KEY_TOTAL_N] = total_n

        if total_n == 0:
            rowDict[KEY_TOTAL_PERCENT] = '0%'
            rowDict[KEY_OFFERED_PERCENT] = '0%'
            rowDict[KEY_NOT_OFFERED_PERCENT] = '0%'
        else:
            rowDict[KEY_TOTAL_PERCENT] = '100%'
            
            if offered_n == 0:
                rowDict[KEY_OFFERED_PERCENT] = '0%'
            else:
                rowDict[KEY_OFFERED_PERCENT] = str(round((offered_n / total_n)*100))+ '%'
            
            if not_offered_n == 0:
                rowDict[KEY_NOT_OFFERED_PERCENT] = '0%'
            else:
                if offered_n == 0:
                    rowDict[KEY_NOT_OFFERED_PERCENT] = '100%'
                else:
                    rowDict[KEY_NOT_OFFERED_PERCENT] = str(100-round((offered_n / total_n)*100)) + '%'  ### str(round(not_offered_n / total_n,2))[2:] 
    
        if filter_string == '':
            rowDict[KEY_CUT] = 'all'

        if cutType == CUT_BY.ALL:
            rowDict[KEY_CUT] = 'all'
        elif cutType == CUT_BY.INDUSTRY:
            rowDict[KEY_CUT] = filter_friendly_string
        elif cutType == CUT_BY.ORGSIZE:
            rowDict[KEY_CUT] = filter_friendly_string
        elif cutType == CUT_BY.REGION:
            rowDict[KEY_CUT] = filter_friendly_string
        elif cutType == CUT_BY.STATE:
            rowDict[KEY_CUT] = filter_friendly_string
    
        df_calculated = df_calculated.append(rowDict, ignore_index=True)

    return df_calculated

def query_append(research_type, arrFilter, arrFilterFriendly, df_calculated, df_raw, cutType, year, df_map_questions):
    filter_string = " & ".join(arrFilter)

    if len(arrFilter) == 0:
        filter_string = ''
    elif len(arrFilter) == 1:
        filter_string = arrFilter[0]
    
    filter_friendly_string = " & ".join(arrFilterFriendly)

    if len(arrFilterFriendly) == 0:
        filter_friendly_string = ''
    elif len(arrFilterFriendly) == 1:
        filter_friendly_string = arrFilterFriendly[0]

    df_calculated = do_calculations(research_type, filter_string, filter_friendly_string, df_calculated, df_raw, cutType, year, df_map_questions)
    
    return df_calculated

def query_by_one(research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions):
    start_time = time.time()
    print('Started {} at {}.'.format(cutType, str(datetime.now())))
    
    if cutType == CUT_BY.ALL:
        temp_df = df_map_all
        filter_column_display_name = 'ALL'
    elif cutType == CUT_BY.INDUSTRY:
        temp_df = df_map_industry
        filter_column = df_map_columns[(df_map_columns[0] == "industry")][1].item().lower()
        filter_column_display_name = 'INDUSTRY'
    elif cutType == CUT_BY.ORGSIZE:
        temp_df = df_map_orgsize
        filter_column = df_map_columns[(df_map_columns[0] == "orgsize")][1].item().lower()
        filter_column_display_name = 'ORGSIZE'
    elif cutType == CUT_BY.REGION:
        temp_df = df_map_region
        filter_column = df_map_columns[(df_map_columns[0] == "region")][1].item().lower()
        filter_column_display_name = 'REGION'
    elif cutType == CUT_BY.STATE:
        temp_df = df_map_state
        filter_column = df_map_columns[(df_map_columns[0] == "state")][1].item().lower()
        filter_column_display_name = 'STATE'

    for index, row in temp_df.iterrows():
        if cutType != CUT_BY.ALL:
            if str(row[0]) == '-1':
                arrFilter = []
            else:
                arrFilter = [filter_column + ' == ' + str(row[0])]
            arrFilterFriendly = [filter_column_display_name + ' == ' + str(row[1])]
        else:
            arrFilter = []
            arrFilterFriendly = [filter_column_display_name + ' == ' + str(row[1])]
        
        df_calculated = query_append(research_type, arrFilter, arrFilterFriendly, df_calculated, df_raw, cutType, year, df_map_questions)

    end_time = time.time()
    print('\tCompleted in {} seconds.'.format(str(end_time-start_time)))

    return df_calculated

def query_by_level_3(arrFilter, arrFilterFriendly, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_orgsize, df_map_all, df_map_questions):
    temp_arrFilter = []
    temp_arrFilterFriendly = []
    temp_df = df_map_orgsize
    filter_column = df_map_columns[(df_map_columns[0] == "orgsize")][1].item().lower()
    filter_column_display_name = 'ORGSIZE'
    for index, row in temp_df.iterrows():
        if index == 0:
            pass
        else:
            temp_arrFilter = arrFilter.copy()
            temp_arrFilter.append(filter_column + ' == ' + str(row[0]))

        temp_arrFilterFriendly = arrFilterFriendly.copy()
        temp_arrFilterFriendly.append(filter_column_display_name + ' == ' + str(row[1]))
        
        df_calculated = query_append(research_type, temp_arrFilter, temp_arrFilterFriendly, df_calculated, df_raw, cutType, year, df_map_questions)
    
    return df_calculated

def query_by_level_2(arrFilter, arrFilterFriendly, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_industry, df_map_orgsize, df_map_all, df_map_questions):
    temp_arrFilter = []
    temp_arrFilterFriendly = []
    temp_df = df_map_industry
    filter_column = df_map_columns[(df_map_columns[0] == "industry")][1].item().lower()
    filter_column_display_name = 'INDUSTRY'
    for index, row in temp_df.iterrows():
        if index == 0:
            pass
        else:
            temp_arrFilter = arrFilter.copy()
            temp_arrFilter.append(filter_column + ' == ' + str(row[0]))

        temp_arrFilterFriendly = arrFilterFriendly.copy()
        temp_arrFilterFriendly.append(filter_column_display_name + ' == ' + str(row[1]))
        
        df_calculated = query_by_level_3(temp_arrFilter, temp_arrFilterFriendly, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_orgsize, df_map_all, df_map_questions)

    return df_calculated

def query_by_level_1(region_state, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions):
    if region_state == 'region':
        arrFilter = []
        temp_df = df_map_region
        filter_column = df_map_columns[(df_map_columns[0] == "region")][1].item().lower()
        filter_column_display_name = 'REGION'
        for index, row in temp_df.iterrows():
            if index == 0:
                arrFilter = []
            else:
                arrFilter = [filter_column + ' == ' + str(row[0])]

            arrFilterFriendly = [filter_column_display_name + ' == ' + str(row[1])]
            
            df_calculated = query_by_level_2(arrFilter, arrFilterFriendly, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_industry, df_map_orgsize, df_map_all, df_map_questions)
    
    if region_state == 'state':
        arrFilter = []
        temp_df = df_map_state
        filter_column = df_map_columns[(df_map_columns[0] == "state")][1].item().lower()
        filter_column_display_name = 'STATE'
        for index, row in temp_df.iterrows():
            if index == 0:
                arrFilter = []
            else:
                arrFilter = [filter_column + ' == ' + str(row[0])]

            arrFilterFriendly = [filter_column_display_name + ' == ' + str(row[1])]
            
            df_calculated = query_by_level_2(arrFilter, arrFilterFriendly, research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_industry, df_map_orgsize, df_map_all, df_map_questions)
    
    return df_calculated

def query_by_all(research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions):
    df_calculated = query_by_level_1('region', research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
    df_calculated = query_by_level_1('state', research_type, df_calculated, df_raw, cutType, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)

    return df_calculated


def isSignificant(p, alpha):
    bSignificant = 0
    if p > alpha: 
        bSignificant = 1
    
    return bSignificant

def addChiSquare(arrConfig, sourceDir, outputFileName, alpha = 0.05):
    from scipy.stats import chi2_contingency
    import os.path
    from os import path

    try:
        if path.exists(sourceDir + '/' + outputFileName):
            df = pd.read_csv (sourceDir + '/' + outputFileName, sep=CSV_SEPARATOR)
            if KEY_SIGNIFICANT not in df.columns:
                df[KEY_SIGNIFICANT] = 0
                df[KEY_P_VALUE] = ''

            for i in df.index:
                #print(df.at[i, str(arrConfig[0]) + '_' + KEY_OFFERED_N], df.at[i, str(arrConfig[1]) + '_' + KEY_OFFERED_N])
                data = [[df.at[i, str(arrConfig[0]) + '_' + KEY_OFFERED_N], df.at[i, str(arrConfig[0]) + '_' + KEY_NOT_OFFERED_N]],[df.at[i, str(arrConfig[1]) + '_' + KEY_OFFERED_N], df.at[i, str(arrConfig[1]) + '_' + KEY_NOT_OFFERED_N]]]
                if not np.isnan(np.sum(data)):
                    stat, p, dof, expected = chi2_contingency(data) 
                    #print(df.at[i, KEY_ITEM] + ": ", isSignificant(p, alpha), "p value is " + str(p))
                    df.at[i, KEY_P_VALUE] = str(p)
                    df.at[i, KEY_SIGNIFICANT] = isSignificant(p, alpha)

            df.to_csv(sourceDir + '/' + outputFileName,sep=CSV_SEPARATOR, index=False, quoting=csv.QUOTE_NONNUMERIC)
    except:
        pass

def mergeRaw_Years(sourceDir, outputFileName):
    try:
        INDEX_NAMES = [KEY_TOP_LEVEL, KEY_SUB_LEVEL, KEY_CATEGORY, KEY_CUT, KEY_ITEM]
        df_master = pd.DataFrame() 
        ndx_dict = 0

        for file in glob.glob(sourceDir + '*.csv'):
            if FILENAME_MERGED_CALCULATED not in file:
                year = str(file[-8:-4])
                df = pd.read_csv (file, sep=CSV_SEPARATOR).rename(columns={\
                KEY_OFFERED_N: str(year) + '_' + KEY_OFFERED_N,\
                KEY_OFFERED_PERCENT: str(year) + '_' + KEY_OFFERED_PERCENT,\
                KEY_NOT_OFFERED_N: str(year) + '_' + KEY_NOT_OFFERED_N,\
                KEY_NOT_OFFERED_PERCENT: str(year) + '_' + KEY_NOT_OFFERED_PERCENT,\
                KEY_TOTAL_N: str(year) + '_' + KEY_TOTAL_N,\
                KEY_TOTAL_PERCENT: str(year) + '_' + KEY_TOTAL_PERCENT,\
                }).drop(columns=[KEY_YEAR])

                #print(df.head())

                if ndx_dict == 0:
                    df_master = df.copy()
                else:
                    df_master = pd.merge(df_master, df, on=INDEX_NAMES, how='outer')
                ndx_dict = ndx_dict + 1

        try:
            os.remove(sourceDir + '/' + outputFileName)
        except OSError:
            pass
        
        if len(df_master) > 0:
            #df_master = df_master[df_master[KEY_CUT] == 'all']  # just for fun.

            # reorder columns
            first_cols = [KEY_TOP_LEVEL, KEY_SUB_LEVEL, KEY_CATEGORY, KEY_CUT, KEY_ITEM]
            last_cols = [col for col in df_master.columns if col not in first_cols]
            df_master = df_master[first_cols+last_cols]

            df_master.to_csv(sourceDir + '/' + outputFileName,sep=CSV_SEPARATOR, index=False)

    except:
        shrm_mailer.send_email('Error: Failed inside membership_roster_prep','Error\n\nFailed inside membership_roster_prep - mergeRaw_Years\n\n error:\n\n', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
        #outputFile.write(primary_key + '\n')
        pass

def defineMgmtVsWorkers(df):
    JOB_TITLE = 'job_title'
    BOSS_TITLE = 'supervisor_title'
    NUM_OVERSEEN = 'employee_oversee'
    TITLE_CALCULATED = 'title_calculated'

    df[TITLE_CALCULATED] = 'Worker'

    mgmtTitles = ["Partner, Principal","President, CEO, Chairman","CHRO, CHCO","VP or Asst/Assoc VP","Asst. or Assoc. Vice Pres","Director or Asst/Assoc Director","Supervisor"]
    mgmtTitles = [title.lower() for title in mgmtTitles]

    nonmgmtTitles = ["Consultant","Coordinator","Legal Counsel","Representative, Associate","Specialist","Other","Administrative Assistant","Administrator"]
    nonmgmtTitles = [title.lower() for title in nonmgmtTitles]

    #df[JOB_TITLE].str.lower()
    #df[BOSS_TITLE].str.lower()

    df[JOB_TITLE] = df[JOB_TITLE].fillna('')
    df[BOSS_TITLE] = df[BOSS_TITLE].fillna('')
    df[NUM_OVERSEEN] = df[NUM_OVERSEEN].fillna('')

    for i, row in df.iterrows():
        title = ''
        if i == 628:
            print('{}'.format(i))
        #try:
        str_job_title = row[JOB_TITLE].lower()
        #except:
        #    str_job_title = ''

        #try:
        str_boss_title = row[BOSS_TITLE].lower()
        #except:
        #    str_boss_title = ''

        #try:
        str_num_overseen = row[NUM_OVERSEEN]
        #except:
        #    str_num_overseen = ''
        
        member_id = row['member_id']
        #print('{} ({}) row, Job Title == "{}", Boss Title == "{}", Num Overseen == "{}"'.format(i,member_id,str_job_title,str_boss_title,str_num_overseen))

        if len(str_job_title) == 0:
            title = 'Worker'
        elif str_job_title in mgmtTitles:
            title = 'Manager'
        elif str_job_title in nonmgmtTitles:
            title = 'Worker'
        elif len(str_boss_title) == 0 or len(str_num_overseen) == 0:
            title = 'Worker'
        elif str_job_title == "Manager, Generalist" and (str_boss_title == "administrator" or str_boss_title == "hr manager" or str_num_overseen == "0"):
            title = 'Worker'
        elif str_job_title == "Manager, Generalist" and str_boss_title != "administrator" and str_boss_title != "hr manager" and str_num_overseen != "0":
            title = 'Manager'
        else:
            title = 'Worker'

        if title == 'Manager':
            df[i, TITLE_CALCULATED] = title
            print('{} ({}) row, Job Title == "{}", Boss Title == "{}", Num Overseen == "{}", Title Calculated == "{}"'.format(i,member_id,str_job_title,str_boss_title,str_num_overseen,title))
        
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
            
    JOB_TITLE = 'job_title'
    BOSS_TITLE = 'supervisor_title'
    NUM_OVERSEEN = 'employee_oversee'
    TITLE_CALCULATED = 'title_calculated'

    mgmt_titles = ["Partner, Principal","President, CEO, Chairman","CHRO, CHCO","VP or Asst/Assoc VP","Asst. or Assoc. Vice Pres","Director or Asst/Assoc Director","Supervisor"]
    mgmt_titles = [title.lower() for title in mgmt_titles]

    #nonmgmtTitles = ["Consultant","Coordinator","Legal Counsel","Representative, Associate","Specialist","Other","Administrative Assistant","Administrator"]
    #nonmgmtTitles = [title.lower() for title in nonmgmtTitles]

    df[JOB_TITLE] = df[JOB_TITLE].fillna('')
    df[BOSS_TITLE] = df[BOSS_TITLE].fillna('')
    df[NUM_OVERSEEN] = df[NUM_OVERSEEN].fillna('')

    df[TITLE_CALCULATED] = df.apply(lambda x: __assign_title(x[JOB_TITLE], x[BOSS_TITLE], x[NUM_OVERSEEN], mgmt_titles), axis=1)
    
    return df

def _callback_process(research_type):
    try:
        start_time = time.time()
        sourceDir = shrm_config.cwd + '/working/'

        for file in glob.glob(sourceDir + '2021 P+S Democratization of Work (HR)_N33333_2021-03-19.csv'):
            #year = re.search(r'[12]\d{3}',file).group(0)

            # init dataframe
            #df_calculated = pd.DataFrame(columns = COLUMN_NAMES).set_index(INDEX_NAMES)

            df_raw = pd.read_csv (file, sep=CSV_SEPARATOR)
            df_raw = df_raw.rename(columns=str.lower)
            """
            JOB_TITLE = 'job_title'
            BOSS_TITLE = 'supervisor_title'
            NUM_OVERSEEN = 'employee_oversee'
            TITLE_CALCULATED = 'title_calculated'
            #df_raw[TITLE_CALCULATED] = 'Worker'

            mgmt_titles = ["Partner, Principal","President, CEO, Chairman","CHRO, CHCO","VP or Asst/Assoc VP","Asst. or Assoc. Vice Pres","Director or Asst/Assoc Director","Supervisor"]
            mgmt_titles = [title.lower() for title in mgmt_titles]

            df_raw[JOB_TITLE] = df_raw[JOB_TITLE].fillna('')
            df_raw[BOSS_TITLE] = df_raw[BOSS_TITLE].fillna('')
            df_raw[NUM_OVERSEEN] = df_raw[NUM_OVERSEEN].fillna('')

            df_raw[TITLE_CALCULATED] = df_raw.apply(lambda x: is_mngr_or_worker(x[JOB_TITLE], x[BOSS_TITLE], x[NUM_OVERSEEN], mgmt_titles), axis=1)
            """

            #Who is a manager vs. a worker> To align with BLS, if they have a manager job title, Manager, otherwise worker. 
            #Our category "Manager, Generalist" is ambiguous, so if they report to a manager or administrator, or have no direct reports we treat them as worker
            df_raw = assign_title(df_raw)
            df_raw.to_csv(sourceDir + 'Output.csv', index = False)

            end_time = time.time()
            print('\tTotal duration: {} seconds.'.format(str(end_time-start_time)))
            #df_raw = defineMgmtVsWorkers(df_raw)
            #print(df_raw.head())

            MEMBER_ID = 'member_id'
            MEMBERSHIP_ITEM = 'membership_item'
            MEMBER_COUNT = 'count'
            MEMBERSHIP_ITEM_KEEP = 'keep'

            keep_list = [
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

            df_membership_items = df_raw.groupby(MEMBERSHIP_ITEM)[MEMBER_ID].nunique()
            df_membership_items = df_membership_items.reset_index()
            df_membership_items.rename(columns={MEMBER_ID: MEMBER_COUNT})

            
            #df_membership_items[MEMBERSHIP_ITEM_KEEP] = False               # set default value to False
            # update 'keep' column based on presence of MEMBERSHIP_ITEM in keep list
            for i, row in df_membership_items.iterrows():
                bKeep = False
                if row[MEMBERSHIP_ITEM] in keep_list:
                    bKeep = True
                df_membership_items.at[i,MEMBERSHIP_ITEM_KEEP] = bKeep


            print(df_membership_items.head(n=40)) 
            
            


            df_map_questions, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all = loadMappings(sourceDir, year)
            """
            if filterBy == FILTER_BY.ONE:
                df_calculated = query_by_one(research_type, df_calculated, df_raw, CUT_BY.ALL, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
                df_calculated = query_by_one(research_type, df_calculated, df_raw, CUT_BY.INDUSTRY, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
                df_calculated = query_by_one(research_type, df_calculated, df_raw, CUT_BY.ORGSIZE, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
                df_calculated = query_by_one(research_type, df_calculated, df_raw, CUT_BY.REGION, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
                df_calculated = query_by_one(research_type, df_calculated, df_raw, CUT_BY.STATE, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
            
            elif filterBy == FILTER_BY.ALL:
                df_calculated = query_by_all(research_type, df_calculated, df_raw, CUT_BY.ALL, year, df_map_columns, df_map_region, df_map_industry, df_map_orgsize, df_map_state, df_map_all, df_map_questions)
            print(df_calculated.head())
            """
            filename = sourceDir + '/' + FILENAME_CALCULATED_ROOT + year + '.csv'
            try:
                os.remove(filename)
            except OSError:
                pass
            #df_calculated.to_csv(filename,sep=CSV_SEPARATOR, index=False, quoting=csv.QUOTE_NONNUMERIC)

        time.sleep(2)
        
        end_time = time.time()
        print('\tTotal duration: {} seconds.'.format(str(end_time-start_time)))

        mergeRaw_Years(sourceDir, FILENAME_MERGED_CALCULATED)

        time.sleep(2)

        arrConfig = [2019, 2020]
        addChiSquare(arrConfig, sourceDir, FILENAME_MERGED_CALCULATED)



    except:
        shrm_mailer.send_email('Error: Failed inside membership_roster_prep','Error\n\nFailed inside membership_roster_prep - _callback_process\n\n error:\n\n', True, [], shrm_config.get_configVal(shrm_config.SECTION_APP_CONFIG, 'email_error'), shrm_logger, shrm_config)
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
