import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Forense Web", layout="wide", page_icon="🔬")

# --- CONEXÃO COM GOOGLE SHEETS ---
# Esta função utiliza o link da planilha configurado nos Secrets do Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Leitura dos dados da aba específica
# Certifique-se de que o nome da aba na sua planilha é exatamente VESTIGIOS
df = conn.read(worksheet="VESTIGIOS")

# --- LISTAS OFICIAIS ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
dispositivos = sorted(["Smartphone", "Chip", "Cartão de memória", "Notebook", "Computador", "SSD", "HD", "Pen drive"])

# --- INTERFACE DO USUÁRIO ---
st.title("🔬 Sistema de Gestão - Informática Forense")

# Menu Lateral
menu = st.sidebar.radio("Navegação", ["Painel de Controle", "Cadastrar REP/Vestígio"])

if menu == "Painel de Controle":
    st.subheader("Lista de REPs e Vestígios")
    
    if df.empty:
        st.info("Nenhum registro encontrado na planilha.")
    else:
        st.dataframe(df, use_container_width=True)

elif menu == "Cadastrar REP/Vestígio":
    st.subheader("Novo Cadastro")
    
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        
        with col1:
            rep = st.text_input("Número da REP")
            data = st.date_input("Data do Recebimento")
            perito = st.selectbox("Perito Responsável", peritos)
        
        with col2:
            item = st.selectbox("Tipo de Dispositivo", dispositivos)
            auxiliar = st.selectbox("Auxiliar", auxiliares)
            status = st.selectbox("Status Atual", ["Pendente", "Em Análise", "Concluído"])
            
        descricao = st.text_area("Descrição do Vestígio")
        
        submit = st.form_submit_button("Salvar Registro")
        
        if submit:
            if rep and descricao:
                # Lógica para adicionar nova linha
                new_data = pd.DataFrame([{
                    "REP": rep,
                    "Data": data.strftime("%d/%m/%Y"),
                    "Dispositivo": item,
                    "Perito": perito,
                    "Auxiliar": auxiliar,
                    "Status": status,
                    "Descrição": descricao
                }])
                
                # Atualiza a planilha
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="VESTIGIOS", data=updated_df)
                st.success("✅ Registro salvo com sucesso!")
                st.balloons()
            else:
                st.error("⚠️ Por favor, preencha o número da REP e a descrição.")
