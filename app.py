import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Forense Web", layout="wide", page_icon="🔬")

# --- CONEXÃO ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Leitura dos dados - Esta é a linha 13 que deve funcionar agora
df = conn.read(worksheet="VESTIGIOS")

# --- LISTAS OFICIAIS ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
tipos_dispositivos = sorted(["Smartphone", "Chip", "Notebook", "Computador", "SSD", "HD", "Pen drive"])

# --- INTERFACE ---
st.title("🔬 Sistema de Gestão - Informática Forense")

menu = st.sidebar.radio("Navegação", ["Painel de Controle", "Cadastrar REP/Vestígio"])

if menu == "Painel de Controle":
    st.subheader("Lista de REPs e Vestígios")
    if df.empty:
        st.info("Nenhum registro encontrado.")
    else:
        st.dataframe(df, use_container_width=True)

elif menu == "Cadastrar REP/Vestígio":
    st.subheader("Novo Cadastro")
    
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        with col1:
            rep = st.text_input("Número da REP")
            perito = st.selectbox("Perito Responsável", peritos)
            lacre = st.text_input("Número do Lacre")
        with col2:
            tipo = st.selectbox("Tipo de Dispositivo", tipos_dispositivos)
            auxiliar = st.selectbox("Auxiliar", auxiliares)
            metodo = st.selectbox("Método", ["Cópia Lógica", "Cópia Física", "Extração de Nuvem"])

        submit = st.form_submit_button("Salvar Registro")
        
        if submit:
            if rep:
                # Criando nova linha conforme as colunas da sua planilha (image_3b2b41)
                new_data = pd.DataFrame([{
                    "REP": rep, "Perito": perito, "Lacre": lacre, 
                    "Tipo": tipo, "Auxiliar": auxiliar, "Acesso": "", 
                    "Bloqueio": "", "Metodo": metodo, "Ferramenta": "", 
                    "Extracao": "", "Relatorio": "Pendente"
                }])
                
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="VESTIGIOS", data=updated_df)
                st.success(f"✅ REP {rep} salva com sucesso!")
                st.rerun()
            else:
                st.error("⚠️ O campo REP é obrigatório.")
