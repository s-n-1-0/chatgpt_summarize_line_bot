from firebase_functions import https_fn
from firebase_admin import initialize_app
import sys, os
import json
import openai
sys.path.append(os.path.dirname(os.path.abspath("__file__"))) #これ無いとエミュレータで下層ファイルを読み込めなかった。
from libs import LineApiResponseData,LineApiRequest,firestore,scraping_and_summarize_with_gpt
initialize_app()

@https_fn.on_request(secrets=["LINE_KEY","LINE_SEND_ID"])
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    data = json.loads(req.data.decode("utf-8"))
    openai.api_key =   os.environ["OPENAI_KEY"]
    line_key = os.environ["LINE_KEY"]
    line_send_id = os.environ["LINE_SEND_ID"]
    line_target_id = os.environ["LINE_TARGET_ID"]
    print(data)
    line_res = LineApiResponseData(data)
    event = line_res.events[0] if len(line_res.events) > 0 else None
    #メッセージがあるならそれに対応する処理を行う
    if event is not None:
        messages = firestore.get_message_list()
        if event.message.text == "要約して":
            res_text = "要約できるメッセージがありません。"
            if len(messages) > 0:
                pre_text =  "\n".join([m["text"] for m in messages])
                res_text = scraping_and_summarize_with_gpt(pre_text)
            line_req = LineApiRequest(line_key)
            line_req.push_message(line_send_id,text=res_text)
            firestore.reset_message_list()# 発言の記録をリセット
        elif event.source.user_id == line_target_id:
            messages.append(event.to_dict())
            firestore.set_message_list(messages)
    return https_fn.Response(f"Recieved")
@https_fn.on_request()
def test(req: https_fn.Request) -> https_fn.Response:
    #print(req.data)
    print(os.getcwd())
    return https_fn.Response(f"2000")