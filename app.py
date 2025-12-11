import streamlit as st
import gerador

st.set_page_config(page_title="Math Tutor", page_icon="📝")

# CSS para garantir que a resolução apareça bonita
st.markdown("""
<style>
.resolucao-box {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #c3e6cb;
    margin-top: 10px;
}
div.stButton > button {width: 100%; height: 50px; font-weight: bold;}
</style>""", unsafe_allow_html=True)

# Inicializa
if 'questoes' not in st.session_state:
    st.session_state.questoes = gerador.gerar_questoes_agora()
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.acertos = 0
    st.session_state.respondido = False
    st.session_state.acertou_atual = False

# Tela de Final
if not st.session_state.questoes or st.session_state.indice >= len(st.session_state.questoes):
    st.title("🎉 Treino Finalizado!")
    st.metric("Total de Acertos", f"{st.session_state.acertos} / {len(st.session_state.questoes)}")
    
    if st.button("🔄 Gerar Novo Simulado"):
        with st.spinner("Criando novas questões..."):
            st.session_state.questoes = gerador.gerar_questoes_agora()
            st.session_state.indice = 0
            st.session_state.acertos = 0
            st.session_state.respondido = False
            st.rerun()
    st.stop()

# Mostra Questão
q = st.session_state.questoes[st.session_state.indice]
st.progress((st.session_state.indice + 1) / len(st.session_state.questoes))
st.write(f"**Tema:** {q['tema']}")
st.markdown(f"### {q['pergunta']}")

# Formulário de Resposta
if not st.session_state.respondido:
    with st.form("quiz"):
        escolha = st.radio("Escolha a alternativa:", q['opcoes'], index=None)
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
                st.warning("Marque uma opção!")
else:
    # --- ÁREA DE RESOLUÇÃO (AGORA IMPOSSÍVEL FICAR EM BRANCO) ---
    if st.session_state.acertou_atual:
        st.success("✅ ACERTOU!")
    else:
        st.error(f"❌ A correta era: {q['correta']}")
    
    # Busca a explicação. Se não tiver, mostra mensagem padrão.
    texto_explicacao = q.get('explicacao', 'Resolução detalhada: Aplique a fórmula do tema abordado.')
    
    st.markdown("### 📝 Resolução:")
    st.markdown(f"<div class='resolucao-box'>{texto_explicacao}</div>", unsafe_allow_html=True)
    
    if st.button("Próxima Questão ➡️"):
        st.session_state.indice += 1
        st.session_state.respondido = False
        st.rerun()
