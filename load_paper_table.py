# Loading paper TABLE,
# it contains basic information of the public papers.

# %% Importing
# System
import os

# Print
from pprint import pprint

# Database
import pandas as pd

# Web
import webbrowser

# Profile
# HTML file name
FILE_NAME = os.path.join('files', 'paper_table.html')

# TABLE file name,
# generated table will be stored here
TABLE_NAME = os.path.join('files', 'table.json')

# Make useable paper src
ELSEVIER_DOMAIN = 'https://www.sciencedirect.com/book'


def mk_src(opts, domain=ELSEVIER_DOMAIN):
    """Make useable paper src

    Arguments:
        opts {str} -- Option parameters of the src

    Keyword Arguments:
        domain {str} -- The Domain part of the src (default: {ELSEVIER_DOMAIN})

    Returns:
        The generated src
    """
    return f'{domain}/{opts}'


# %% Loading paper table
# Read the table in html,
# restore it into [TABLE]
TABLE = pd.read_html(FILE_NAME)[0]

# Regulation
TABLE.columns = TABLE.loc[0]
TABLE = TABLE.loc[1:]
TABLE.index = range(len(TABLE))

# Add html
TABLE['Src'] = TABLE.EISBN.map(lambda s: mk_src(s.replace('-', '')))

# Save
TABLE.to_json(TABLE_NAME)

# Print
TABLE

# %%
for src in TABLE['Src']:
    print(src)


# %%
