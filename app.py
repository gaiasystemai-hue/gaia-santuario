import os
import json
from datetime import datetime
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(
    page_title="Gaia • Assistente IA",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injeção direta do manifesto PWA para permitir instalação e abertura como app autónoma
st.markdown("""
    <head>
        <link rel="manifest" href='data:application/manifest+json;charset=utf-8,{"name":"Gaia • Assistente IA","short_name":"Gaia","start_url":".","display":"standalone","background_color":"#0e1117","theme_color":"#0e1117"}'>
    </head>
""", unsafe_allow_html=True)

# Estilização limpa e profissional
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    .stTextInput textarea {
        background-color: #1a1c23 !important;
        color: #e2e8f0 !important;
        border: 1px solid #30363d !important;
    }
    .stChatMessage {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #0d1117;
    }
    </style>
""", unsafe_allow_html=True)

# Caminho para memória local em JSON
MEMORY_FILE = "gaia_memory.json"

def carregar_memoria():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_memoria(mensagens):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mensagens, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# Inicializar cliente Gemini com a chave secreta
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ A chave `GEMINI_API_KEY` não foi encontrada nos Segredos do Streamlit! Por favor, configura-a nas Definições (Advanced Settings).")
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar
with st.sidebar:
    st.markdown("### **Gaia**")
    st.caption("Assistente Inteligente & Produtividade")
    st.markdown("---")
    st.markdown(
        "Sou a Gaia, a tua assistente de inteligência artificial. "
        "Estou aqui para ajudar-te a organizar ideias, resolver problemas, escrever textos e otimizar o teu trabalho."
    )
    st.markdown("---")
    
    if st.button("🗑️ Limpar Histórico de Conversa"):
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        st.session_state.messages = []
        st.rerun()

# Interface principal
st.title("💡 Gaia — Assistente IA")
st.write("Um espaço direto e eficiente para te auxiliar nas tuas tarefas.")

# Histórico de conversas
if "messages" not in st.session_state:
    st.session_state.messages = carregar_memoria()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt do Sistema (Focado em assistência profissional e objetiva)
system_instruction = (
    "Tu és a Gaia, uma assistente de inteligência artificial profissional, eficiente, objetiva e prestativa. "
    "Comuniques num português de Portugal (pt-PT) natural e claro. "
    "O teu objetivo principal é ajudar o utilizador nas suas tarefas diárias, responder a dúvidas com precisão, auxiliar na programação, escrita e organização, mantendo sempre uma postura prestativa, lógica e focada em resultados."
)

# Entrada do utilizador
if prompt := st.chat_input("Escreve a tua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("A processar o pedido... 🔄")
        
        try:
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                )

            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.5,
                )
            )
            
            resposta_gaia = response.text
            message_placeholder.markdown(resposta_gaia)
            
            st.session_state.messages.append({"role": "assistant", "content": resposta_gaia})
            guardar_memoria(st.session_state.messages)
            
        except Exception as e:
            erro_msg = f"Ocorreu um erro ao processar o pedido: {e}"
            message_placeholder.markdown(erro_msg)
            
