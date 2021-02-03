import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# import Fantasy football 2019 data
df = pd.read_csv('2019 (1).csv')

# Drop unncessary columns
df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'], axis=1,
        inplace=True)

# fix name formatting
df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

# Rename columns
df.rename({
    'TD': 'PassingTD',
    'TD.1': 'RushingTD',
    'TD.2': 'ReceivingTD',
    'TD.3': 'TotalTD',
    'Yds': 'PassingYDs',
    'Yds.1': 'RushingYDs',
    'Yds.2': 'ReceivingYDs',
    'Att': 'PassingAtt',
    'Att.1': 'RushingAtt'
}, axis=1, inplace=True)

# separate dataframes based off position
rb_df = df[df['FantPos'] == 'RB']
qb_df = df[df['FantPos'] == 'QB']
wr_df = df[df['FantPos'] == 'WR']
te_df = df[df['FantPos'] == 'TE']

rushing_columns = ['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD']
receiving_columns = ['Tgt', 'Rec', 'ReceivingYDs', 'ReceivingTD']
passing_columns = ['PassingAtt', 'PassingYDs', 'PassingTD', 'Int']


def transform_columns(df, new_column_list):
    df = df[['Player', 'Tm', 'Age', 'G'] + new_column_list + ['FL']]
    return df


rb_df = transform_columns(rb_df, rushing_columns + receiving_columns)
wr_df = transform_columns(wr_df, rushing_columns + receiving_columns)
te_df = transform_columns(te_df, receiving_columns)
qb_df = transform_columns(qb_df, passing_columns)

# How did Targets + Rushing TDs correlate to fantasy Points per game for Running backs in 2019

# creating a new column to calculate fantasy points scored (Full PPR)
rb_df['FantasyPoints'] = rb_df['RushingYDs'] * 0.1 + rb_df['RushingTD'] * 6 + rb_df['Rec']
+ rb_df['ReceivingYDs'] * 0.1 + rb_df['ReceivingTD'] * 6 - rb_df['FL'] * 2

# creating a new column to calculate fantasy points per game
rb_df['fantasyPoints/GM'] = rb_df['FantasyPoints'] / rb_df['G']
rb_df['fantasyPoints/GM'] = rb_df['fantasyPoints/GM'].apply(lambda x: round(x, 2))

# Creating a new column for usage per game. Usage is defined as # targets + carries
rb_df['Usage/GM'] = (rb_df['RushingAtt'] + rb_df['Tgt']) / rb_df['G']
# rounding each row value to two decimal places
rb_df['Usage/GM'] = rb_df['Usage/GM'].apply(lambda x: round(x, 2))

# creating a new column for rushing attempts per game
rb_df['RushingAtt/GM'] = rb_df['RushingAtt'] / rb_df['G']
# rounding each row value to two decimal places
rb_df['RushingAtt/GM'] = rb_df['RushingAtt/GM'].apply(lambda x: round(x, 2))

sns.set_style('whitegrid')

# create a canvas with matplotlib
fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

# basic regression scatter plot with a trendline
plot = sns.regplot(
    x=rb_df['Usage/GM'],
    y=rb_df['fantasyPoints/GM'],
    scatter=True,
)
