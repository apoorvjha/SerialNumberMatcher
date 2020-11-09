#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time
import math
import csv
start=time.time()


# In[2]:


def read_data(filename):
    dataset=pd.read_csv(filename)
    return dataset['data']


# In[3]:


def det_stat(dataset):
    # this function makes this program more flexible as it allows us to find the cutoff score 
    # for our dataset so that we can find all matching serial numbers whose score fall in 90th percentile range.
    d=[]
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            if(dataset[i]!=dataset[j]):
                d.append(KMP(dataset[i],dataset[j],1,0))
    d.sort()
    return(d[math.floor(0.9*len(d))])


# In[4]:


def check(data):
    # this function helps us check wheather the string is in exponential floating number format or a normal string
    # of characters and digits.
    for j in range(len(data)):
        s=data[j]
        for i in range(len(s)-1):
            if(s[i].isdigit() and s[i+1]=='.'):
                temp=data[j]
                if(s[i+1:].find('E')!=-1):
                    temp=int(float(data[j]))
                data[j]=temp
    return(data)    


# In[5]:


def KMP(test_string,pattern,mode,cutoff):
    # it is a modyfied string matching algorithm which works in three modes.
    #     $ mode 0 is for calculating and getting the Match score.
    #     $ mode 1 is for using the supplied cutoff as matching criterion.
    #     $ mode 2 is hardwired cutoff criterion i.e. change is 2 or less characters should be labeled 1 otherwise 0.
    i=0
    j=0
    c=0
    while(i<len(test_string) and j<len(pattern)): 
            if(test_string[i]==pattern[j]):
                j+=1
                c+=1
            i+=1
    if(mode==2):
        c=max(len(test_string),len(pattern))-c
        if(c<=cutoff):
            return(1)
        else:
            return(0)
    c=c/max(len(test_string),len(pattern))
    if(mode==1):
        return(c)
    if(c>=cutoff):
        return(1)
    else:
        return(0)  


# In[6]:


def preprocess(s):
    l=[]
    distinct=[]
    data=check(s)
    for i in data:
        if(i not in distinct):
            if(type(i)==int and i!=0):
                # this condition handles case for exponent floating point numbers.
                l.append(str(i))
                distinct.append(str(i))
            else:
                temp=""
                if(i!='0'):
                    for j in range(len(i)):
                        if(i[j]!='-' and i[j]!=' ' and i[j]!='.' and i[j]!='+'):
                            temp+=i[j]
                    l.append(temp)
                    distinct.append(temp)
    return(l)   


# In[7]:


def create_csv(filename,dict_obj):
    with open(filename,'w') as out:
        out.write("substr_SN , SerialNumber\n")
        for i in dict_obj.keys():
            temp=list(set(dict_obj[i]))
            k=""
            for j in temp:
                k+=j
                k+=" "
            out.write("%s, %s\n"%(i,k))
    return


# In[8]:


def process(in_filename,out_filename):
    data=read_data(in_filename)
    dataset=preprocess(data)
    #k=det_stat(dataset)  # can only be used with KMP with mode 1.
    k=2                   # our hardwired matching cariterion.
    print("cutoff : "+str(k)) # ditermined cutoff / percentage match criterion.
    d={}
    for i in range(len(dataset)):
        d[dataset[i]]=[]
        for j in range(len(dataset)):
            if(dataset[i]!=dataset[j]):
                if(KMP(dataset[i],dataset[j],2,k)==1):
                    d[dataset[i]].append(dataset[j])
    create_csv(out_filename,d)
    return


# In[9]:


process("data1.csv","output.csv")
end=time.time()
print("time taken to execute : "+str(end-start)+"seconds")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




