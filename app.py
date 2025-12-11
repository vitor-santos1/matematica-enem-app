import streamlit as st
import gerador
import time

st.set_page_config(page_title="IA Tutor ENEM", page_icon="🎓", layout="centered")

# Estilo visual moderno
st.markdown("""
<style>
.stButton>button {width: 100%; height: 50px; font-weight: bold; border-radius: 10px; font-size: 18px;}
.resolucao {background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50; color: #1b5e20;}
.dica {background-color: #fff8e1; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; color: #663c00;}
</style>""", unsafe_allow_html=True)

st.title("🎓 IA Tutor: Matemática ENEM")
st.write("Simulado Inteligente de Alta Complexidade")

# --- INICIALIZAÇÃO ---
if 'questoes' not in st.session_state:
    # AQUI ESTAVA O ERRO: Mudei para o nome correto da função
    with st.spinner("Preparando o motor de inteligência..."):
        st.session_state.questoes = gerador.gerar_questoes_agora()
    
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# --- TELA DE RESULTADO FINAL ---
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.balloons()
    st.success(f"🏆 FIM DO TREINO! Você acertou {st.session_state.acertos} de {len(st.session_state.questoes)}.")
    
    if st.button("🔄 Gerar Novo Simulado Nível Hard"):
        with st.spinner("A IA está criando novas situações complexas..."):
            time.sleep(0.5) 
            # Chama a função certa novamente
            st.session_state.questoes = gerador.gerar_questoes_agora()
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            st.rerun()
    st.stop()

# --- EXIBIÇÃO DA QUESTÃO ---
q = st.session_state.questoes[st.session_state.indice]
total = len(st.session_state.questoes)

# Barra de progresso
st.progress((st.session_state.indice + 1) / total)
st.caption(f"Questão {st.session_state.indice + 1} de {total} | Tema: {q['tema']}")

st.markdown(f"### {q['pergunta']}")

# Botão de Dica
with st.expander("💡 Precisa de uma ajuda?"):
    # Garante que não quebre se a dica vier vazia
    dica = q.get('dica_mestra') or "Leia atentamente o enunciado e identifique as variáveis."
    st.markdown(f"<div class='dica'><b>Dica do Tutor:</b> {dica}</div>", unsafe_allow_html=True)

# Área de Resposta
if not st.session_state.respondido:
    with st.form("quiz_form"):
        escolha = st.radio("Sua resposta:", q['opcoes'], index=None)
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

# Pós-Resposta (Feedback)
else:
    if st.session_state.acertou_atual:
        st.success("✅ RESPOSTA CORRETA!")
    else:
        st.error(f"❌ INCORRETO. A resposta certa era: {q['correta']}")
    
    st.markdown("### 📝 Explicação Passo a Passo:")
    st.markdown(f"<div class='resolucao'>{q['explicacao']}</div>", unsafe_allow_html=True)
    
    if st.button("➡️ Próxima Questão"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()
