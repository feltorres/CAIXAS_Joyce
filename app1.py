import streamlit as st

st.set_page_config(page_title="Orçamento - Caixas de Papelão", layout="wide")
st.title("Sistema de Orçamento - Caixas e Chapas de Papelão")

# Controle de sessão para múltiplas linhas com IDs únicos
if 'item_ids' not in st.session_state:
    st.session_state.item_ids = [0]
    st.session_state.next_id = 1

def adicionar_item():
    st.session_state.item_ids.append(st.session_state.next_id)
    st.session_state.next_id += 1

def remover_item(item_id):
    if len(st.session_state.item_ids) > 1:
        st.session_state.item_ids.remove(item_id)

st.sidebar.header("Parâmetros Base")
preco_kg = st.sidebar.number_input("Preço do KG do Papelão (R$)", min_value=0.0, value=0.0, step=0.1)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("**Preços para Negociação (Opcional)**")
preco_300 = st.sidebar.number_input("Preço do KG para 300kg (R$)", min_value=0.0, value=12.35, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_1000 = st.sidebar.number_input("Preço do KG para 1000kg (R$)", min_value=0.0, value=11.50, step=0.1, help="Deixe 0.0 para usar o preço padrão.")
preco_recibo = st.sidebar.number_input("Preço do KG mediante recibo (R$)", min_value=0.0, value=11.20, step=0.1, help="Deixe 0.0 para usar o preço padrão.")

st.markdown("---")

itens_para_calcular = []
opcoes_modelos = [
    "Abas Normais", 
    "Aba Dupla / Total", 
    "Aba Dupla Inferior ou Superior", 
    "Sem Aba Superior", 
    "Transpassadas",
    "Cinta-Tab-Chapa", 
    "Corte e Vinco"
]

for idx, item_id in enumerate(st.session_state.item_ids):
    st.markdown(f"**Item {idx+1}**")
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2.2, 1.3, 1, 1, 1, 1, 0.5])
    
    with col1:
        modelo = st.selectbox("Modelo", opcoes_modelos, key=f"mod_{item_id}")
        
    is_chapa = modelo in ["Cinta-Tab-Chapa", "Corte e Vinco"]
    
    with col2:
        gramatura = st.number_input("Gramat. (g/m²)", min_value=1, value=378, step=1, key=f"gram_{item_id}")
    with col3:
        c = st.number_input("C (mm)", min_value=0, value=240, step=1, key=f"c_{item_id}")
    with col4:
        l = st.number_input("L (mm)", min_value=0, value=180, step=1, key=f"l_{item_id}")
    with col5:
        a = st.number_input("A (mm)", min_value=0, value=0 if is_chapa else 175, step=1, disabled=is_chapa, key=f"a_{item_id}")
    with col6:
        qtd = st.number_input("Qtd", min_value=1, value=2500, step=1, key=f"q_{item_id}")
    with col7:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.button("❌", key=f"rm_{item_id}", on_click=remover_item, args=(item_id,), disabled=len(st.session_state.item_ids) == 1, help="Remover este item")
        
    transp_sup = transp_inf = 0
    if modelo == "Transpassadas":
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            transp_sup = st.number_input("Transpasse Sup (mm)", min_value=0, value=40, step=1, key=f"ts_{item_id}")
        with t_col2:
            transp_inf = st.number_input("Transpasse Inf (mm)", min_value=0, value=40, step=1, key=f"ti_{item_id}")
            
    if is_chapa:
        desc = f"C {c} x L {l} - {modelo}"
    else:
        desc = f"C {c} x L {l} x A {a} - {modelo}"
        
    itens_para_calcular.append({
        'nome': f"Item {idx+1}",
        'modelo': modelo,
        'gramatura': gramatura,
        'c': c, 'l': l, 'a': a, 'qtd': qtd,
        'transp_sup': transp_sup, 'transp_inf': transp_inf,
        'desc': desc
    })

col_btn1, _ = st.columns([2, 8])
with col_btn1:
    st.button("➕ ADICIONAR ITEM", on_click=adicionar_item, use_container_width=True)

st.markdown("---")

def formata_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_peso(peso):
    return f"{peso:.1f}".replace(".", ",") + " Kg"

def formata_qtd(quantidade):
    return f"{quantidade:,}".replace(",", ".")

