import streamlit as st
from services.local_service import LocalClienteService, LocalProdutoService, LocalVendaService
from utils.permissions import can_access, can_edit, can_delete, can_create

cliente_service = LocalClienteService()
produto_service = LocalProdutoService() 
venda_service = LocalVendaService()

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Dashboard - ERP",
    page_icon="📊",
    layout="wide"
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

# ========== MENU LATERAL ==========
with st.sidebar:
    st.title("🏢 ERP Sistema")
    st.write(f"**Usuário:** {st.session_state.usuario}")
    st.write(f"**Cargo:** {st.session_state.cargo}")
    st.divider()
    
    st.subheader("🧭 Navegação")
    
    # Menu baseado nas permissões - APENAS mostre o que o usuário pode acessar
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")
    
    # 👥 CLIENTES - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'clientes'):
        if st.button("👥 Clientes", use_container_width=True):
            st.switch_page("pages/2_👥_Clientes.py")
    
    # 📦 PRODUTOS - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'produtos'):
        if st.button("📦 Produtos", use_container_width=True):
            st.switch_page("pages/3_📦_Produtos.py")
    
    # 💰 VENDAS - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'vendas'):
        # Verifica se está na página atual para usar type="primary"
        current_page = st.query_params.get("page", "1_🏠_Dashboard")
        is_current = current_page == "4_💰_Vendas"
        
        if st.button("💰 Vendas", use_container_width=True, type="primary" if is_current else "secondary"):
            st.switch_page("pages/4_💰_Vendas.py")
    
    # 💸 FINANCEIRO - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'financeiro'):
        current_page = st.query_params.get("page", "1_🏠_Dashboard")
        is_current = current_page == "5_💸_Financeiro"
        
        if st.button("💸 Financeiro", use_container_width=True, type="primary" if is_current else "secondary"):
            st.switch_page("pages/5_💸_Financeiro.py")
    
    # 📋 FISCAL - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'fiscal'):
        current_page = st.query_params.get("page", "1_🏠_Dashboard")
        is_current = current_page == "6_📋_Fiscal"
        
        if st.button("📋 Fiscal", use_container_width=True, type="primary" if is_current else "secondary"):
            st.switch_page("pages/6_📋_Fiscal.py")
    
    # ⚙️ CONFIGURAÇÕES - só mostra se tiver permissão
    if can_access(st.session_state.cargo, 'configuracoes'):
        current_page = st.query_params.get("page", "1_🏠_Dashboard")
        is_current = current_page == "7_⚙️_Configurações"
        
        if st.button("⚙️ Configurações", use_container_width=True, type="primary" if is_current else "secondary"):
            st.switch_page("pages/7_⚙️_Configurações.py")
    
    st.divider()

# ========== CONTEÚDO ==========
st.title("📊 Dashboard do Sistema ERP")
st.success(f"✅ Bem-vindo, {st.session_state.usuario}!")

# Métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Clientes", "25")
with col2:
    st.metric("📦 Produtos", "48") 
with col3:
    st.metric("💰 Vendas", "156")
with col4:
    st.metric("📊 Estoque", "324")

st.divider()
st.info("🎉 Sistema ERP funcionando perfeitamente!")