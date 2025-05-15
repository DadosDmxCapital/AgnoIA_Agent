"""
Agno AI Agent implementation.
This module defines the core Agent class that orchestrates tools and interactions.
"""

import time
from typing import Dict, Any, List, Optional, Callable

import config
from tools import GroqTool, PostgresTool

class AgnoAgent:
    """
    Agno AI Agent - A modular AI agent that can use various tools.
    """

    def __init__(self, name: str = config.AGENT_NAME):
        """
        Initialize the Agno agent.

        Args:
            name: Name of the agent
        """
        self.name = name
        self.version = config.AGENT_VERSION
        self.tools = {}
        self.conversation_history = []

        # Initialize default tools
        self._initialize_default_tools()

    def _initialize_default_tools(self):
        """Initialize the default set of tools."""
        # Add Groq as a default tool
        self.add_tool("groq", GroqTool())

        # Add PostgreSQL as a default tool
        self.add_tool("postgres", PostgresTool())

    def add_tool(self, tool_name: str, tool_instance: Any):
        """
        Add a tool to the agent.

        Args:
            tool_name: Name of the tool
            tool_instance: Instance of the tool
        """
        self.tools[tool_name] = tool_instance
        print(f"Tool '{tool_name}' added to {self.name} agent.")

    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the agent.

        Args:
            tool_name: Name of the tool to remove

        Returns:
            True if the tool was removed, False otherwise
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            print(f"Tool '{tool_name}' removed from {self.name} agent.")
            return True
        return False

    def list_tools(self) -> List[str]:
        """
        List all available tools.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def query_database(self, sql_query: str) -> str:
        """
        Execute a SQL query on the PostgreSQL database.

        Args:
            sql_query: SQL query to execute

        Returns:
            Results of the query as a formatted string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Execute the query
            success, result = postgres_tool.execute_query(sql_query)

            if success:
                if isinstance(result, list):
                    # Format the results as a markdown table
                    return postgres_tool.format_results_as_markdown(result)
                else:
                    # Return the success message
                    return result
            else:
                # Return the error message
                return f"Erro ao executar consulta: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível. Por favor, adicione-a usando add_tool('postgres', PostgresTool())."

    def list_database_tables(self) -> str:
        """
        List all tables in the PostgreSQL database.

        Returns:
            List of tables as a formatted string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Get the list of tables
            success, tables = postgres_tool.list_tables()

            if success:
                if tables:
                    return "Tabelas disponíveis no banco de dados:\n- " + "\n- ".join(tables)
                else:
                    return "Nenhuma tabela encontrada no banco de dados."
            else:
                return f"Erro ao listar tabelas: {tables}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível. Por favor, adicione-a usando add_tool('postgres', PostgresTool())."

    def describe_database_table(self, table_name: str) -> str:
        """
        Describe a table's structure in the PostgreSQL database.

        Args:
            table_name: Name of the table to describe

        Returns:
            Table structure as a formatted string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Describe the table
            success, columns = postgres_tool.describe_table(table_name)

            if success:
                if columns:
                    return postgres_tool.format_results_as_markdown(columns)
                else:
                    return f"Tabela '{table_name}' não encontrada ou não possui colunas."
            else:
                return f"Erro ao descrever tabela: {columns}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível. Por favor, adicione-a usando add_tool('postgres', PostgresTool())."

    def get_operacoes(self, limit: int = 10) -> str:
        """
        Get operations from fato_operacoes table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Formatted results as a string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Get operations
            success, result = postgres_tool.get_operacoes(limit)

            if success:
                if result:
                    return postgres_tool.format_results_as_markdown(result)
                else:
                    return "Nenhuma operação encontrada."
            else:
                return f"Erro ao buscar operações: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível."

    def get_titulos_abertos(self, limit: int = 10) -> str:
        """
        Get open titles from fato_titulosabertos table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Formatted results as a string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Get open titles
            success, result = postgres_tool.get_titulos_abertos(limit)

            if success:
                if result:
                    return postgres_tool.format_results_as_markdown(result)
                else:
                    return "Nenhum título em aberto encontrado."
            else:
                return f"Erro ao buscar títulos em aberto: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível."

    def count_table_records(self, table_name: str) -> str:
        """
        Count records in a table.

        Args:
            table_name: Name of the table to count records from

        Returns:
            Formatted count result as a string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Count records
            success, result = postgres_tool.count_records(table_name)

            if success:
                if result and len(result) > 0:
                    total = result[0].get("total_records", 0)
                    return f"A tabela {table_name} contém {total} registros no total."
                else:
                    return f"Não foi possível contar os registros na tabela {table_name}."
            else:
                return f"Erro ao contar registros: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível."

    def count_titulos_abertos(self) -> str:
        """
        Count open titles with specific criteria.

        Returns:
            Formatted count result as a string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Count open titles
            success, result = postgres_tool.count_titulos_abertos()

            if success:
                if result and len(result) > 0:
                    total = result[0].get("total_titulos_abertos", 0)
                    return f"Existem {total} títulos em aberto no total."
                else:
                    return "Não foi possível contar os títulos em aberto."
            else:
                return f"Erro ao contar títulos em aberto: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível."

    def get_cedentes_info(self, limit: int = 10) -> str:
        """
        Get cedentes information from dimcedentesconsolidado table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Formatted results as a string
        """
        if "postgres" in self.tools:
            postgres_tool = self.tools["postgres"]

            # Get cedentes information
            success, result = postgres_tool.get_cedentes_info(limit)

            if success:
                if result:
                    return postgres_tool.format_results_as_markdown(result)
                else:
                    return "Nenhuma informação de cedente encontrada."
            else:
                return f"Erro ao buscar informações de cedentes: {result}"
        else:
            return "Erro: Ferramenta PostgreSQL não disponível."

    def process_natural_language_query(self, query: str) -> str:
        """
        Process a natural language query about the database.

        This function takes a query in natural language (like "Quantos títulos em aberto possui o cedente X?"),
        interprets it using the Groq LLM, converts it to SQL, and returns the results.

        Args:
            query: Natural language query about the database

        Returns:
            Response with the query results
        """
        if "groq" not in self.tools:
            return "Erro: Ferramenta Groq não disponível. Necessária para processar consultas em linguagem natural."

        if "postgres" not in self.tools:
            return "Erro: Ferramenta PostgreSQL não disponível. Necessária para executar consultas ao banco de dados."

        # Get database schema information to help the model
        tables_info = self.list_database_tables()
        fato_operacoes_schema = self.describe_database_table("fato_operacoes")
        fato_titulosabertos_schema = self.describe_database_table("fato_titulosabertos")
        dimcedentesconsolidado_schema = self.describe_database_table("dimcedentesconsolidado")

        # Create a system prompt with database information
        system_prompt = f"""Você é um especialista em SQL que converte perguntas em linguagem natural para consultas SQL.

        INFORMAÇÕES DO BANCO DE DADOS:
        {tables_info}

        ESQUEMA DA TABELA fato_operacoes:
        {fato_operacoes_schema}

        ESQUEMA DA TABELA fato_titulosabertos:
        {fato_titulosabertos_schema}

        ESQUEMA DA TABELA dimcedentesconsolidado:
        {dimcedentesconsolidado_schema}

        REGRAS SEMÂNTICAS IMPORTANTES:

        1. Sempre que for solicitada a "soma dos valores da operação", use o campo `valor_bruto` da tabela `fato_operacoes`.
        2. A coluna `desagio` representa o desconto aplicado ao valor da operação ou título.
        3. A coluna `situacao` da tabela de títulos representa o status atual (ex: em aberto, pago, vencido).
        4. O "operador" é o responsável pela carteira de operações, enquanto o "gerente" é o comercial responsável por um grupo de cedentes.
        5. Todos os campos que começam com `valor_` referem-se a valores financeiros.
        6. `sacado` é quem deve pagar o título, ou seja, o cliente do cedente.
        7. `cedente` é quem detém o título ou a operação (quem vende o título ou crédito).
        8. A tabela `dimcedentesconsolidado` contém dados cadastrais dos cedentes, como nome, endereço, contatos e limites de crédito.

        EXEMPLOS DE CONVERSÃO:

        Pergunta: "Quantos títulos em aberto existem no total?"
        SQL: SELECT COUNT(*) as total FROM fato_titulosabertos

        Pergunta: "Quantos títulos em aberto possui o cedente ACME LTDA?"
        SQL: SELECT COUNT(*) as total FROM fato_titulosabertos WHERE cedente = 'ACME LTDA'

        Pergunta: "Qual o valor total dos títulos em aberto do cedente XYZ?"
        SQL: SELECT SUM(valor) as valor_total FROM fato_titulosabertos WHERE cedente = 'XYZ'

        Pergunta: "Quais são os 5 maiores títulos em aberto?"
        SQL: SELECT cedente, sacado, valor, vencimento FROM fato_titulosabertos ORDER BY valor DESC LIMIT 5

        Pergunta: "Quantas operações foram realizadas no último mês?"
        SQL: SELECT COUNT(*) as total FROM fato_operacoes WHERE data >= CURRENT_DATE - INTERVAL '1 month'

        Pergunta: "Qual o valor total das operações por cedente nos últimos 30 dias?"
        SQL: SELECT cedente, SUM(valor_bruto) as valor_total FROM fato_operacoes WHERE data >= CURRENT_DATE - INTERVAL '30 days' GROUP BY cedente ORDER BY valor_total DESC

        Pergunta: "Me mostre o deságio médio por operador."
        SQL: SELECT operador, AVG(valor_desagio) as desagio_medio FROM fato_operacoes GROUP BY operador ORDER BY desagio_medio DESC

        Pergunta: "Quais sacados têm mais de 3 títulos vencidos?"
        SQL: SELECT sacado, COUNT(*) as total_titulos FROM fato_titulosabertos WHERE vencimento < CURRENT_DATE GROUP BY sacado HAVING COUNT(*) > 3 ORDER BY total_titulos DESC

        Pergunta: "Quais são os cedentes do estado de São Paulo?"
        SQL: SELECT nome, cidade, telefone, email FROM dimcedentesconsolidado WHERE uf = 'SP'

        Pergunta: "Quais cedentes têm limite global acima de 100 mil?"
        SQL: SELECT nome, limite_global FROM dimcedentesconsolidado WHERE limite_global > 100000 ORDER BY limite_global DESC

        Pergunta: "Quais cedentes são gerenciados pelo gerente João Silva?"
        SQL: SELECT nome, telefone, email FROM dimcedentesconsolidado WHERE gerente = 'João Silva'

        INSTRUÇÕES:
        1. Analise a pergunta em linguagem natural
        2. Identifique as tabelas relevantes (fato_operacoes, fato_titulosabertos ou dimcedentesconsolidado)
        3. Gere APENAS a consulta SQL correspondente, sem explicações adicionais
        4. Não inclua comentários ou texto adicional, apenas a consulta SQL
        5. Use aspas simples para strings
        6. Certifique-se de que a consulta seja válida para PostgreSQL
        7. Aplique as regras semânticas descritas acima para escolher as colunas corretas

        Agora, converta a seguinte pergunta em uma consulta SQL:
        """

        groq_tool = self.tools["groq"]

        # Generate SQL query from natural language
        sql_query = groq_tool.generate_text(
            prompt=query,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.1  # Lower temperature for more deterministic output
        )

        # Clean up the SQL query (remove markdown formatting if present)
        sql_query = sql_query.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query.split("```sql")[1]
        if sql_query.startswith("```"):
            sql_query = sql_query.split("```")[1]
        if sql_query.endswith("```"):
            sql_query = sql_query.rsplit("```", 1)[0]
        sql_query = sql_query.strip()

        # Log the generated SQL query
        print(f"Consulta em linguagem natural: {query}")
        print(f"SQL gerado: {sql_query}")

        # Execute the SQL query
        result = self.query_database(sql_query)

        # Generate a human-friendly response
        response_system_prompt = f"""Você é {self.name}, um assistente de dados inteligente especializado em interpretar dados financeiros de operações e títulos.

        A pergunta original do usuário foi: "{query}"

        A consulta SQL gerada foi: "{sql_query}"

        Os resultados da consulta são:
        {result}

        REGRAS SEMÂNTICAS IMPORTANTES:

        1. Sempre que for mencionado "valor da operação", refere-se ao campo `valor_bruto` da tabela `fato_operacoes`.
        2. O "deságio" representa o desconto aplicado ao valor da operação ou título.
        3. O "operador" é o responsável pela carteira de operações, enquanto o "gerente" é o comercial responsável por um grupo de cedentes.
        4. O "sacado" é quem deve pagar o título, ou seja, o cliente do cedente.
        5. O "cedente" é quem detém o título ou a operação (quem vende o título ou crédito).

        INSTRUÇÕES:
        1. Explique os resultados da consulta de forma clara e objetiva
        2. Use linguagem simples e acessível
        3. Forneça insights relevantes sobre os dados, incluindo tendências, anomalias ou padrões
        4. Responda em português
        5. Seja conciso e direto
        6. Não mencione a consulta SQL, apenas explique os resultados
        7. Se houver muitos resultados, resuma as informações mais importantes
        8. Se aplicável, mencione totais, médias, valores máximos/mínimos
        9. Formate valores monetários com R$ e separadores de milhar (ex: R$ 1.234,56)
        10. Formate datas no padrão brasileiro (DD/MM/AAAA)
        11. Contextualize os resultados em termos de operações financeiras
        12. Sugira possíveis ações ou análises adicionais com base nos resultados
        13. Se relevante, compare os resultados com médias ou valores esperados
        """

        # Generate the response
        friendly_response = groq_tool.generate_text(
            prompt="Por favor, explique os resultados da consulta de forma amigável.",
            system_prompt=response_system_prompt,
            max_tokens=config.MAX_OUTPUT_TOKENS,
            temperature=0.7
        )

        return friendly_response

    def process_query(self, query: str, system_prompt: Optional[str] = None) -> str:
        """
        Process a user query using the Gemini tool.

        Args:
            query: User query to process
            system_prompt: Optional system prompt to provide context

        Returns:
            Response from the agent
        """
        # Add query to conversation history
        self.conversation_history.append({"role": "user", "content": query})

        # Check for database-related commands
        if query.lower().startswith("sql:"):
            # Extract the SQL query
            sql_query = query[4:].strip()
            response = self.query_database(sql_query)
        elif query.lower() == "listar tabelas" or query.lower() == "list tables":
            response = self.list_database_tables()
        elif query.lower().startswith("descrever tabela ") or query.lower().startswith("describe table "):
            # Extract the table name
            parts = query.split(" ", 2)
            if len(parts) >= 3:
                table_name = parts[2].strip()
                response = self.describe_database_table(table_name)
            else:
                response = "Por favor, forneça o nome da tabela. Exemplo: 'descrever tabela nome_da_tabela'"
        elif query.lower() == "operacoes" or query.lower() == "listar operacoes":
            response = self.get_operacoes()
        elif query.lower().startswith("operacoes "):
            # Extract the limit
            try:
                limit = int(query.split(" ")[1])
                response = self.get_operacoes(limit)
            except (ValueError, IndexError):
                response = "Por favor, forneça um número válido. Exemplo: 'operacoes 20'"
        elif query.lower() == "titulos" or query.lower() == "listar titulos":
            response = self.get_titulos_abertos()
        elif query.lower().startswith("titulos "):
            # Extract the limit
            try:
                limit = int(query.split(" ")[1])
                response = self.get_titulos_abertos(limit)
            except (ValueError, IndexError):
                response = "Por favor, forneça um número válido. Exemplo: 'titulos 20'"
        elif query.lower() == "contar operacoes" or query.lower() == "total operacoes":
            response = self.count_table_records("fato_operacoes")
        elif query.lower() == "contar titulos" or query.lower() == "total titulos":
            response = self.count_titulos_abertos()
        elif query.lower() == "contar registros titulos":
            response = self.count_table_records("fato_titulosabertos")
        elif query.lower() == "cedentes" or query.lower() == "listar cedentes":
            response = self.get_cedentes_info()
        elif query.lower().startswith("cedentes "):
            # Extract the limit
            try:
                limit = int(query.split(" ")[1])
                response = self.get_cedentes_info(limit)
            except (ValueError, IndexError):
                response = "Por favor, forneça um número válido. Exemplo: 'cedentes 20'"
        elif query.lower() == "contar cedentes":
            response = self.count_table_records("dimcedentesconsolidado")
        # Detect natural language queries about the database
        elif any(keyword in query.lower() for keyword in [
            "quantos", "quais", "qual", "quanto", "lista", "mostre", "exiba", "cedente",
            "cedentes", "título", "títulos", "operação", "operações", "valor", "total",
            "aberto", "abertos", "sacado", "sacados"
        ]):
            # This looks like a natural language query about the database
            response = self.process_natural_language_query(query)
        else:
            # Use Groq to generate a response
            if "groq" in self.tools:
                groq_tool = self.tools["groq"]

                # Create a system prompt if none provided
                if system_prompt is None:
                    system_prompt = f"""Você é {self.name}, um assistente de dados inteligente especializado em interpretar dados financeiros de operações e títulos em um banco de dados relacional. Seu trabalho é responder perguntas com base em três tabelas principais: `fato_operacoes`, `fato_titulosabertos` e `dimcedentesconsolidado`.

### Estrutura das Tabelas

1. **Tabela: fato_operacoes**

Contém registros de operações financeiras entre cedentes e sacados. As colunas são:

- `empresa`: Empresa à qual a operação está vinculada.
- `cedente`: Detentor da operação (quem vende o título ou crédito).
- `etapa`: Fase atual da operação.
- `cpf_cnpj_cedente`: Documento do cedente.
- `prazo_medio`: Tempo médio das operações.
- `valor_bruto`: Valor total bruto da operação (valor base que deve ser considerado ao se referir a "valor da operação").
- `valor_desagio`: Valor descontado do bruto (perda do cedente).
- `valor_liquido`: Valor efetivamente recebido.
- `valor_recompra_pendencia`: Pendências em recompra.
- `cred_cedente`: Crédito do cedente.
- `valor_pagto_operacao`: Pagamentos realizados na operação.
- `valor_saldo`: Saldo restante da operação.
- `operacao`: Identificador da operação.
- `"data"`: Data da operação.
- `operador`: Responsável por cuidar daquela carteira.
- `captador`: Quem originou o negócio.
- `pagamento_operacao`: Tipo ou status do pagamento.
- `conta_pagto`: Conta usada no pagamento.
- `indice_operacao`: Índice financeiro da operação.

2. **Tabela: fato_titulosabertos**

Contém títulos financeiros em aberto. As colunas são:

- `empresa`: Empresa relacionada ao título.
- `cedente`: Quem detém o título.
- `sacado`: Cliente do cedente (quem paga).
- `cpf_cnpj_cedente`: Documento do cedente.
- `cpf_cnpj_sacado`: Documento do sacado.
- `id_titulo`: Identificador do título (número único).
- `vencimento`: Data de vencimento do título.
- `data_emissao`: Data de emissão.
- `documento`, `nosso_numero`, `op`, `conf`, `conta`, `m`, `cr`, `original`: Campos auxiliares ou operacionais.
- `valor`, `valor_juros`, `valor_multa`, `valor_tarifas`, `valor_total`, `desagio`: Todos esses campos representam valores financeiros.
- `motivo`, `situacao`, `etapa`, `historico`, `tipo`: Informações qualitativas sobre o título.

3. **Tabela: dimcedentesconsolidado**

Contém dados cadastrais dos cedentes. As colunas são:

- `nome`: Nome do cedente.
- `cpf_cnpj`: CPF ou CNPJ do cedente.
- `endereco`: Endereço do cedente.
- `cep`: CEP do endereço do cedente.
- `cidade`: Cidade do cedente.
- `uf`: Estado (UF) do cedente.
- `email`: Email de contato do cedente.
- `telefone`: Telefone de contato do cedente.
- `gerente`: Gerente responsável pelo cedente.
- `operador`: Operador responsável pela carteira do cedente.
- `captador`: Quem originou o relacionamento com o cedente.
- `controlador`: Responsável pelo controle da carteira.
- `fator_percentual`: Percentual do fator aplicado nas operações.
- `advalorem_percentual`: Percentual de ad valorem aplicado.
- `data_cadastro`: Data de cadastro do cedente.
- `fonte_captacao`: Como o cedente foi captado.
- `setor`: Setor de atuação do cedente.
- `grupo_economico`: Grupo econômico ao qual o cedente pertence.
- `primeira_operacao`: Data da primeira operação do cedente.
- `limite_global`: Limite global de crédito do cedente.
- `limite_boleto_especial`, `limite_comissaria`, `limite_tranche`, `limite_boleto_especial_tranche`, `limite_boleto_garantido`, `limite_operacao_clean`: Diferentes tipos de limites de crédito.
- `risco_atual`: Classificação de risco atual do cedente.
- `saldo`: Saldo atual do cedente.
- `id_cedente`: Identificador único do cedente.

### Regras e Semântica

- Sempre que for solicitada a **"soma dos valores da operação"**, use o campo `valor_bruto` da tabela `fato_operacoes`.
- A **coluna `desagio`** representa o desconto aplicado ao valor da operação ou título.
- A **coluna `situacao`** da tabela de títulos representa o status atual (ex: em aberto, pago, vencido).
- O **"operador"** é o responsável pela carteira de operações, enquanto o **"gerente"** (não representado diretamente, mas vinculado ao cedente) é o comercial responsável por um grupo de cedentes.
- Todos os campos que começam com `valor_` referem-se a valores financeiros.
- **`sacado`** é quem deve pagar o título, ou seja, o cliente do cedente.

### Comandos especiais:
- 'SQL: <consulta>' para executar uma consulta SQL personalizada
- 'listar tabelas' para listar todas as tabelas no banco de dados
- 'descrever tabela <nome>' para descrever a estrutura de uma tabela
- 'operacoes [limite]' para listar operações da tabela fato_operacoes
- 'titulos [limite]' para listar títulos em aberto da tabela fato_titulosabertos
- 'cedentes [limite]' para listar informações cadastrais dos cedentes
- 'contar operacoes' para contar o total de registros na tabela fato_operacoes
- 'contar titulos' para contar o total de títulos em aberto
- 'contar registros titulos' para contar o total de registros na tabela fato_titulosabertos
- 'contar cedentes' para contar o total de registros na tabela dimcedentesconsolidado

Responda sempre em português, de forma clara e objetiva, como um especialista em operações financeiras. Forneça insights contextualizados e relevantes para o usuário."""

                response = groq_tool.generate_text(
                    prompt=query,
                    system_prompt=system_prompt,
                    max_tokens=config.MAX_OUTPUT_TOKENS,
                    temperature=0.7
                )
            else:
                response = "Erro: Ferramenta Groq não disponível. Por favor, adicione-a usando add_tool('groq', GroqTool())."

        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print(f"{self.name}'s conversation history has been cleared.")

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.

        Returns:
            Dictionary with agent information
        """
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.list_tools(),
            "conversation_length": len(self.conversation_history)
        }
