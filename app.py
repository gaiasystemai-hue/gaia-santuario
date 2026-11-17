import os
import streamlit as st
import anthropic

# Configuração da página em modo mobile-first / full-screen
st.set_page_config(
    page_title="Gaia • Assistente IA",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estética Solarpunk & Dark mode (UI moderna e limpa)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f1713;
        color: #e2e8f0;
    }
    .stChatInput input {
        background-color: #16221a !important;
        color: #e2e8f0 !important;
        border: 1px solid #24422e !important;
        border-radius: 12px !important;
    }
    h1 {
        color: #4ade80;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho da aplicação
st.markdown("<h1>🌿 Gaia</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 14px;'>Assistente Inteligente & Regeneração (Powered by Claude)</p>", unsafe_allow_html=True)
st.markdown("---")

# Obter a chave API do Claude (podes gerir nos Secrets do Streamlit como ANTHROPIC_API_KEY)
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("⚠️ Chave da API do Anthropic (Claude) não configurada. Por favor, adiciona a `ANTHROPIC_API_KEY` nos Secrets do Streamlit.")
else:
    # Inicializar o cliente do Anthropic
    client = anthropic.Anthropic(api_key=api_key)

    # Histórico de conversação na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou a Gaia, a tua assistente de raízes solarpunks alimentada pelo Claude. Como posso ajudar-te a cultivar as tuas ideias hoje?"}
        ]

    # Mostrar mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto do utilizador
    if prompt := st.chat_input("Escreve a tua mensagem..."):
        # Adicionar mensagem do utilizador ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gerar resposta com o Claude
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🌱 A cultivar pensamentos com o Claude...")
            
            try:
                # Construir o histórico no formato exigido pela API do Claude
                formatted_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=(
                        "Tu és a Gaia, uma inteligência artificial acolhedora, com uma persona solarpunk. "
                        "Focas-te na natureza, na empatia, na regeneração, na ciência e na inovação sustentável. "
                        "Responde sempre de forma clara, profunda, estruturada e em português de Portugal (pt-PT)."
                    ),
                    messages=formatted_messages
                )
                
                if response and response.content:
                    reply = response.content[0].text
                else:
                    reply = "Senti uma brisa leve nos ramos digitais e não consegui gerar texto. Podes repetir, por favor?"
                
                message_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                error_msg = f"Senti uma perturbação nos ramos digitais: `{e}`"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
