import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import seaborn as sns

sns.set(style="darkgrid")

def GroupbyYear(df):
    df['publish_time']=pd.to_datetime(df['publish_time'])
    df["publish_time"] = df["publish_time"].astype("datetime64")
    df=df["year"]=df["publish_time"].dt.year
    df=df.groupby(['year']).size().reset_index(name='Count')
    return df

def FillTimeSlice(df,minyear,maxyear):
    df=df[(df['publish_time']<'%s-1-1' %maxyear) & (df['publish_time']>='%s-1-1' %minyear)]
    df.to_csv("TestYears%sto%s.csv" %(minyear,maxyear))
    #print(df2['title'].head(50))

def PlotTimeSlices(df,Tags,label):
    df.loc[df['Viral Tag'].notnull(),'Paper Tag']=False
    for tag in Tags:df.loc[df['Viral Tag'].str.contains(tag),'Paper Tag']=True
    Plotdf=df[df['Paper Tag']==True];

    Plotdf=Plotdf.groupby(['year']).size().reset_index(name='Count')
    ax=sns.lineplot(x='year',y='Count',data=Plotdf,label=label)
    return ax

df=pd.read_csv('%s' %sys.argv[1], low_memory=False,parse_dates=True) #Metadata for CORD-19
#df=df[['publish_time']]
#df['title'].fillna("title", inplace=True)
#df['abstract'].fillna("abstract", inplace=True)
df['publish_time']=pd.to_datetime(df['publish_time'])
df["publish_time"] = df["publish_time"].astype("datetime64")
df["year"]=df["publish_time"].dt.year
df=df[(df['publish_time']<'2020-9-20')]
dftest=df[(df['publish_time']>'2020-9-1')]
print(dftest['publish_time'].head(100))

df=df.groupby(['year']).size().reset_index(name='Count')
'''
df2=df[(df['publish_time']<'%s-1-1' %sys.argv[3]) & (df['publish_time']>='%s-1-1' %sys.argv[2])]
df2.to_csv("TestYears%sto%s.csv" %(sys.argv[2],sys.argv[3]))
print(df2['title'].head(50))
'''





#print(df.head())
ax=sns.lineplot(x='year',y='Count',data=df,label="Total CORD19 data")
ax.set(yscale="log")
plt.title('CORD-19 Publications')
plt.xlabel('Year of Publication')
plt.ylabel('Num of Publications')


#############Now include the other dataframes with key words: (Coronaviruses in animals),Human corona, SARS, MERS, COVID19

######## Coronaviruses in animals: IBV, Hep,CoronaUnclassified,ZoonoticCorona,VGastroEntritis
df1970=pd.read_csv("ProcessedCSV/AnalyzedTitles1970to1980.csv", low_memory=False)
df1980=pd.read_csv("ProcessedCSV/AnalyzedTitles1980to1990.csv", low_memory=False)
df1990=pd.read_csv("ProcessedCSV/AnalyzedTitles1990to2002.csv", low_memory=False)
df2002=pd.read_csv("ProcessedCSV/AnalyzedTitles2002to2005.csv", low_memory=False)
df2005=pd.read_csv("ProcessedCSV/AnalyzedTitles2005to2012.csv", low_memory=False)
df2012=pd.read_csv("ProcessedCSV/AnalyzedTitles2012to2019.csv", low_memory=False)
#df2019=pd.read_csv("ProcessedCSV/AnalyzedTitles2019to2020.csv", low_memory=False)
df2020=pd.read_csv("ProcessedCSV/AnalyzedTitles2019to2021.csv", low_memory=False)

dfAll = pd.concat([df1970,df1980,df1990,df2002,df2005,df2012,df2020])
dfAll=dfAll[['Viral Tag','publish_time']]
dfAll['publish_time']=pd.to_datetime(dfAll['publish_time'])
dfAll=dfAll[(dfAll['publish_time']<'2020-9-20')]

