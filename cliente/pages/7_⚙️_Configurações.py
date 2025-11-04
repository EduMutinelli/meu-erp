import streamlit as st
from utils.permissions import can_access

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Configurações - ERP",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="auto"
)

# ========== VERIFICAR LOGIN ==========
if 'logado' not in st.session_state or not st.session_state.logado:
    st.error("🔒 Você precisa fazer login primeiro!")
    st.stop()

# ========== VERIFICAR PERMISSÃO ==========
if not can_access(st.session_state.cargo, 'configuracoes'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== INICIALIZAR CONFIGURAÇÕES ==========
if 'configuracoes' not in st.session_state:
    st.session_state.configuracoes = {
        'tema': 'Claro',
        'idioma': 'Português',
        'itens_por_pagina': 10,
        'usuario_info': {
            'nome': st.session_state.usuario,
            'cargo': st.session_state.cargo,
            'email': 'admin@email.com',  # Exemplo
            'telefone': '(11) 99999-9999'  # Exemplo
        }
    }

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

# ========== MENU LATERAL PERSONALIZADO ==========
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
    
# ========== HEADER ==========
st.title("⚙️ Configurações do Sistema")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== ABAS ==========
tab1, tab2, tab3, tab4 = st.tabs(["👤 Perfil do Usuário", "🎨 Preferências", "💾 Backup e Exportação", "🔧 Sistema"])

with tab1:
    st.subheader("Informações Pessoais")
    
    with st.form("form_perfil"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input(
                "Nome", 
                value=st.session_state.configuracoes['usuario_info']['nome'],
                disabled=True
            )
            cargo = st.text_input(
                "Cargo", 
                value=st.session_state.configuracoes['usuario_info']['cargo'],
                disabled=True
            )
        
        with col2:
            email = st.text_input(
                "Email", 
                value=st.session_state.configuracoes['usuario_info']['email']
            )
            telefone = st.text_input(
                "Telefone", 
                value=st.session_state.configuracoes['usuario_info']['telefone']
            )
        
        if st.form_submit_button("💾 Salvar Alterações do Perfil"):
            st.session_state.configuracoes['usuario_info']['email'] = email
            st.session_state.configuracoes['usuario_info']['telefone'] = telefone
            st.success("✅ Alterações do perfil salvas com sucesso!")

with tab2:
    st.subheader("Preferências de Interface")
    
    with st.form("form_preferencias"):
        col1, col2 = st.columns(2)
        
        with col1:
            tema = st.selectbox(
                "Tema",
                options=["Claro", "Escuro", "Automático"],
                index=["Claro", "Escuro", "Automático"].index(st.session_state.configuracoes['tema'])
            )
            
            idioma = st.selectbox(
                "Idioma",
                options=["Português", "English", "Español"],
                index=["Português", "English", "Español"].index(st.session_state.configuracoes['idioma'])
            )
        
        with col2:
            itens_por_pagina = st.slider(
                "Itens por página",
                min_value=5,
                max_value=50,
                value=st.session_state.configuracoes['itens_por_pagina']
            )
            
            # Exemplo de outras preferências
            notificacoes = st.checkbox("Receber notificações por email", value=True)
        
        if st.form_submit_button("💾 Salvar Preferências"):
            st.session_state.configuracoes.update({
                'tema': tema,
                'idioma': idioma,
                'itens_por_pagina': itens_por_pagina,
                'notificacoes': notificacoes
            })
            st.success("✅ Preferências salvas com sucesso!")
            
            # Mostrar preview das configurações
            st.info(f"**Configurações aplicadas:** Tema: {tema} | Idioma: {idioma} | Itens por página: {itens_por_pagina}")

with tab3:
    st.subheader("Backup e Exportação de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📦 Backup do Sistema**")
        st.write("Faça backup completo dos dados do sistema.")
        
        if st.button("🔄 Gerar Backup Completo", use_container_width=True):
            # Simulação de backup
            st.success("✅ Backup gerado com sucesso!")
            st.info("**Arquivo:** backup_sistema_2024.db")
            
        st.download_button(
            label="📥 Download do Backup",
            data="conteúdo_simulado_do_backup",  # Substituir por dados reais
            file_name="backup_sistema.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.write("**📤 Exportar Dados**")
        st.write("Exporte dados específicos do sistema.")
        
        modulo_export = st.selectbox(
            "Selecionar módulo para exportar:",
            ["Clientes", "Produtos", "Vendas", "Todos os dados"]
        )
        
        formato_export = st.radio("Formato:", ["CSV", "JSON", "Excel"])
        
        if st.button("🚀 Exportar Dados", use_container_width=True):
            st.success(f"✅ Dados de {modulo_export} exportados em {formato_export}!")
            st.balloons()

with tab4:
    st.subheader("Configurações do Sistema")
    
    st.warning("⚠️ **Atenção:** Estas configurações afetam todo o sistema.")
    
    with st.form("form_sistema"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Configurações de negócio
            nome_empresa = st.text_input("Nome da Empresa", value="Minha Empresa LTDA")
            cnpj = st.text_input("CNPJ", value="12.345.678/0001-90")
            timezone = st.selectbox("Fuso Horário", ["America/Sao_Paulo", "UTC", "Europe/London"])
        
        with col2:
            # Configurações técnicas
            manutencao = st.checkbox("Modo Manutenção")
            log_level = st.selectbox("Nível de Log", ["INFO", "DEBUG", "WARNING", "ERROR"])
            auto_backup = st.checkbox("Backup Automático Diário", value=True)
        
        if st.form_submit_button("💾 Salvar Configurações do Sistema"):
            st.success("✅ Configurações do sistema salvas com sucesso!")
            st.info("Algumas configurações podem requerer reinicialização do sistema.")

# ========== INFORMACOES DAS CONFIGURAÇÕES ATUAIS ==========
st.divider()
st.subheader("📋 Configurações Atuais")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**👤 Perfil**")
    st.write(f"Nome: {st.session_state.configuracoes['usuario_info']['nome']}")
    st.write(f"Email: {st.session_state.configuracoes['usuario_info']['email']}")

with col2:
    st.write("**🎨 Preferências**")
    st.write(f"Tema: {st.session_state.configuracoes['tema']}")
    st.write(f"Idioma: {st.session_state.configuracoes['idioma']}")

with col3:
    st.write("**⚙️ Sistema**")
    st.write(f"Itens por página: {st.session_state.configuracoes['itens_por_pagina']}")
    st.write("Status: ✅ Ativo")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")
