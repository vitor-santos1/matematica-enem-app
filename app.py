import streamlit as st
import json
import os
import random
import time
# AQUI ESTÁ A MÁGICA: Importamos seu script de geração
import gerador 

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Math Trainer", page_icon="📐", layout="centered")

st.markdown("""
    <style>
    .stButton>button {width: 100%; border-radius: 10px; height: 3em; font-weight: bold;}
    .big-success {background-color: #d4edda; color: #155724; padding: 20px; border-radius: 10px; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def load_data():
    if os.path.exists("banco_questoes.json"):
        with open("banco_questoes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- ESTADO (MEMÓRIA DO SITE) ---
if 'questoes' not in st.session_state:
    raw_data = load_data()
    if raw_data:
        random.shuffle(raw_data)
        st.session_state.questoes = raw_data
    else:
        st.session_state.questoes = []

if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False 
    st.session_state.acertou_atual = False

# --- TELA DE "ACABOU" ---
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.title("🎉 Treino Finalizado!")
    
    # Placar
    total = len(st.session_state.questoes)
    if total > 0:
        score = st.session_state.acertos
        st.markdown(f"<div class='big-success'><h3>Você acertou {score} de {total} questões!</h3></div>", unsafe_allow_html=True)
    else:
        st.warning("O banco de dados está vazio.")

    st.divider()
    st.subheader("O que você quer fazer agora?")

    col1, col2 = st.columns(2)
    
    with col1:
        # Botão 1: Apenas refazer as mesmas misturadas
        if st.button("🔄 Refazer Estas Questões"):
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            random.shuffle(st.session_state.questoes)
            st.rerun()

    with col2:
        # Botão 2: MÁGICA DA IA - Gera novas perguntas
        if st.button("✨ Gerar NOVAS com IA"):
            try:
                # Mostra um aviso enquanto a IA pensa
                with st.spinner("A IA está criando perguntas inéditas... (Isso leva uns 40 segundos)"):
                    # Chama a função do seu arquivo gerador.py
                    gerador.gerar_questoes()
                    
                    # Recarrega tudo
                    st.session_state.questoes = load_data()
                    st.session_state.indice = 0
                    st.session_state.acertos = 0
                    st.session_state.respondido = False
                    
                st.success("Novas questões prontas!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
                st.info("Verifique se a Chave API no gerador.py está correta.")

    st.stop()

# --- LÓGICA DO QUIZ (IGUAL ANTES) ---
q_atual = st.session_state.questoes[st.session_state.indice]
total_questoes = len(st.session_state.questoes)

# Barra de progresso
progresso = (st.session_state.indice) / total_questoes
st.progress(progresso)
st.caption(f"Questão {st.session_state.indice + 1} de {total_questoes}")

st.divider()

# Mostra Pergunta
st.subheader(f"{q_atual['tema']}")
st.markdown(f"### {q_atual['pergunta']}")

# Área de Resposta
if not st.session_state.respondido:
    with st.form("quiz_form"):
        # Segurança anti-bug
        if q_atual['correta'] not in q_atual['opcoes']:
            q_atual['opcoes'].append(q_atual['correta'])
            
        escolha = st.radio("Escolha:", q_atual['opcoes'], index=None)
        if st.form_submit_button("Confirmar"):
            if escolha:
                st.session_state.respondido = True
                if escolha == q_atual['correta']:
                    st.session_state.acertos += 1
                    st.session_state.acertou_atual = True
                else:
                    st.session_state.acertou_atual = False
                st.rerun()
            else:
                st.warning("Escolha uma opção!")
else:
    if st.session_state.acertou_atual:
        st.success("✅ ACERTOU!")
    else:
        st.error(f"❌ A resposta certa era: {q_atual['correta']}")
    
    st.info(f"**Explicação:** {q_atual.get('explicacao', '')}")
    
    if st.button("Próxima Questão ➡️"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()