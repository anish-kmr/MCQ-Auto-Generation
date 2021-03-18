import requests
import json
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn

class get_distractors:

    def __init__(self,keyword,sentence):
        self.keyword = keyword
        self.sentence = sentence

    def get_distractors_wordnet(self):
        distractors=[]
        word= self.keyword.lower()
        orig_word = word
        if len(word.split())>0:
            word = word.replace(" ","_")
        hypernym = syn.hypernyms()
        if len(hypernym) == 0: 
            return distractors
        for item in hypernym[0].hyponyms():
            name = item.lemmas()[0].name()
            #print ("name ",name, " word",orig_word)
            if name == orig_word:
                continue
            name = name.replace("_"," ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)
        return distractors

    def get_wordsense(self):
        word = self.keyword.lower()
        
        if len(word.split())>0:
            word = word.replace(" ","_")
        
        
        synsets = wn.synsets(word,'n')
        if synsets:
            wup = max_similarity(self.sentance, word, 'wup', pos='n')
            adapted_lesk_output =  adapted_lesk(self.sentance, word, pos='n')
            lowest_index = min (synsets.index(wup),synsets.index(adapted_lesk_output))
            return synsets[lowest_index]
        else:
            return None

    # Distractors from http://conceptnet.io/
    def get_distractors_conceptnet(self):
        word = self.keyword.lower()
        original_word= word
        if (len(word.split())>0):
            word = word.replace(" ","_")
        distractor_list = [] 
        url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word)
        obj = requests.get(url).json()

        for edge in obj['edges']:
            link = edge['end']['term'] 

            url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractor_list and original_word.lower() not in word2.lower():
                    distractor_list.append(word2)
                    
        return distractor_list

