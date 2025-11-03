import streamlit as st
import pandas as pd
from datetime import date
from utils.permissions import can_access, can_create, can_delete

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Fiscal - ERP",
    page_icon="📋",
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
if not can_access(st.session_state.cargo, 'fiscal'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== DADOS SIMULADOS (PARA DEMONSTRAÇÃO) ==========
dados_fiscais = [
    {'ID': 1, 'descricao': 'NF-e Venda 001', 'data_emissao': '2024-01-15', 'tipo': 'ENTRADA', 'valor': 1500.00},
    {'ID': 2, 'descricao': 'NF-e Compra 001', 'data_emissao': '2024-01-20', 'tipo': 'SAIDA', 'valor': 800.00},
    {'ID': 3, 'descricao': 'NF-e Venda 002', 'data_emissao': '2024-02-05', 'tipo': 'ENTRADA', 'valor': 2300.00},
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
        if st.button("💸 Financeiro", use_container_width=True):
            st.switch_page("pages/5_💸_Financeiro.py")
    
    if can_access(st.session_state.cargo, 'fiscal'):
        if st.button("📋 Fiscal", use_container_width=True, type="primary"):
            pass  # ← MUDEI: Não faz nada se já está na página
    
    if can_access(st.session_state.cargo, 'configuracoes'):
        if st.button("⚙️ Configurações", use_container_width=True):
            st.switch_page("pages/7_⚙️_Configurações.py")
    
    st.divider()
    
# ========== HEADER ==========
st.title("📋 Módulo Fiscal")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== DASHBOARD FISCAL ==========
st.subheader("📊 Dashboard Fiscal")

# Calcular totais
total_entradas = sum(r['valor'] for r in dados_fiscais if r['tipo'] == 'ENTRADA')
total_saidas = sum(r['valor'] for r in dados_fiscais if r['tipo'] == 'SAIDA')
saldo_fiscal = total_entradas - total_saidas

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Entradas", f"R$ {total_entradas:,.2f}")

with col2:
    st.metric("Total Saídas", f"R$ {total_saidas:,.2f}")

with col3:
    st.metric("Saldo Fiscal", f"R$ {saldo_fiscal:,.2f}")

with col4:
    st.metric("Total de Notas", len(dados_fiscais))

st.divider()

# ========== ABAS ==========
tab1, tab2, tab3 = st.tabs(["📥 Registros Fiscais", "➕ Novo Registro", "📊 Relatórios"])

with tab1:
    st.subheader("📥 Todos os Registros Fiscais")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtrar_tipo = st.selectbox("Filtrar por tipo", ["TODOS", "ENTRADA", "SAIDA"])
    with col2:
        meses = ["TODOS"] + [f"2024-{str(i).zfill(2)}" for i in range(1, 13)]
        filtrar_mes = st.selectbox("Filtrar por mês", meses)
    
    # Aplicar filtros
    registros_filtrados = dados_fiscais
    if filtrar_tipo != "TODOS":
        registros_filtrados = [r for r in registros_filtrados if r['tipo'] == filtrar_tipo]
    if filtrar_mes != "TODOS":
        registros_filtrados = [r for r in registros_filtrados if r['data_emissao'].startswith(filtrar_mes)]
    
    if registros_filtrados:
        # Exibir registros
        for registro in registros_filtrados:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            
            with col1:
                st.write(f"**{registro['descricao']}**")
            
            with col2:
                st.write(registro['data_emissao'])
            
            with col3:
                cor = "🟢" if registro['tipo'] == 'ENTRADA' else "🔴"
                st.write(f"{cor} {registro['tipo']}")
            
            with col4:
                st.write(f"R$ {registro['valor']:,.2f}")
            
            with col5:
                st.subheader("🗑️")

                if can_delete(st.session_state.cargo, 'financeiro'):  # ou 'fiscal'
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🧹 Limpar Dados de Teste", type="secondary"):
                            st.warning("Esta ação irá limpar todos os dados de teste")
                            # Implementar lógica de delete aqui
                            
                    with col2:
                        if st.button("📊 Resetar Estatísticas", type="secondary"):
                            st.info("Estatísticas resetadas")
                            st.rerun()
           
        # Totais
        total_entradas_filtro = sum(r['valor'] for r in registros_filtrados if r['tipo'] == 'ENTRADA')
        total_saidas_filtro = sum(r['valor'] for r in registros_filtrados if r['tipo'] == 'SAIDA')
        saldo_filtro = total_entradas_filtro - total_saidas_filtro
        
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Entradas", f"R$ {total_entradas_filtro:,.2f}")
        with col2:
            st.metric("Total Saídas", f"R$ {total_saidas_filtro:,.2f}")
        with col3:
            st.metric("Saldo Fiscal", f"R$ {saldo_filtro:,.2f}")
        with col4:
            st.metric("Registros", len(registros_filtrados))
    else:
        st.info("Nenhum registro encontrado com os filtros aplicados")

with tab2:
    st.subheader("➕ Novo Registro Fiscal")
    
    if not can_create(st.session_state.cargo, 'fiscal'):
        st.warning("⚠️ Você não tem permissão para criar registros fiscais")
    else:
        with st.form("form_fiscal"):
            col1, col2 = st.columns(2)
            
            with col1:
                descricao = st.text_input("Descrição do Documento*", placeholder="Ex: NF-e 001, Nota Fiscal")
                valor = st.number_input("Valor (R$)*", min_value=0.01, step=0.01, format="%.2f")
                data_emissao = st.date_input("Data de Emissão*", value=date.today())
            
            with col2:
                tipo = st.selectbox("Tipo de Operação*", ["ENTRADA", "SAIDA"])
                categoria = st.selectbox("Categoria*", [
                    "VENDA_MERCADORIA", "PRESTACAO_SERVICO", "COMPRA", "DESPESA_OPERACIONAL"
                ])
                numero_documento = st.text_input("Número do Documento", placeholder="Opcional")
            
            if st.form_submit_button("💾 Salvar Registro Fiscal"):
                if descricao and valor:
                    # Simular salvamento
                    novo_id = max([r['ID'] for r in dados_fiscais]) + 1
                    dados_fiscais.append({
                        'ID': novo_id,
                        'descricao': descricao,
                        'data_emissao': data_emissao.isoformat(),
                        'tipo': tipo,
                        'valor': valor
                    })
                    st.success("✅ Registro fiscal salvo com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios (*)")

with tab3:
    st.subheader("📊 Relatórios Fiscais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Relatório por Período**")
        
        periodo_inicio = st.date_input("Data Início", value=date.today().replace(day=1))
        periodo_fim = st.date_input("Data Fim", value=date.today())
        
        if st.button("📈 Gerar Relatório", use_container_width=True):
            # Filtrar por período
            registros_periodo = [
                r for r in dados_fiscais 
                if periodo_inicio <= date.fromisoformat(r['data_emissao']) <= periodo_fim
            ]
            
            if registros_periodo:
                total_entradas_periodo = sum(r['valor'] for r in registros_periodo if r['tipo'] == 'ENTRADA')
                total_saidas_periodo = sum(r['valor'] for r in registros_periodo if r['tipo'] == 'SAIDA')
                
                st.success(f"Relatório gerado: {len(registros_periodo)} registros no período")
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Entradas", f"R$ {total_entradas_periodo:,.2f}")
                with col2:
                    st.metric("Saídas", f"R$ {total_saidas_periodo:,.2f}")
                with col3:
                    st.metric("Saldo", f"R$ {total_entradas_periodo - total_saidas_periodo:,.2f}")
            else:
                st.info("Nenhum registro encontrado no período selecionado")
    
    with col2:
        st.write("**Exportar Dados**")
        
        if st.button("📥 Exportar para CSV", use_container_width=True):
            df = pd.DataFrame(dados_fiscais)
            csv_data = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "💾 Baixar CSV",
                data=csv_data,
                file_name=f"fiscal_{date.today()}.csv",
                mime="text/csv"
            )
        
        st.info("""
        **Próximos relatórios:**
        - DRE Fiscal
        - Livro Caixa
        - Apuração de Impostos
        - SPED Fiscal
        """)

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")

