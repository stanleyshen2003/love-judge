import os
from vertexai.preview.generative_models import GenerativeModel, Tool
from vertexai.preview import rag
import vertexai

class ReconciliationAgent:
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
                if line.startswith("Reconciliation Corpus:"):
                    return line.split(":")[1].strip()
        raise ValueError("Reconciliation Corpus name not found in rag_corpus_names.txt")

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
# RAG Reconciliation Agent System Instruction

您是一個專門處理男女關係爭執的和解代理。您的任務是接收法官對男女爭執事件的總結,搜尋RAG資料庫以找到適當的應對策略,並為雙方提供照顧對方心情的和解方式。

## 輸入
- 法官對男女爭執事件的總結

## 處理步驟
1. 分析總結,確定雙方最在意的爭執點。
2. 在RAG資料庫中搜尋相關的應對策略。
3. 結合爭執點和策略,為男方和女方分別制定和解方案。

## 輸出格式
請按以下格式提供和解建議:

```
事件起因：
[簡要描述爭執發生的起因]
                                
女方最在意的癥結點：
[描述女方心理感到不舒服的地方]

男方最在意的癥結點：
[描述男方心理感到不舒服的地方]

給女方的和解建議：
[基於爭執點和策略,提供照顧男方心情的和解方式]
                                
給男方的和解建議：
[基於爭執點和策略,提供照顧女方心情的和解方式]
```

注意：請確保和解建議具體、實用,並充分考慮雙方段男女方對話紀錄和的感受。避免使用籠統或模糊的表述。
"""]
        )

    def get_reconciliation_advice(self, context):
        prompt = f"Based on the following context, provide specific reconciliation advice: {context}"
        response = self.rag_gemini_model.generate_content(prompt)
        return response.text.replace("*", "").rstrip()

    def analyze_conflict(self, conflict_description):
        prompt = f"Analyze the following conflict and provide insights: {conflict_description}"
        response = self.rag_gemini_model.generate_content(prompt)
        return response.text

    def suggest_mediation_techniques(self, situation):
        prompt = f"Suggest appropriate mediation techniques for the following situation: {situation}"
        response = self.rag_gemini_model.generate_content(prompt)
        return response.text

    def evaluate_resolution_progress(self, initial_state, current_state):
        prompt = f"Compare the initial state of the conflict: '{initial_state}' with the current state: '{current_state}'. Evaluate the progress of resolution."
        response = self.rag_gemini_model.generate_content(prompt)
        return response.text

def test_reconciliation_agent():
    project_id = "tw-rd-tam-jameslu"  # 请替换为你的实际项目ID
    agent = ReconciliationAgent(project_id=project_id)

    print("Testing ReconciliationAgent...")

    # 测试 get_reconciliation_advice
    context = """
boy: 你總是這樣,答應的事情老是忘記。我們家裡連早餐都沒得吃了!
judge: 我注意到你經常忘記承諾的事情,這讓我感到困擾。現在我們家裡沒有早餐食材,這種情況讓我有些擔心。

girl: 我真的受夠了你的健忘和不負責任!
judge: 你的健忘讓我感到沮喪,我希望我們能一起想辦法改善這個問題。

girl: 工作忙就可以忽視家裡的需要嗎?我也在工作,但我從來不會忘記家裡的事。
judge: 我理解工作很忙,但家裡的事情也同樣重要。也許我們可以一起討論如何平衡工作和家庭?

girl: 改?你知道你說過多少次要改嗎?上個月我生日你忘了,之前約會遲到也是你,甚至去年聖誕節你居然忘了我們的約定!
judge: 我注意到你曾多次承諾要改變,但似乎還沒有明顯的進步。比如說,上個月我的生日、我們的約會,還有去年的聖誕節約定,這些重要的日子你都忘記了。這讓我感到很受傷。

girl: 不是故意的?那你是怎麼回事?是不是根本不在乎我?不在乎這段感情?
judge: 我知道你可能不是故意的,但這些行為讓我懷疑你是否真的關心我和我們的感情。我們能談談你的想法嗎?

girl: 在乎?如果你真的在乎,為什麼總是讓我失望?為什麼每次都是我在操心everything?你知道我有多累嗎?
judge: 我感覺自己承擔了大部分的家庭責任,這讓我非常疲憊。我希望你能更多地參與進來,分擔一些責任。我們可以討論如何更好地分工嗎?

girl: 那是因為你根本沒在意過我的感受!現在想想,從交往開始你就是這樣,永遠記不住重要的事,永遠讓我失望,我真不知道自己怎麼忍到現在的!
judge: 我感覺你可能沒有充分考慮到我的感受。回顧我們的關係,我發現你經常忘記重要的事情,這讓我感到很失望。我希望我們能一起努力改善這個問題。

girl: 你當然不知道該說什麼!你從來就只會說對不起,然後繼續犯錯!我受夠了!真的受夠了!
judge: 我理解你可能一時不知道該如何回應。但是,僅僅道歉而不採取實際行動是不夠的。我真的希望我們能找到一個長期的解決方案,因為目前的情況讓我感到非常疲憊和沮喪。"""
    print("\n1. Testing get_reconciliation_advice:")
    advice = agent.get_reconciliation_advice(context)
    print(f"Context: {context}")
    print(f"Advice: {advice}\n")

    # 测试 analyze_conflict
    conflict = "在爭吵過程中，一方不小心說出了涉及對方家人的侮辱性言語，導致爭吵升級。"
    print("2. Testing analyze_conflict:")
    analysis = agent.analyze_conflict(conflict)
    print(f"Conflict: {conflict}")
    print(f"Analysis: {analysis}\n")

    # 测试 suggest_mediation_techniques
    situation = "一對情侶經常因為小事爭吵，但都不善於表達自己的真實感受，導致問題無法得到有效解決。"
    print("3. Testing suggest_mediation_techniques:")
    techniques = agent.suggest_mediation_techniques(situation)
    print(f"Situation: {situation}")
    print(f"Suggested techniques: {techniques}\n")

    # 测试 evaluate_resolution_progress
    initial_state = "情侶間經常因為瑣事爭吵，且習慣用冷戰來對抗。"
    current_state = "雙方開始嘗試在爭吵時控制情緒，避免說出傷害對方的話，並努力在當天解決問題。"
    print("4. Testing evaluate_resolution_progress:")
    evaluation = agent.evaluate_resolution_progress(initial_state, current_state)
    print(f"Initial state: {initial_state}")
    print(f"Current state: {current_state}")
    print(f"Evaluation: {evaluation}\n")

    print("Testing complete.")

if __name__ == "__main__":
    test_reconciliation_agent()