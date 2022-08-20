address="http://gateway.marvel.com/v1/public/characters"
import pandas as pd
import requests
import json
import sys

def apicaller(apikey,hash):
    dfcc=pd.DataFrame()
    if(len(apikey)==0 or len(hash)==0):
        raise Exception("APIKEY or Hash not found")
    else:
        for off in range(0,1600,100):
            ls=[]
            paramst={"apikey":"e5da24be18953a81291bbce3feca7373","hash":"3058cb89eee118bfe90cd12d40c2e7fe","ts":"0", "limit":100, "offset":off}
            respt= requests.get(url=address, params=paramst)
            ret=respt.json()
            for i in range(0,100):
                if(i==62 and off==1500):
                    break
                row=[]
                row.append(ret['data']['results'][i]['id'])
                row.append(ret['data']['results'][i]['name'])
                row.append(ret['data']['results'][i]['comics']['available'])
                row.append(ret['data']['results'][i]['series']['available'])
                row.append(ret['data']['results'][i]['stories']['available'])
                row.append(ret['data']['results'][i]['events']['available'])
                ls.append(row)  
            dft=pd.DataFrame(ls,columns=['num_id','name','num_comics','num_series','num_stories','num_events'])
            if(off==0):
               dfcc=dft
            else:
                dfcc=pd.concat([dft,dfcc], join='outer')
        return dfcc


def apifilter(dataframe,columns,filter_condition):
    return dataframe.query(columns+filter_condition)


if __name__=="__main__":
    args=sys.argv[1:]
    print(apicaller(*args)['num_id'].nunique())
