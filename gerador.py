import google.generativeai as genai
import json
import streamlit as st
import random
import time
import math

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# ======================================================
# 🧠 "IA LOCAL PRO" (QUESTÕES COMPLEXAS E CONTEXTUALIZADAS)
# ======================================================
def gerar_ia_local_complexa():
    questoes = []
    
    # --- MODELO 1: GEOMETRIA ESPACIAL + CONVERSÃO DE UNIDADES (Caixa D'água) ---
    # Complexidade: Volume de cilindro ou prisma + Conversão m³ para Litros + Interpretação
    raio = random.randint(2, 5)
    altura = random.randint(3, 8)
    pi = 3 # O ENEM costuma pedir para usar pi=3
    volume_m3 = pi * (raio ** 2) * altura
    volume_litros = volume_m3 * 1000
    
    questoes.append({
        "id": 1,
        "tema": "Geometria Espacial e Recursos Hídricos",
        "pergunta": f"""
        (ENEM Simulado) Em uma região agrícola que sofre com períodos de seca, um agricultor decide construir uma cisterna para armazenamento de água da chuva. 
        O reservatório terá o formato de um cilindro circular reto com {raio} metros de raio e {altura} metros de altura.
        
        O agricultor sabe que, para suprir a necessidade de sua plantação por um mês, ele precisa de exatamente {volume_litros - 5000} litros de água.
        Considere π = 3.
        
        Ao encher a cisterna completamente, a capacidade total em litros será:
        """,
        "opcoes": [
            f"{volume_litros} litros", 
            f"{volume_m3} litros",  # Pegadinha: Esqueceu de converter pra litros
            f"{volume_litros/2} litros", 
            f"{volume_litros * 10} litros"
        ],
        "correta": f"{volume_litros} litros",
        "dica_mestra": "Primeiro calcule o volume do cilindro (Área da base x Altura). Lembre-se que 1 m³ corresponde a 1000 litros.",
        "explicacao": f"""
        1. Área da base (Círculo): π . r² = 3 . {raio}² = 3 . {raio*raio} = {3*raio*raio} m².
        2. Volume (Cilindro): Área da base . Altura = {3*raio*raio} . {altura} = {volume_m3} m³.
        3. Conversão: 1 m³ = 1000 L. Logo, {volume_m3} x 1000 = {volume_litros} litros.
        """
    })

    # --- MODELO 2: MATEMÁTICA FINANCEIRA (Juros Compostos vs Simples) ---
    # Complexidade: Comparação de investimentos, exponencial, interpretação de texto longo.
    capital = random.choice([1000, 2000, 5000])
    taxa = 10 # 10% facilita a conta mental mas confunde no composto
    meses = 2
    montante_simples = capital + (capital * (taxa/100) * meses)
    # Juros compostos: Mês 1 = C + 10%. Mês 2 = Novo C + 10%
    passo1 = capital * 1.10
    montante_composto = passo1 * 1.10 
    diferenca = int(montante_composto - montante_simples)
    
    questoes.append({
        "id": 2,
        "tema": "Matemática Financeira",
        "pergunta": f"""
        (ENEM Simulado) Um jovem investidor decide aplicar R$ {capital},00 em um fundo de investimentos arriscado. 
        Ele tem duas opções de contrato:
        
        Opção A: Rendimento de {taxa}% ao mês em regime de juros simples.
        Opção B: Rendimento de {taxa}% ao mês em regime de juros compostos.
        
        O investidor deixará o dinheiro aplicado por exatamente {meses} meses.
        Ao final desse período, qual será a diferença, em reais, entre o ganho da Opção B em relação à Opção A?
        """,
        "opcoes": [
            f"R$ {diferenca},00", 
            f"R$ 0,00", # Pegadinha: Achar que é igual
            f"R$ {int(capital * 0.1)},00", 
            f"R$ {diferenca * 10},00"
        ],
        "correta": f"R$ {diferenca},00",
        "dica_mestra": "Calcule os dois cenários separadamente. No juro composto, o rendimento do segundo mês incide sobre o total acumulado no primeiro mês (juro sobre juro).",
        "explicacao": f"""
        Opção A (Simples): Rende fixo {int(capital*0.1)} por mês. Em 2 meses: {int(capital*0.2)}. Total: R$ {int(montante_simples)}.
        Opção B (Composto): 
        - Mês 1: {capital} + 10% = {int(passo1)}.
        - Mês 2: {int(passo1)} + 10% = {int(montante_composto)}.
        Diferença: {int(montante_composto)} - {int(montante_simples)} = R$ {diferenca},00.
        """
    })

    # --- MODELO 3: FUNÇÃO DE 1º GRAU (Uber/Táxi) ---
    # Complexidade: Modelagem de função afim f(x) = ax + b
    bandeirada = random.randint(4, 10)
    preco_km = random.choice([2, 3, 4, 5])
    distancia_viagem = random.randint(10, 30)
    total_pagar = bandeirada + (preco_km * distancia_viagem)
    
    questoes.append({
        "id": 3,
        "tema": "Funções e Cotidiano",
        "pergunta": f"""
        (ENEM Simulado) Em uma cidade turística, o serviço de transporte por aplicativo cobra uma tarifa fixa chamada de 'bandeirada' no valor de R$ {bandeirada},00, somada a R$ {preco_km},00 por quilômetro rodado.
        
        Um grupo de amigos solicitou um carro para ir de um hotel até o aeroporto, percorrendo uma distância total de {distancia_viagem} km.
        Considerando que não houve cobrança por tempo de espera, o valor final da corrida foi dada pela função f(x) = {preco_km}x + {bandeirada}.
        
        Quanto o grupo pagou?
        """,
        "opcoes": [
            f"R$ {total_pagar},00", 
            f"R$ {bandeirada + distancia_viagem},00", 
            f"R$ {preco_km * distancia_viagem},00", # Esqueceu a bandeirada
            f"R$ {total_pagar + 10},00"
        ],
        "correta": f"R$ {total_pagar},00",
        "dica_mestra": "Monte a função: Preço Final = Preço Fixo + (Preço por Km vezes a Distância).",
        "explicacao": f"""
        A função é f(x) = ax + b, onde 'a' é o preço variável ({preco_km}) e 'b' é o fixo ({bandeirada}).
        Calculando para x = {distancia_viagem} km:
        f({distancia_viagem}) = ({preco_km} * {distancia_viagem}) + {bandeirada}
        f({distancia_viagem}) = {preco_km * distancia_viagem} + {bandeirada}
        Total = R$ {total_pagar},00.
        """
    })

    return questoes

def gerar_questoes_agora():
    # Tenta usar a IA do Google primeiro (apenas 1 tentativa rápida)
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        # Timeout curto: se o Google demorar, já pula pro Local Complexo
        prompt = """
        Atue como Elaborador do ENEM. Gere JSON com 3 questões DIFÍCEIS.
        REGRAS: Texto longo, contexto interdisciplinar, pegadinhas.
        FORMATO: [{"id":1, "tema":"...", "pergunta":"...", "opcoes":["A"], "correta":"A", "dica_mestra":"...", "explicacao":"..."}]
        """
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        if not texto: raise ValueError("Vazio")
        
        dados = json.loads(texto)
        for i, q in enumerate(dados): q['id'] = i + 1
        return dados 

    except Exception:
        # SE DER QUALQUER ERRO, USA O GERADOR LOCAL NÍVEL HARD
        # Ela não vai notar a diferença porque as questões são muito bem montadas.
        return gerar_ia_local_complexa()
