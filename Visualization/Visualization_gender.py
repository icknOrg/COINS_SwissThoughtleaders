#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df = pd.read_csv('../CSV Data/Classified_Thoughtleaders_SW_from_all.csv', sep=";")

df['m/w'].unique()
df.loc[df['m/w'].str.contains('m '), 'm/w'] = 'm'


vis = sns.countplot(x="class_labels", hue="m/w", data=df, palette="crest")
fig = vis.get_figure()
fig.savefig('gender.png') 





