from .gemini import Gemini
from .prompts import Prompts

class User():
    def __init__(self, name, project):
        self.name = name
        self.filtered_records = []
        self.prompts = Prompts()
        self.filtered_records.append({'text':self.prompts.get_prompt('judge_start'), 'sender':'judge'})
        
        system_instruction_lawyer = self.prompts.get_prompt('lawyer')
        self.lawyer = Gemini(system_instruction=system_instruction_lawyer, project=project)
        self.lawyer_records = []
        self.lawyer_new_info = []
        
    def message_append(self, message):
        self.filtered_records.append({'text': message, 'sender': self.name})
        self.lawyer_new_info.append(self.name + ": " + message)
    
  
    def ask_lawyer(self, message):
        if len(self.lawyer_new_info) > 0:
            self.lawyer.insert_record(self.lawyer_new_info)
            self.lawyer_new_info = []
        self.lawyer_records.append(self.lawyer.query(message))
        self.lawyer_new_info = []
        return self.lawyer_records