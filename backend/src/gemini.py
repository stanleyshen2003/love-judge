import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

class Gemini:
    def __init__(self, system_instruction, project, location = "asia-east1", model_name = "gemini-1.5-flash-002"):
        vertexai.init(project=project, location=location)
        self.model = GenerativeModel(
            model_name,
            system_instruction=[system_instruction]
        )
        self.chat = self.model.start_chat()
        
        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }
        self.safety_settings = [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
        ]
    def query(self, query):
        return self.chat.send_message(
            [query],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

if __name__ == '__main__':
    gemini = Gemini("I want to create a chatbot that can answer questions and have a conversation with users.", "tw-rd-tam-stanleyshen")
    response = gemini.query("""What is the capital of France?""")
    print(response)
    response = gemini.query("""What is the capital of Germany?""")
    print(response)
    