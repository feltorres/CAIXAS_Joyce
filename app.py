import streamlit as st

st.set_page_config(page_title="Orçamento - Caixas de Papelão", layout="wide")
st.title("Sistema de Orçamento - Caixas e Chapas de Papelão")

st.sidebar.header("Parâmetros Base")
preco_kg = st.sidebar.number_input("Preço do KG do Papelão (R$)", min_value=0.0, value=10.60, step=0.1)
gramatura = st.sidebar.number_input("Gramatura (g/m²)", min_value=0, value=378, step=1)

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
        
        qtd_300 = int(300 / peso_unit_kg)
        valor_300 = qtd_300 * preco_unit
        
        qtd_1000 = int(1000 / peso_unit_kg)
        valor_1000 = qtd_1000 * preco_unit
        
        # Injeção de CSS para os cards coloridos
        st.markdown("""
        <style>
        .card-azul {
            background-color: #EBF5FB;
            border-left: 6px solid #2874A6;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .card-verde {
            background-color: #EAFAF1;
            border-left: 6px solid #239B56;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
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
            margin-bottom: 5px;
        }
        .valor-card {
            font-size: 1.6em;
            color: #000;
            margin-bottom: 15px;
        }
        .ref-linha {
            font-size: 1.2em;
            margin-bottom: 8px;
            color: #333;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("### Resultados")
        
        col_azul, col_verde = st.columns(2)
        
        with col_azul:
            st.markdown(f"""
            <div class="card-azul">
                <div class="titulo-card">Peso unitário:</div>
                <div class="valor-card">{formata_peso(peso_unit_kg)}</div>
                <div class="titulo-card">Valor unitário:</div>
                <div class="valor-card" style="margin-bottom: 0;">{formata_moeda(preco_unit)}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_verde:
            st.markdown(f"""
            <div class="card-verde">
                <div class="titulo-card">Peso total:</div>
                <div class="valor-card">{formata_peso(peso_total_kg)}</div>
                <div class="titulo-card">Valor total:</div>
                <div class="valor-card" style="margin-bottom: 0;">{formata_moeda(preco_total)}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
        <div class="card-laranja">
            <div class="titulo-card" style="margin-bottom: 15px; font-size: 1.2em;">Referências para Negociação</div>
            <div class="ref-linha">
                <strong>Quantidade para 300kg:</strong> {formata_qtd(qtd_300)} unidades &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Total:</strong> {formata_moeda(valor_300)}
            </div>
            <div class="ref-linha" style="margin-bottom: 0;">
                <strong>Quantidade para 1000kg:</strong> {formata_qtd(qtd_1000)} unidades &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Total:</strong> {formata_moeda(valor_1000)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Insira dimensões, gramatura e preço válidos.")
