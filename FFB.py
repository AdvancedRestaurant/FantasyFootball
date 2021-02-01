import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split



def covariance(x, y):
    n = len(x)
    return sum((x - np.mean(x)) * (y - np.mean(y))) * 1/(n-1)


def corr(x, y):
    return covariance(x,y)/(np.std(x) * np.std(y))


csv_path = '2019.csv'

df = pd.read_csv(csv_path)
df = df.loc[df['Pos'] == 'RB', ['Player', 'Tgt', 'RushingAtt', 'FantasyPoints']]
df['Usage'] = df['Tgt'] + df['RushingAtt']  # added a new column called usage targets + rushing attempts for RB
df['UsageRank'] = df['Usage'].rank(ascending=False)
df['FantasyPointsRank'] = df['FantasyPoints'].rank(ascending=False)

df.sort_values(by='UsageRank').head(15)

x = df['Usage'].values
y = df['FantasyPoints'].values

X = df['Usage'].values
Y = df['FantasyPoints'].values
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)


covariance(x, y)

plt.style.use('ggplot')
df.plot(x='Usage',y='FantasyPoints',kind='scatter')

df.head()

print(df.shape)
print('We have', df.shape[0], 'players we can analyze for the 2019 season')
print('We have', df.shape[1], 'columns of data we can analyze for the 2019 season')
