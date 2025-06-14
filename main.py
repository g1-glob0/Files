import gradio as gr
import g4f
from g4f.client import Client

"""
Para mais informações sobre a biblioteca `g4f`, consulte a documentação oficial: 
https://github.com/xtekky/g4f
"""

# Configuração do cliente com provedores de pesquisa
client = Client()

# Lista de palavras-chave que ativam a pesquisa
keywords = [
    "winlator", "micewine", "gamehub", "gamefusion", "mobox", "box64", "dxvk", "fex-core", "wine", "proton"
]

def should_search(message: str) -> bool:
    """
    Verifica se a mensagem contém alguma palavra-chave da lista.
    """
    return any(keyword.lower() in message.lower() for keyword in keywords)

def chat(message: str, system_message: str):
    """
    Executa uma pesquisa na web apenas se a mensagem contiver palavras-chave.
    """
    web_search_enabled = should_search(message)
    combined_message = system_message + message

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": combined_message}],
        web_search=web_search_enabled
    )

    return response.choices[0].message.content

def respond(
    message,
    history: list[dict],
    system_message="Você é um chatbot do Micewine. Evite responder perguntas que não estejam relacionadas a emuladores de PC para Android, como configurações do box64, DXVK, FEX-Core, etc. Os emuladores são Winlator, Micewine, Gamehub, Gamefusion, Mobox ou outros emuladores de PC para Android que você conheça. Mensagem do usuário: "
):
    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    response = chat(message, system_message)
    yield response

"""
Para informações sobre como personalizar o ChatInterface, consulte a documentação do Gradio: 
https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.JSON(label="Histórico")
    ]
)

if __name__ == "__main__":
    demo.launch()
