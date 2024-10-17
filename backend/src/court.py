from gemini import Gemini
from prompts import Prompts

class Court():
    def __init__(self, project):
        self.prompts = Prompts()
        self.tone_correction = Gemini(system_instruction=self.prompts.get_prompt('tone_correction'), project=project)