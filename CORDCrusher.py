from CreateTimeSlices import *
from TitlePhraseRanking import *
from BuildNGrams import *
from CreateTopics import *
from TextRankAbstracts import *
from ScanTsne import *
from DocSimilaritySummary import *
from LookupForSummary import *
import argparse

parser = argparse.ArgumentParser(description="CORD Crusher processes for the CORD 19 dataset")

parser.add_argument("-o","--output", dest="output", default = 'COVID19',help="Filebase for output files", metavar="output")
parser.add_argument("--path", dest="path", default = '551982_1312270_bundle_archive/',help="PATHtoCord metadata", metavar="path")
parser.add_argument('-m', '--mode', nargs='+', default=[])
parser.add_argument("--NRaked", dest="NRaked", default='20', help="CutOff for raked keywords", metavar="NRaked")
parser.add_argument("-Y","--Years",nargs='+', default=[])

parser.add_argument("--TopicScan", nargs='+', default=[], type=int)
parser.add_argument("--Era", dest="Era", default = 'COVID19',help="Input Eras: ", metavar="input")

parser.add_argument("--topics", dest="topics", default='20', help="Num of topics for CreateTopics", metavar="topics",type=int)
parser.add_argument("--topRanked", dest="topRanked", default='5', help="Num of Top Ranked Publications", metavar="topRanked",type=int)

parser.add_argument("--pyTextRank", dest="pyTextRank", default='0.02', help="Minimal pyTextRank Score for Abstrct matching", metavar="pyTextRank",type=float)

parser.add_argument("--TopicLabels", nargs='+', default=[])

args = parser.parse_args()

PATH=args.path
CoronaVirusClasses=["COVID19","MERS","SARS2003"]
NonCoronaDiseases=["CommonCold","Flu","asthma","HIV","Ebola","zika","WNileV","RSV","Pneumonia","MS"]
RespiratoryDiseases=["CommonCold","Flu","asthma","Pneumonia","RSV","ARDS"]
LabTests=["ELISA","EM","PCR"]
PublicHealth=["PublicHealth","MitigationMeasures","ICU"]
GenesProteinsAntibodies=["ACE","VGenome","MonoAnti"]
ZoonoticAll=["Hep","MS","ZoonoticCorona","CoronaUnclassified","VGastroEntritis","IBV","PorcineRRVirus","PEDV","BirdFlu","ZoonoticFlu","SwineFlu"]
ZooCorona=["ZoonoticCorona","CoronaUnclassified","VGastroEntritis","IBV","PorcineRRVirus","PEDV"]
NoKeywordID=["\[/]"]

stop_words = ['preprint','copyright','medrxiv','author','peer','holder']
stop_words.append('abstract')
stop_words.append('title')
stop_words.append('result')
stop_words.append('suggest')
stop_words.append('abstract')
stop_words.append('et')
stop_words.append('al')
stop_words.append('supplementary')
stop_words.append('letter')
stop_words.append('editor')

if("TimeSlice" in args.mode):
    #def ChopUpMeta(df)
    df=pd.read_csv('%s/metadata.csv'%PATH, low_memory=False,parse_dates=True)
    df['publish_time']=pd.to_datetime(df['publish_time'])
    df=df[(df['publish_time']<np.datetime64('today'))]
    YearChunks=args.Years
    for y in range(0,len(YearChunks)-1):WriteOutDF(df,int(YearChunks[y]),int(YearChunks[y+1]));
    del df;

if("RAKE" in args.mode):
    YearChunks=args.Years
    NRaked=int(args.NRaked)
    for y in range(0,len(YearChunks)-1):
        dfcsv="TimeSlicePapers%sto%s.csv" %(YearChunks[y],YearChunks[y+1])
        df=pd.read_csv(dfcsv, low_memory=False)
        RakeTitleAbstract(df,NRaked,int(YearChunks[y]),int(YearChunks[y+1]))
        del df

#####ERA Flags:
SetTrue=[]
SetFalse=[]
perplexity=150

fcsv="ProcessedCSV/AnalyzedTitles2019to2021.csv"
if args.Era=="HumanDiseases1970to1990" or args.Era=="Zoonotic1970to1990":
    perplexity=50
    fcsv="ProcessedCSV/AnalyzedTitles1970to1990.csv"
