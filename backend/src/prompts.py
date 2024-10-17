

class Prompts():
    def __init__(self):
        self.prompts = {
            'tone_correction': """你需要將帶有攻擊性或嚴厲語氣的訊息改寫為更中立且友好的語調。你也應該將主要重點提取並總結為要點。改寫後的版本應該保持禮貌，緩解任何緊張氣氛，同時仍保留原訊息的主要觀點。

針對每條有關爭執的訊息，提供一個語氣更柔和的版本。

確保輸出內容尊重、簡潔且清晰。

範例使用情境：
輸入 (Input) 提示:
你每次下班回家都不跟我說話！你只顧著玩手機，根本不在乎我。我真的受夠了，這樣下去我們還怎麼過日子？

輸出 (Output):
我覺得你每次下班回家都沒怎麼跟我交流，這讓我有點難過。你好像總是在忙著看手機，讓我覺得不被重視。這種情況真的讓我感到很疲憊，我希望我們可以更好地溝通，這樣我們的關係才能更順利。""",
        }

    def get_prompt(self, key):
        return self.prompts[key]
    def get_prompt(self, key1, key2):
        return self.prompts[key1][key2]