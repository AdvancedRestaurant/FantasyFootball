import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# importing the csv file
df = pd.read_csv('2019 (1).csv')

# dropping unnecessary columns
df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS', 'Age', 'Tgt',
         'Y/A', 'Att', 'Att.1', 'Cmp', 'Y/R'], axis=1, inplace=True)

# Fixing name formatting
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
}, axis=1, inplace=True)

# creating fantasy points column, PPR
df['FantasyPoints'] = (df['PassingYDs'] * 0.04 + df['PassingTD'] * 4 - df['Int'] * 2 + df['RushingYDs'] * 0.1
                       + df['RushingTD'] * 6 + df['Rec'] * 1 + df['ReceivingYDs'] * 0.1 + df['ReceivingTD'] * 6 - df[
                           'FL'] * 2)

# creating fantasy points per game
df['FantasyPoints/GM'] = df['FantasyPoints'] / df['G']

df = df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]

# Removing players that played more than 2 teams
df = df[df['Tm'] != '2TM']
df = df[df['Tm'] != '3TM']

# separating dataframes off position
rb_df = df[df['FantPos'] == "RB"]
qb_df = df[df['FantPos'] == "QB"]
wr_df = df[df['FantPos'] == "WR"]
te_df = df[df['FantPos'] == "TE"]

# sample data frame for correlation matrix
examp_column_names = ['QB1', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE']
random_numbers = np.random.randn(10, 7)
example_df = pd.DataFrame(random_numbers, columns=examp_column_names)


# Function to find the top fantasy players based on position
def get_top_players(df, n):
    return df.groupby("Tm").apply(lambda x: x.nlargest(n, ['FantasyPoints']).min()).reset_index(drop=True)


# creating separate data frames for each of the positions based on their performance
qb_df = get_top_players(qb_df, 1)
te_df = get_top_players(te_df, 1)
rb1_df = get_top_players(rb_df, 1)
rb2_df = get_top_players(rb_df, 2)
wr1_df = get_top_players(wr_df, 1)
wr2_df = get_top_players(wr_df, 2)
wr3_df = get_top_players(wr_df, 3)

# renaming data frames
new_names = {
    "QB1": qb_df,
    "TE1": te_df,
    'RB1': rb1_df,
    'RB2': rb2_df,
    'WR1': wr1_df,
    'WR2': wr2_df,
    'WR3': wr3_df
}

for name, new_df in new_names.items():
    new_df.rename({'FantasyPoints/GM': name}, axis=1, inplace=True)
    new_df.drop(['FantPos', 'FantasyPoints'], axis=1, inplace=True)
    new_df.set_index('Tm', inplace=True)

df = pd.concat([qb_df, te_df, rb1_df, rb2_df, wr1_df, wr2_df, wr3_df], axis=1)

# correlation matrix
corrMatrix = df.corr()

fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

cmap = sns.diverging_palette(0, 250, as_cmap=True)

# heatmap of correlation matrix
vizCorrMatrix = sns.heatmap(corrMatrix, cmap=cmap, center=0)
