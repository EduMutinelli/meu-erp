import streamlit as st
import pandas as pd
from services.local_service import LocalVendaService, LocalClienteService, LocalProdutoService
from utils.permissions import can_access, can_create

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Vendas - ERP",
    page_icon="💰", 
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
if not can_access(st.session_state.cargo, 'vendas'):
    st.error("❌ Você não tem permissão para acessar este módulo!")
    st.stop()

# ========== SERVIÇOS ==========
venda_service = VendaService()
cliente_service = ClienteService()
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
        if st.button("📦 Produtos", use_container_width=True):
            st.switch_page("pages/3_📦_Produtos.py")
    
    if can_access(st.session_state.cargo, 'vendas'):
        if st.button("💰 Vendas", use_container_width=True, type="primary"):
            st.rerun()
    
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
st.title("💰 Gestão de Vendas")
st.write(f"**Usuário:** {st.session_state.usuario} | **Cargo:** {st.session_state.cargo}")

# ========== SESSION STATE PARA ITENS DA VENDA ==========
if 'itens_venda' not in st.session_state:
    st.session_state.itens_venda = []

# ========== ABAS ==========
tab1, tab2 = st.tabs(["📋 Histórico de Vendas", "➕ Nova Venda"])

with tab1:
    st.subheader("Vendas Realizadas")
    
    if st.button("🔄 Carregar Vendas", key="carregar_vendas"):
        try:
            vendas = venda_service.listar_vendas()
            if vendas and len(vendas) > 0:
                # Formatar dados para exibição
                vendas_formatadas = []
                for venda in vendas:
                    total_float = float(venda['total'])
                    vendas_formatadas.append({
                        "ID": venda['id'],
                        "Cliente": venda.get('cliente_nome', 'N/A'),
                        "Data": venda['data_venda'][:10],
                        "Total": f"R$ {total_float:.2f}",
                        "Observação": venda.get('observacao', '')
                    })
                
                st.dataframe(vendas_formatadas, width='stretch')
                st.success(f"✅ {len(vendas)} vendas encontradas")
                
            else:
                st.info("📝 Nenhuma venda registrada no momento")
        except Exception as e:
            st.error(f"❌ Erro ao carregar vendas: {e}")

with tab2:
    st.subheader("Registrar Nova Venda")
    
    if not can_create(st.session_state.cargo, 'vendas'):
        st.warning("⚠️ Você não tem permissão para registrar vendas")
    else:
        # Carregar clientes e produtos
        try:
            clientes = cliente_service.listar_clientes() or []
            produtos = produto_service.listar_produtos() or []
            
            if not clientes:
                st.warning("⚠️ Cadastre clientes antes de fazer vendas")
            elif not produtos:
                st.warning("⚠️ Cadastre produtos antes de fazer vendas")
            else:
                # Formulário para adicionar itens
                st.subheader("🛒 Adicionar Itens à Venda")
                
                col_a, col_b, col_c = st.columns([3, 2, 1])
                with col_a:
                    produto_selecionado = st.selectbox(
                        "Selecione o Produto",
                        options=produtos,
                        format_func=lambda x: f"{x['nome']} - R$ {float(x['preco']):.2f} (Estoque: {x['estoque']})",
                        key="select_produto_venda"
                    )
                with col_b:
                    quantidade = st.number_input("Quantidade", min_value=1, value=1, key="quantidade_venda")
                with col_c:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("➕ Adicionar Item", key="btn_adicionar_item"):
                        if produto_selecionado:
                            # Verificar estoque
                            if produto_selecionado['estoque'] >= quantidade:
                                novo_item = {
                                    "produto_id": produto_selecionado['id'],
                                    "produto_nome": produto_selecionado['nome'],
                                    "quantidade": quantidade,
                                    "preco_unitario": float(produto_selecionado['preco']),
                                    "subtotal": quantidade * float(produto_selecionado['preco'])
                                }
                                
                                # Verificar se produto já está na lista
                                item_existente = next((item for item in st.session_state.itens_venda 
                                                     if item['produto_id'] == novo_item['produto_id']), None)
                                
                                if item_existente:
                                    st.warning("⚠️ Produto já adicionado à venda")
                                else:
                                    st.session_state.itens_venda.append(novo_item)
                                    st.success(f"✅ {quantidade}x {produto_selecionado['nome']} adicionado")
                                    st.rerun()
                            else:
                                st.error(f"❌ Estoque insuficiente! Disponível: {produto_selecionado['estoque']}")
                
                # Mostrar itens adicionados
                if st.session_state.itens_venda:
                    st.subheader("📋 Itens da Venda")
                    itens_df = []
                    total_venda = 0
                    
                    for item in st.session_state.itens_venda:
                        itens_df.append({
                            "Produto": item['produto_nome'],
                            "Quantidade": item['quantidade'],
                            "Preço Unit.": f"R$ {item['preco_unitario']:.2f}",
                            "Subtotal": f"R$ {item['subtotal']:.2f}"
                        })
                        total_venda += item['subtotal']
                    
                    st.dataframe(itens_df, width='stretch')
                    st.metric("💰 Total da Venda", f"R$ {total_venda:.2f}")
                    
                    # Botão para limpar itens
                    if st.button("🗑️ Limpar Todos os Itens", key="btn_limpar_itens"):
                        st.session_state.itens_venda = []
                        st.rerun()
                    
                    # Formulário para finalizar venda
                    st.subheader("💾 Finalizar Venda")
                    with st.form("form_finalizar_venda"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            cliente_selecionado = st.selectbox(
                                "Selecione o Cliente*",
                                options=clientes,
                                format_func=lambda x: f"{x['id']} - {x['nome']}",
                                key="select_cliente_venda"
                            )
                        
                        with col2:
                            observacao = st.text_area("Observações", placeholder="Observações da venda...", key="obs_venda")
                        
                        finalizar_venda = st.form_submit_button("💾 Registrar Venda")
                        
                        if finalizar_venda:
                            if cliente_selecionado and st.session_state.itens_venda:
                                venda_data = {
                                    "cliente_id": cliente_selecionado['id'],
                                    "itens": [
                                        {
                                            "produto_id": item['produto_id'],
                                            "quantidade": item['quantidade'],
                                            "preco_unitario": item['preco_unitario']
                                        } for item in st.session_state.itens_venda
                                    ],
                                    "observacao": observacao.strip() if observacao else None
                                }
                                
                                try:
                                    resultado = venda_service.criar_venda(venda_data)
                                    if resultado:
                                        st.success("✅ Venda registrada com sucesso!")
                                        st.balloons()
                                        # Limpar itens
                                        st.session_state.itens_venda = []
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao registrar venda")
                                except Exception as e:
                                    st.error(f"❌ Erro: {e}")
                            else:
                                st.error("❌ Selecione um cliente e adicione itens à venda")
                else:
                    st.info("➕ Use o botão 'Adicionar Item' para começar uma venda")
                            
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {e}")

# ========== NAVEGAÇÃO ==========
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("pages/1_🏠_Dashboard.py")

