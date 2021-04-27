import os
import urllib.request
import shutil
from zipfile import ZipFile

DIR_NOTEBOOK = './notebooks'
DIR_NOTEBOOK_HELPERS = './notebooks/helpers'
DIR_TMP = './tmp'
DIR_TMP_NOTEBOOK = './tmp/shrm_research-main/notebooks'
DIR_TMP_NOTEBOOK_HELPERS = './tmp/shrm_research-main/notebooks/helpers'
FILE_MAIN_ZIP = './main.zip'
URL = 'https://github.com/bgebert/shrm_research/archive/refs/heads/main.zip'

print('Deleting previous zip file.')
try:
    os.remove(FILE_MAIN_ZIP)
except:
    pass

print('Deleting tmp directory.')
try:
    shutil.rmtree(DIR_TMP)
except:
    pass

print('Creating tmp directory')
try:
    os.mkdir(DIR_TMP)
except:
    pass


def gen_files(dir, pattern):
   for dirname, subdirs, files in os.walk(dir):
      for f in files:
         if f.endswith(pattern):
            yield os.path.join(dirname, f)

for f in gen_files(DIR_NOTEBOOK, '.ipynb'):
   os.remove(f)
print('...Deleting all .ipynb files.')

for f in gen_files(DIR_NOTEBOOK_HELPERS, '.py'):
   os.remove(f)
print('...Deleting all .py files.')


urllib.request.urlretrieve(URL, FILE_MAIN_ZIP)
print('Downloading latest notebooks.')


with ZipFile(FILE_MAIN_ZIP, 'r') as zipObj:
   # Extract all the contents of zip file into temp directory
   zipObj.extractall(DIR_TMP)
   print('Extracting Zip file to {}'.format(DIR_TMP))


src_files = os.listdir(DIR_TMP_NOTEBOOK)
for file_name in src_files:
    full_file_name = os.path.join(DIR_TMP_NOTEBOOK, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, DIR_NOTEBOOK)
print('...Copying all .ipynb files.')

src_files = os.listdir(DIR_TMP_NOTEBOOK_HELPERS)
for file_name in src_files:
    full_file_name = os.path.join(DIR_TMP_NOTEBOOK_HELPERS, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, DIR_NOTEBOOK_HELPERS)
print('...Copying all .py files.')

print('...Deleting zip file.')
try:
    os.remove(FILE_MAIN_ZIP)
except:
    pass

print('...Deleting tmp directory.')
try:
    shutil.rmtree(DIR_TMP)
except:
    pass

print('\nNotebooks has been updated!  Enjoy :)')