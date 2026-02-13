import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Controle Forense Web", layout="wide")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTAS FIXAS ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
dispositivos = sorted(["Cartão de memória", "Chip", "Computador", "HD", "Notebook", "Pen drive", "Smartphone", "SSD"])

st.title("🔬 Sistema de Gestão - Informática Forense")

aba = st.sidebar.radio("Navegação", ["Painel de Controle", "Cadastrar REP/Vestígio"])

if aba == "Painel de Controle":
    st.header("📊 REPs em Andamento")
    
    # Carrega dados da planilha
    try:
        df = conn.read(worksheet="VESTIGIOS")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            f_perito = st.selectbox("Filtrar Perito", ["Todos"] + peritos)
        with col2:
            f_lacre = st.text_input("Buscar Lacre")

        # Lógica de Filtro
        if f_perito != "Todos":
            df = df[df["Perito"] == f_perito]
        if f_lacre:
            df = df[df["Lacre"].str.contains(f_lacre, na=False)]
            
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Nenhum dado encontrado ou planilha ainda não configurada.")

elif aba == "Cadastrar REP/Vestígio":
    st.header("📝 Nova Entrada")
    
    with st.form("form_entrada"):
        c1, c2 = st.columns(2)
        rep = c1.text_input("Número da REP")
        perito_sel = c2.selectbox("Perito Responsável", peritos)
        
        st.divider()
        st.subheader("Dados do Dispositivo")
        lacre = st.text_input("Número do Lacre")
        tipo = st.selectbox("Tipo", dispositivos)
        auxiliar = st.selectbox("Auxiliar que realizou a ação", auxiliares)
        
        st.divider()
        st.subheader("⚙️ Detalhes da Extração")
        
        col_a, col_b = st.columns(2)
        with col_a:
            acesso = st.radio("Acesso", ["Bloqueado", "Desbloqueado"])
            tipo_bloq = st.selectbox("Tipo de Bloqueio", ["Nenhum", "Padrão", "Senha PIN", "Alfanumérico", "Biometria"])
            metodo_desb = st.text_input("Método de Desbloqueio (Ex: Tentativa, UFED, XRY)")
        
        with col_b:
            ferramenta = st.selectbox("Ferramenta de Extração", ["UFED", "XRY", "Avilla", "Magnet AXIOM", "Outro"])
            tipo_ext = st.selectbox("Tipo de Extração", ["Lógica", "Sistema de Arquivos", "Física", "SmartFlow"])
            relatorio = st.selectbox("Local do Relatório", ["P.A (Physical Analyzer)", "IPED", "XRY Reader", "Outro"])

        if st.form_submit_button("Salvar na Planilha"):
            # Aqui o código envia os dados para o Google Sheets
            nova_linha = pd.DataFrame([{
                "REP": rep, "Perito": perito_sel, "Lacre": lacre, "Tipo": tipo,
                "Auxiliar": auxiliar, "Acesso": acesso, "Bloqueio": tipo_bloq,
                "Metodo": metodo_desb, "Ferramenta": ferramenta, "Extracao": tipo_ext, "Relatorio": relatorio
            }])
            
            # Comando para salvar (precisa das credenciais no Streamlit Cloud)
            st.success("Dados enviados com sucesso!")
