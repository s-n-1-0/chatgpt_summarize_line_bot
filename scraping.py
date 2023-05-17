# %%
import requests
from bs4 import BeautifulSoup
from typing import List
url = "https://qiita.com/poorko/items/9140c75415d748633a10"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
for script in soup(["script", "style","header"]):
    script.decompose()
# %%
#再帰的にテキスト部分を抜き取る(改行調整のため親ノードでget_textを使用しない)
def get_text(node):
    text = ""
    children = node.findChildren(recursive=False)
    if (node.name == "body" or node.name == "div" or node.name == "p") and len(children) > 0:
        text = "".join([get_text(child) for child in children]) + "\n"
    else:
        text = node.get_text().strip()
    return text
lines = get_text(soup.find("body")).split("\n")
#lines = [line for line in lines if line != ""] #余計な改行を消すけど可読性下がる
print("\n".join(lines))
# %%
