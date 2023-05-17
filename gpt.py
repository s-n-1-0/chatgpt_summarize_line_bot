# %%
from scraping import get_text
from key import *
import openai

# スクレイピング
text = get_text("https://prtimes.jp/main/html/rd/p/000000027.000100410.html")
# %%

text = "テスト送信です。"


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "要約してください。"},
        {"role": "user", "content": text[:2000]}
    ]   
)
print(type(response))
print(response)

# %%
print(response.choices[0].message.content)
# %%
print("awdawd"[:2000])
# %%
