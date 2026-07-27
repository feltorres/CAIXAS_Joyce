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
        "Normal", 
        "Aba Dupla / Total", 
        "Aba Dupla Inferior ou Superior", 
        "Sem Aba Superior", 
        "Transpassadas"
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Valores inteiros, sem decimais
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
    
    # Fórmulas exatas extraídas da linha 14 da planilha
    if modelo == "Normal":
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
        
    # Fórmulas exatas extraídas das colunas G e H
    if modelo_chapa == "Cinta-Tab-Chapa":
        area_m2 = (c * l) / 1000000
    elif modelo_chapa == "Corte e Vinco":
        area_m2 = ((c + 30) * (l + 30)) / 1000000

if st.button("Calcular"):
    if area_m2 > 0 and preco_kg > 0 and gramatura > 0:
        # Cálculos de Peso (Linhas 15 e 16)
        peso_unit_kg = (area_m2 * gramatura) / 1000
        peso_total_kg = peso_unit_kg * qtd
        
        # Cálculos de Preço (Linhas 17 e 18)
        preco_unit = peso_unit_kg * preco_kg
        preco_total = preco_unit * qtd
        
        st.markdown("### Resultados")
        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        
        r_col1.metric("Peso Unitário (kg)", f"{peso_unit_kg:.4f}")
        r_col2.metric("Peso Total (kg)", f"{peso_total_kg:.2f}")
        r_col3.metric("Valor Unitário (R$)", f"{preco_unit:.4f}")
        r_col4.metric("Valor Total (R$)", f"{preco_total:.2f}")
    else:
        st.error("Insira as dimensões, o peso e a gramatura.")
