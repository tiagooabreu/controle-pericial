import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Forense Web", layout="wide", page_icon="🔬")

# --- CONEXÃO COM GOOGLE SHEETS ---
# Usa o link da planilha configurado nos Secrets do Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Leitura dos dados da aba VESTIGIOS conforme sua imagem
df = conn.read(worksheet="VESTIGIOS")

# --- LISTAS OFICIAIS (Ajuste conforme sua necessidade) ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
tipos_dispositivos = sorted(["Smartphone", "Chip", "Notebook", "Computador", "SSD", "HD", "Pen drive"])

# --- INTERFACE DO USUÁRIO ---
st.title("🔬 Sistema de Gestão - Informática Forense")

# Menu Lateral
menu = st.sidebar.radio("Navegação", ["Painel de Controle", "Cadastrar REP/Vestígio"])

if menu == "Painel de Controle":
    st.subheader("Lista de REPs e Vestígios")
    
    if df.empty:
        st.info("Nenhum registro encontrado na planilha.")
    else:
        # Exibe a tabela com as colunas da sua imagem (REP, Perito, Lacre, etc.)
        st.dataframe(df, use_container_width=True)

elif menu == "Cadastrar REP/Vestígio":
    st.subheader("Novo Cadastro")
    
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        
        with col1:
            rep = st.text_input("Número da REP (Ex: 123/2026)")
            perito = st.selectbox("Perito Responsável", peritos)
            lacre = st.text_input("Número do Lacre")
            tipo = st.selectbox("Tipo de Dispositivo", tipos_dispositivos)
        
        with col2:
            auxiliar = st.selectbox("Auxiliar", auxiliares)
            metodo = st.selectbox("Método", ["Cópia Lógica", "Cópia Física", "Extração de Nuvem"])
            ferramenta = st.text_input("Ferramenta Utilizada")
            status_relatorio = st.selectbox("Relatório", ["Pendente", "Em elaboração", "Concluído"])

        submit = st.form_submit_button("Salvar Registro")
        
        if submit:
            if rep:
                # Cria a nova linha com as colunas EXATAS da sua planilha image_3b2b41
                new_data = pd.DataFrame([{
                    "REP": rep,
                    "Perito": perito,
                    "Lacre": lacre,
                    "Tipo": tipo,
                    "Auxiliar": auxiliar,
                    "Acesso": "", # Campos que podem ser preenchidos depois
                    "Bloqueio": "",
                    "Metodo": metodo,
                    "Ferramenta": ferramenta,
                    "Extracao": "",
                    "Relatorio": status_relatorio
                }])
                
                # Junta o dado novo com o que já existe
                updated_df = pd.concat([df, new_data], ignore_index=True)
                
                # Envia de volta para a planilha
                conn.update(worksheet="VESTIGIOS", data=updated_df)
                
                st.success(f"✅ REP {rep} salva com sucesso em VESTIGIOS!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ O campo REP é obrigatório.")
