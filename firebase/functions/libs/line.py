import requests
class LineApiRequest():
    def __init__(self,line_key:str) -> None:
        self.line_key = line_key
        self.headers = {'content-type': 'application/json',"Authorization":f"Bearer {line_key}"}

    def push_message(self,to_id:str,text:str):
        res = requests.post('https://api.line.me/v2/bot/message/push', json={
        "to":to_id,
        "messages":[
            {
                "type":"text",
                "text":text
            }
        ]
        },headers=self.headers)
        return res


class LineApiResponseData():
    def __init__(self,data) -> None:
        self.events = [LineApiResponseDataEvent(e) for e in data["events"]] if "events" in data else []
    
    """
    events先頭のeventにメッセージがあれば返します。なければNone
    """
    def get_first_message(self):
        events = self.events
        message:LineApiResponseDataEventMessage = None
        if len(events) > 0:
            message = events[0].message
        return message

class LineApiResponseDataEvent():
    def __init__(self,event) -> None:
        self.type = event["type"] if "type" in event else ""
        self.message = LineApiResponseDataEventMessage(event["message"]) if "message" in event else None
class LineApiResponseDataEventMessage():
    def __init__(self,message) -> None:
        self.type = message["type"] if "type" in message else ""
        self.id =   message["id"] if "type" in message else ""
        self.text = message["text"] if "text" in message else ""
        
