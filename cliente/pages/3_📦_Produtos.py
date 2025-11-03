import streamlit as st
import pandas as pd
from services.produto_service import ProdutoService
from utils.permissions import can_access, can_edit, can_delete, can_create
produto_service = ProdutoService()

# ========== PERMISSÕES TEMPORÁRIAS ==========
def can_access(cargo, modulo):
    permissoes = {
        'ADM': ['clientes', 'produtos', 'vendas', 'financeiro', 'fiscal', 'configuracoes'],
        'financeiro': ['clientes', 'produtos', 'vendas', 'financeiro'],
        'usuario': ['produtos', 'vendas']
    }
    return cargo in permissoes and modulo in permissoes[cargo]

def can_edit(cargo, modulo):
    return can_access(cargo, modulo)

def can_delete(cargo, modulo):
    return cargo == 'ADM'

def can_create(cargo, modulo):
    return can_access(cargo, modulo)

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Produtos - ERP", 
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="auto"
)

# ========== ESCONDER MENU LATERAL PADRÃO ==========
st.markdown("""
<style>
    .css-1d391kg {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
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
if not can_access(st.session_state.cargo, 'produtos'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== MENU LATERAL PERSONALIZADO ==========
with st.sidebar:
    st.title("🏢 ERP Sistema")
    st.write(f"**Usuário:** {st.session_state.usuario}")
    st.write(f"**Cargo:** {st.session_state.cargo}")
    st.divider()
    
    st.subheader("🧭 Navegação")
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")
    
    if can_access(st.session_state.cargo, 'clientes'):
        if st.button("👥 Clientes", use_container_width=True):
            st.switch_page("pages/2_👥_Clientes.py")
    
    if can_access(st.session_state.cargo, 'produtos'):
        if st.button("📦 Produtos", use_container_width=True, type="primary"):
            st.rerun()
    
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
st.title("📦 Gestão de Produtos")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== ABAS ==========
tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar Produtos", "➕ Novo Produto", "📊 Estoque", "✏️ Editar Produto"])

with tab1:
    st.subheader("Produtos Cadastrados")
    
    if st.button("🔄 Atualizar Lista", key="atualizar_produtos"):
        try:
            produtos = produto_service.listar_produtos()
            if produtos and len(produtos) > 0:
                df_produtos = pd.DataFrame(produtos)
                st.dataframe(df_produtos, width='stretch')
                st.success(f"✅ {len(produtos)} produtos encontrados")
            else:
                st.info("📝 Nenhum produto cadastrado no momento")
        except Exception as e:
            st.error(f"❌ Erro ao carregar produtos: {e}")

with tab2:
    st.subheader("Cadastrar Novo Produto")
    
    if not can_create(st.session_state.cargo, 'produtos'):
        st.warning("⚠️ Você não tem permissão para criar novos produtos")
    else:
        with st.form("form_novo_produto", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome do Produto*", placeholder="Notebook Dell")
                preco = st.number_input("Preço*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
            
            with col2:
                estoque = st.number_input("Estoque*", min_value=0, value=0)
                categoria = st.text_input("Categoria", placeholder="Eletrônicos, Informática...")
            
            descricao = st.text_area("Descrição", placeholder="Descrição detalhada do produto...")
            
            submitted = st.form_submit_button("💾 Salvar Produto")
            
            if submitted:
                if nome and nome.strip() and preco >= 0:
                    produto_data = {
                        "nome": nome.strip(),
                        "preco": float(preco),
                        "estoque": int(estoque),
                        "categoria": categoria.strip() if categoria else None,
                        "descricao": descricao.strip() if descricao else None
                    }
                    
                    try:
                        resultado = produto_service.criar_produto(produto_data)
                        if resultado:
                            st.success("✅ Produto cadastrado com sucesso!")
                            st.balloons()
                        else:
                            st.error("❌ Erro ao cadastrar produto")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
                else:
                    st.error("❌ Nome e preço são obrigatórios!")

with tab3:
    st.subheader("📊 Controle de Estoque")
    
    if st.button("🔄 Carregar Estoque", key="carregar_estoque"):
        try:
            produtos = produto_service.listar_produtos()
            if produtos:
                # Produtos com estoque baixo
                estoque_baixo = [p for p in produtos if p.get('estoque', 0) < 10]
                    
                col1, col2, col3 = st.columns(3)
                    
                with col1:
                    st.metric("Total de Produtos", len(produtos))
                    
                with col2:
                    total_estoque = sum(p.get('estoque', 0) for p in produtos)
                    st.metric("Itens em Estoque", total_estoque)
                    
                with col3:
                    st.metric("Estoque Baixo", len(estoque_baixo), delta=f"-{len(estoque_baixo)}")
                    
                # Lista de estoque baixo
                if estoque_baixo:
                    st.warning("⚠️ Produtos com estoque baixo:")
                    for produto in estoque_baixo:
                        st.write(f"**{produto['nome']}** - Estoque: {produto['estoque']}")
                else:
                    st.success("✅ Todos os produtos com estoque adequado")
                        
                # Valor total do estoque
                valor_total = sum(p.get('estoque', 0) * float(p.get('preco', 0)) for p in produtos)
                st.info(f"💰 **Valor total do estoque:** R$ {valor_total:,.2f}")
                    
            else:
                st.info("📝 Nenhum produto cadastrado")
        except Exception as e:
            st.error(f"❌ Erro ao carregar estoque: {e}")
    else:
        st.info("👆 Clique no botão para carregar o estoque")
    
with tab4:  # ABA EDITAR PRODUTO
    st.subheader("✏️ Editar Produto")
    
    if not can_edit(st.session_state.cargo, 'produtos'):
        st.warning("⚠️ Você não tem permissão para editar produtos")
    else:
        if st.button("🔄 Carregar Produtos para Edição", key="carregar_edicao"):
            try:
                produtos = produto_service.listar_produtos()
                if produtos:
                    produto_selecionado = st.selectbox(
                        "Selecione o produto para editar:",
                        options=produtos,
                        format_func=lambda x: f"{x['id']} - {x['nome']} (R$ {x['preco']})",
                        key="select_produto_editar"
                    )
                    
                    if produto_selecionado:
                        with st.form("form_editar_produto"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                nome_edit = st.text_input("Nome", value=produto_selecionado['nome'])
                                preco_edit = st.number_input("Preço", min_value=0.0, value=float(produto_selecionado['preco']), step=0.01, format="%.2f")
                            
                            with col2:
                                estoque_edit = st.number_input("Estoque", min_value=0, value=produto_selecionado['estoque'])
                                categoria_edit = st.text_input("Categoria", value=produto_selecionado.get('categoria', ''))
                            
                            descricao_edit = st.text_area("Descrição", value=produto_selecionado.get('descricao', ''))
                            
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if st.form_submit_button("💾 Atualizar Produto"):
                                    produto_data = {
                                        "nome": nome_edit.strip(),
                                        "preco": float(preco_edit),
                                        "estoque": int(estoque_edit),
                                        "categoria": categoria_edit.strip() if categoria_edit else None,
                                        "descricao": descricao_edit.strip() if descricao_edit else None
                                    }
                                    
                                    try:
                                        resultado = produto_service.atualizar_produto(
                                            produto_selecionado['id'], 
                                            produto_data
                                        )
                                        if resultado:
                                            st.success("✅ Produto atualizado com sucesso!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao atualizar produto")
                                    except Exception as e:
                                        st.error(f"❌ Erro: {e}")
                            
                            with col_btn2:
                                if can_delete(st.session_state.cargo, 'produtos'):
                                    if st.form_submit_button("🗑️ Excluir Produto", type="secondary"):
                                        try:
                                            resultado = produto_service.excluir_produto(produto_selecionado['id'])
                                            if resultado:
                                                st.success("✅ Produto excluído com sucesso!")
                                                st.rerun()
                                            else:
                                                st.error("❌ Erro ao excluir produto")
                                        except Exception as e:
                                            st.error(f"❌ Erro: {e}")
                else:
                    st.info("📝 Nenhum produto cadastrado para editar")
            except Exception as e:
                st.error(f"❌ Erro ao carregar produtos: {e}")
        else:
            st.info("👆 Clique no botão para carregar os produtos")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")