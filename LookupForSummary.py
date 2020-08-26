import pandas as pd
import re
####Look up functions
def SORTbyRank(fbase,topicnumber,toprank):
    #df=pd.read_csv('%s.csv_Topic%d.csv' %(fbase,topicnumber), low_memory=True,memory_map=True)
    df=pd.read_csv('%s_Topic%d.csv' %(fbase,topicnumber), low_memory=True,memory_map=True)
    df.sort_values(by=['Rankscore'],inplace=True,ascending=False)
    #print(df.head(toprank))
    return df

def LookUpText(fbase,matchtext,topicnumber):
    df=pd.read_csv('%s.csv' %(fbase), low_memory=True,memory_map=True)
    df=df[df['topic']==topicnumber]

    matchtext=re.sub(r"[^a-zA-Z\d\_]+", "", matchtext)
    #print(matchtext)
    df["matched_lines"]=df["matched_lines"].str.replace(r"[^a-zA-Z\d\_]+", "")
    df=df[df['matched_lines'].str.contains(matchtext,regex=True)]

    return df

def LookUpURLFromTitle(titles,fbase):
    df=pd.read_csv('%s.csv' %(fbase), low_memory=True,memory_map=True)
    df=df[df['title'].isin(titles)]
    ListURL=[]
    for t in titles:
        urlMatch=df.loc[df['title'] == t, 'url'].values[0]
        ListURL.append(urlMatch)
    return ListURL
def TopicLabeling(fbase, dictLabels):
    df=pd.read_csv('%s.csv' %(fbase), low_memory=True,memory_map=True)
    df["topic"].replace(dictLabels, inplace=True)
    return df;

def WriteOutSummary(fbase,no_topics,toprank,dictLabels):
    fout=open('FullSummary%s.md' %(fbase),'w')
    fout.write("# %s\n" %fbase)

    for i in range(no_topics):
    #for i in range(12,13):
        df=SORTbyRank(fbase,i,toprank)
        #print(df.head())
        df=df.head(toprank)
        df.reset_index(drop=True, inplace=True)
        titles=df['title'].tolist()
        Ranks=df['Rankscore'].tolist()
        URL=LookUpURLFromTitle(titles,fbase);
        del df;

        #df.insert(len(df.columns),'url',URL)
        #RankedDocs=df.to_string(columns=['Rankscore','title','url'])
        fout.write("## Topic %s: Topic words \n" %dictLabels[i])
        fout.write('\n')
        ftopics=open("TopicWords%s_%d.txt" %(fbase,i),'r')
        fout.write(ftopics.read()+'\n')
        ftopics.close()
        fout.write("## Topic %s Most Similar Documents \n" %dictLabels[i])
        fout.write('\n')

        fout.write('TF-IDF Score | Title | Link to Doc \n')
        fout.write('------------ | ------------- | -------------\n')
        for j in range(len(titles)):
            fout.write(" %.4f| %s | %s \n" %(Ranks[j],titles[j],URL[j]))
        #fout.write(RankedDocs)
        fout.write('\n')

        #print(df.to_string(columns=['Rankscore','title','URL']).split('\n'))
        fout.write("## Topic %s Long Summary" %dictLabels[i])
        fout.write('\n')

        f=open("%sTopicSummary%d.txt" %(fbase,i))
        paragraphs=f.readlines();
        countlines=1
        for line in paragraphs:
            ####Stray characters
            #if line=='\n':continue
            if(len(line)>10):### Remove stray characters and fragments
                #print(line)
                dfMatch=LookUpText(fbase,line,i)
                #print(dfMatch.head())
                URLFirst=dfMatch['url'].values[0]
                if(";" in URLFirst):URLFirst=URLFirst.split(";")[0]
                #print(URLFirst)
                fout.write("[%s](%s)" %(dfMatch['title'].values[0],URLFirst) +'\n')
                fout.write("> "+line +'\n')
                del dfMatch
                countlines=countlines+1
                if countlines>toprank:break
        f.close()
        fout.write("## Topic %s Short Summary" %dictLabels[i])
        fout.write('\n')
        f=open("%sShortNotes%d.txt" %(fbase,i),'r')
        paragraphs=f.readlines();
        countlines=1
        for line in paragraphs:
            ####Stray characters
            #if line=='\n':continue
            print(len(line))
            if(len(line)>30):### Remove stray characters and fragments
                #print(line)
                print(line)
                dfMatch=LookUpText(fbase,line,i)
                print(dfMatch.head())
                URLFirst=dfMatch['url'].values[0]
                if(";" in URLFirst):URLFirst=URLFirst.split(";")[0]
                print(URLFirst)
                fout.write("[%s](%s)" %(dfMatch['title'].values[0],URLFirst) +'\n')
                fout.write("> "+line +'\n')
                del dfMatch
                countlines=countlines+1
                if countlines>toprank:break
        f.close()
        #LookUpText()
    fout.close()

#WriteOutSummary("COVID19andACE", 15,5)
