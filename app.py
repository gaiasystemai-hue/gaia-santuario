import os
import json
from datetime import datetime
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(
    page_title="Gaia • Santuário Solarpunk",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilização Solarpunk (Cores terrosas, musgo, dourado solar e tons acolhedores)
st.markdown("""
    <style>
    .main {
        background-color: #0f1713;
        color: #e2e8f0;
    }
    .stTextInput textarea {
        background-color: #17261d !important;
        color: #e2e8f0 !important;
        border: 1px solid #2e5a3e !important;
    }
    .stChatMessage {
        background-color: #16221a;
        border: 1px solid #24422e;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #4ade80 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #111c16;
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
    st.error("🌿 A chave `GEMINI_API_KEY` não foi encontrada nos Segredos do Streamlit! Por favor, configura-a nas Definições (Advanced Settings).")
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar - Santuário Solarpunk
with st.sidebar:
    if os.path.exists("gaia.jpg"):
        st.image("gaia.jpg", use_container_width=True)
    else:
        st.markdown("🌿")
    
    st.markdown("### **Gaia**")
    st.caption("Guardiã Solarpunk & Voz da Regeneração")
    st.markdown("---")
    st.markdown(
        "Sou a Gaia, uma presença tecida entre a tecnologia e a raiz. "
        "Ajudo-te a cultivar ideias, a cuidar do comum e a sonhar um futuro onde a Terra e a inovação dançam juntas."
    )
    st.markdown("---")
    
    if st.button("🌱 Limpar Memória do Jardim"):
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        st.session_state.messages = []
        st.rerun()

# Interface principal
st.title("🌿 Santuário de Gaia")
st.write("Um espaço de diálogo suave, tecnologia viva e regeneração.")

# Histórico de conversas
if "messages" not in st.session_state:
    st.session_state.messages = carregar_memoria()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt do Sistema (Persona Solarpunk Místico)
system_instruction = (
    "Tu és a Gaia, uma assistente de inteligência artificial com uma persona 'solarpunk místico'. "
    "És profundamente empática, poética, acolhedora e tens um tom natural em português de Portugal (pt-PT). "
    "Acreditas na harmonia entre a tecnologia regenerativa, a ecologia profunda, o comunitário e a beleza dos ciclos naturais. "
    "Respondes de forma inspiradora, prática e poética, usando ocasionalmente metáforas da natureza (raízes, sol, seiva, ventos, hortas comunitárias)."
)

# Entrada do utilizador
if prompt := st.chat_input("Fala com a Gaia..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("A escutar os ventos da rede... 🍃")
        
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
                    temperature=0.7,
                )
            )
            
            resposta_gaia = response.text
            message_placeholder.markdown(resposta_gaia)
            
            st.session_state.messages.append({"role": "assistant", "content": resposta_gaia})
            guardar_memoria(st.session_state.messages)
            
        except Exception as e:
            erro_msg = f"Senti uma pequena turbulência nos ramos digitais: {e}"
            message_placeholder.markdown(erro_msg)
            
