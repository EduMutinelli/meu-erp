import streamlit as st
import pandas as pd
from services.local_service import LocalClienteService
cliente_service = LocalClienteService()

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Clientes - ERP",
    page_icon="👥",
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
if not can_access(st.session_state.cargo, 'clientes'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== SERVIÇO ==========
cliente_service = ClienteService()

# ========== MENU LATERAL ==========
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
        if st.button("👥 Clientes", use_container_width=True, type="primary"):
            st.rerun()
    
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
        if st.button("📋 Fiscal", use_container_width=True):
            st.switch_page("pages/6_📋_Fiscal.py")
    
    if can_access(st.session_state.cargo, 'configuracoes'):
        if st.button("⚙️ Configurações", use_container_width=True):
            st.switch_page("pages/7_⚙️_Configurações.py")
    
    st.divider()
    
    

# ========== HEADER ==========
st.title("👥 Gestão de Clientes")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== ABAS ==========
tab1, tab2, tab3 = st.tabs(["📋 Listar Clientes", "➕ Novo Cliente", "✏️ Editar Cliente"])

with tab1:
    st.subheader("Clientes Cadastrados")
    
    if st.button("🔄 Atualizar Lista", key="atualizar_clientes"):
        try:
            clientes = cliente_service.listar_clientes()
            if clientes and len(clientes) > 0:
                df_clientes = pd.DataFrame(clientes)
                st.dataframe(df_clientes, width='stretch')
                st.success(f"✅ {len(clientes)} clientes encontrados")
            else:
                st.info("📝 Nenhum cliente cadastrado no momento")
        except Exception as e:
            st.error(f"❌ Erro ao carregar clientes: {e}")

with tab2:
    st.subheader("Cadastrar Novo Cliente")
    
    if not can_create(st.session_state.cargo, 'clientes'):
        st.warning("⚠️ Você não tem permissão para criar novos clientes")
    else:
        with st.form("form_novo_cliente", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo*", placeholder="João Silva")
                email = st.text_input("Email", placeholder="joao@empresa.com")
            
            with col2:
                telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
                endereco = st.text_area("Endereço", placeholder="Rua, Número, Cidade, Estado...")
            
            submitted = st.form_submit_button("💾 Salvar Cliente")
            
            if submitted:
                if nome and nome.strip():
                    cliente_data = {
                        "nome": nome.strip(),
                        "email": email.strip() if email else None,
                        "telefone": telefone.strip() if telefone else None,
                        "endereco": endereco.strip() if endereco else None
                    }
                    
                    try:
                        resultado = cliente_service.criar_cliente(cliente_data)
                        if resultado:
                            st.success("✅ Cliente cadastrado com sucesso!")
                            st.balloons()
                        else:
                            st.error("❌ Erro ao cadastrar cliente")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
                else:
                    st.error("❌ Nome é obrigatório!")

with tab3:
    st.subheader("Editar Cliente")
    
    if not can_edit(st.session_state.cargo, 'clientes'):
        st.warning("⚠️ Você não tem permissão para editar clientes")
    else:
        try:
            clientes = cliente_service.listar_clientes() or []
            if clientes:
                cliente_selecionado = st.selectbox(
                    "Selecione o cliente para editar:",
                    options=clientes,
                    format_func=lambda x: f"{x['id']} - {x['nome']}",
                    key="select_cliente_editar"
                )
                
                if cliente_selecionado:
                    with st.form("form_editar_cliente"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nome_edit = st.text_input("Nome", value=cliente_selecionado['nome'])
                            email_edit = st.text_input("Email", value=cliente_selecionado.get('email', ''))
                        
                        with col2:
                            telefone_edit = st.text_input("Telefone", value=cliente_selecionado.get('telefone', ''))
                            endereco_edit = st.text_area("Endereço", value=cliente_selecionado.get('endereco', ''))
                        
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            if st.form_submit_button("💾 Atualizar Cliente"):
                                cliente_data = {
                                    "nome": nome_edit.strip(),
                                    "email": email_edit.strip() if email_edit else None,
                                    "telefone": telefone_edit.strip() if telefone_edit else None,
                                    "endereco": endereco_edit.strip() if endereco_edit else None
                                }
                                
                                try:
                                    resultado = cliente_service.atualizar_cliente(
                                        cliente_selecionado['id'], 
                                        cliente_data
                                    )
                                    if resultado:
                                        st.success("✅ Cliente atualizado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao atualizar cliente")
                                except Exception as e:
                                    st.error(f"❌ Erro: {e}")
                        
                        with col_btn2:
                            if can_delete(st.session_state.cargo, 'clientes'):
                                if st.form_submit_button("🗑️ Excluir Cliente", type="secondary"):
                                    try:
                                        resultado = cliente_service.excluir_cliente(cliente_selecionado['id'])
                                        if resultado:
                                            st.success("✅ Cliente excluído com sucesso!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao excluir cliente")
                                    except Exception as e:
                                        st.error(f"❌ Erro: {e}")
            else:
                st.info("📝 Nenhum cliente cadastrado para editar")
        except Exception as e:
            st.error(f"❌ Erro ao carregar clientes: {e}")

# ========== ESTATÍSTICAS ==========
st.divider()
st.subheader("📊 Estatísticas de Clientes")

try:
    clientes = cliente_service.listar_clientes() or []
    if clientes:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Clientes", len(clientes))
        
        with col2:
            clientes_com_email = len([c for c in clientes if c.get('email')])
            st.metric("Clientes com Email", clientes_com_email)
        
        with col3:
            clientes_com_telefone = len([c for c in clientes if c.get('telefone')])
            st.metric("Clientes com Telefone", clientes_com_telefone)
    else:
        st.info("Nenhum dado disponível para estatísticas")
except Exception as e:
    st.error(f"Erro ao carregar estatísticas: {e}")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")

