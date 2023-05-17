# %%
from scraping import get_text
from text import split_url
from key import *
import openai
def summarize_with_gpt(text:str,limit_text_size = 2000,system_text="要約してください。"):
    text =  text[:limit_text_size] #過剰な問い合わせ防止
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_text},
        {"role": "user", "content": text[:2000]}
    ]   
    )
    res_text = response.choices[0].message.content
    return res_text

# %%
def scraping_and_summarize_with_gpt(text:str):
    limit_scraping_list = 5
    limit_tmp_text_size = 3000
    text_url_lst = split_url(text) #テキストとURLが分離されたリスト
    tmp_text = ""
    scraping_list = []
    for text in text_url_lst:
        if text.startswith("http"):
            tmp_text += "[URL削除済]"
            scraping_list.append(get_text(text))
        else:
            tmp_text += text
    tmp_text += "\n ■URL削除済は以下の内容のURLでした。\n"
    
    scraping_list = scraping_list[:limit_scraping_list]
    res_gpt_list = []
    for sc_text in scraping_list:
         res_gpt_list.append(summarize_with_gpt(sc_text))
    tmp_text += "\n\n".join(res_gpt_list)
    tmp_text = tmp_text[:limit_tmp_text_size] #結合後のテキスト最大サイズ
    result_text = summarize_with_gpt(tmp_text,system_text="要約してください。内容は、複数の話題から構成されている場合があります。")
    return result_text

# %%
if __name__ == "__main__":
    test_text = 'https://prtimes.jp/main/html/rd/p/000000027.000100410.html，https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC'
    t = scraping_and_summarize_with_gpt(test_text)
    print(t)

