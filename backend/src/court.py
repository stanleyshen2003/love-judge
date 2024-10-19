from .gemini import Gemini
from .prompts import Prompts
from .user import User

class Court():
    def __init__(self, project):
        self.prompts = Prompts()
        self.tone_correction = Gemini(system_instruction=self.prompts.get_prompt('tone_correction'), project=project)
        self.summarizer = Gemini(system_instruction=self.prompts.get_prompt('summarizer'), project=project)
        self.stage = 0
        self.stages = {
            0: "boy_girl",
            1: "summarize",
            2: "boy_girl",
            3: "summarize",
            4: "boy_girl",
            5: "analyze",
        }
        self.message_recieved = [{'text':self.prompts.get_prompt('judge_start'), 'sender':'judge'}]
        self.boy = User(name="boy", project=project)
        self.girl = User(name="girl", project=project)
        self.girl_done = False
        self.boy_done = False
        
    def message_in(self, user, message):
        filtered_message = self.tone_correction.prompt_once(message)
        if user == 'boy':
            self.boy.message_append(message=message, user=user)
            self.girl.message_append(message=filtered_message, user=user)
            self.boy_done = True
        else:
            self.boy.message_append(message=filtered_message, user=user)
            self.girl.message_append(message=message, user=user)
            self.girl_done = True
        
        self.message_recieved.append({'text': message, 'sender': user})
        
        if self.boy_done and self.girl_done:
            self.stage += 1
        
        if self.stages[self.stage] == "summarize":
            ## TBD ---------------------------------------------------------
            summarize_message = [mes['sender'] + ": " + mes['text'] for mes in self.message_recieved]
            summarize_message = "\n".join(summarize_message)
            print(summarize_message)
            summary = self.summarizer.prompt_once("\n".join(summarize_message))
            self.message_recieved.append({'text': summary, 'sender': 'judge'})
            self.boy.message_append(summary, user='judge')
            self.girl.message_append(summary, user='judge')
            self.girl_done = False
            self.boy_done = False
            self.stage += 1
        
        if user == 'boy':
            return self.boy.filtered_records
        else:
            return self.girl.filtered_records
        
        
            
            
            