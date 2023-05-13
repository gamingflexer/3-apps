import gradio as gr
import requests
from bs4 import BeautifulSoup

def clean_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# input = "Who are you?"
def chat_base(input):
    try:
        url = 'https://multimodalart-chatglm-6b.hf.space/api/predict/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "session_hash":  str(input),
            "event_id":  str(input),
            "data": [
                str(input)
            ],
            "event_data": str(input),
            "fn_index": 0,
            "batched": False,
            "request": {}
        }
        response = requests.post(url, headers=headers, json=data)
        return clean_html(response.json()['data'][0][0][1])
    except Exception as e:
        print(e)
        return f" ERROR : {e}"
    

def chat(message):
    history = gr.get_state() or []
    print(history)
    response = chat_base(message)
    history.append((message, response))
    gr.set_state(history)
    html = "<div class='chatbot'>"
    for user_msg, resp_msg in history:
        html += f"<div class='user_msg'>{user_msg}</div>"
        html += f"<div class='resp_msg'>{resp_msg}</div>"
    html += "</div>"
    return response

iface = gr.Interface(chat_base, gr.inputs.Textbox(label="Ask Chatbot a Question"), "text", allow_screenshot=False, allow_flagging=False,title="CHATGLM Chatbot")
iface.launch(server_name="0.0.0.0")