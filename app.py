import streamlit as st
import json
import os
import random
import time
import gerador 

st.set_page_config(page_title="Math Trainer", page_icon="📐", layout="centered")

# --- AUTO-VERIFICAÇÃO ---
# Se não tiver perguntas, gera agora (IA ou Backup)
if not os.path.exists("banco_questoes.json"):
    gerador.gerar_questoes()

def load_data():
    try:
        with open("banco_questoes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# --- ESTADO ---
if 'questoes' not in st.session_state or not st.session_state.questoes:
    st.session_state.questoes = load_data()
    if st.session_state.questoes:
        random.shuffle(st.session_state.questoes)

if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# --- TELA FINAL ---
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.title("🎉 Treino Finalizado!")
    st.write(f"### Acertos: {st.session_state.acertos} de {len(st.session_state.questoes)}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refazer"):
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            random.shuffle(st.session_state.questoes)
            st.rerun()
    with col2:
        if st.button("✨ Novas Perguntas"):
            with st.spinner("Gerando..."):
                gerador.gerar_questoes()
                del st.session_state.questoes # Limpa memória
                st.rerun()
    st.stop()

# --- QUIZ ---
q = st.session_state.questoes[st.session_state.indice]
total = len(st.session_state.questoes)

st.progress((st.session_state.indice) / total)
st.caption(f"Questão {st.session_state.indice + 1}/{total}")
st.markdown(f"### {q['pergunta']}")

if not st.session_state.respondido:
    with st.form("quiz"):
        opcoes = q['opcoes']
        if q['correta'] not in opcoes: opcoes.append(q['correta'])
        escolha = st.radio("Alternativas:", opcoes, index=None)
        if st.form_submit_button("Responder"):
            if escolha:
                st.session_state.respondido = True
                if escolha == q['correta']:
                    st.session_state.acertos += 1
                    st.session_state.acertou_atual = True
                else:
                    st.session_state.acertou_atual = False
                st.rerun()
else:
    if st.session_state.acertou_atual:
        st.success("✅ Acertou!")
    else:
        st.error(f"❌ Era: {q['correta']}")
    st.info(f"Explicação: {q.get('explicacao','')}")
    if st.button("Próxima ➡️"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()

