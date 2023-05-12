import gradio as gr
import requests

# input = "Who are you?"
def chat_base(input):
  response = requests.post("https://gradio-chatbot.hf.space/run/predict", json={
    "data": [
      str(input),
    ]
  }).json()
  return response["data"][0]
  
import gradio as gr

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

iface = gr.Interface(chat_base, gr.inputs.Textbox(label="Ask Chatbot a Question"), "text", allow_screenshot=False, allow_flagging=False)
iface.launch()