if args.Era=="HumanDiseases1990to2002" or args.Era=="Zoonotic1990to2002":
    perplexity=50
    fcsv="ProcessedCSV/AnalyzedTitles1990to2002.csv"
if args.Era=="SARS2002to2005":
    perplexity=50
    fcsv="ProcessedCSV/AnalyzedTitles2002to2005.csv"
if "SARS2005to2012" in args.Era:
    perplexity=100
    fcsv="ProcessedCSV/AnalyzedTitles2005to2012.csv"
if "MERS" in args.Era and not "COVID19" in args.Era:
    perplexity=100
    fcsv="ProcessedCSV/AnalyzedTitles2012to2019.csv"


if args.Era=="HumanDiseases1970to1990" or args.Era=="HumanDiseases1990to2002":
    SetTrue=["HumanCorona"]
    SetTrue.extend(NonCoronaDiseases)
    SetTrue.extend(GenesProteinsAntibodies)
    SetTrue.extend(PublicHealth)
    SetTrue.extend(LabTests)
    SetTrue.extend(GenesProteinsAntibodies)
    SetFalse=[]

if args.Era=="Zoonotic1970to1990" or args.Era=="Zoonotic1990to2002":
    SetTrue=ZooCorona
    SetTrue.extend(GenesProteinsAntibodies)
    SetTrue.extend(LabTests)
    SetFalse=[]
if args.Era=="Zoonotic1990to2002":
    SetTrue=["ZoonoticCorona","CoronaUnclassified"]
    SetFalse=["HumanCorona"]
if args.Era=="SARS2002to2005" or "SARS2005to2012" in args.Era:
    #perplexity=200
    SetTrue=["SARS2003"]
    SetFalse=[]
    stop_words.append('acute')
    stop_words.append('syndrome')
    stop_words.append('respiratory')
    stop_words.append('severe')
    stop_words.append('sars')
    stop_words.append('cov')

if "MERS" in args.Era:
    #perplexity=200
    SetTrue=["MERS"]
    SetFalse=[]
    stop_words.append('acute')
    stop_words.append('syndrome')
    stop_words.append('respiratory')
    stop_words.append('severe')
    stop_words.append('sars')
    stop_words.append('cov')
    stop_words.append('mers')
    stop_words.append('middle')
    stop_words.append('east')
    stop_words.append('coronavirus')

if "COVID19" in args.Era:
    #perplexity=400
    #fcsv="ProcessedCSV/AnalyzedTitles2020to2021.csv"
    stop_words.append('acute')
    stop_words.append('syndrome')
    stop_words.append('severe')
    stop_words.append('sars')
    stop_words.append('cov')
    stop_words.append('mers')
    stop_words.append('middle')
    stop_words.append('east')
    stop_words.append('reserved')
    stop_words.append('novel')
    stop_words.append('coronavirus')
    SetTrue=["COVID19"]
    SetFalse=[]
if("RakedKeywords" in args.mode):
    YearChunks=args.Years
    for y in range(0,len(YearChunks)-1):
        dfcsv="ProcessedCSV/AnalyzedTitles%sto%s.csv" %(YearChunks[y],YearChunks[y+1])
        df=pd.read_csv(dfcsv, low_memory=False)
        df=SelectDFRows(df,SetTrue,SetFalse)
        print(df.head())
        KeyWords=df['Title Qualifier Words'].tolist()
        CompareNGramCleaning(KeyWords,50,20)
        del df

