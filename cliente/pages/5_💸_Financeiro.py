import streamlit as st
import pandas as pd
from datetime import date
from utils.permissions import can_access, can_create, can_edit, can_delete

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Financeiro - ERP",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="auto"
)

# ========== ESCONDER MENU LATERAL PADRÃO ==========
st.markdown("""
<style>
    /* Esconder o menu lateral padrão do Streamlit */
    .css-1d391kg {display: none !important;}
    
    /* Esconder qualquer outro elemento do menu padrão */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    /* Garantir que nosso menu personalizado fique visível */
    section[data-testid="stSidebar"] {
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== VERIFICAR LOGIN ==========
if 'logado' not in st.session_state or not st.session_state.logado:
    st.error("🔒 Você precisa fazer login primeiro!")
    st.stop()

# ========== VERIFICAR PERMISSÃO ==========
if not can_access(st.session_state.cargo, 'financeiro'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== DADOS SIMULADOS (PARA DEMONSTRAÇÃO) ==========
dados_financeiro = [
    {'ID': 1, 'descricao': 'Venda de Produtos', 'data': '2024-01-15', 'tipo': 'RECEITA', 'categoria': 'VENDAS', 'valor': 1500.00},
    {'ID': 2, 'descricao': 'Pagamento de Fornecedor', 'data': '2024-01-20', 'tipo': 'DESPESA', 'categoria': 'FORNECEDORES', 'valor': 800.00},
    {'ID': 3, 'descricao': 'Serviços Prestados', 'data': '2024-02-05', 'tipo': 'RECEITA', 'categoria': 'SERVIÇOS', 'valor': 2300.00},
    {'ID': 4, 'descricao': 'Salários', 'data': '2024-02-10', 'tipo': 'DESPESA', 'categoria': 'PESSOAL', 'valor': 4500.00},
]

# ========== MENU LATERAL PERSONALIZADO ==========
with st.sidebar:
    st.title("🏢 ERP Sistema")
    st.write(f"**Usuário:** {st.session_state.usuario}")
    st.write(f"**Cargo:** {st.session_state.cargo}")
    st.divider()
    
    st.subheader("🧭 Navegação")
    
    # Menu baseado nas permissões
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")
    
    if can_access(st.session_state.cargo, 'clientes'):
        if st.button("👥 Clientes", use_container_width=True):
            st.switch_page("pages/2_👥_Clientes.py")
    
    if can_access(st.session_state.cargo, 'produtos'):
        if st.button("📦 Produtos", use_container_width=True):
            st.switch_page("pages/3_📦_Produtos.py")
    
    if can_access(st.session_state.cargo, 'vendas'):
        if st.button("💰 Vendas", use_container_width=True):
            st.switch_page("pages/4_💰_Vendas.py")
    
    if can_access(st.session_state.cargo, 'financeiro'):
        if st.button("💸 Financeiro", use_container_width=True, type="primary"):
            pass  # ← MUDEI: Não faz nada se já está na página
    
    if can_access(st.session_state.cargo, 'fiscal'):
        if st.button("📋 Fiscal", use_container_width=True):
            st.switch_page("pages/6_📋_Fiscal.py")
    
    if can_access(st.session_state.cargo, 'configuracoes'):
        if st.button("⚙️ Configurações", use_container_width=True):
            st.switch_page("pages/7_⚙️_Configurações.py")
    
    st.divider()

# ========== HEADER ==========
st.title("💸 Área Financeira")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== DASHBOARD FINANCEIRO ==========
st.subheader("📊 Dashboard Financeiro")

# Calcular totais
total_receitas = sum(r['valor'] for r in dados_financeiro if r['tipo'] == 'RECEITA')
total_despesas = sum(r['valor'] for r in dados_financeiro if r['tipo'] == 'DESPESA')
saldo_atual = total_receitas - total_despesas

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Saldo Atual", f"R$ {saldo_atual:,.2f}", 
              delta=f"R$ {total_receitas - total_despesas:,.2f}")

with col2:
    st.metric("Total Receitas", f"R$ {total_receitas:,.2f}")

with col3:
    st.metric("Total Despesas", f"R$ {total_despesas:,.2f}")

with col4:
    st.metric("Fluxo Mensal", f"R$ {total_receitas:,.2f}", 
              delta=f"-R$ {total_despesas:,.2f}")

st.divider()

# ========== ABAS ==========
tab1, tab2, tab3 = st.tabs(["📋 Todos os Registros", "➕ Novo Registro", "📈 Relatórios"])

with tab1:
    st.subheader("📋 Registros Financeiros")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtrar_tipo = st.selectbox("Filtrar por tipo", ["TODOS", "RECEITA", "DESPESA"])
    with col2:
        categorias = ["TODAS"] + list(set(r['categoria'] for r in dados_financeiro))
        filtrar_categoria = st.selectbox("Filtrar por categoria", categorias)
    
    # Aplicar filtros
    registros_filtrados = dados_financeiro
    if filtrar_tipo != "TODOS":
        registros_filtrados = [r for r in registros_filtrados if r['tipo'] == filtrar_tipo]
    if filtrar_categoria != "TODAS":
        registros_filtrados = [r for r in registros_filtrados if r['categoria'] == filtrar_categoria]
    
    if registros_filtrados:
        # Exibir registros
        for registro in registros_filtrados:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
            
            with col1:
                st.write(registro['data'])
            
            with col2:
                st.write(registro['descricao'])
            
            with col3:
                st.write(registro['categoria'])
            
            with col4:
                cor = "🟢" if registro['tipo'] == 'RECEITA' else "🔴"
                st.write(f"{cor} {registro['tipo']}")
            
            with col5:
                st.write(f"R$ {registro['valor']:,.2f}")
            
            with col6:
                if can_delete(st.session_state.cargo, 'financeiro'):
                    if st.button("🗑️", key=f"del_fin_{registro['ID']}"):
                        st.warning("Funcionalidade em desenvolvimento")
        
        # Total filtrado
        total_filtrado = sum(r['valor'] for r in registros_filtrados if r['tipo'] == 'RECEITA') - \
                        sum(r['valor'] for r in registros_filtrados if r['tipo'] == 'DESPESA')
        
        st.info(f"**Total filtrado:** R$ {total_filtrado:,.2f} | **Registros:** {len(registros_filtrados)}")
    else:
        st.info("Nenhum registro encontrado com os filtros aplicados")

with tab2:
    st.subheader("➕ Novo Registro Financeiro")
    
    if not can_create(st.session_state.cargo, 'financeiro'):
        st.warning("⚠️ Você não tem permissão para criar registros financeiros")
    else:
        with st.form("form_financeiro"):
            col1, col2 = st.columns(2)
            
            with col1:
                descricao = st.text_input("Descrição*", placeholder="Ex: Venda de produtos, Pagamento de conta")
                valor = st.number_input("Valor*", min_value=0.01, step=0.01, format="%.2f")
                data_registro = st.date_input("Data*", value=date.today())
            
            with col2:
                tipo = st.selectbox("Tipo*", ["RECEITA", "DESPESA"])
                categoria = st.selectbox("Categoria*", [
                    "VENDAS", "SERVIÇOS", "FORNECEDORES", "PESSOAL", 
                    "MATERIAIS", "TRANSPORTE", "OUTROS"
                ])
                nova_categoria = st.text_input("Ou digite nova categoria")
            
            # Usar categoria personalizada se fornecida
            categoria_final = nova_categoria if nova_categoria else categoria
            
            if st.form_submit_button("💾 Salvar Registro"):
                if descricao and valor and categoria_final:
                    # Simular salvamento
                    novo_id = max([r['ID'] for r in dados_financeiro]) + 1
                    dados_financeiro.append({
                        'ID': novo_id,
                        'descricao': descricao,
                        'data': data_registro.isoformat(),
                        'tipo': tipo,
                        'categoria': categoria_final,
                        'valor': valor
                    })
                    st.success("✅ Registro salvo com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios (*)")

with tab3:
    st.subheader("📈 Relatórios Financeiros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Relatório por Categoria**")
        
        # Agrupar por categoria
        categorias_relatorio = {}
        for registro in dados_financeiro:
            cat = registro['categoria']
            if cat not in categorias_relatorio:
                categorias_relatorio[cat] = {'receitas': 0, 'despesas': 0}
            
            if registro['tipo'] == 'RECEITA':
                categorias_relatorio[cat]['receitas'] += registro['valor']
            else:
                categorias_relatorio[cat]['despesas'] += registro['valor']
        
        for categoria, valores in categorias_relatorio.items():
            with st.expander(f"{categoria} - Saldo: R$ {valores['receitas'] - valores['despesas']:,.2f}"):
                st.write(f"Receitas: R$ {valores['receitas']:,.2f}")
                st.write(f"Despesas: R$ {valores['despesas']:,.2f}")
    
    with col2:
        st.write("**Exportar Dados**")
        
        if st.button("📥 Exportar para CSV", use_container_width=True):
            df = pd.DataFrame(dados_financeiro)
            csv_data = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "💾 Baixar CSV",
                data=csv_data,
                file_name=f"financeiro_{date.today()}.csv",
                mime="text/csv"
            )
        
        st.info("""
        **Próximos relatórios:**
        - Fluxo de Caixa Mensal
        - Projeção de Receitas
        - Análise de Despesas
        - DRE Completo
        """)

# ========== GRÁFICOS ==========
st.divider()
st.subheader("📊 Visualizações")

col1, col2 = st.columns(2)

with col1:
    st.write("**Receitas vs Despesas**")
    dados_grafico = {
        'Categoria': ['Receitas', 'Despesas'],
        'Valor': [total_receitas, total_despesas]
    }
    st.bar_chart(dados_grafico, x='Categoria', y='Valor', use_container_width=True)

with col2:
    st.write("**Distribuição por Categoria**")
    # Dados para pizza (simplificado)
    categorias_pizza = {}
    for registro in dados_financeiro:
        cat = registro['categoria']
        categorias_pizza[cat] = categorias_pizza.get(cat, 0) + registro['valor']
    
    if categorias_pizza:
        st.write("**Valores por Categoria:**")
        for cat, valor in categorias_pizza.items():
            st.write(f"- {cat}: R$ {valor:,.2f}")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")

