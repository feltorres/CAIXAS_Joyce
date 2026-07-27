import streamlit as st

def calcular_area_caixa(modelo, c, l, a, aba_colagem=40):
    # Dimensões em milímetros. Retorna a área da chapa em metros quadrados.
    comprimento_chapa = (c * 2) + (l * 2) + aba_colagem
    
    if modelo == "Normal":
        largura_chapa = a + l
    elif modelo == "Aba Dupla / Total":
        largura_chapa = a + (l * 2)
    elif modelo == "Sem Aba Superior":
        largura_chapa = a + (l / 2)
    elif modelo == "Aba Dupla Inferior ou Superior":
        # Uma aba padrão (L/2) e uma dupla (L)
        largura_chapa = a + (1.5 * l)
    elif modelo == "Transpassada":
        # Assumindo transpasse que exige aba maior. Ajuste os 60mm se necessário.
        largura_chapa = a + l + 60
    else:
        largura_chapa = 0

    return (comprimento_chapa * largura_chapa) / 1000000

def calcular_area_chapa(c, l):
    # Para chapas e caixas corte/vinco
    return (c * l) / 1000000

st.set_page_config(page_title="Orçamento - Caixas de Papelão", layout="wide")
st.title("Sistema de Orçamento - Caixas e Chapas de Papelão")

st.sidebar.header("Parâmetros Base")
preco_kg = st.sidebar.number_input("Preço do KG do Papelão (R$)", min_value=0.0, value=5.0, step=0.1)
gramatura = st.sidebar.number_input("Gramatura (g/m²)", min_value=0, value=400, step=10)
aba_colagem = st.sidebar.number_input("Aba de Colagem (mm)", min_value=0, value=40, help="Tamanho da orelha de colagem.")

tipo_produto = st.radio("O que deseja orçar?", ["Caixa Maleta (Modelos Específicos)", "Chapa / Corte e Vinco"])

st.markdown("---")

if tipo_produto == "Caixa Maleta (Modelos Específicos)":
    modelo = st.selectbox("Selecione o Modelo da Caixa", [
        "Normal", 
        "Aba Dupla / Total", 
        "Sem Aba Superior", 
        "Aba Dupla Inferior ou Superior", 
        "Transpassada"
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        c = st.number_input("Comprimento (mm)", min_value=0.0, value=0.0)
    with col2:
        l = st.number_input("Largura (mm)", min_value=0.0, value=0.0)
    with col3:
        a = st.number_input("Altura (mm)", min_value=0.0, value=0.0)
    with col4:
        qtd = st.number_input("Quantidade", min_value=1, value=1)
        
    area_m2 = calcular_area_caixa(modelo, c, l, a, aba_colagem)

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.number_input("Comprimento da Chapa (mm)", min_value=0.0, value=0.0)
    with col2:
        l = st.number_input("Largura da Chapa (mm)", min_value=0.0, value=0.0)
    with col3:
        qtd = st.number_input("Quantidade", min_value=1, value=1)
        
    area_m2 = calcular_area_chapa(c, l)

if st.button("Calcular"):
    if area_m2 > 0 and preco_kg > 0 and gramatura > 0:
        peso_unit_kg = area_m2 * (gramatura / 1000)
        peso_total_kg = peso_unit_kg * qtd
        
        preco_unit = peso_unit_kg * preco_kg
        preco_total = preco_unit * qtd
        
        st.markdown("### Resultados")
        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        
        r_col1.metric("Peso Unitário", f"{peso_unit_kg:.4f} kg")
        r_col2.metric("Peso Total", f"{peso_total_kg:.2f} kg")
        r_col3.metric("Valor Unitário", f"R$ {preco_unit:.2f}")
        r_col4.metric("Valor Total", f"R$ {preco_total:.2f}")
        
    else:
        st.error("Insira dimensões, peso e gramatura maiores que zero.")
