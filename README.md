# Agno IA - Agente Pessoal de Operações Financeiras

Agno IA é um assistente de inteligência artificial especializado em operações financeiras, desenvolvido para facilitar o acesso a informações sobre títulos, operações e cedentes no sistema.

## Características

- **Interface em Linguagem Natural**: Permite que usuários sem conhecimento técnico façam consultas ao banco de dados usando linguagem natural
- **Especialista em Operações Financeiras**: Focado em fornecer informações sobre títulos em aberto, operações financeiras e cedentes
- **Interface Web com Streamlit**: Interface amigável e intuitiva para interação com o agente
- **Alimentado pelo Google Gemini**: Utiliza o modelo de linguagem Gemini para processamento de linguagem natural

## Requisitos

- Python 3.12+
- PostgreSQL
- Bibliotecas Python (ver `requirements.txt`)
- Chave API do Google Gemini

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/DadosDmxCapital/AgnoIA_Agent.git
cd AgnoIA_Agent
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente no arquivo `.env`:
```
# LLM API Keys
GEMINI_API_KEY=sua_chave_api_gemini

# PostgreSQL Database Configuration
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=seu_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=seu_banco
```

## Uso

### Interface de Linha de Comando

Para iniciar o agente no terminal:

```bash
python main.py
```

### Interface Web com Streamlit

Para iniciar a interface web:

```bash
streamlit run streamlit_app.py
```

## Comandos Disponíveis

### Comandos Básicos
- `help` - Mostrar mensagem de ajuda
- `exit`, `quit` - Sair do programa
- `clear` - Limpar o histórico de conversas
- `info` - Mostrar informações sobre o agente
- `tools` - Listar ferramentas disponíveis
- `models` - Listar modelos Gemini disponíveis

### Comandos de Banco de Dados
- `listar tabelas` - Listar todas as tabelas no banco de dados
- `descrever tabela <nome>` - Descrever a estrutura de uma tabela
- `SQL: <consulta>` - Executar uma consulta SQL personalizada
- `operacoes [limite]` - Listar operações da tabela fato_operacoes
- `titulos [limite]` - Listar títulos em aberto da tabela fato_titulosabertos
- `contar operacoes` - Contar o total de registros na tabela fato_operacoes
- `contar titulos` - Contar o total de títulos em aberto
- `contar registros titulos` - Contar o total de registros na tabela fato_titulosabertos

### Consultas em Linguagem Natural
Você também pode fazer perguntas em linguagem natural sobre o banco de dados, como:
- "Quantos títulos em aberto possui o cedente X?"
- "Qual o valor total dos títulos em aberto?"
- "Quais são os 5 maiores títulos em aberto?"
- "Quantas operações foram realizadas no último mês?"

## Configuração do Repositório Git

Para configurar o repositório Git e fazer push para o GitHub:

1. Inicialize o repositório Git (se ainda não estiver inicializado):
```bash
git init
```

2. Adicione os arquivos ao repositório:
```bash
git add .
```

3. Faça o commit das alterações:
```bash
git commit -m "Commit inicial do Agno IA"
```

4. Configure o repositório remoto:
```bash
git remote add origin https://github.com/DadosDmxCapital/AgnoIA_Agent.git
```

5. Faça o push para o repositório remoto (você precisará de um token de acesso pessoal do GitHub):
```bash
git push -u origin master
```

## Licença

Este projeto é proprietário e de uso exclusivo da DMX Capital.

## Contato

Para mais informações, entre em contato com a equipe de dados da DMX Capital.
