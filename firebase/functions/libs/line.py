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

class LineApiResponseDataEvent():
    def __init__(self,event) -> None:
        self.type = event["type"] if "type" in event else ""
        self.timestamp = event["timestamp"] if "timestamp" in event else 0
        self.message = LineApiResponseDataEventMessage(event["message"]) if "message" in event else None
        self.source = LineApiResponseDataEventSource(event["source"]) if "source" in event else None
    
    def to_dict(self):
        d = {"timestamp":self.timestamp}
        if self.message is not None:
            d.update(self.message.message_dict)
        if self.source is not None:
            d.update(self.source.source_dict)
        return d

class LineApiResponseDataEventMessage():
    def __init__(self,message) -> None:
        self.type = message["type"] if "type" in message else ""
        self.id =   message["id"] if "type" in message else ""
        self.text = message["text"] if "text" in message else ""
        self.message_dict = message
class LineApiResponseDataEventSource():
    def __init__(self,source) -> None:
        self.type = source["type"] if "type" in source else ""
        self.user_id = source["userId"] if "userId" in source else ""
        self.source_dict = source
