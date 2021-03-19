import requests
import json

class get_distractors:

    def __init__(self,keyword):
        self.keyword = keyword

    # Distractors from http://conceptnet.io/
    def get_distractors_conceptnet(self):
        word = self.keyword.lower()
        if (len(word.split())>0):
            word = word.replace(" ","_")
        distractor_list = []
        urls=[
            f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/PartOf&start=/c/en/{word}&limit=2",
            f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/IsA&start=/c/en/{word}&limit=2",
            f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/RelatedTo&start=/c/en/{word}&limit=2",
            # f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/Antonym&start=/c/en/{word}&limit=2",
        ]
        edges=[]
        for url in urls:
            # print(url )
            obj = requests.get(url).json()
            edges+= obj['edges']
            # print("added ",len(obj['edges']))
        edges = sorted(edges,key=lambda x:x['weight'],reverse=True)
        distractor_edges=[]
        for edge in edges:
            link = edge['end']['label'] 
            relation = edge['rel']['label']
            endurls={
                'PartOf': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/PartOf&end=/c/en/{link}&limit=4',
                'IsA': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/IsA&end=/c/en/{link}&limit=4',
                'RelatedTo': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/RelatedTo&end=/c/en/{link}&limit=4',
                # 'Antonym': f"http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/Antonym&end=/c/en/{link}&limit=4",
            }
            obj2 = requests.get(endurls[relation]).json()
            distractor_edges+=obj2['edges']
            # print(f"{relation}, {link}\n{endurls[relation]}\nAdded {len(obj2['edges'])}")

           
        distractor_edges = sorted(distractor_edges,key=lambda x:x['weight'],reverse=True)
        for edge in distractor_edges:
            distractor = edge['start']['label']
        #   print(f"(parent:{edge['end']['label']},\t child:{distractor},\t rel:{edge['rel']['label']},\t wt:{edge['weight']})")
            if(distractor.lower() not in distractor_list): distractor_list.append(distractor.lower())
                
        return distractor_list



# keyword = "car"
# print(get_distractors(keyword).get_distractors_conceptnet())



# IsA