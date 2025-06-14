import gradio as gr
import g4f
from g4f.client import Client

"""
Para mais informações sobre a biblioteca `g4f`, consulte a documentação oficial: 
https://github.com/xtekky/g4f
"""

# Configuração do cliente com provedores de pesquisa
client = Client()

def chat(message: str):
    """
    Executa uma pesquisa na web usando `get_search_message` e retorna a resposta.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}],
        web_search=True
    )

    return response.choices[0].message.content


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = chat(message)


"""
Para informações sobre como personalizar o ChatInterface, consulte a documentação do Gradio: 
https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="Avoid answering questions that are not related to PC emulators for Android, such as box64 settings, DXVK, FEX-Core, etc. Emulators are Winlator, Micewine, Gamehub Gamefusion, Mobox or others that you know.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)

if __name__ == "__main__":
    demo.launch()
