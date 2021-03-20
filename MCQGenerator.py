import random
from pipelines import Summarizer
from KeywordExtraction import KeywordExtraction
from distractor import get_distractors_conceptnet

class MCQGenerator:
    def __init__(self,text,num_question):
        self.num_question = num_question
        self.summarizer = Summarizer(text,num_question)
        # Will Summarize depending on the length of content when uploaded in Courses
        # self.summary = self.summarizer.summarize() 
        self.keyword_extractor = KeywordExtraction(text)
    
    def generate(self):
        sent_key = self.keyword_extractor.extract()
        questions=[]
        for candidate in sent_key:
            sentence,keys = candidate["sentence"],candidate["keywords"]
            qualified_distractors=[]
            qualified_key=""
            for key in keys:
                distractors = get_distractors_conceptnet(key['text'])
                if(len(distractors)>3):
                    qualified_distractors=distractors
                    qualified_key=key['text']
                    sentence_with_blank = sentence[:key['start']]+"_"*10 + sentence[key['end']:]
                    break
            if(len(qualified_distractors)<3):continue
            options=qualified_distractors[:3]+[qualified_key]
            random.shuffle(options)
            more_wrong_choices = [] if len(qualified_distractors)<4 else qualified_distractors[3:]
            questions.append({
                "sentence":sentence_with_blank,
                "key": qualified_key,
                "options":options,
                "more_wrong_choices":more_wrong_choices
            })
            if(len(questions)==self.num_question):break
        return questions

# t="""
# The Nile River fed Egyptian civilization for hundreds of years. It begins near the equator in Africa and flows north to the Mediterranean Sea. A delta is an area near a river’s mouth where the water deposits fine soil called silt. This soil was fertile, which means it was good for growing crops. The red land was the barren desert beyond the fertile region. When the birds arrived, the annual flood waters would soon follow. Then they used a tool called a shaduf to spread the water across the fields. These innovative, or new, techniques gave them more farmland. They were the first to grind wheat into flour and to mix the flour with yeast and water to make dough rise into bread. Egyptians often painted walls white to reflect the blazing heat. Poorer Egyptians simply went to the roof to cool off after sunset. Even during the cool season, chipping minerals out of the rock was miserable work. One ancient painting even shows a man ready to hit a catfish with a wooden hammer. A boomerang is a curved stick that returns to the person who threw it.) The river’s current was slow, so boaters used paddles to go faster when they traveled north with the current. Going south, they raised a sail and let the winds that blew in that direction push them. The Nile provided so well for Egyptians that sometimes they had surpluses, or more goods than they needed. Ancient Egypt had no money, so people exchanged goods that they grew or made. This prosperity made life easier and provided greater opportunities for many Egyptians. For example, some ancient Egyptians learned to be scribes, people whose job was to write and keep records. Some skilled artisans erected stone or brick houses and temples. A few Egyptians traveled to the upper Nile to trade with other Africans. They brought back exotic woods, animal skins, and live beasts. Egyptians created a government that divided the empire into 42 provinces. Many officials worked to keep the provinces running smoothly. Priests followed formal rituals and took care of the temples. Before entering a temple, a priest bathed and put on special linen garments and white sandals. Together, the priests and the ruler held ceremonies to please the gods. By doing so, they hoped to maintain the social and political order. In Egypt, people became slaves if they owed a debt, committed a crime, or were captured in war. Unlike other ancient African cultures, in Egyptian society men and women had fairly equal rights. For example, they could both own and manage their own property. Children in Egypt played with toys such as dolls, animal figures, board games, and marbles. Almost all Egyptians married when they were in their early teens. As in many ancient societies, much of the knowledge of Egypt came about as priests studied the world to find ways to please the gods. Doctors believed that the heart controlled thought and the brain circulated blood, which is the opposite of what is known now. Early Egyptians created a hieroglyphic system with about 700 characters. Legend says a king named Narmer united Upper and Lower Egypt. Some historians think Narmer actually represents several kings who gradually joined the two lands. It combined the red Crown of Lower Egypt with the white Crown of Upper Egypt. When a king died, one of his children usually took his place as ruler. Historians divide ancient Egyptian dynasties into the Old Kingdom, the Middle Kingdom, and the New Kingdom. The Old Kingdom started about 2575 B.C., when the Egyptian empire was gaining strength. In such a case, a rival might drive him from power and start a new dynasty. The first rulers of Egypt were often buried in an underground tomb topped by mud brick. They replaced the mud brick with a small pyramid of brick or stone. It is called a step pyramid because its sides rise in a series of giant steps. He ordered the construction of the largest pyramid ever built. One reason is that the pyramids drew attention to the tombs inside them. Grave robbers broke into the tombs to steal the treasure buried with the pharaohs. Egyptians believed that if a tomb was robbed, the person buried there could not have a happy afterlife. This way, the pharaohs hoped to protect their bodies and treasures from robbers. This was to confuse grave robbers about which passage to take. Tombs were supposed to be the palaces of pharaohs in the afterlife. Mourners filled the tomb with objects ranging from food to furniture that the mummified pharaoh would need. Such activities included growing and preparing food, caring for animals, and building boats. Only a secret tomb built for a New Kingdom pharaoh was ever found with much of its treasure untouched. The dazzling riches found in this tomb show how much wealth the pharaohs spent preparing for the afterlife. This period of Egyptian history is called the Middle Kingdom."""
# a = MCQGenerator(t,5).generate()
# for i in a:
#     print(i,"\n\n")

# print(len(a))