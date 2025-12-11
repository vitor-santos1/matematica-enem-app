import streamlit as st
import gerador

st.set_page_config(page_title="Math Tutor ENEM", page_icon="🎓", layout="centered")

# CSS para ficar bonito
st.markdown("""
<style>
div.stButton > button {width: 100%; border-radius: 10px; font-weight: bold;}
.explicacao-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50;}
.dica-box {background-color: #fff3cd; padding: 10px; border-radius: 10px; border-left: 5px solid #ffc107; color: #856404;}
</style>""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'questoes' not in st.session_state:
    st.session_state.questoes = gerador.gerar_questoes_agora()
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# --- TELA FINAL ---
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.title("🎓 Treino Concluído!")
    st.write(f"Você acertou **{st.session_state.acertos}** de **{len(st.session_state.questoes)}**.")
    if st.button("✨ Gerar Novo Simulado (IA)"):
        with st.spinner("O Professor Virtual está elaborando novas questões..."):
            st.session_state.questoes = gerador.gerar_questoes_agora()
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            st.rerun()
    st.stop()

# --- A QUESTÃO ---
q = st.session_state.questoes[st.session_state.indice]

st.caption(f"Questão {st.session_state.indice + 1} de {len(st.session_state.questoes)} | Tema: {q['tema']}")
st.progress((st.session_state.indice) / len(st.session_state.questoes))

st.markdown(f"### {q['pergunta']}")

# --- ÁREA DE RESPOSTA ---
if not st.session_state.respondido:
    # 💡 BOTÃO DE DICA (NOVIDADE!)
    with st.expander("💡 Precisa de uma ajuda? (Dica do Professor)"):
        st.markdown(f"<div class='dica-box'>{q.get('dica_mestra', 'Leia o enunciado com atenção.')}</div>", unsafe_allow_html=True)

    with st.form("quiz"):
        opcoes = q['opcoes'].copy()
        if q['correta'] not in opcoes: opcoes.append(q['correta'])
        escolha = st.radio("Sua resposta:", opcoes, index=None)
        
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
                st.warning("Escolha uma alternativa!")

# --- PÓS-RESPOSTA (EXPLICAÇÃO) ---
else:
    if st.session_state.acertou_atual:
        st.success("✅ ACERTOU! Parabéns!")
    else:
        st.error(f"❌ Que pena! A correta era: {q['correta']}")
    
    # 📝 EXPLICAÇÃO DETALHADA (NOVIDADE!)
    st.markdown("### 📝 Resolução Passo a Passo:")
    st.markdown(f"<div class='explicacao-box'>{q.get('explicacao', 'Sem explicação disponível.')}</div>", unsafe_allow_html=True)
    
    if st.button("Próxima Questão ➡️"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()
