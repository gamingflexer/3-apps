import gradio as gr
from gradio_client import Client
from bs4 import BeautifulSoup

client = Client("https://monster-vicuna-7b.hf.space/")

def clean_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# input = "Who are you?"
def chat_base(input):
    try:
        result = client.predict(
				str(input),	# str representing string value in 'Prompt' Textbox component
				fn_index=0)
        return clean_html(result)
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

iface = gr.Interface(chat_base, gr.inputs.Textbox(label="Ask Chatbot a Question"), "text", allow_screenshot=False, allow_flagging=False,title="Vicuna Chatbot")
iface.launch(server_name="0.0.0.0")