import streamlit as st
import json
import os
import gerador

st.set_page_config(page_title="Diagnóstico", page_icon="🔧")

st.title("🔧 Modo de Diagnóstico")

# 1. TESTE DA CHAVE
st.write("### 1. Verificando Senha (Secrets)")
try:
    chave = st.secrets["GOOGLE_API_KEY"]
    if chave:
        st.success(f"✅ Chave encontrada! Começa com: {chave[:5]}...")
    else:
        st.error("❌ A chave existe mas está vazia.")
except Exception as e:
    st.error(f"❌ O site não achou a chave nos Secrets. Erro: {e}")
    st.info("Vá nas configurações do App no Streamlit > Settings > Secrets e verifique.")

# 2. TESTE DO GERADOR
st.write("### 2. Testando Gerador de Perguntas")
if st.button("Tentar Gerar Agora"):
    try:
        with st.spinner("Tentando falar com a IA..."):
            gerador.gerar_questoes()
        st.success("✅ Sucesso! O gerador funcionou.")
        
        # Mostra o que foi gerado
        if os.path.exists("banco_questoes.json"):
            with open("banco_questoes.json", "r") as f:
                dados = json.load(f)
            st.json(dados)
        else:
            st.warning("O gerador rodou mas não criou o arquivo.")
            
    except Exception as e:
        st.error(f"❌ ERRO CRÍTICO NA IA: {e}")
        st.write("Mande print desse erro vermelho acima para o suporte.")
