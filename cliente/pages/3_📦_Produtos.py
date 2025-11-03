import streamlit as st
import pandas as pd
from services.local_service import LocalProdutoService
produto_service = LocalProdutoService()


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
if not can_access(st.session_state.cargo, 'produtos'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== SERVIÇO ==========
produto_service = ProdutoService()

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
        if st.button("📦 Produtos", use_container_width=True, type="primary"):
            pass  # ← MUDEI: Não faz nada se já está na página
    
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
    
    if st.button("🚪 Sair", use_container_width=True, type="secondary"):
        st.session_state.logado = False
        st.switch_page("main.py")

# ========== HEADER ==========
st.title("📦 Gestão de Produtos")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== ABAS ==========
tab1, tab2, tab3 = st.tabs(["📋 Listar Produtos", "➕ Novo Produto", "📊 Estoque"])

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
    
    try:
        produtos = produto_service.listar_produtos() or []
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
            st.info("Nenhum produto cadastrado")
    except Exception as e:
        st.error(f"Erro ao carregar estoque: {e}")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")