if st.button("Calcular"):
    if preco_kg <= 0:
        st.error("Insira o Preço do KG base maior que zero na barra lateral.")
    else:
        resultados = []
        valor_total_pedido = 0.0
        
        preco_efetivo_300 = preco_300 if preco_300 > 0 else preco_kg
        preco_efetivo_1000 = preco_1000 if preco_1000 > 0 else preco_kg
        preco_efetivo_recibo = preco_recibo if preco_recibo > 0 else preco_kg

        for it in itens_para_calcular:
            area_m2 = 0.0
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
            elif it['modelo'] == "Cinta-Tab-Chapa":
                area_m2 = (c * l) / 1000000
            elif it['modelo'] == "Corte e Vinco":
                area_m2 = ((c + 30) * (l + 30)) / 1000000
            
            if area_m2 > 0:
                peso_unit_kg = (area_m2 * it['gramatura']) / 1000
                peso_total_kg = peso_unit_kg * it['qtd']
                
                preco_unit = peso_unit_kg * preco_kg
                preco_total = preco_unit * it['qtd']
                valor_total_pedido += preco_total
                
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
                    'modelo': it['modelo'],
                    'c': c, 'l': l, 'a': a,
                    'gramatura': it['gramatura'],
                    'qtd': it['qtd'],
                    'peso_unit_kg': peso_unit_kg,
                    'preco_unit': preco_unit,
                    'peso_total': peso_total_kg,
                    'preco_total': preco_total,
                    'qtd_300': qtd_300, 'preco_unit_300': preco_unit_300, 'valor_300': valor_300,
                    'qtd_1000': qtd_1000, 'preco_unit_1000': preco_unit_1000, 'valor_1000': valor_1000,
                    'preco_unit_recibo': preco_unit_recibo, 'valor_recibo': valor_recibo
                })

        if not resultados:
            st.warning("Não foi possível calcular nenhum item. Verifique as dimensões inseridas.")
        else:
            st.markdown("""
            <style>
            .card-azul {
                background-color: #EBF5FB;
                border-left: 6px solid #2874A6;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            .header-azul {
                font-size: 1.1em;
                font-weight: bold;
                color: #2874A6;
                margin-bottom: 15px;
                border-bottom: 1px solid #BDC3C7;
                padding-bottom: 5px;
            }
            .flex-container {
                display: flex;
                justify-content: space-between;
                text-align: center;
            }
            .flex-item {
                flex: 1;
            }
            .titulo-campo {
                font-size: 0.9em;
                color: #555;
                font-weight: bold;
            }
            .valor-campo {
                font-size: 1.4em;
                color: #000;
                font-weight: bold;
            }
            .valor-destaque {
                color: #239B56;
            }
            .sub-valor {
                font-size: 0.85em;
                color: #777;
                margin-top: 3px;
            }
            .total-box {
                background-color: #EAFAF1;
                border-left: 6px solid #239B56;
                padding: 20px;
                border-radius: 5px;
                text-align: center;
                margin: 25px 0;
            }
            .card-laranja {
                background-color: #FEF5E7;
                border-left: 6px solid #D68910;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            .header-laranja {
                font-size: 1.1em;
                font-weight: bold;
                color: #D68910;
                margin-bottom: 10px;
                border-bottom: 1px solid #F5CBA7;
                padding-bottom: 5px;
            }
            .linha-neg {
                font-size: 1em;
                color: #333;
                margin-bottom: 8px;
                border-bottom: 1px dashed #FAD7A1;
                padding-bottom: 5px;
            }
            .linha-neg:last-child {
                border-bottom: none;
                margin-bottom: 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("### Resultados do Orçamento")
            
            html_itens = ""
            for r in resultados:
                html_itens += f"""
                <div class="card-azul">
                    <div class="header-azul">{r['nome']} ({r['desc']}) - Gramatura {r['gramatura']}g</div>
                    <div class="flex-container">
                        <div class="flex-item">
                            <div class="titulo-campo">Quantidade</div>
                            <div class="valor-campo">{formata_qtd(r['qtd'])} un</div>
                        </div>
                        <div class="flex-item">
                            <div class="titulo-campo">Valor Unitário</div>
                            <div class="valor-campo">{formata_moeda(r['preco_unit'])}</div>
                        </div>
                        <div class="flex-item">
                            <div class="titulo-campo">Peso Total</div>
                            <div class="valor-campo">{formata_peso(r['peso_total'])}</div>
                            <div class="sub-valor">Peso unit.: {formata_peso(r['peso_unit_kg'])}</div>
                        </div>
                        <div class="flex-item">
                            <div class="titulo-campo">Valor Total</div>
                            <div class="valor-campo valor-destaque">{formata_moeda(r['preco_total'])}</div>
                        </div>
                    </div>
                </div>
                """
            st.markdown(html_itens, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="total-box">
                <div style="font-size: 1.2em; font-weight: bold; color: #333;">VALOR TOTAL DO PEDIDO</div>
                <div style="font-size: 2.2em; font-weight: bold; color: #000;">{formata_moeda(valor_total_pedido)}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Referências para Negociação")
            
            html_300 = '<div class="card-laranja"><div class="header-laranja">Para 300kg</div>'
            for r in resultados:
                html_300 += f"""
                <div class="linha-neg">
                    <strong>{r['nome']}:</strong> Quantidade: {formata_qtd(r['qtd_300'])} un &nbsp;|&nbsp; 
                    Unitário: {formata_moeda(r['preco_unit_300'])} &nbsp;|&nbsp; 
                    Total: <strong>{formata_moeda(r['valor_300'])}</strong>
                </div>"""
            html_300 += '</div>'
            st.markdown(html_300, unsafe_allow_html=True)

            html_1000 = '<div class="card-laranja"><div class="header-laranja">Para 1000kg</div>'
            for r in resultados:
                html_1000 += f"""
                <div class="linha-neg">
                    <strong>{r['nome']}:</strong> Quantidade: {formata_qtd(r['qtd_1000'])} un &nbsp;|&nbsp; 
                    Unitário: {formata_moeda(r['preco_unit_1000'])} &nbsp;|&nbsp; 
                    Total: <strong>{formata_moeda(r['valor_1000'])}</strong>
                </div>"""
            html_1000 += '</div>'
            st.markdown(html_1000, unsafe_allow_html=True)

            html_recibo = '<div class="card-laranja" style="border-left-color: #E74C3C; background-color: #FDEDEC; margin-bottom: 30px;"><div class="header-laranja" style="color: #C0392B; border-bottom-color: #F5B7B1;">Mediante Recibo (Base 300kg)</div>'
            for r in resultados:
                html_recibo += f"""
                <div class="linha-neg" style="color: #C0392B;">
                    <strong>{r['nome']}:</strong> Quantidade: {formata_qtd(r['qtd_300'])} un &nbsp;|&nbsp; 
                    Unitário: {formata_moeda(r['preco_unit_recibo'])} &nbsp;|&nbsp; 
                    Total: <strong>{formata_moeda(r['valor_recibo'])}</strong>
                </div>"""
            html_recibo += '</div>'
            st.markdown(html_recibo, unsafe_allow_html=True)

            # Construção da string para o WhatsApp
            whatsapp_msg = ""
            for i, r in enumerate(resultados):
                is_chapa = r['modelo'] in ["Cinta-Tab-Chapa", "Corte e Vinco"]
                if is_chapa:
                    dim_str = f"C {r['c']} x L {r['l']} mm"
                else:
                    dim_str = f"C {r['c']} x L {r['l']} x A {r['a']} mm"
                
                whatsapp_msg += f"*{r['nome']} - {r['modelo']}*\n"
                whatsapp_msg += f"📏 {dim_str} - Gramatura {r['gramatura']}g\n"
                whatsapp_msg += f"📦 Quantidade: {formata_qtd(r['qtd'])} un\n"
                whatsapp_msg += f"💲 Preço Unitário: {formata_moeda(r['preco_unit'])}\n"
                whatsapp_msg += f"💰 Valor total: {formata_moeda(r['preco_total'])}\n"
                
                if i < len(resultados) - 1:
                    whatsapp_msg += "\n"
            
            whatsapp_msg += "\n\n"
            whatsapp_msg += "🖨️ ____ IMPRESSÃO \n"
            whatsapp_msg += "🗓️ Prazo de Produção - 20 a 25 dias ÚTEIS \n"
            whatsapp_msg += "🚚 FRETE CIF - BH E REGIÃO \n"
            whatsapp_msg += "🧾 IPI - 0%"

            # Renderização visual do box azul para o texto
            st.markdown("""
            <div class="card-azul" style="margin-top: 10px; margin-bottom: 5px;">
                <div class="header-azul" style="margin-bottom: 5px; border: none;">📱 Mensagem para WhatsApp</div>
                <div style="font-size: 0.9em; color: #555;">Copie o texto abaixo para enviar ao cliente:</div>
            </div>
            """, unsafe_allow_html=True)
            
            # st.code renderiza o bloco com um botão de cópia rápido
            st.code(whatsapp_msg, language="markdown")
