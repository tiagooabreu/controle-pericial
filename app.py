import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Forense Web", layout="wide", page_icon="🔬")

# Conexão com Google Sheets usando Service Account (Secrets)
# Versão simplificada que funciona com o link público
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTAS OFICIAIS ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
dispositivos = sorted(["Smartphone", "Chip", "Cartão de memória", "Notebook", "Computador", "SSD", "HD", "Pen drive"])

st.title("🔬 Sistema de Gestão - Informática Forense")

aba = st.sidebar.radio("Navegação", ["📊 Painel de Controle", "📝 Cadastrar REP/Vestígio"])

if aba == "📊 Painel de Controle":
    st.header("Lista de REPs e Vestígios")
    
    try:
        # ttl=0 força o sistema a buscar dados novos sempre
        df = conn.read(worksheet="VESTIGIOS")
        
        if df is not None and not df.empty:
            # Filtros
            c1, c2 = st.columns(2)
            with c1:
                f_perito = st.selectbox("Filtrar por Perito", ["Todos"] + peritos)
            with c2:
                f_lacre = st.text_input("Buscar por Lacre")

            df_filtrado = df.copy()
            if f_perito != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Perito"] == f_perito]
            if f_lacre:
                df_filtrado = df_filtrado[df_filtrado["Lacre"].astype(str).str.contains(f_lacre, na=False)]
            
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.info("A planilha está vazia ou a aba VESTIGIOS não foi encontrada.")
            
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        st.warning("Verifique se você compartilhou a planilha com o e-mail da conta de serviço como EDITOR.")

elif aba == "📝 Cadastrar REP/Vestígio":
    st.header("Cadastro de Nova Entrada")
    
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            rep = st.text_input("Número da REP")
            perito_sel = st.selectbox("Perito Responsável", peritos)
            lacre = st.text_input("Número do Lacre")
        with col2:
            tipo = st.selectbox("Tipo de Dispositivo", dispositivos)
            auxiliar = st.selectbox("Auxiliar", auxiliares)

        st.divider()
        st.subheader("⚙️ Detalhes Técnicos")
        
        c3, c4 = st.columns(2)
        with c3:
            acesso = st.radio("Estado de Acesso", ["Bloqueado", "Desbloqueado"], horizontal=True)
            tipo_bloq = st.selectbox("Tipo de Bloqueio", ["Nenhum", "Padrão", "Senha PIN", "Alfanumérico", "Biometria"])
            metodo_desb = st.text_input("Método de Desbloqueio")
        with c4:
            ferramenta = st.selectbox("Ferramenta", ["UFED", "XRY", "Avilla", "Magnet AXIOM", "Outro"])
            tipo_ext = st.selectbox("Tipo de Extração", ["Lógica", "Sistema de Arquivos", "Física", "SmartFlow"])
            relatorio = st.selectbox("Relatório em:", ["P.A", "IPED", "XRY Reader", "Outro"])

        if st.form_submit_button("🚀 Salvar Registro"):
            if not rep or not lacre:
                st.error("Preencha REP e Lacre!")
            else:
                nova_linha = pd.DataFrame([{
                    "REP": str(rep), "Perito": perito_sel, "Lacre": str(lacre), "Tipo": tipo,
                    "Auxiliar": auxiliar, "Acesso": acesso, "Bloqueio": tipo_bloq,
                    "Metodo": metodo_desb, "Ferramenta": ferramenta, "Extracao": tipo_ext, "Relatorio": relatorio
                }])
                
                try:
                    # Tenta ler e concatenar
                    try:
                        existentes = conn.read(worksheet="VESTIGIOS", ttl=0)
                        df_final = pd.concat([existentes, nova_linha], ignore_index=True)
                    except:
                        df_final = nova_linha
                    
                    # Salva
                    conn.update(worksheet="VESTIGIOS", data=df_final)
                    st.success("✅ Salvo com sucesso!")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
