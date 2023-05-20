"""
テキスト前処理
"""
import re 
def split_url(text:str):
    pattern = "(https?://[A-Za-z0-9_/:%#$&?()~.=+-]+?(?=https?:|[^A-Za-z0-9_/:%#$&?()~.=+-]|$))"
    return [text for text in re.split(pattern, text) if text != ""]
