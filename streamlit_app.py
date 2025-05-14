"""
Aplicação Streamlit para o Agno IA - Seu agente pessoal de operações financeiras.
Esta aplicação fornece uma interface web para interagir com o agente Agno.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
from datetime import datetime
import base64

# Importar o agente
from agent import AgnoAgent

# Configurações da página
st.set_page_config(
    page_title="Agno IA - Seu Agente Pessoal de Operações",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para gerar um logo mais profissional em base64
def get_logo_base64():
    # Código SVG para um logo financeiro profissional
    svg_code = '''
    <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <!-- Fundo circular com gradiente -->
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#1E40AF;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1" />
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.3"/>
            </filter>
        </defs>

        <!-- Círculo de fundo -->
        <circle cx="60" cy="60" r="56" fill="url(#grad1)" filter="url(#shadow)" />

        <!-- Símbolo de gráfico financeiro -->
        <polyline points="30,80 45,60 60,70 75,50 90,40"
                 stroke="white" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" />

        <!-- Símbolo de moeda/cifrão estilizado -->
        <path d="M60,30 C55,30 50,32 50,38 C50,44 55,46 60,46 C65,46 70,48 70,54 C70,60 65,62 60,62 M60,26 L60,66"
              stroke="white" stroke-width="4" fill="none" stroke-linecap="round" />

        <!-- Texto "AGNO" -->
        <text x="60" y="90" font-family="Arial, sans-serif" font-size="16" font-weight="bold"
              text-anchor="middle" fill="white" letter-spacing="1">AGNO</text>
    </svg>
    '''

    # Converter SVG para base64
    svg_bytes = svg_code.encode('utf-8')
    b64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

# Função para carregar CSS personalizado
def load_css():
    st.markdown("""
    <style>
    /* Cores principais */
    :root {
        --primary-color: #1E3A8A;
        --primary-light: #3B82F6;
        --primary-dark: #1E40AF;
        --secondary-color: #10B981;
        --secondary-light: #D1FAE5;
        --secondary-dark: #065F46;
        --neutral-50: #F9FAFB;
        --neutral-100: #F3F4F6;
        --neutral-200: #E5E7EB;
        --neutral-300: #D1D5DB;
        --neutral-600: #4B5563;
        --neutral-700: #374151;
        --neutral-800: #1F2937;
        --neutral-900: #111827;
        --danger: #EF4444;
        --warning: #F59E0B;
        --success: #10B981;

        /* Cores de texto e fundo para melhor legibilidade */
        --text-dark: #111827;
        --text-light: #F9FAFB;
        --bg-user-message: #EBF5FF;
        --bg-assistant-message: #F0FFF4;
        --border-user: #2563EB;
        --border-assistant: #059669;
    }

    /* Estilos globais */
    .main {
        background-color: var(--neutral-100);
        color: var(--neutral-800);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Cabeçalho */
    .header-container {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        color: white;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .header-logo {
        width: 70px;
        height: 70px;
        filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.2));
    }

    .header-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
        letter-spacing: -0.5px;
    }

    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.25rem 0 0 0;
        padding: 0;
    }

    .finance-badge {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 0.35rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.8rem;
        margin-top: 0.75rem;
        display: inline-block;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Container de chat */
    .chat-container {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        height: 65vh;
        overflow-y: auto;
        margin-bottom: 1.5rem;
        border: 1px solid var(--neutral-200);
    }

    /* Mensagens de chat */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 1.25rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        font-size: 1rem;
    }

    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .chat-message.user {
        background-color: var(--bg-user-message);
        border-left: 5px solid var(--border-user);
        margin-left: 2rem;
        margin-right: 0.5rem;
    }

    .chat-message.assistant {
        background-color: var(--bg-assistant-message);
        border-left: 5px solid var(--border-assistant);
        margin-right: 2rem;
        margin-left: 0.5rem;
    }

    .chat-message .avatar {
        min-width: 48px;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .chat-message .user-avatar {
        background-color: var(--border-user);
    }

    .chat-message .assistant-avatar {
        background-color: var(--border-assistant);
    }

    .chat-message .content {
        flex-grow: 1;
        overflow-x: auto;
        color: var(--text-dark);
        line-height: 1.6;
        font-size: 1.05rem;
    }

    .chat-message .content p {
        margin-bottom: 1rem;
    }

    .chat-message .content p:last-child {
        margin-bottom: 0;
    }

    .chat-message .content pre {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #1E293B;
        color: #E2E8F0;
        overflow-x: auto;
        border: 1px solid var(--neutral-700);
        margin: 1rem 0;
        font-size: 0.95rem;
    }

    .chat-message .content code {
        font-size: 0.95rem;
        font-family: 'Consolas', 'Monaco', monospace;
    }

    /* Cabeçalho de mensagem */
    .message-header {
        font-weight: 700;
        font-size: 1rem;
        color: var(--primary-dark);
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--neutral-200);
    }

    .message-body {
        line-height: 1.6;
    }

    /* Área de entrada */
    .chat-input {
        background-color: white;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--neutral-200);
    }

    /* Botões */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton button:hover {
        background-color: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar e estatísticas */
    .sidebar-content {
        padding: 1.25rem;
    }

    .sidebar-header {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1.25rem;
        color: var(--primary-dark);
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-light);
    }

    .sidebar-section {
        margin-bottom: 2rem;
    }

    .sidebar-section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--primary-color);
    }

    .financial-stats {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .financial-stat {
        background-color: white;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--neutral-200);
        transition: transform 0.2s ease;
    }

    .financial-stat:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .financial-stat-title {
        font-size: 0.9rem;
        color: var(--neutral-600);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }

    .financial-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-dark);
    }

    /* Caixa de informações */
    .info-box {
        background-color: #EFF6FF;
        border-left: 4px solid var(--primary-color);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .info-box-title {
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: var(--primary-dark);
        font-size: 1.2rem;
    }

    .info-box p {
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
        color: var(--text-dark);
    }

    /* Tabelas */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.25rem 0;
        font-size: 1rem;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    th {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
        text-align: left;
        padding: 1rem 1.25rem;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }

    td {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--neutral-200);
        color: var(--text-dark);
    }

    tr:nth-child(even) {
        background-color: var(--neutral-50);
    }

    tr:nth-child(odd) {
        background-color: white;
    }

    tr:hover {
        background-color: var(--neutral-100);
    }

    /* Tabela dentro de mensagens */
    .chat-message .content table {
        margin: 1.25rem 0;
        font-size: 0.95rem;
    }

    .chat-message .content th {
        padding: 0.9rem 1.1rem;
        font-size: 0.85rem;
    }

    .chat-message .content td {
        padding: 0.9rem 1.1rem;
    }

    /* Container de tabela */
    .table-container {
        margin: 1.5rem 0;
        overflow-x: auto;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--neutral-200);
        background-color: white;
    }

    .table-cell {
        padding: 0.25rem;
        display: inline-block;
    }

    /* Blocos de código */
    .code-block {
        margin: 1.25rem 0;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        border: 1px solid var(--neutral-700);
    }

    .code-header {
        background-color: var(--primary-dark);
        color: white;
        padding: 0.75rem 1.25rem;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .code-block pre {
        margin: 0;
        padding: 1.25rem;
        background-color: #1E293B;
        color: #E2E8F0;
        overflow-x: auto;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .code-block code {
        font-family: 'Consolas', 'Monaco', monospace;
    }

    /* Formatação de SQL */
    .sql-keyword {
        color: #93C5FD;
        font-weight: bold;
    }

    .sql-function {
        color: #C4B5FD;
    }

    .sql-table {
        color: #FCA5A5;
    }

    .sql-column {
        color: #A5F3FC;
    }

    /* Ajustes para elementos Streamlit */
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
        border: 1px solid var(--neutral-300);
        padding: 0.75rem 1rem;
        font-size: 1.05rem;
    }

    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 1px solid var(--neutral-300);
        padding: 0.75rem 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.05rem;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    /* Melhorar legibilidade de texto em geral */
    p, li, div {
        color: var(--text-dark);
    }

    /* Melhorar contraste de links */
    a {
        color: var(--primary-color);
        font-weight: 500;
        text-decoration: underline;
    }

    a:hover {
        color: var(--primary-dark);
    }

    /* Lista de consultas populares */
    .query-list {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }

    .query-list li {
        margin-bottom: 0.85rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        background-color: white;
        border: 1px solid var(--neutral-200);
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        line-height: 1.5;
    }

    .query-list li:hover {
        transform: translateX(5px);
        border-left: 3px solid var(--primary-color);
        background-color: var(--neutral-50);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .query-tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 0.5rem;
        background-color: var(--primary-color);
        color: white;
        letter-spacing: 0.5px;
    }

    /* Caixa Sobre */
    .about-box {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.25rem;
        border: 1px solid var(--neutral-200);
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .about-box p {
        margin-bottom: 1rem;
    }

    .about-box p strong {
        color: var(--primary-dark);
    }

    .version-info {
        margin-top: 1.25rem;
        font-size: 0.85rem;
        color: var(--neutral-600);
        text-align: right;
        font-style: italic;
        border-top: 1px solid var(--neutral-200);
        padding-top: 0.75rem;
    }

    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--neutral-100);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-light);
        border-radius: 5px;
        border: 2px solid var(--neutral-100);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }

    /* Melhorias para visualização de dados */
    .dataframe {
        font-size: 1rem !important;
    }

    .dataframe th {
        background-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 600 !important;
    }

    .dataframe td {
        font-size: 0.95rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar o agente
@st.cache_resource
def get_agent():
    return AgnoAgent()

# Função para exibir mensagens de chat
def display_chat_message(role, content):
    # Formatar tabelas para melhor visualização
    if "|" in content and "---" in content:
        # Detectar tabelas markdown e adicionar classes para estilização
        content = content.replace("<table>", '<table class="styled-table">')

        # Melhorar a formatação de tabelas markdown
        lines = content.split('\n')
        formatted_lines = []
        in_table = False

        for line in lines:
            if '|' in line:
                if not in_table:
                    in_table = True
                    formatted_lines.append('<div class="table-container">')

                # Formatar cabeçalhos de tabela
                if '---' in line:
                    formatted_lines.append(line)
                else:
                    # Adicionar classes para células
                    cells = line.split('|')
                    formatted_cells = []
                    for cell in cells:
                        if cell.strip():
                            formatted_cells.append(f'<span class="table-cell">{cell.strip()}</span>')
                        else:
                            formatted_cells.append('')
                    formatted_lines.append('|'.join(formatted_cells))
            else:
                if in_table:
                    in_table = False
                    formatted_lines.append('</div>')
                formatted_lines.append(line)

        if in_table:
            formatted_lines.append('</div>')

        content = '\n'.join(formatted_lines)

    # Formatar código SQL para melhor visualização
    if "```sql" in content.lower():
        # Substituir blocos de código SQL por versões estilizadas com highlight
        parts = content.split("```sql")
        for i in range(1, len(parts)):
            if "```" in parts[i]:
                code, rest = parts[i].split("```", 1)
                # Aplicar highlight para palavras-chave SQL
                code = code.replace("SELECT", '<span class="sql-keyword">SELECT</span>')
                code = code.replace("FROM", '<span class="sql-keyword">FROM</span>')
                code = code.replace("WHERE", '<span class="sql-keyword">WHERE</span>')
                code = code.replace("ORDER BY", '<span class="sql-keyword">ORDER BY</span>')
                code = code.replace("GROUP BY", '<span class="sql-keyword">GROUP BY</span>')
                code = code.replace("LIMIT", '<span class="sql-keyword">LIMIT</span>')
                code = code.replace("JOIN", '<span class="sql-keyword">JOIN</span>')
                code = code.replace("COUNT", '<span class="sql-function">COUNT</span>')
                code = code.replace("SUM", '<span class="sql-function">SUM</span>')
                code = code.replace("AVG", '<span class="sql-function">AVG</span>')
                code = code.replace("MAX", '<span class="sql-function">MAX</span>')
                code = code.replace("MIN", '<span class="sql-function">MIN</span>')

                # Destacar tabelas
                code = code.replace("fato_operacoes", '<span class="sql-table">fato_operacoes</span>')
                code = code.replace("fato_titulosabertos", '<span class="sql-table">fato_titulosabertos</span>')

                parts[i] = f'<div class="code-block"><div class="code-header">SQL</div><pre><code>{code}</code></pre></div>{rest}'

        content = "```sql".join(parts)

    # Formatar outros blocos de código
    if "```" in content:
        # Substituir blocos de código por versões estilizadas
        parts = content.split("```")
        for i in range(1, len(parts), 2):
            if i < len(parts):
                # Verificar se há especificação de linguagem
                code_lines = parts[i].strip().split("\n")
                lang = ""
                code_content = parts[i]

                if len(code_lines) > 0 and not code_lines[0].startswith(" "):
                    lang = code_lines[0]
                    code_content = "\n".join(code_lines[1:])

                # Substituir o bloco de código por uma versão estilizada
                parts[i] = f'<div class="code-block"><div class="code-header">{lang}</div><pre><code>{code_content}</code></pre></div>'

        content = "".join(parts)

    # Definir ícones e classes com base no papel (usuário ou assistente)
    if role == "user":
        avatar = "👤"
        avatar_class = "user-avatar"
        message_class = "user"
        role_label = "Você"
    else:
        avatar = "💼"  # Ícone financeiro para o assistente
        avatar_class = "assistant-avatar"
        message_class = "assistant"
        role_label = "Agno IA"

    # Renderizar a mensagem com cabeçalho de papel
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar {avatar_class}">{avatar}</div>
        <div class="content">
            <div class="message-header">{role_label}</div>
            <div class="message-body">{content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Função para processar a consulta do usuário
def process_user_query(agent, query):
    with st.spinner("Agno está pensando..."):
        response = agent.process_query(query)
    return response

# Função para exibir estatísticas financeiras
def display_financial_stats(agent):
    try:
        # Obter contagem de títulos em aberto
        titulos_abertos = agent.process_natural_language_query("Quantos títulos em aberto existem no total?")
        # Extrair apenas o número da resposta
        import re
        titulos_abertos_num = re.search(r'(\d+[\.,]?\d*)', titulos_abertos)
        titulos_abertos_num = titulos_abertos_num.group(1) if titulos_abertos_num else "N/A"

        # Criar colunas para estatísticas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="financial-stat">
                <div class="financial-stat-title">Títulos em Aberto</div>
                <div class="financial-stat-value">{}</div>
            </div>
            """.format(titulos_abertos_num), unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="financial-stat">
                <div class="financial-stat-title">Data Atual</div>
                <div class="financial-stat-value">{}</div>
            </div>
            """.format(datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="financial-stat">
                <div class="financial-stat-title">Status do Sistema</div>
                <div class="financial-stat-value">Online</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {str(e)}")

# Função principal
def main():
    # Carregar CSS
    load_css()

    # Inicializar o agente
    agent = get_agent()

    # Inicializar o histórico de chat se não existir
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Obter o logo em base64
    logo_base64 = get_logo_base64()

    # Remover o menu padrão do Streamlit e o rodapé
    hide_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)

    # Cabeçalho
    st.markdown(f"""
    <div class="header-container">
        <img src="{logo_base64}" class="header-logo" alt="Agno IA Logo"/>
        <div>
            <h1 class="header-title">Agno IA</h1>
            <p class="header-subtitle">Seu agente pessoal de operações financeiras</p>
            <span class="finance-badge">Especialista em Operações</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Layout principal com duas colunas
    col1, col2 = st.columns([3, 1])

    with col1:
        # Área de chat
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">Assistente Financeiro</div>
            <p>Olá! Sou o Agno IA, seu assistente especializado em operações financeiras.</p>
            <p>Posso ajudar com consultas sobre títulos em aberto, operações financeiras e muito mais, usando linguagem natural.</p>
            <p><strong>Experimente perguntar:</strong> "Quantos títulos em aberto temos?" ou "Qual o valor total dos títulos do cedente X?"</p>
        </div>
        """, unsafe_allow_html=True)

        # Container para o chat
        st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

        # Exibir histórico de chat
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                display_chat_message(message["role"], message["content"])
        else:
            # Mensagem quando não há histórico
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: var(--neutral-600);">
                <div style="font-size: 2rem; margin-bottom: 1rem;">💬</div>
                <p>Faça sua primeira pergunta sobre operações financeiras!</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Input do usuário
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area("Digite sua consulta financeira:",
                                      placeholder="Ex: Quantos títulos em aberto temos? Quais são os maiores títulos?",
                                      height=80,
                                      key="user_input")

            cols = st.columns([1, 1, 6])
            with cols[0]:
                submit_button = st.form_submit_button("💬 Enviar")
            with cols[1]:
                clear_button = st.form_submit_button("🗑️ Limpar")

        if submit_button and user_input:
            # Adicionar mensagem do usuário ao histórico
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Processar a consulta
            with st.spinner("Agno está analisando sua consulta financeira..."):
                response = process_user_query(agent, user_input)

            # Adicionar resposta do assistente ao histórico
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Recarregar a página para exibir as novas mensagens
            st.rerun()

        if clear_button:
            st.session_state.chat_history = []
            agent.clear_conversation_history()
            st.rerun()

    with col2:
        # Sidebar com informações e estatísticas
        st.markdown('<div class="sidebar-header">Painel Financeiro</div>', unsafe_allow_html=True)

        # Exibir estatísticas financeiras
        st.markdown('<div class="sidebar-section-title">Estatísticas Atuais</div>', unsafe_allow_html=True)
        display_financial_stats(agent)

        # Comandos úteis
        st.markdown('<div class="sidebar-section-title">Consultas Populares</div>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="query-list">
            <li><span class="query-tag">Básico</span> Quantos títulos em aberto temos?</li>
            <li><span class="query-tag">Análise</span> Quais são os 5 maiores títulos?</li>
            <li><span class="query-tag">Cedente</span> Títulos do cedente ACME LTDA</li>
            <li><span class="query-tag">Valor</span> Valor total dos títulos em aberto</li>
            <li><span class="query-tag">Prazo</span> Títulos com vencimento este mês</li>
            <li><span class="query-tag">Técnico</span> Listar tabelas disponíveis</li>
        </ul>
        """, unsafe_allow_html=True)

        # Sobre o Agno IA
        st.markdown('<div class="sidebar-section-title">Sobre o Agno IA</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-box">
            <p>O <strong>Agno IA</strong> é um assistente especializado em operações financeiras,
            desenvolvido para facilitar o acesso a informações sobre títulos,
            operações e cedentes no sistema.</p>

            <p>Utilize linguagem natural para fazer suas consultas, sem necessidade
            de conhecimento técnico em banco de dados.</p>

            <p>Powered by <strong>Google Gemini</strong> 🧠</p>

            <div class="version-info">Versão 1.0</div>
        </div>
        """, unsafe_allow_html=True)

        # Botão para limpar o histórico
        if st.button("🗑️ Limpar Histórico de Conversa"):
            st.session_state.chat_history = []
            agent.clear_conversation_history()
            st.rerun()

if __name__ == "__main__":
    main()
