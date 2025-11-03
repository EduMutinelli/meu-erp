import streamlit as st
import time

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="ERP - Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== VERIFICAR SE JÁ ESTÁ LOGADO ==========
if 'logado' in st.session_state and st.session_state.logado:
    st.switch_page("./pages/1_🏠_Dashboard.py")

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

# ========== ESTILOS ATUALIZADOS ==========
st.markdown("""
<style>
    /* ====== OCULTAR APENAS O MENU LATERAL ====== */
    section[data-testid="stSidebar"] {display: none !important;}

    /* ====== FUNDO ====== */
    .stApp {
        background: linear-gradient(135deg, #0f1116 0%, #1a1d2b 100%);
        font-family: 'Segoe UI', sans-serif;
    }

    /* ====== CARD LOGO ====== */
    .login-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.4), rgba(255, 255, 255, 0.2));
        padding: 35px 40px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(12px);
        margin: 30px auto;
        max-width: 420px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
    }

    .login-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: 0.5s;
    }

    .login-header:hover::before {
        left: 100%;
    }

    .login-logo {
        font-size: 55px;
        margin-bottom: 15px;
        filter: drop-shadow(0 5px 15px rgba(102, 126, 234, 0.4));
    }

    .login-title {
        font-size: 26px;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    /* ====== FORMULÁRIO ====== */
    .login-form {
        background: rgba(255,255,255,0.08);
        padding: 30px 35px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        max-width: 420px;
        margin: 20px auto;
        backdrop-filter: blur(10px);
    }

    /* ====== INPUTS MODERNOS ====== */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.2);
        padding: 14px 18px;
        font-size: 15px;
        background: rgba(255, 255, 255, 0.08);
        color: white;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        background: rgba(255,255,255,0.12);
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }

    .stTextInput>div>div>input::placeholder {
        color: rgba(255,255,255,0.6);
        font-weight: 400;
    }

    /* ====== BOTÃO MODERNO ====== */
    .stButton>button {
        border-radius: 12px;
        padding: 16px 28px;
        font-weight: 700;
        font-size: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 15px;
        position: relative;
        overflow: hidden;
    }

    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }

    .stButton>button:hover::before {
        left: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* ====== CREDENCIAIS ====== */
    .credenciais-container {
        background: rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 20px;
        margin: 25px auto;
        max-width: 420px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
    }

    .credenciais-title {
        font-weight: 600;
        color: white;
        margin-bottom: 15px;
        font-size: 16px;
        text-align: center;
        opacity: 0.9;
    }

    .credenciais-item {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 12px 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }

    .credenciais-item:hover {
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
    }

    /* ====== LABELS ====== */
    .stTextInput label, .stTextInput p {
        color: white !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ========== USUÁRIOS ==========
contas = (
    {'nome': 'admin', 'senha': 'admin123', 'cargo': 'ADM'},
    {'nome': 'gerente', 'senha': 'gerente123', 'cargo': 'financeiro'},
    {'nome': 'usuario', 'senha': 'user123', 'cargo': 'usuario'}
)

# ========== INTERFACE DE LOGIN ==========
st.markdown("""
<div class="login-header">
    <div class="login-logo">🏢</div>
    <div class="login-title">Sistema ERP</div>
</div>
""", unsafe_allow_html=True)

#st.markdown('<div class="login-form">', unsafe_allow_html=True)

usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")

if st.button("🚀 Entrar no Sistema", use_container_width=True):
    if not usuario or not senha:
        st.error("❌ Preencha usuário e senha!")
    else:
        login_sucesso = False
        for conta in contas:
            if conta['nome'] == usuario and conta['senha'] == senha:
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.cargo = conta['cargo']
                st.success(f"✅ Login realizado! Bem-vindo, {usuario}!")
                login_sucesso = True
                
                time.sleep(1)
                st.switch_page("./pages/1_🏠_Dashboard.py")
                break
        
        if not login_sucesso:
            st.error("❌ Usuário ou senha incorretos!")

st.markdown('</div>', unsafe_allow_html=True)

# Credenciais
st.markdown("""
<div class="credenciais-container">
    <div class="credenciais-title">🔑 Credenciais de Teste</div>
    <div class="credenciais-item">
        <strong>👑 ADMIN</strong><br>
        <code>usuário: admin | senha: admin123</code>
    </div>
    <div class="credenciais-item">
        <strong>💼 GERENTE</strong><br>
        <code>usuário: gerente | senha: gerente123</code>
    </div>
    <div class="credenciais-item">
        <strong>👤 USUÁRIO</strong><br>
        <code>usuário: usuario | senha: user123</code>
    </div>
</div>
""", unsafe_allow_html=True)