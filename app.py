import streamlit as st
import gerador
import time

st.set_page_config(page_title="IA ENEM Tutor", page_icon="🧠", layout="centered")

# CSS para visual profissional
st.markdown("""
<style>
.stButton>button {width: 100%; height: 50px; font-weight: bold; border-radius: 10px;}
.resolucao {background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 1px solid #4caf50; color: #1b5e20;}
.dica {background-color: #fff3e0; padding: 10px; border-radius: 10px; border: 1px solid #ff9800; color: #e65100; font-size: 0.9em;}
</style>""", unsafe_allow_html=True)

st.title("🧠 IA Tutor: Matemática ENEM")

# --- INICIALIZAÇÃO DO ESTOQUE ---
if 'estoque_questoes' not in st.session_state:
    st.session_state.estoque_questoes = [] # Começa vazio

if 'questao_atual' not in st.session_state:
    st.session_state.questao_atual = None

if 'respondido' not in st.session_state:
    st.session_state.respondido = False

# --- FUNÇÃO PARA PEGAR A PRÓXIMA DO ESTOQUE ---
def proxima_questao():
    if len(st.session_state.estoque_questoes) > 0:
        # Pega a primeira da fila e remove do estoque
        st.session_state.questao_atual = st.session_state.estoque_questoes.pop(0)
        st.session_state.respondido = False
        st.rerun()
    else:
        st.session_state.questao_atual = None
        st.rerun()

# --- LÓGICA PRINCIPAL ---

# Cenario 1: Sem questão atual e sem estoque (Precisa carregar)
if st.session_state.questao_atual is None and not st.session_state.estoque_questoes:
    st.info("👋 Olá! O Tutor Virtual está pronto.")
    st.write("Clique abaixo para gerar um novo simulado com 5 questões.")
    
    if st.button("✨ Gerar Simulado (IA)"):
        with st.spinner("Conectando ao cérebro da IA... Criando 5 questões inéditas..."):
            novas = gerador.buscar_lote_questoes()
            
            if novas:
                st.session_state.estoque_questoes = novas
                proxima_questao() # Já puxa a primeira
            else:
                st.error("⚠️ A IA está muito ocupada agora (Erro de Tráfego). Espere 10 segundos e tente de novo.")

# Cenario 2: Tem questão na tela
elif st.session_state.questao_atual:
    q = st.session_state.questao_atual
    
    # Barra de progresso visual (Quantas faltam no estoque)
    restantes = len(st.session_state.estoque_questoes)
    st.caption(f"Questão Atual (Restam {restantes} na memória)")
    
    st.subheader(f"Tema: {q.get('tema', 'Geral')}")
    st.write(q['pergunta'])
    
    # Botão de Dica
    with st.expander("💡 Precisa de uma dica?"):
        st.markdown(f"<div class='dica'>{q.get('dica_mestra', 'Leia atentamente.')}</div>", unsafe_allow_html=True)

    # Formulário
    if not st.session_state.respondido:
        with st.form("quiz"):
            escolha = st.radio("Alternativa:", q['opcoes'], index=None)
            if st.form_submit_button("Confirmar Resposta"):
                if escolha:
                    st.session_state.respondido = True
                    if escolha == q['correta']:
                        st.success("✅ ACERTOU!")
                    else:
                        st.error(f"❌ Errou! A correta era: {q['correta']}")
                    st.rerun()
                else:
                    st.warning("Escolha uma opção!")
    
    # Pós-resposta (Explicação e Próxima)
    else:
        if q['correta'] in q['opcoes']: # Recalcula feedback visual se re-renderizar
            pass 
            
        st.markdown("### 📝 Explicação do Tutor:")
        st.markdown(f"<div class='resolucao'>{q.get('explicacao', 'Sem explicação.')}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➡️ Próxima Questão"):
                proxima_questao()