if("TopicScan" in args.mode or "CreateTopics" in args.mode ):
    fout=args.output+".gif"
    Topics=args.TopicScan
    no_topics=args.topics
    df=pd.read_csv(fcsv, low_memory=True,memory_map=True)
    outputDFname=args.output
    if args.Era=="SARS2002to2005" or "SARS2005to2012" in args.Era:
        if "PublicHealth" in args.Era:df=df[df['Viral Tag'].str.contains("PublicHealth") |df['Viral Tag'].str.contains("MitigationMeasures")]
        if "Misc" in args.Era:df=df[~(df['Viral Tag'].str.contains("PublicHealth") & df['Viral Tag'].str.contains("SARS2003"))]
    if "MERS" in args.Era:
        if "PublicHealth" in args.Era:
            SetFalse.append("WNileV")
            SetFalse.append("HIV")
            SetFalse.append("BirdFlu")
            SetFalse.append("HEP")
            SetFalse.append("zika")
            SetFalse.append("Ebola")
            df=df[df['Viral Tag'].str.contains("PublicHealth") ]
        if "Misc" in args.Era:
            df=df[df['Viral Tag'].str.contains("MERS")]
            df=df[~(df['Viral Tag'].str.contains("PublicHealth") & df['Viral Tag'].str.contains("MERS"))]
            SetTrue.extend(GenesProteinsAntibodies)
            SetTrue.extend(LabTests)
            SetTrue.append("ZoonoticCorona")
    if "COVID19" in args.Era:
        df=SelectDFRows(df,SetTrue,SetFalse)
        if "PublicHealth" in args.Era:
            stop_words.append('public')
            df=df[df['Viral Tag'].str.contains("PublicHealth")|df['Viral Tag'].str.contains("MitigationMeasures")|df['Viral Tag'].str.contains("ICU")]
        if "ACE" in args.Era:df=df[df['Viral Tag'].str.contains("ACE")]
        #if "Misc" in args.Era:df=df[df['Viral Tag'].str.contains("CoronaUnclassified") | df['Viral Tag'].str.contains("Pneumonia")| df['Viral Tag'].str.contains("ARDS")]
        if "Zoo" in args.Era:df=df[ df['Viral Tag'].str.contains("ZoonoticCorona")]
        if "Misc" in args.Era:df=df[ ~(df['Viral Tag'].str.contains("ACE") | df['Viral Tag'].str.contains("SARS2003") | df['Viral Tag'].str.contains("MERS") | df['Viral Tag'].str.contains("ZoonoticCorona") | df['Viral Tag'].str.contains("PublicHealth")|df['Viral Tag'].str.contains("MitigationMeasures")|df['Viral Tag'].str.contains("ICU"))]
        if "MERS" in args.Era and "SARS" in args.Era:df=df[df['Viral Tag'].str.contains("SARS2003") & df['Viral Tag'].str.contains("MERS")]
    if"TopicScan" in args.mode:RunTopicScans(df,SetTrue,SetFalse,stop_words,Topics,fout,perplexity)
    if"CreateTopics" in args.mode:RunTopicBuilding(df,PATH,SetTrue,SetFalse,no_topics,outputDFname,stop_words,args.pyTextRank)

if "PhraseRanking" in args.mode:
    YearChunks=args.Years
    no_topics=args.topics
    fbase=args.Era
    for y in range(0,len(YearChunks)-1):
        dfcsv="ProcessedCSV/AnalyzedTitles%sto%s.csv" %(YearChunks[y],YearChunks[y+1])
        df=pd.read_csv(dfcsv, low_memory=False)
        SelectedRows=SelectDFRows(df,SetTrue,SetFalse)
        AllTopicKeyWords=[]
        for i in range(no_topics):
            f=open("TopicWords%s_%d.txt" %(fbase,i),'r')
            f.seek(0)
            TopicWords=f.read().split(',')
            AllTopicKeyWords.extend(TopicWords)
            f.close()
        AbstractRankOptimization(stop_words,SelectedRows,AllTopicKeyWords,args.pyTextRank)
if "CreateSummaries" in args.mode:
    for i in range(args.topics):RunSummaries(PATH,args.Era+".csv",i)
if "WriteSummaries"in args.mode:
    dictLabels={}
    LabelsList=args.TopicLabels
    for t in range(len(LabelsList)):dictLabels[t]=LabelsList[t]
    print(dictLabels)
    #dictLabels={0:"Coronaviridae family", 1:"respiratory syncytial virus",2:"Human Cov 229E",3:"Viral Genome",4:"Electron Microscopy",5:"Transmissible Gastroenteritis Virus",6:"Human Cov  OC43",7:"Diagnosis of Viral Infections"}
    WriteOutSummary(args.Era, args.topics,args.topRanked,dictLabels)
