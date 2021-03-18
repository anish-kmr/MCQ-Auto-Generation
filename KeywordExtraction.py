#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm



class KeywordExtraction :
    def __init__(self , text):
        self.text = text
        
    def keywordExtract(self):
        nlp = en_core_web_sm.load()
        doc = nlp(self.text)
        
        sentences = [x for x in doc.sents]
        
        dict = {}
        for sent in sentences:
            keywords = [str(x) for x in nlp(str(sent)).ents]
                
            if len(keywords) == 0 :
                continue
                
            dict[sent] = keywords
            
        return dict


# In[ ]:




