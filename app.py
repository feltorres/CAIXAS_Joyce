import streamlit as st

st.set_page_config(page_title="Orçamento - Caixas de Papelão", layout="wide")
st.title("Sistema de Orçamento - Caixas e Chapas de Papelão")

# Controle de sessão para múltiplas linhas
if 'num_itens' not in st.session_state:
    st.session_state.num_itens = 1

def adicionar_item():
    st.session_state.num_itens += 1

def resetar_itens():
    st.session_state.num_itens = 1

st.sidebar.header("Parâmetros Base")
preco_kg = st.sidebar.number_input("Preço do KG do Papelão (R$)", min_value=0.0, value=0.0, step=0.1)
gramatura = st.sidebar.number_input("Gramatura (g/m²)", min_value=0, value=378, step=1)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("**Preços para Negociação (Opcional)**")
preco_300 = st.sidebar.number_input("Preço do KG para 300kg (R$)", min_value=0.0, value=12.35, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_1000 = st.sidebar.number_input("Preço do KG para 1000kg (R$)", min_value=0.0, value=11.50, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_recibo = st.sidebar.number_input("Preço do KG mediante recibo (R$)", min_value=0.0, value=11.20, step=0.1, help="Deixe 0.0 para usar o preço padrão.")

tipo_produto = st.radio("O que deseja orçar?", ["Caixa Maleta (Modelos Específicos)", "Chapa / Corte e Vinco"], on_change=resetar_itens)

st.markdown("---")

itens_para_calcular = []

if tipo_produto == "Caixa Maleta (Modelos Específicos)":
    for i in range(st.session_state.num_itens):
        st.markdown(f"**Caixa {i+1}**")
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            modelo = st.selectbox("Modelo", ["Abas Normais", "Aba Dupla / Total", "Aba Dupla Inferior ou Superior", "Sem Aba Superior", "Transpassadas"], key=f"mod_cx_{i}")
        with col2:
            c = st.number_input("C (mm)", min_value=0, value=240, step=1, key=f"c_cx_{i}")
        with col3:
            l = st.number_input("L (mm)", min_value=0, value=180, step=1, key=f"l_cx_{i}")
        with col4:
            a = st.number_input("A (mm)", min_value=0, value=175, step=1, key=f"a_cx_{i}")
        with col5:
            qtd = st.number_input("Qtd", min_value=1, value=2500, step=1, key=f"q_cx_{i}")
            
        transp_sup = transp_inf = 0
        if modelo == "Transpassadas":
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                transp_sup = st.number_input("Transpasse Sup (mm)", min_value=0, value=40, step=1, key=f"ts_{i}")
            with t_col2:
                transp_inf = st.number_input("Transpasse Inf (mm)", min_value=0, value=40, step=1, key=f"ti_{i}")
                
        itens_para_calcular.append({
            'nome': f"Caixa {i+1}",
            'modelo': modelo,
            'c': c, 'l': l, 'a': a, 'qtd': qtd,
            'transp_sup': transp_sup, 'transp_inf': transp_inf,
            'desc': f"C {c} x L {l} x A {a} - {modelo}"
        })
else:
    for i in range(st.session_state.num_itens):
        st.markdown(f"**Item {i+1}**")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            modelo = st.selectbox("Tipo", ["Cinta-Tab-Chapa", "Corte e Vinco"], key=f"mod_ch_{i}")
        with col2:
            c = st.number_input("C (mm)", min_value=0, value=390, step=1, key=f"c_ch_{i}")
        with col3:
            l = st.number_input("L (mm)", min_value=0, value=260, step=1, key=f"l_ch_{i}")
        with col4:
            qtd = st.number_input("Quantidade", min_value=1, value=8000, step=1, key=f"q_ch_{i}")
            
        itens_para_calcular.append({
            'nome': f"Item {i+1}",
            'modelo': modelo,
            'c': c, 'l': l, 'qtd': qtd,
            'desc': f"C {c} x L {l} - {modelo}"
        })

st.button("➕ ADICIONAR " + ("CAIXA" if tipo_produto == "Caixa Maleta (Modelos Específicos)" else "ITEM"), on_click=adicionar_item)

st.markdown("---")

def formata_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_peso(peso):
    return f"{peso:.1f}".replace(".", ",") + " Kg"

def formata_qtd(quantidade):
    return f"{quantidade:,}".replace(",", ".")

if st.button("Calcular"):
    if preco_kg <= 0 or gramatura <= 0:
        st.error("Insira os parâmetros base (Preço e Gramatura).")
    else:
        resultados = []
        valor_total_pedido = 0.0
        
        preco_efetivo_300 = preco_300 if preco_300 > 0 else preco_kg
        preco_efetivo_1000 = preco_1000 if preco_1000 > 0 else preco_kg
        preco_efetivo_recibo = preco_recibo if preco_recibo > 0 else preco_kg

        for it in itens_para_calcular:
            area_m2 = 0.0
            
            if tipo_produto == "Caixa Maleta (Modelos Específicos)":
                c, l, a = it['c'], it['l'], it['a']
                if it['modelo'] == "Abas Normais":
                    area_m2 = ((c + l) * 2 * (l + a) * 1.1) / 1000000
                elif it['modelo'] == "Aba Dupla / Total":
                    area_m2 = (((c + l) * 2) * (l + l + a) * 1.1) / 1000000
                elif it['modelo'] == "Aba Dupla Inferior ou Superior":
                    area_m2 = (((c + l) * 2) * (l + (l / 2) + a) * 1.1) / 1000000
                elif it['modelo'] == "Sem Aba Superior":
                    area_m2 = ((c + l) * 2 * ((l / 2) + a) * 1.1) / 1000000
                elif it['modelo'] == "Transpassadas":
                    area_m2 = ((c + l) * 2 * (l + a + it['transp_sup'] + it['transp_inf']) * 1.1) / 1000000
            else:
                c, l = it['c'], it['l']
                if it['modelo'] == "Cinta-Tab-Chapa":
                    area_m2 = (c * l) / 1000000
                elif it['modelo'] == "Corte e Vinco":
                    area_m2 = ((c + 30) * (l + 30)) / 1000000
            
            if area_m2 > 0:
                peso_unit_kg = (area_m2 * gramatura) / 1000
                peso_total_kg = peso_unit_kg * it['qtd']
                
                preco_unit = peso_unit_kg * preco_kg
                preco_total = preco_unit * it['qtd']
                valor_total_pedido += preco_total
                
                # Cálculos de Negociação
                qtd_300 = int(300 / peso_unit_kg) if peso_unit_kg > 0 else 0
                preco_unit_300 = peso_unit_kg * preco_efetivo_300
                valor_300 = qtd_300 * preco_unit_300
                
                qtd_1000 = int(1000 / peso_unit_kg) if peso_unit_kg > 0 else 0
                preco_unit_1000 = peso_unit_kg * preco_efetivo_1000
                valor_1000 = qtd_1000 * preco_unit_1000
                
                preco_unit_recibo = peso_unit_kg * preco_efetivo_recibo
                valor_recibo = qtd_300 * preco_unit_recibo

                resultados.append({
                    'nome': it['nome'],
                    'desc': it['desc'],
                    'preco_unit': preco_unit,
                    'peso_total': peso_total_kg,
                    'preco_total': preco_total,
                    'qtd_300': qtd_300, 'preco_unit_300': preco_unit_300, 'valor_300': valor_300,
                    'qtd_1000': qtd_1000, 'preco_unit_1000': preco_unit_1000, 'valor_1000': valor_1000,
                    'preco_unit_recibo': preco_unit_recibo, 'valor_recibo': valor_recibo
                })

        if not resultados:
            st.warning("Verifique as dimensões. Não foi possível calcular nenhum item.")
        else:
            st.markdown("""
            <style>
            .resumo-box {
                background-color: #F8F9F9;
                border-left: 6px solid #2C3E50;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .linha-resumo {
                font-size: 1.1em;
                margin-bottom: 10px;
                color: #333;
            }
            .total-box {
                background-color: #EAFAF1;
                border-left: 6px solid #239B56;
                padding: 20px;
                border-radius: 5px;
                text-align: center;
                margin-bottom: 30px;
            }
            .card-laranja {
                background-color: #FEF5E7;
                border-left: 6px solid #D68910;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            .ref-linha {
                font-size: 1.1em;
                margin-bottom: 5px;
                color: #333;
            }
            .texto-recibo {
                color: #FF0000;
                font-weight: bold;
                border-top: 1px solid #ccc;
                padding-top: 8px;
                margin-top: 8px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("### Resultados do Orçamento")
            
            # Box único com a lista
            html_lista = '<div class="resumo-box">'
            for r in resultados:
                html_lista += f"""
                <div class="linha-resumo">
                    <strong>{r['nome']} ({r['desc']})</strong> &nbsp;&gt;&nbsp; 
                    Valor Unitário: <strong>{formata_moeda(r['preco_unit'])}</strong> &nbsp;&gt;&nbsp; 
                    Peso total: <strong>{formata_peso(r['peso_total'])}</strong> &nbsp;&gt;&nbsp; 
                    Valor Total: <strong style="color: #239B56;">{formata_moeda(r['preco_total'])}</strong>
                </div>
                """
            html_lista += '</div>'
            st.markdown(html_lista, unsafe_allow_html=True)
            
            # Valor Total
            st.markdown(f"""
            <div class="total-box">
                <div style="font-size: 1.2em; font-weight: bold; color: #333;">VALOR TOTAL DO PEDIDO</div>
                <div style="font-size: 2.2em; font-weight: bold; color: #000;">{formata_moeda(valor_total_pedido)}</div>
            </div>
            """, unsafe_allow_html=True)

            # Referências de Negociação Individuais
            st.markdown("### Referências para Negociação")
            for r in resultados:
                st.markdown(f"""
                <div class="card-laranja">
                    <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 10px;">{r['nome']} ({r['desc']})</div>
                    <div class="ref-linha">
                        <strong>300kg:</strong> {formata_qtd(r['qtd_300'])} un &nbsp;|&nbsp; <strong>Unitário:</strong> {formata_moeda(r['preco_unit_300'])} &nbsp;|&nbsp; <strong>Total:</strong> {formata_moeda(r['valor_300'])}
                    </div>
                    <div class="ref-linha">
                        <strong>1000kg:</strong> {formata_qtd(r['qtd_1000'])} un &nbsp;|&nbsp; <strong>Unitário:</strong> {formata_moeda(r['preco_unit_1000'])} &nbsp;|&nbsp; <strong>Total:</strong> {formata_moeda(r['valor_1000'])}
                    </div>
                    <div class="ref-linha texto-recibo">
                        Preço Mediante Recibo ({formata_qtd(r['qtd_300'])} un) &nbsp;|&nbsp; Unitário: {formata_moeda(r['preco_unit_recibo'])} &nbsp;|&nbsp; Total: {formata_moeda(r['valor_recibo'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