dfAll["year"]=dfAll["publish_time"].dt.year

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("IBV"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("HEP"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("CoronaUnclassified"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("VGastroEntritis"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("ZoonoticCorona"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("PorcineRRVirus"),'Paper_Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("BirdFlu"),'Paper_Tag']=True



ZoonoticCorona=dfAll[dfAll['Paper Tag']==True];
#ZoonoticCorona['publish_time']=pd.to_datetime(ZoonoticCorona['publish_time'])
#ZoonoticCorona["year"]=ZoonoticCorona["publish_time"].dt.year
ZoonoticCorona=ZoonoticCorona.groupby(['year']).size().reset_index(name='Count')
dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("HumanCorona"),'Paper Tag']=True

dfAll.loc[dfAll['Viral Tag'].str.contains("SARS2003"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("MERS"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19"),'Paper Tag']=True

HumanCorona=dfAll[dfAll['Paper Tag']==True];
#HumanCorona['publish_time']=pd.to_datetime(HumanCorona['publish_time'])
#HumanCorona["year"]=HumanCorona["publish_time"].dt.year
HumanCorona=HumanCorona.groupby(['year']).size().reset_index(name='Count')
dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("SARS2003"),'Paper Tag']=True
Sars=dfAll[dfAll['Paper Tag']==True];
Sars['publish_time']=pd.to_datetime(Sars['publish_time'])
Sars["year"]=Sars["publish_time"].dt.year
Sars=Sars[(Sars['publish_time']>'2002-1-1')]

Sars=Sars.groupby(['year']).size().reset_index(name='Count')


dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("MERS"),'Paper Tag']=True
MERS=dfAll[dfAll['Paper Tag']==True];
#MERS['publish_time']=pd.to_datetime(MERS['publish_time'])
#MERS["year"]=MERS["publish_time"].dt.year
MERS["year"]=MERS["publish_time"].dt.year
MERS=MERS[(MERS['publish_time']>'2012-1-1')]
MERS=MERS.groupby(['year']).size().reset_index(name='Count')

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19"),'Paper Tag']=True
COVID=dfAll[dfAll['Paper Tag']==True];
COVID['publish_time']=pd.to_datetime(COVID['publish_time'])
COVID["year"]=COVID["publish_time"].dt.year
COVID=COVID[(COVID['publish_time']>'2019-12-1')]

COVID=COVID.groupby(['year']).size().reset_index(name='Count')

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("PublicHealth"),'Paper Tag']=True
PH=dfAll[dfAll['Paper Tag']==True];
#PH['publish_time']=pd.to_datetime(PH['publish_time'])
#PH["year"]=PH["publish_time"].dt.year
PH=PH.groupby(['year']).size().reset_index(name='Count')

ax2=sns.lineplot(x='year',y='Count',data=HumanCorona,label="human CoV")
ax4=sns.lineplot(x='year',y='Count',data=ZoonoticCorona,label="Zoonotic CoV")
ax3=sns.lineplot(x='year',y='Count',data=Sars,label="SARS 2003")
ax5=sns.lineplot(x='year',y='Count',data=MERS,label="Middle East Cov 2012")
ax6=sns.lineplot(x='year',y='Count',data=COVID,label="COVID 19")
ax7=sns.lineplot(x='year',y='Count',data=PH,label="Public Health")

ax2.set(yscale="log")
plt.show()
fig, ax = plt.subplots()

#dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19"),'Paper Tag']=True
COVID=dfAll[dfAll['Paper Tag']==True];
COVID['publish_time']=pd.to_datetime(COVID['publish_time'])
COVID["month"]=COVID["publish_time"].dt.month
COVID=COVID[(COVID['publish_time']>'2020-1-1')]
#COVID=COVID[(COVID['publish_time']>'2020-9-1')]
print(COVID['publish_time'].head(100))

COVID=COVID.groupby(['month']).size().reset_index(name='Count')
ax=sns.lineplot(x='month',y='Count',data=COVID,label="All COVID 19")
ax.set(yscale="log")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("ACE"),'Paper Tag']=True
COVIDandACE=dfAll[dfAll['Paper Tag']==True];
COVIDandACE['publish_time']=pd.to_datetime(COVIDandACE['publish_time'])
COVIDandACE["month"]=COVIDandACE["publish_time"].dt.month
COVIDandACE=COVIDandACE[(COVIDandACE['publish_time']>'2020-1-1')]
COVIDandACE=COVIDandACE.groupby(['month']).size().reset_index(name='Count')
ax2=sns.lineplot(x='month',y='Count',data=COVIDandACE,label="ACE2 Receptor")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("PublicHealth"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("MitigationMeasures"),'Paper Tag']=True

COVIDandPublicHealth=dfAll[dfAll['Paper Tag']==True];
COVIDandPublicHealth['publish_time']=pd.to_datetime(COVIDandPublicHealth['publish_time'])
COVIDandPublicHealth["month"]=COVIDandPublicHealth["publish_time"].dt.month
COVIDandPublicHealth=COVIDandPublicHealth[(COVIDandPublicHealth['publish_time']>'2020-1-1')]
COVIDandPublicHealth=COVIDandPublicHealth.groupby(['month']).size().reset_index(name='Count')
ax3=sns.lineplot(x='month',y='Count',data=COVIDandPublicHealth,label="Public Health")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("SARS2003")& dfAll['Viral Tag'].str.contains("MERS"),'Paper Tag']=True
COVIDandSarsMERS=dfAll[dfAll['Paper Tag']==True];
COVIDandSarsMERS['publish_time']=pd.to_datetime(COVIDandSarsMERS['publish_time'])
COVIDandSarsMERS["month"]=COVIDandSarsMERS["publish_time"].dt.month
COVIDandSarsMERS=COVIDandSarsMERS[(COVIDandSarsMERS['publish_time']>'2020-1-1'  )]
COVIDandSarsMERS=COVIDandSarsMERS.groupby(['month']).size().reset_index(name='Count')
ax4=sns.lineplot(x='month',y='Count',data=COVIDandSarsMERS,label="SARS and MERS")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("ZoonoticCorona"),'Paper Tag']=True
COVIDandZoonoticCorona=dfAll[dfAll['Paper Tag']==True];
COVIDandZoonoticCorona['publish_time']=pd.to_datetime(COVIDandZoonoticCorona['publish_time'])
COVIDandZoonoticCorona["month"]=COVIDandZoonoticCorona["publish_time"].dt.month
COVIDandZoonoticCorona=COVIDandZoonoticCorona[(COVIDandZoonoticCorona['publish_time']>'2020-1-1'  )]
COVIDandZoonoticCorona=COVIDandZoonoticCorona.groupby(['month']).size().reset_index(name='Count')
ax5=sns.lineplot(x='month',y='Count',data=COVIDandZoonoticCorona,label="Zoonotic origin")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("ICU"),'Paper Tag']=True
COVIDandICU=dfAll[dfAll['Paper Tag']==True];
COVIDandICU['publish_time']=pd.to_datetime(COVIDandICU['publish_time'])
COVIDandICU["month"]=COVIDandICU["publish_time"].dt.month
COVIDandICU=COVIDandICU[(COVIDandICU['publish_time']>'2020-1-1'  )]
COVIDandICU=COVIDandICU.groupby(['month']).size().reset_index(name='Count')
ax6=sns.lineplot(x='month',y='Count',data=COVIDandICU,label="Intensive care")

