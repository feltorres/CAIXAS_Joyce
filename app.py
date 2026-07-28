import streamlit as st

st.set_page_config(page_title="Orçamento - Caixas de Papelão", layout="wide")
st.title("Sistema de Orçamento - Caixas e Chapas de Papelão")

st.sidebar.header("Parâmetros Base")
preco_kg = st.sidebar.number_input("Preço do KG do Papelão (R$)", min_value=0.0, value=0.0, step=0.1)
gramatura = st.sidebar.number_input("Gramatura (g/m²)", min_value=0, value=378, step=1)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

st.sidebar.markdown("**Preços para Negociação (Opcional)**")
preco_300 = st.sidebar.number_input("Preço do KG para 300kg (R$)", min_value=0.0, value=12.35, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_1000 = st.sidebar.number_input("Preço do KG para 1000kg (R$)", min_value=0.0, value=11.50, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_recibo = st.sidebar.number_input("Preço do KG mediante recibo (R$)", min_value=0.0, value=11.20, step=0.1, help="Deixe 0.0 para usar o preço padrão.")

tipo_produto = st.radio("O que deseja orçar?", ["Caixa Maleta (Modelos Específicos)", "Chapa / Corte e Vinco"])

st.markdown("---")

area_m2 = 0.0
qtd = 1

if tipo_produto == "Caixa Maleta (Modelos Específicos)":
    modelo = st.selectbox("Selecione o Modelo da Caixa", [
        "Abas Normais", 
        "Aba Dupla / Total", 
        "Aba Dupla Inferior ou Superior", 
        "Sem Aba Superior", 
        "Transpassadas"
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        c = st.number_input("Comprimento (mm)", min_value=0, value=240, step=1)
    with col2:
        l = st.number_input("Largura (mm)", min_value=0, value=180, step=1)
    with col3:
        a = st.number_input("Altura (mm)", min_value=0, value=175, step=1)
    with col4:
        qtd = st.number_input("Quantidade", min_value=1, value=2500, step=1)
        
    if modelo == "Transpassadas":
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            transp_sup = st.number_input("Abas Transpassadas - Superior (mm)", min_value=0, value=40, step=1)
        with t_col2:
            transp_inf = st.number_input("Abas Transpassadas - Inferior (mm)", min_value=0, value=40, step=1)
    
    if modelo == "Abas Normais":
        area_m2 = ((c + l) * 2 * (l + a) * 1.1) / 1000000
    elif modelo == "Aba Dupla / Total":
        area_m2 = (((c + l) * 2) * (l + l + a) * 1.1) / 1000000
    elif modelo == "Aba Dupla Inferior ou Superior":
        area_m2 = (((c + l) * 2) * (l + (l / 2) + a) * 1.1) / 1000000
    elif modelo == "Sem Aba Superior":
        area_m2 = ((c + l) * 2 * ((l / 2) + a) * 1.1) / 1000000
    elif modelo == "Transpassadas":
        area_m2 = ((c + l) * 2 * (l + a + transp_sup + transp_inf) * 1.1) / 1000000

else:
    modelo_chapa = st.selectbox("Selecione o Tipo", ["Cinta-Tab-Chapa", "Corte e Vinco"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.number_input("Comprimento (mm)", min_value=0, value=390, step=1)
    with col2:
        l = st.number_input("Largura (mm)", min_value=0, value=260, step=1)
    with col3:
        qtd = st.number_input("Quantidade", min_value=1, value=8000, step=1)
        
    if modelo_chapa == "Cinta-Tab-Chapa":
        area_m2 = (c * l) / 1000000
    elif modelo_chapa == "Corte e Vinco":
        area_m2 = ((c + 30) * (l + 30)) / 1000000

# Funções auxiliares para formatação BR
def formata_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_peso(peso):
    return f"{peso:.1f}".replace(".", ",") + " Kg"

def formata_qtd(quantidade):
    return f"{quantidade:,}".replace(",", ".")

if st.button("Calcular"):
    if area_m2 > 0 and preco_kg > 0 and gramatura > 0:
        peso_unit_kg = (area_m2 * gramatura) / 1000
        peso_total_kg = peso_unit_kg * qtd
        
        preco_unit = peso_unit_kg * preco_kg
        preco_total = preco_unit * qtd
        
        # Definição dos preços efetivos
        preco_efetivo_300 = preco_300 if preco_300 > 0 else preco_kg
        preco_efetivo_1000 = preco_1000 if preco_1000 > 0 else preco_kg
        preco_efetivo_recibo = preco_recibo if preco_recibo > 0 else preco_kg
        
        # Cálculos para 300kg
        qtd_300 = int(300 / peso_unit_kg)
        preco_unit_300 = peso_unit_kg * preco_efetivo_300
        valor_300 = qtd_300 * preco_unit_300
        
        # Cálculos para 1000kg
        qtd_1000 = int(1000 / peso_unit_kg)
        preco_unit_1000 = peso_unit_kg * preco_efetivo_1000
        valor_1000 = qtd_1000 * preco_unit_1000
        
        # Cálculos para recibo (baseado em 300kg)
        preco_unit_recibo = peso_unit_kg * preco_efetivo_recibo
        valor_recibo = qtd_300 * preco_unit_recibo
        
        st.markdown("""
        <style>
        .card-verde {
            background-color: #EAFAF1;
            border-left: 6px solid #239B56;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
        }
        .card-azul {
            background-color: #EBF5FB;
            border-left: 6px solid #2874A6;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
        }
        .card-laranja {
            background-color: #FEF5E7;
            border-left: 6px solid #D68910;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .titulo-card {
            font-size: 1.1em;
            font-weight: bold;
            color: #333;
        }
        .valor-card {
            font-size: 1.5em;
            color: #000;
        }
        .peso-unitario-pequeno {
            font-size: 0.85em;
            color: #555;
            margin-top: 5px;
        }
        .ref-linha {
            font-size: 1.2em;
            margin-bottom: 8px;
            color: #333;
        }
        .linha-separadora {
            margin: 15px 0;
            border-top: 2px solid #000;
        }
        .texto-recibo {
            color: #FF0000;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("### Resultados")
        
        # Quadro 1: Valores (Verde)
        st.markdown(f"""
        <div class="card-verde">
            <span class="titulo-card">Valor unitário:</span> 
            <span class="valor-card">{formata_moeda(preco_unit)}</span>
            <span style="font-size: 1.5em; margin: 0 15px; color: #239B56;">&mdash;</span>
            <span class="titulo-card">Total ({formata_qtd(qtd)}und):</span> 
            <span class="valor-card">{formata_moeda(preco_total)}</span>
        </div>
        """, unsafe_allow_html=True)
            
        # Quadro 2: Pesos (Azul)
        st.markdown(f"""
        <div class="card-azul">
            <div>
                <span class="titulo-card">Peso Total:</span> 
                <span class="valor-card">{formata_peso(peso_total_kg)}</span>
            </div>
            <div class="peso-unitario-pequeno">Peso unitário: {formata_peso(peso_unit_kg)}</div>
        </div>
        """, unsafe_allow_html=True)
            
        # Quadro 3: Negociação (Laranja)
        st.markdown(f"""
        <div class="card-laranja">
            <div class="titulo-card" style="margin-bottom: 15px; font-size: 1.2em;">Referências para Negociação</div>
            <div class="ref-linha">
                <strong>Quantidade para 300kg:</strong> {formata_qtd(qtd_300)} un &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Preço unitário:</strong> {formata_moeda(preco_unit_300)} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Total:</strong> {formata_moeda(valor_300)}
            </div>
            <div class="ref-linha" style="margin-bottom: 0;">
                <strong>Quantidade para 1000kg:</strong> {formata_qtd(qtd_1000)} un &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Preço unitário:</strong> {formata_moeda(preco_unit_1000)} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Total:</strong> {formata_moeda(valor_1000)}
            </div>
            <div class="linha-separadora"></div>
            <div class="ref-linha texto-recibo" style="margin-bottom: 0;">
                Preço Mediante Recibo ({formata_qtd(qtd_300)} un) &nbsp;&nbsp;|&nbsp;&nbsp; Preço unitário: {formata_moeda(preco_unit_recibo)} &nbsp;&nbsp;|&nbsp;&nbsp; Total: {formata_moeda(valor_recibo)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Insira as dimensões, o peso e certifique-se de que o Preço do KG base seja maior que zero.")
