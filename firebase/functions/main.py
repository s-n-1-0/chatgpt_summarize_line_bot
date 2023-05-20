from firebase_functions import https_fn
from firebase_admin import initialize_app
import sys, os
import json
sys.path.append(os.path.dirname(os.path.abspath("__file__"))) #これ無いとエミュレータで下層ファイルを読み込めなかった。
from libs import LineApiResponseData,LineApiRequest
initialize_app()

@https_fn.on_request(secrets=["LINE_KEY","LINE_SEND_ID"])
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    data = json.loads(req.data.decode("utf-8"))
    print(data)
    line_res = LineApiResponseData(data)
    message = line_res.get_first_message()

    #メッセージがあるならそれに対応する処理を行う
    if message is not None and message.text == "要約して":
        line_req = LineApiRequest(os.environ["LINE_KEY"])
        line_req.push_message(os.environ["LINE_SEND_ID"],text="要約しました。")
    return https_fn.Response(f"Recieved")
@https_fn.on_request()
def test(req: https_fn.Request) -> https_fn.Response:
    #print(req.data)
    print(os.getcwd())
    return https_fn.Response(f"2000")