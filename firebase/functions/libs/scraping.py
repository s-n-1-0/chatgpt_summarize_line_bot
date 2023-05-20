# %%
import requests
import re
from bs4 import BeautifulSoup

#再帰的にテキスト部分を抜き取る(改行調整のため親ノードでget_textを使用しない)
def get_node_text(node):
    text = ""
    children = node.findChildren(recursive=False)
    if (node.name == "body" or node.name == "div" or node.name == "p") and len(children) > 0:
        text = "".join([get_node_text(child) for child in children]) + "\n"
    elif node.name == "br":
        text = "\n"
    else:
        text = node.get_text().strip()
    return text

def get_text(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style","header","footer","img","nav"]):
        script.decompose()
    #lines = [line for line in lines if line != ""] #余計な改行を消すけど可読性下がる
    text = get_node_text(soup.find("body"))
    text = re.sub("\n+", "\n", text)
    text = re.sub('[ 　]+', ' ', text)
    return text
# %%
if __name__ == "__main__":
    print(get_text("https://prtimes.jp/main/html/rd/p/000000027.000100410.html"))

# %%
