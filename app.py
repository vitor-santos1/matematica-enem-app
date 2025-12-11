import streamlit as st
import gerador # Seu motor de IA própria
import time

st.set_page_config(page_title="Vitor-AI Tutor", page_icon="🚀", layout="centered")

# CSS para ficar bonito (Estilo App Profissional)
st.markdown("""
<style>
.stButton>button {width: 100%; height: 50px; font-weight: bold; border-radius: 10px; font-size: 18px;}
.resolucao {background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50; color: #1b5e20;}
.dica {background-color: #fff8e1; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; color: #663c00;}
</style>""", unsafe_allow_html=True)

st.title("🚀 IA Própria: Treino ENEM")
st.write("Gerador Procedural de Alta Complexidade (Offline)")

# --- LÓGICA DE ESTADO ---
# Garante que as questões não sumam quando clica
if 'questoes' not in st.session_state:
    st.session_state.questoes = gerador.gerar_questoes_agora()
    
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# --- TELA DE FIM DE JOGO ---
if st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.success(f"🏆 FIM! Você acertou {st.session_state.acertos} de {len(st.session_state.questoes)}.")
    
    if st.button("🔄 Gerar Novas (Infinitas)"):
        with st.spinner("A IA está criando novas histórias..."):
            time.sleep(0.5) # Charme visual
            st.session_state.questoes = gerador.gerar_questoes_agora()
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            st.rerun()
    st.stop()

# --- MOSTRAR QUESTÃO ATUAL ---
q = st.session_state.questoes[st.session_state.indice]
total = len(st.session_state.questoes)

st.progress((st.session_state.indice + 1) / total)
st.caption(f"Questão {st.session_state.indice + 1} de {total} | Tema: {q['tema']}")

st.markdown(f"### {q['pergunta']}")

# Botão de Dica
with st.expander("💡 Precisa de uma dica?"):
    st.markdown(f"<div class='dica'><b>Dica da IA:</b> {q['dica_mestra']}</div>", unsafe_allow_html=True)

# Área de Resposta
if not st.session_state.respondido:
    with st.form("quiz_form"):
        escolha = st.radio("Sua resposta:", q['opcoes'], index=None)
        if st.form_submit_button("Confirmar"):
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

# Área de Explicação (Só aparece depois de responder)
else:
    if st.session_state.acertou_atual:
        st.success("✅ CORRETO!")
    else:
        st.error(f"❌ ERRADO. A correta era: {q['correta']}")
    
    st.markdown("### 📝 Explicação Passo a Passo:")
    st.markdown(f"<div class='resolucao'>{q['explicacao']}</div>", unsafe_allow_html=True)
    
    if st.button("➡️ Próxima"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()
