import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import seaborn as sns
from datetime import datetime
import numpy as np
sns.set(style="darkgrid")

def GroupbyYear(df):
    df['publish_time']=pd.to_datetime(df['publish_time'])
    df["publish_time"] = df["publish_time"].astype("datetime64")
    df["year"]=df["publish_time"].dt.year
    df=df.groupby(['year']).size().reset_index(name='Count')
    return df

def FillTimeSlice(df,minyear,maxyear):
    df=df[(df['publish_time']<'%s-1-1' %maxyear) & (df['publish_time']>='%s-1-1' %minyear)]
    df.to_csv("TestYears%sto%s.csv" %(minyear,maxyear))

def PlotTimeSlices(df,Tags,label):
    df.loc[df['Viral Tag'].notnull(),'Paper Tag']=False

    for tag in Tags:df.loc[df['Viral Tag'].str.contains(tag),'Paper Tag']=True
    Plotdf=df[df['Paper Tag']==True];

    Plotdf=Plotdf.groupby(['year']).size().reset_index(name='Count')
    ax=sns.lineplot(x='year',y='Count',data=Plotdf,label=label)
    return ax

def WriteOutDF(df,startyear,endyear):
    df['publish_time']=pd.to_datetime(df['publish_time'])
    df["publish_time"] = df["publish_time"].astype("datetime64")
    df2=df[(df['publish_time']<'%d-1-1' %endyear) & (df['publish_time']>='%d-1-1' %startyear)]
    df2.to_csv("TimeSlicePapers%dto%d.csv" %(startyear,endyear))
    #return df2

#def ChopUpMeta(df)
'''
df=pd.read_csv('%s' %sys.argv[1], low_memory=False,parse_dates=True) #Metadata for CORD-19
df['publish_time']=pd.to_datetime(df['publish_time'])
df=df[(df['publish_time']<np.datetime64('today'))]
print(df.head())
WriteOutDF(df,1990,2002);
'''
#
#df=df[['publish_time']]
#df['title'].fillna("title", inplace=True)
#df['abstract'].fillna("abstract", inplace=True)
#df['publish_time']=pd.to_datetime(df['publish_time'])
#df["publish_time"] = df["publish_time"].astype("datetime64")
#df["year"]=df["publish_time"].dt.year
#df=df.groupby(['year']).size().reset_index(name='Count')



#### Move this to a plotting function
'''
df=GroupbyYear(df)
ax=sns.lineplot(x='year',y='Count',data=df,label="Total CORD19 data")
ax.set(yscale="log")
plt.title('CORD-19 Publications')
plt.xlabel('Year of Publication')
plt.ylabel('Num of Publications')
del df;

#############Now include the other dataframes with key words: (Coronaviruses in animals),Human corona, SARS, MERS, COVID19

df1970=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles1970to1980.csv", low_memory=False)
df1980=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles1980to1990.csv", low_memory=False)
df1990=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles1990to2002.csv", low_memory=False)
df2002=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles2002to2005.csv", low_memory=False)
df2005=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles2005to2012.csv", low_memory=False)
df2012=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles2012to2019.csv", low_memory=False)
df2019=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles2019to2020.csv", low_memory=False)
df2020=pd.read_csv("../CORD19/ProcessedCSV/AnalyzedTitles2020to2021.csv", low_memory=False)

dfAll = pd.concat([df1970,df1980,df1990,df2002,df2005,df2012,df2019,df2020])
dfAll=dfAll[['Viral Tag','publish_time']]
dfAll['publish_time']=pd.to_datetime(dfAll['publish_time'])
dfAll=dfAll[(dfAll['publish_time']<np.datetime64('today'))]

dfAll["year"]=dfAll["publish_time"].dt.year
ax2=PlotTimeSlices(dfAll,['HumanCorona'],"human CoV")
ax3=PlotTimeSlices(dfAll,['SARS2003'],"SARS 2003")
ax4=PlotTimeSlices(dfAll,['IBV','HEP','CoronaUnclassified','VGastroEntritis','ZoonoticCorona','PorcineRRVirus','BirdFlu'],"Zoonotic CoV")
ax5=PlotTimeSlices(dfAll,['MERS'],"Middle East Cov 2012")
ax6=PlotTimeSlices(dfAll,['COVID19'],"COVID 19")
ax7=PlotTimeSlices(dfAll,['PublicHealth'],"Public Health")

plt.show()
'''
