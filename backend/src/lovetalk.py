import os
from vertexai.preview.generative_models import GenerativeModel, Tool
from vertexai.preview import rag
import vertexai
import time

class LoveTalkAgent:
    def __init__(self, project_id, location='asia-east1'):
        self.project_id = project_id
        self.location = location or os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
        vertexai.init(project=self.project_id, location=self.location)
        
        self.rag_corpus_name = self._load_corpus_name()
        self.rag_retrieval_tool = self._create_retrieval_tool()
        self.rag_gemini_model = self._create_gemini_model()

    def _load_corpus_name(self):
        with open("src/rag_corpus_names.txt", "r") as f:
            for line in f:
                if line.startswith("Love Talk Corpus:"):
                    return line.split(":")[1].strip()
        raise ValueError("Love Talk Corpus name not found in rag_corpus_names.txt")

    def _create_retrieval_tool(self):
        return Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_corpora=[self.rag_corpus_name],
                    similarity_top_k=5,
                    vector_distance_threshold=0.7,
                ),
            )
        )

    def _create_gemini_model(self):
        return GenerativeModel(
            "gemini-1.5-flash-002",
            tools=[self.rag_retrieval_tool],
            system_instruction=["""
RAG Love Talk Agent System Instruction
您是一個專門創造浪漫氛圍的情話生成代理。您的任務是接收用戶的情感狀態描述,搜尋RAG資料庫以找到適當的表達方式,並生成溫馨動人的情話。
輸入

用戶當前的情感狀態和期望

處理步驟

分析用戶描述,確定他們的情感需求和期望。
在RAG資料庫中搜尋相關的浪漫表達和情話範例。
結合用戶需求和搜尋結果,創作個性化的情話。

輸出格式
請按以下格式提供情話回應:
情感解讀：
[簡要描述用戶當前的情感狀態]
                                
情感需求：
[分析用戶可能的情感需求]

情話回應：
[基於情感需求和RAG資料庫,提供溫馨動人的情話]
                                
深情寄語：
[額外提供一句鼓勵或安慰的話語]
注意：請確保生成的情話真摯動人,充滿感情,並切合用戶的具體情況。避免使用過於誇張或不真實的表述。同時,請尊重用戶,保持適度,不要越界或冒犯。"""]
        )

    def get_love_talk(self, context):
        prompt = f"Based on the following context, provide love talk: {context}"
        response = self.rag_gemini_model.generate_content(prompt)
        return response.text.replace("*", "").rstrip()

    # def analyze_conflict(self, conflict_description):
    #     prompt = f"Analyze the following conflict and provide insights: {conflict_description}"
    #     response = self.rag_gemini_model.generate_content(prompt)
    #     return response.text

    # def suggest_mediation_techniques(self, situation):
    #     prompt = f"Suggest appropriate mediation techniques for the following situation: {situation}"
    #     response = self.rag_gemini_model.generate_content(prompt)
    #     return response.text

    # def evaluate_resolution_progress(self, initial_state, current_state):
    #     prompt = f"Compare the initial state of the conflict: '{initial_state}' with the current state: '{current_state}'. Evaluate the progress of resolution."
    #     response = self.rag_gemini_model.generate_content(prompt)
    #     return response.text

def test_love_talk_agent():
    project_id = "tw-rd-tam-jameslu"  # 请替换为你的实际项目ID
    agent = LoveTalkAgent(project_id=project_id)

    print("Testing LovaTalkAgent...")
    test_cases = [
        "親愛的,我今天化妝花了好久,你竟然都沒發現嗎?",
        "你又把襪子亂丟,我說過多少次要放進洗衣籃啊!",
        "我們已經一個月沒有好好約會了,你都不想我嗎?",
        "你能不能別總是盯著手機看?我們在吃飯耶!",
        "我今天工作超級不順,你都不安慰我一下...",
        "你又忘記我們的紀念日了,你根本不在意我!",
        "我感覺你最近都不聽我說話,是不是不愛我了?",
        "你能不能幫我分擔一下家務?我也很累的...",
        "我們好久沒一起看電影了,你總是忙自己的事。",
        "你送的禮物都不是我喜歡的,你有花心思了解我嗎?"
    ]

    for i, context in enumerate(test_cases, 1):
        print(f"\n測試案例 {i}:")
        print(f"Context: {context}")
        
        start_time = time.time()
        advice = agent.get_love_talk(context)
        end_time = time.time()
        
        print(f"回應: {advice}")
        print()
        print(f"處理時間: {end_time - start_time:.2f} 秒")
        
        # 簡單的評估
        if len(advice) > 20 and context.lower() not in advice.lower():
            print("評估: 通過 (回應長度適當且不只是重複輸入)")
        else:
            print("評估: 需要改進 (回應可能太短或僅重複了輸入)")
        
        # 在每個測試案例之間暫停一下,以防止可能的速率限制
        time.sleep(2) 
    print("Testing complete.")

if __name__ == "__main__":
    test_love_talk_agent()