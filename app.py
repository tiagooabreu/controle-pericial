import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Controle Forense Web", layout="wide")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Listas
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
dispositivos = sorted(["Cartão de memória", "Chip", "Computador", "HD", "Notebook", "Pen drive", "Smartphone", "SSD"])

st.title("🔬 Sistema de Gestão - Informática Forense")

aba = st.sidebar.radio("Navegação", ["Painel de Controle", "Cadastrar REP/Vestígio"])

if aba == "Painel de Controle":
    st.header("📊 REPs e Vestígios")
    try:
        # Lê os dados da aba VESTIGIOS
        df = conn.read(worksheet="VESTIGIOS")
        if not df.empty:
            f_perito = st.selectbox("Filtrar Perito", ["Todos"] + peritos)
            if f_perito != "Todos":
                df = df[df["Perito"] == f_perito]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("A planilha está vazia.")
    except Exception as e:
        st.error("Erro ao ler planilha. Verifique se o nome da aba é VESTIGIOS.")

elif aba == "Cadastrar REP/Vestígio":
    st.header("📝 Nova Entrada")
    with st.form("form_entrada"):
        c1, c2 = st.columns(2)
        rep = c1.text_input("Número da REP")
        perito_sel = c2.selectbox("Perito Responsável", peritos)
        lacre = st.text_input("Número do Lacre")
        tipo = st.selectbox("Tipo", dispositivos)
        auxiliar = st.selectbox("Auxiliar", auxiliares)
        
        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            acesso = st.radio("Acesso", ["Bloqueado", "Desbloqueado"])
            tipo_bloq = st.selectbox("Tipo de Bloqueio", ["Nenhum", "Padrão", "Senha PIN", "Alfanumérico", "Biometria"])
            metodo_desb = st.text_input("Método de Desbloqueio")
        with c4:
            ferramenta = st.selectbox("Ferramenta", ["UFED", "XRY", "Avilla", "Magnet AXIOM", "Outro"])
            tipo_ext = st.selectbox("Tipo de Extração", ["Lógica", "Sistema de Arquivos", "Física", "SmartFlow"])
            relatorio = st.selectbox("Relatório", ["P.A", "IPED", "XRY Reader", "Outro"])

        if st.form_submit_button("Salvar na Planilha"):
            # Lógica para adicionar nova linha
            nova_linha = pd.DataFrame([{
                "REP": rep, "Perito": perito_sel, "Lacre": lacre, "Tipo": tipo,
                "Auxiliar": auxiliar, "Acesso": acesso, "Bloqueio": tipo_bloq,
                "Metodo": metodo_desb, "Ferramenta": ferramenta, "Extracao": tipo_ext, "Relatorio": relatorio
            }])
            
            # Tenta ler dados existentes para concatenar
            try:
                existentes = conn.read(worksheet="VESTIGIOS")
                updated_df = pd.concat([existentes, nova_linha], ignore_index=True)
            except:
                updated_df = nova_linha
            
            # Atualiza a planilha
            conn.update(worksheet="VESTIGIOS", data=updated_df)
            st.success("Dados salvos com sucesso! Atualize a página do Dashboard.")
            st.cache_data.clear() # Limpa o cache para forçar a leitura nova
