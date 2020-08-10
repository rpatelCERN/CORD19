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
    '''
    matchtext=matchtext.replace('\n','')
    matchtext=matchtext.replace('(','')
    matchtext=matchtext.replace(')','')
    matchtext=matchtext.replace('[','')
    matchtext=matchtext.replace(']','')
    matchtext=matchtext.replace('~','')
    matchtext=matchtext.replace('=','')
    '''

    matchtext=re.sub(r"[^a-zA-Z\d\_]+", "", matchtext)
    #print(matchtext)
    df["matched_lines"]=df["matched_lines"].str.replace(r"[^a-zA-Z\d\_]+", "")
    '''
    df["matched_lines"]=df["matched_lines"].str.replace('\\n','')
    df["matched_lines"]=df["matched_lines"].str.replace('\(','')
    df["matched_lines"]=df["matched_lines"].str.replace('\)','')
    df["matched_lines"]=df["matched_lines"].str.replace('\[','')
    df["matched_lines"]=df["matched_lines"].str.replace('\]','')
    df["matched_lines"]=df["matched_lines"].str.replace('~','')
    df["matched_lines"]=df["matched_lines"].str.replace('=','')
    '''
    df=df[df['matched_lines'].str.contains(matchtext,regex=True)]
    '''
    if df.empty:
        df=pd.read_csv('%s.csv' %(fbase), low_memory=True,memory_map=True)
        df=df[df['topic']==topicnumber]
        df["matched_lines"]=df["matched_lines"].str.replace('\\n','')
        df["matched_lines"]=df["matched_lines"].str.replace('\(','')
        df["matched_lines"]=df["matched_lines"].str.replace('\)','')
        df["matched_lines"]=df["matched_lines"].str.replace('\[','')
        df["matched_lines"]=df["matched_lines"].str.replace('\]','')
        df["matched_lines"]=df["matched_lines"].str.replace('~','')
        df["matched_lines"]=df["matched_lines"].str.replace('=','')
        MatchExp=matchtext.split("...")
        MatchExp=MatchExp[0:int(len(MatchExp)/2)]###Match 1/2 the sentences
        #MatchExp=MatchExp[0:1]###Match 1/3 the sentences
        for m in MatchExp:
            matchtext=m

            matchtext=matchtext.replace('\n','')
            matchtext=matchtext.replace('(','')
            matchtext=matchtext.replace(')','')
            matchtext=matchtext.replace('[','')
            matchtext=matchtext.replace(']','')
            matchtext=matchtext.replace('~','')
            matchtext=matchtext.replace('=','')

            print(m.strip())
            df=df[df['matched_lines'].str.contains(matchtext.strip(),regex=True)]
    '''
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
    fout.write("#%s" %fbase)

    for i in range(no_topics):
    #for i in range(12,13):
        df=SORTbyRank(fbase,i,toprank)
        #print(df.head())
        df=df.head(toprank)
        df.reset_index(drop=True, inplace=True)
        titles=df['title'].tolist()
        URL=LookUpURLFromTitle(titles,fbase);
        df.insert(len(df.columns),'url',URL)
        RankedDocs=df.to_string(columns=['Rankscore','title','url'])
        fout.write("## Topic %s Most Similar Documents" %dictLabels[i])
        fout.write('\n')
        fout.write(RankedDocs)
        fout.write('\n')

        #print(df.to_string(columns=['Rankscore','title','URL']).split('\n'))
        del df;
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
                URLFirst=dfMatch['url']
                if(";" in URLFirst):URLFirst=URLFirst.split(";")[0]
                fout.write("[%s](%s)" %(dfMatch['title'].values[0],dfMatch['url'].values[0]))
                fout.write(line +'\n')
                del dfMatch
                countlines=countlines+1
                if countlines>toprank:break
        f.close()
    fout.close()

#WriteOutSummary("COVID19andACE", 15,5)
