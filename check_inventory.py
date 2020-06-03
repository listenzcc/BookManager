# %%
# Importing
# System
import os
import zipfile

# Database
import pandas as pd

# Settings
# Path of raw zip files
RAW_ZIP_PATH = os.path.join('files', 'raw_zips')

# Path of inventory
INVENTORY_PATH = os.path.join('files', 'inventory')

# Get Paper Table
TABLE_NAME = os.path.join('files', 'table.json')
TABLE = pd.read_json(TABLE_NAME)
TABLE

# %%
# Walk through RAW_ZIP_PATH
# Remove unreadable files
removed_count = 0
total_count = 0
for j, fname in enumerate(os.listdir(RAW_ZIP_PATH)):
    # print(fname)
    total_count += 1

    # Remove none .zip file
    if not fname.endswith('.zip'):
        os.remove(os.path.join(RAW_ZIP_PATH, fname))
        removed_count += 1
        print(f'Removed NONE ZIP file {fname}')
        continue

    # Remove unreadable file
    try:
        with zipfile.ZipFile(os.path.join(RAW_ZIP_PATH, fname)) as f:
            pass
    except zipfile.BadZipFile:
        os.remove(os.path.join(RAW_ZIP_PATH, fname))
        removed_count += 1
        print(f'Removed BAD ZIP file {fname}')
        continue

print(f'{total_count} files in total, {removed_count} files is removed.')

# %%
# Inventory management


def parse_copyright(copyright):
    split = copyright.split('_', 2)
    _name = split[-1]

    assert(_name.endswith('.pdf'))

    name = _name[:-4].replace('-', ' ')
    name = name.replace(' ', '')

    return name


def mkdir(path):
    if os.path.exists(path):
        assert(os.path.isdir(path))
        return None

    os.mkdir(path)
    return path


bad_zip_files = []
total_count = 0
for j, fname in enumerate(os.listdir(RAW_ZIP_PATH)):
    fpath = os.path.join(RAW_ZIP_PATH, fname)
    total_count += 1

    with zipfile.ZipFile(fpath) as f:
        namelist = f.namelist()

        copyright = [e for e in namelist if e.startswith('Copyrigh')]
        if len(copyright) == 0:
            copyright = [e for e in namelist if e.startswith('Dedication')]

        if not len(copyright) == 1:
            bad_zip_files.append(fname)
            print(f'Can not correctly parse the zip file {fname}')
            continue

        name = parse_copyright(copyright[0])
        print(name)

        path = mkdir(os.path.join(INVENTORY_PATH, name))
        if path is not None:
            f.extractall(path=path)

print(f'{total_count} files in total, {len(bad_zip_files)} files is bad.')
print(f'Bad zip files are {bad_zip_files}')

# %%
# Check inventory
bad_inventory_folders = []

for name in os.listdir(INVENTORY_PATH):
    fpath = os.path.join(INVENTORY_PATH, name)
    if len([e for e in os.listdir(fpath)]) == 0:
        bad_inventory_folders.append(name)

print(f'Bad inventory folders are: {bad_inventory_folders}')

# %%
# Feed Table


def subject2name(subject):
    invalid_chars = [' ', ',', '\'', ':', '&', '-']
    name = subject
    for c in invalid_chars:
        name = name.replace(c, '')
    return name.lower()


TABLE['Inventory'] = ''

names = [e.lower() for e in os.listdir(INVENTORY_PATH)]

found_count = 0
for j, subject in enumerate(TABLE['题名']):
    print(j, subject)
    name = subject2name(subject)

    if name in names:
        print(f'Found {name} in inventory.')
        found_count += 1
        series = TABLE.iloc[j]
        series['Inventory'] = name
        TABLE.iloc[j] = series

print(f'Found {found_count} in inventory.')

TABLE

# %%
TABLE.to_json(TABLE_NAME)
TABLE

# %%
# Summary

print('Following is what you should be concerned')
print(f'Bad inventory folders are: {bad_inventory_folders}')
print(f'Bad zip files are: {bad_zip_files}')

# %%
table = TABLE.loc[TABLE['Inventory'] == '']
table

# %%
# subject = table['题名'].loc[250]
# name = subject2name(subject)
# (subject, name)

# %%
names

# %%
TABLE.to_html('a.html')

# %%
