'''This program takes in a CSV generated by datacollect.py and generates graphics showing statistics 
for each hiking region in Washington.'''

import math
import matplotlib.pyplot as plt
import pandas as pd

f = 'data.csv'
df = pd.read_csv(f)

#Number of hiking trails pre region
bar = df.loc[:,'Region'].value_counts().plot.bar(legend=None)
plt.show(bar.set_ylabel('Hikes'))

#Average max_elevation per region, measured in feet
regions = df.Region.unique()
mean_elev = []
for region in regions:
	mean = df.loc[df.Region.isin([region])]['Max Elevation'].mean()
	mean_elev.append(mean)
d = zip(regions,mean_elev)
elevdf = pd.DataFrame(data=d).sort_values(1, ascending=False)
plt.show(elevdf.plot.bar(x=regions,legend=None).set_ylabel('Feet'))

#Average grade (steepness) per region, measured in degrees
grade = df.apply(lambda srs: srs.Gain / (5280/2 * srs.Length), axis = "columns")
dfgrade = df
dfgrade['Grade'] = grade
mean_grade = []
for region in regions:
	mean = dfgrade.loc[df.Region.isin([region]) & ~dfgrade.Grade.isnull()]['Grade'].mean()
	mean_grade.append(math.atan(mean)*180/math.pi)
d = zip(regions,mean_grade)
gradedf = pd.DataFrame(data=d).sort_values(1, ascending=False)
plt.show(gradedf.plot.bar(x=regions,legend=None).set_ylabel('Degrees'))
