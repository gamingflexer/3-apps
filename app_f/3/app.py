import gradio as gr
import requests
from bs4 import BeautifulSoup

def clean_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# input = "Who are you?"
def chat_base(input):
    try:
        response = requests.post("https://tloen-alpaca-lora.hf.space/run/predict", json={
        "data": [
            str(input),
            str(input),
            0.1,
            0.75,
            40,
            4,
            128,
        ]
    }).json()

        return clean_html(response["data"][0])
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

iface = gr.Interface(chat_base, gr.inputs.Textbox(label="Ask Chatbot a Question"), "text", allow_screenshot=False, allow_flagging=False,title="Alpaca Chatbot")
iface.launch()