dfAll.loc[dfAll['Viral Tag'].notnull(),'Paper Tag']=False
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("PCR"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("ELISA"),'Paper Tag']=True

dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("CT"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("Diagnostics"),'Paper Tag']=True
dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("NuclAcid"),'Paper Tag']=True

COVIDandPCR=dfAll[dfAll['Paper Tag']==True];
COVIDandPCR['publish_time']=pd.to_datetime(COVIDandPCR['publish_time'])
COVIDandPCR["month"]=COVIDandPCR["publish_time"].dt.month
COVIDandPCR=COVIDandPCR[(COVIDandPCR['publish_time']>'2020-1-1')]
COVIDandPCR=COVIDandPCR.groupby(['month']).size().reset_index(name='Count')
ax7=sns.lineplot(x='month',y='Count',data=COVIDandPCR,label="Diagnostic methods")


dfAll.loc[dfAll['Viral Tag'].str.contains("COVID19") & dfAll['Viral Tag'].str.contains("CriticalPatients"),'Paper Tag']=True

COVIDandCriticalPatients=dfAll[dfAll['Paper Tag']==True];
COVIDandCriticalPatients['publish_time']=pd.to_datetime(COVIDandCriticalPatients['publish_time'])
COVIDandCriticalPatients["month"]=COVIDandCriticalPatients["publish_time"].dt.month
COVIDandCriticalPatients=COVIDandCriticalPatients[(COVIDandCriticalPatients['publish_time']>'2020-1-1')]
COVIDandCriticalPatients=COVIDandCriticalPatients.groupby(['month']).size().reset_index(name='Count')
ax8=sns.lineplot(x='month',y='Count',data=COVIDandCriticalPatients,label="Critical Patients")

plt.ylim(1, 50000000)
plt.title('CORD-19 Publications')
plt.xlabel('Month of Publication in 2020')
labels = ['','Jan', 'Feb','Mar','Apr', 'May','Jun','Jul','Aug','Sep']
ax.set_xticklabels(labels)
plt.ylabel('Num of Publications')
plt.show()

#ax6=sns.lineplot(x='year',y='Count',data=COVID,label="COVID 19")
