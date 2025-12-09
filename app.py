import streamlit as st
import random
import gerador # Importa o arquivo novo

st.set_page_config(page_title="Math Trainer", page_icon="📐", layout="centered")

# --- CSS PARA BOTÕES GRANDES ---
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
}
</style>""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'questoes' not in st.session_state:
    # Começa gerando perguntas direto
    st.session_state.questoes = gerador.gerar_questoes_agora()

if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# --- TELA FINAL ---
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.success(f"🎉 FIM! Você acertou {st.session_state.acertos} de {len(st.session_state.questoes)}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refazer Mesmas"):
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            st.rerun()
            
    with col2:
        # AQUI É O PULO DO GATO
        if st.button("✨ Gerar Novas (IA)"):
            with st.spinner("A IA está criando perguntas fresquinhas..."):
                # Chama a função e joga direto na variável, sem passar por arquivo
                novas = gerador.gerar_questoes_agora()
                st.session_state.questoes = novas
                
                # Reseta contadores
                st.session_state.indice = 0
                st.session_state.acertos = 0
                st.session_state.respondido = False
                st.rerun()
    st.stop()

# --- QUIZ ---
q = st.session_state.questoes[st.session_state.indice]

# Barra de progresso
st.progress((st.session_state.indice) / len(st.session_state.questoes))
st.caption(f"Questão {st.session_state.indice + 1}")

st.markdown(f"### {q['tema']}")
st.write(f"## {q['pergunta']}")

if not st.session_state.respondido:
    with st.form("form_quiz"):
        # Mistura opções para não viciar
        opcoes = q['opcoes'].copy()
        if q['correta'] not in opcoes: opcoes.append(q['correta'])
        
        escolha = st.radio("Sua resposta:", opcoes, index=None)
        
        # Botão de Enviar dentro do form
        if st.form_submit_button("Confirmar Resposta"):
            if escolha:
                st.session_state.respondido = True
                if escolha == q['correta']:
                    st.session_state.acertos += 1
                    st.session_state.acertou_atual = True
                else:
                    st.session_state.acertou_atual = False
                st.rerun()
            else:
                st.warning("Selecione uma alternativa!")
else:
    # Feedback
    if st.session_state.acertou_atual:
        st.success("✅ ACERTOU!")
    else:
        st.error(f"❌ Errado! A correta era: {q['correta']}")
    
    st.info(f"💡 {q.get('explicacao', 'Sem explicação.')}")
    
    if st.button("Próxima Questão ➡️"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()
