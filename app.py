import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(page_title="Controle Forense v1.0", layout="wide")

# --- BANCO DE DATOS SIMPLIFICADO (Arquivos CSV) ---
def carregar_dados(arquivo, colunas):
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=colunas)

# Inicialização das listas e dados
reps_df = carregar_dados('reps.csv', ['id_rep', 'perito', 'data_entrada', 'status_geral'])
vestigios_df = carregar_dados('vestigios.csv', [
    'id_rep', 'lacre', 'tipo_dispositivo', 'auxiliar', 'status',
    'bloqueio_inicial', 'tipo_bloqueio', 'metodo_desbloqueio', 
    'ferramenta_extracao', 'tipo_extracao', 'local_relatorio'
])

# --- LISTAS INICIAIS ---
peritos_init = sorted(["Flaudizio Barbosa", "Cyntia Toledo", "Wellington Melo", "Renato", "Anderson", "José de Farias"])
auxiliares_init = sorted(["Tiago Abreu", "Edson"])
dispositivos_init = sorted(["smartphone", "chip", "cartão de memória", "notebook", "computador", "SSD", "HD", "pen drive"])

# --- INTERFACE ---
st.title("🔬 Sistema de Controle - Informática Forense")

menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Cadastrar REP/Vestígio", "Configurações"])

if menu == "Dashboard":
    st.header("📊 Painel de Controle")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        f_perito = st.selectbox("Filtrar por Perito", ["Todos"] + peritos_init)
    with col2:
        f_status = st.selectbox("Filtrar por Status", ["Todos", "Pendente", "Em Extração", "Concluído"])

    # Exibição da Tabela (Lógica de Filtro)
    df_display = vestigios_df.copy()
    if f_perito != "Todos":
        # Cruza com a tabela de REPs para saber o perito
        reps_do_perito = reps_df[reps_df['perito'] == f_perito]['id_rep']
        df_display = df_display[df_display['id_rep'].isin(reps_do_perito)]
    
    st.dataframe(df_display, use_container_width=True)

elif menu == "Cadastrar REP/Vestígio":
    st.header("📝 Entrada de Material")
    
    with st.form("form_rep"):
        c1, c2 = st.columns(2)
        rep_num = c1.text_input("Número da REP")
        perito_sel = c2.selectbox("Perito Designado", peritos_init)
        
        st.divider()
        st.subheader("Dados do Vestígio (Lacre)")
        lacre_num = st.text_input("Número do Lacre")
        tipo_disp = st.selectbox("Tipo de Dispositivo", dispositivos_init)
        aux_sel = st.selectbox("Auxiliar Responsável", auxiliares_init)
        
        st.divider()
        st.subheader("📋 Detalhes Técnicos (Ações do Auxiliar)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            bloqueio = st.radio("Aparelho Bloqueado?", ["Sim", "Não"])
            tipo_bloq = st.selectbox("Tipo de Bloqueio", ["Nenhum", "Padrão", "Senha PIN", "Alfanumérico", "Biometria"])
            metodo_desb = st.text_input("Como foi realizado o desbloqueio? (Tentativa, UFED, XRY...)")
        
        with col_b:
            ferramenta = st.selectbox("Onde foi realizada a extração?", ["UFED", "XRY", "Avilla", "Magnet AXIOM", "Outro"])
            tipo_ext = st.selectbox("Tipo de Extração", ["Lógica", "Sistema de Arquivos", "Física", "SmartFlow"])
            relatorio = st.selectbox("Relatório gerado onde?", ["P.A (Physical Analyzer)", "IPED", "XRY Reader", "Outro"])

        if st.form_submit_button("Salvar Cadastro"):
            # Lógica para salvar nos CSVs (Simplificada para o exemplo)
            st.success(f"REP {rep_num} e Lacre {lacre_num} cadastrados com sucesso!")

elif menu == "Configurações":
    st.header("⚙️ Gerenciar Listas")
    st.info("Aqui você poderá adicionar novos peritos, auxiliares e tipos de dispositivos futuramente.")
    # Implementação de adição de novas linhas nas listas
