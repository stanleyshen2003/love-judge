from .gemini import Gemini, Lawyer
from .prompts import Prompts

class User():
    def __init__(self, name, project):
        self.name = name
        self.filtered_records = []
        self.prompts = Prompts()
        self.filtered_records.append({'text':self.prompts.get_prompt('judge_start'), 'sender':'judge'})
        
        system_instruction_lawyer = self.prompts.get_prompt('lawyer_' + name  + '_sys')
        self.lawyer = Lawyer(system_instruction=system_instruction_lawyer, project=project)
        init_mes = self.prompts.get_prompt('lawyer_' + name)
        self.lawyer_records = [{'text': init_mes, 'sender': 'lawyer'}]
        self.lawyer_new_info = []
        
    def message_append(self, message, user):
        self.filtered_records.append({'text': message, 'sender': user})
        self.lawyer_new_info.append(self.name + ": " + message)
    
  
    def ask_lawyer(self, message, user):
        if len(self.lawyer_new_info) > 0:
            self.lawyer.insert_record(self.lawyer_new_info)
            self.lawyer_new_info = []
        self.lawyer_records.append({"text": message, "sender": user})
        self.lawyer_records.append({"text": self.lawyer.query(message), "sender": "lawyer"})
        self.lawyer_new_info = []
        return self.lawyer_records