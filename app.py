import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página para ocupar a tela inteira
st.set_page_config(page_title="Controle Forense Web", layout="wide", page_icon="🔬")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTAS OFICIAIS (Ordem Alfabética) ---
peritos = sorted(["Anderson", "Cyntia Toledo", "Flaudizio Barbosa", "José de Farias", "Renato", "Wellington Melo"])
auxiliares = sorted(["Edson", "Tiago Abreu"])
dispositivos = sorted(["Smartphone", "Chip", "Cartão de memória", "Notebook", "Computador", "SSD", "HD", "Pen drive"])

st.title("🔬 Sistema de Gestão - Informática Forense")

# Menu de Navegação Lateral
aba = st.sidebar.radio("Navegação", ["📊 Painel de Controle", "📝 Cadastrar REP/Vestígio"])

if aba == "📊 Painel de Controle":
    st.header("Lista de REPs e Vestígios")
    
    try:
        # Lê os dados da planilha forçando atualização (ttl=0)
        df = conn.read(worksheet="VESTIGIOS", ttl=0)
        
        if not df.empty:
            # Filtros no topo do painel
            c1, c2 = st.columns(2)
            with c1:
                f_perito = st.selectbox("Filtrar por Perito", ["Todos"] + peritos)
            with c2:
                f_lacre = st.text_input("Buscar por Número do Lacre")

            # Aplicação dos filtros
            df_filtrado = df.copy()
            if f_perito != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Perito"] == f_perito]
            if f_lacre:
                df_filtrado = df_filtrado[df_filtrado["Lacre"].astype(str).str.contains(f_lacre, na=False)]
            
            st.dataframe(df_filtrado, use_container_width=True)
            
            if st.button("🔄 Atualizar Dados"):
                st.cache_data.clear()
                st.rerun()
        else:
            st.info("A planilha está vazia. Cadastre o primeiro vestígio na aba ao lado.")
            
    except Exception as e:
        st.error("Erro ao ler a planilha. Verifique se o nome da aba é VESTIGIOS e se os títulos estão corretos.")

elif aba == "📝 Cadastrar REP/Vestígio":
    st.header("Cadastro de Nova Entrada")
    
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            rep = st.text_input("Número da REP (Ex: 2026-INF-001)")
            perito_sel = st.selectbox("Perito Responsável", peritos)
            lacre = st.text_input("Número do Lacre")
        with col2:
            tipo = st.selectbox("Tipo de Dispositivo", dispositivos)
            auxiliar = st.selectbox("Auxiliar que realizou a ação", auxiliares)

        st.divider()
        st.subheader("⚙️ Detalhes Técnicos e Extração")
        
        col_a, col_b = st.columns(2)
        with col_a:
            acesso = st.radio("Estado de Acesso", ["Bloqueado", "Desbloqueado"], horizontal=True)
            tipo_bloq = st.selectbox("Tipo de Bloqueio", ["Nenhum", "Padrão", "Senha PIN", "Alfanumérico", "Biometria"])
            metodo_desb = st.text_input("Como foi realizado o desbloqueio? (Ex: Tentativa, UFED, XRY)")
        
        with col_b:
            ferramenta = st.selectbox("Ferramenta de Extração", ["UFED", "XRY", "Avilla", "Magnet AXIOM", "Outro"])
            tipo_ext = st.selectbox("Tipo de Extração", ["Lógica", "Sistema de Arquivos", "Física", "SmartFlow"])
            relatorio = st.selectbox("Relatório Gerado em:", ["P.A (Physical Analyzer)", "IPED", "XRY Reader", "Outro"])

        if st.form_submit_button("🚀 Salvar Registro"):
            if not rep or not lacre:
                st.warning("Por favor, preencha o número da REP e do Lacre.")
            else:
                # Cria a nova linha de dados
                nova_linha = pd.DataFrame([{
                    "REP": str(rep),
                    "Perito": perito_sel,
                    "Lacre": str(lacre),
                    "Tipo": tipo,
                    "Auxiliar": auxiliar,
                    "Acesso": acesso,
                    "Bloqueio": tipo_bloq,
                    "Metodo": metodo_desb,
                    "Ferramenta": ferramenta,
                    "Extracao": tipo_ext,
                    "Relatorio": relatorio
                }])
                
                try:
                    # Lê dados atuais
                    try:
                        existentes = conn.read(worksheet="VESTIGIOS", ttl=0)
                        df_final = pd.concat([existentes, nova_linha], ignore_index=True)
                    except:
                        df_final = nova_linha
                    
                    # Salva no Google Sheets
                    conn.update(worksheet="VESTIGIOS", data=df_final)
                    
                    st.success(f"✅ Sucesso! Lacre {lacre} (REP {rep}) salvo na planilha.")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Erro ao salvar: Verifique se a planilha está como 'Editor' para qualquer pessoa com o link. Detalhe: {e}")
