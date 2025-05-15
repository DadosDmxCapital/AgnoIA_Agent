"""
PostgreSQL integration tool for the Agno AI agent.
This module provides a tool for interacting with PostgreSQL databases.
"""

from typing import Dict, Any, Optional, List, Tuple, Union
import json

import config

# Check if psycopg2 is available
try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("Warning: psycopg2 library not available. Using fallback mechanism.")

class PostgresTool:
    """Tool for interacting with PostgreSQL databases."""

    def __init__(self,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[str] = None,
                 database: Optional[str] = None):
        """
        Initialize the PostgreSQL tool.

        Args:
            user: Database user. If not provided, will use the one from config.
            password: Database password. If not provided, will use the one from config.
            host: Database host. If not provided, will use the one from config.
            port: Database port. If not provided, will use the one from config.
            database: Database name. If not provided, will use the one from config.
        """
        self.user = user or config.POSTGRES_USER
        self.password = password or config.POSTGRES_PASSWORD
        self.host = host or config.POSTGRES_HOST
        self.port = port or config.POSTGRES_PORT
        self.database = database or config.POSTGRES_DATABASE

        self.connection = None
        self.cursor = None

        # Check if we have the required libraries
        if not PSYCOPG2_AVAILABLE:
            print("PostgreSQL tool requires psycopg2 library. Please install it with: pip install psycopg2-binary")

    def connect(self) -> bool:
        """
        Connect to the PostgreSQL database.

        Returns:
            True if connection was successful, False otherwise
        """
        if not PSYCOPG2_AVAILABLE:
            print("Erro: biblioteca psycopg2 não está disponível.")
            return False

        try:
            # Close existing connection if any
            if self.connection:
                self.close()

            # Print connection details (without password)
            print(f"Tentando conectar ao banco de dados PostgreSQL:")
            print(f"  Host: {self.host}")
            print(f"  Porta: {self.port}")
            print(f"  Usuário: {self.user}")
            print(f"  Banco de dados: {self.database}")

            # Connect to the database
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )

            # Create a cursor
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            print("Conexão com o banco de dados PostgreSQL estabelecida com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao conectar ao banco de dados PostgreSQL: {str(e)}")
            return False

    def close(self) -> None:
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Execute a SQL query.

        Args:
            query: SQL query to execute
            params: Optional parameters for the query

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of dictionaries with query results if successful, error message otherwise
        """
        if not PSYCOPG2_AVAILABLE:
            return False, "psycopg2 library not available. Please install it with: pip install psycopg2-binary"

        # Connect if not already connected
        if not self.connection or not self.cursor:
            print("Conexão não estabelecida. Tentando conectar...")
            if not self.connect():
                return False, "Failed to connect to the database"

        try:
            # Print query for debugging
            print(f"Executando consulta: {query}")
            if params:
                print(f"Parâmetros: {params}")

            # Execute the query
            self.cursor.execute(query, params or {})

            # Check if the query returns results
            if query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE", "EXPLAIN")):
                # Fetch all results
                results = self.cursor.fetchall()

                # Print number of results for debugging
                print(f"Consulta retornou {len(results)} resultados")

                # Convert results to list of dictionaries
                result_list = []
                for row in results:
                    result_list.append(dict(row))

                return True, result_list
            else:
                # Commit the transaction for non-SELECT queries
                self.connection.commit()
                return True, f"Query executed successfully. Affected rows: {self.cursor.rowcount}"

        except Exception as e:
            # Rollback in case of error
            if self.connection:
                self.connection.rollback()

            return False, f"Error executing query: {str(e)}"

    def list_tables(self) -> Tuple[bool, Union[List[str], str]]:
        """
        List all tables in the database.

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of table names if successful, error message otherwise
        """
        print(f"Listando tabelas do banco de dados: {self.database}")

        # Verificar se estamos conectados
        if not self.connection or not self.cursor:
            print("Não estamos conectados ao banco de dados. Tentando conectar...")
            if not self.connect():
                return False, "Falha ao conectar ao banco de dados"

        try:
            # Consulta para listar todas as tabelas
            query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
            """

            print(f"Executando consulta: {query}")
            self.cursor.execute(query)

            # Buscar resultados
            results = self.cursor.fetchall()
            print(f"Resultados obtidos: {len(results)} tabelas")

            # Converter resultados para lista de nomes de tabelas
            table_names = [table["table_name"] for table in results]
            print(f"Tabelas encontradas: {table_names}")

            return True, table_names

        except Exception as e:
            error_msg = f"Erro ao listar tabelas: {str(e)}"
            print(error_msg)
            return False, error_msg

    def describe_table(self, table_name: str) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Describe a table's structure.

        Args:
            table_name: Name of the table to describe

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of column descriptions if successful, error message otherwise
        """
        return self.execute_query(
            """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM
                information_schema.columns
            WHERE
                table_schema = 'public' AND
                table_name = %s
            ORDER BY
                ordinal_position
            """,
            {"table_name": table_name}
        )

    def get_operacoes(self, limit: int = 10) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Get operations from fato_operacoes table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of operations if successful, error message otherwise
        """
        return self.execute_query(
            f"""
            SELECT empresa, cedente, etapa, cpf_cnpj_cedente, prazo_medio,
                   valor_bruto, valor_desagio, valor_liquido, valor_recompra_pendencia,
                   cred_cedente, valor_pagto_operacao, valor_saldo, operacao,
                   "data", operador, captador, pagamento_operacao, conta_pagto, indice_operacao
            FROM public.fato_operacoes
            ORDER BY "data" DESC
            LIMIT {limit}
            """
        )

    def get_titulos_abertos(self, limit: int = 10) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Get open titles from fato_titulosabertos table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of open titles if successful, error message otherwise
        """
        return self.execute_query(
            f"""
            SELECT empresa, cedente, conf, conta, cpf_cnpj_cedente, cpf_cnpj_sacado,
                   cr, data_emissao, documento, etapa, historico, id_titulo,
                   id_titulo_original, m, motivo, vencimento, nosso_numero, op,
                   original, sacado, situacao, tipo, valor, valor_juros,
                   valor_multa, valor_tarifas, valor_total, desagio
            FROM public.fato_titulosabertos
            ORDER BY data_emissao DESC
            LIMIT {limit}
            """
        )

    def count_records(self, table_name: str) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Count records in a table.

        Args:
            table_name: Name of the table to count records from

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List with count result if successful, error message otherwise
        """
        # Validate table name to prevent SQL injection
        valid_tables = ["fato_operacoes", "fato_titulosabertos", "dimcedentesconsolidado"]
        if table_name not in valid_tables:
            return False, f"Tabela inválida. Tabelas válidas: {', '.join(valid_tables)}"

        # Print debug information
        print(f"Contando registros na tabela {table_name}...")

        # Execute the query with explicit casting to bigint to avoid any type issues
        success, result = self.execute_query(
            f"""
            SELECT CAST(COUNT(*) AS bigint) as total_records
            FROM public.{table_name}
            """
        )

        # Print the result for debugging
        if success and result:
            print(f"Resultado da contagem: {result}")
            print(f"Tipo do resultado: {type(result)}")
            if len(result) > 0:
                print(f"Primeiro item: {result[0]}")
                print(f"Tipo do primeiro item: {type(result[0])}")
                if 'total_records' in result[0]:
                    print(f"total_records: {result[0]['total_records']}")
                    print(f"Tipo de total_records: {type(result[0]['total_records'])}")

        return success, result

    def count_titulos_abertos(self) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Count open titles with specific criteria.

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List with count result if successful, error message otherwise
        """
        print("Executando contagem específica de títulos em aberto...")

        return self.execute_query(
            """
            SELECT CAST(COUNT(*) AS bigint) as total_titulos_abertos
            FROM public.fato_titulosabertos
            """
        )

    def get_cedentes_info(self, limit: int = 10) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Get cedentes information from dimcedentesconsolidado table.

        Args:
            limit: Maximum number of rows to return

        Returns:
            Tuple of (success, result)
            - success: True if query was successful, False otherwise
            - result: List of cedentes information if successful, error message otherwise
        """
        return self.execute_query(
            f"""
            SELECT nome, cpf_cnpj, endereco, cep, cidade, uf, email, telefone,
                   gerente, operador, captador, controlador, fator_percentual,
                   advalorem_percentual, data_cadastro, fonte_captacao, setor,
                   grupo_economico, primeira_operacao, limite_global,
                   limite_boleto_especial, limite_comissaria, limite_tranche,
                   limite_boleto_especial_tranche, limite_boleto_garantido,
                   limite_operacao_clean, risco_atual, saldo, id_cedente
            FROM public.dimcedentesconsolidado
            ORDER BY nome
            LIMIT {limit}
            """
        )

    def format_results_as_markdown(self, results: List[Dict[str, Any]], max_rows: int = 10) -> str:
        """
        Format query results as a markdown table.

        Args:
            results: List of dictionaries with query results
            max_rows: Maximum number of rows to include in the output

        Returns:
            Markdown formatted table
        """
        if not results:
            return "Nenhum resultado encontrado."

        # Get column names
        columns = list(results[0].keys())

        # Limit the number of columns if there are too many
        if len(columns) > 10:
            print(f"Muitas colunas ({len(columns)}), limitando a exibição para as 10 primeiras")
            columns = columns[:10]

        # Create header row
        header = "| " + " | ".join(columns) + " |"

        # Create separator row
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"

        # Create data rows (limited to max_rows)
        rows = []
        for i, row in enumerate(results):
            if i >= max_rows:
                rows.append(f"| ... | ... | ... | (Mostrando {max_rows} de {len(results)} linhas) |")
                break

            formatted_row = []
            for col in columns:
                value = row.get(col)
                if value is None:
                    formatted_value = "NULL"
                elif isinstance(value, (dict, list)):
                    formatted_value = json.dumps(value)
                else:
                    # Limit the length of string values
                    formatted_value = str(value)
                    if len(formatted_value) > 50:
                        formatted_value = formatted_value[:47] + "..."
                formatted_row.append(formatted_value)
            rows.append("| " + " | ".join(formatted_row) + " |")

        # Combine all parts
        return "\n".join([header, separator] + rows)
