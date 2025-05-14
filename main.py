#!/usr/bin/env python3
"""
Main entry point for the Agno AI Agent.
This script provides a command-line interface for interacting with the agent.
"""

import sys
import argparse
from colorama import init, Fore, Style

from agent import AgnoAgent
import config

# Initialize colorama for cross-platform colored terminal output
init()

def print_header():
    """Print the agent header."""
    print(f"{Fore.CYAN}=" * 50)
    print(f"  {Fore.WHITE}{Style.BRIGHT}{config.AGENT_NAME} Agente de IA v{config.AGENT_VERSION}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 50)
    print(f"{Fore.GREEN}Digite 'exit', 'quit', ou pressione Ctrl+C para sair.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Digite 'help' para ver os comandos disponíveis.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}-" * 50 + Style.RESET_ALL)

def print_help():
    """Print help information."""
    print(f"\n{Fore.YELLOW}Comandos Disponíveis:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}help{Style.RESET_ALL} - Mostrar esta mensagem de ajuda")
    print(f"  {Fore.WHITE}exit{Style.RESET_ALL}, {Fore.WHITE}quit{Style.RESET_ALL} - Sair do programa")
    print(f"  {Fore.WHITE}clear{Style.RESET_ALL} - Limpar o histórico de conversas")
    print(f"  {Fore.WHITE}info{Style.RESET_ALL} - Mostrar informações sobre o agente")
    print(f"  {Fore.WHITE}tools{Style.RESET_ALL} - Listar ferramentas disponíveis")
    print(f"  {Fore.WHITE}models{Style.RESET_ALL} - Listar modelos Gemini disponíveis")
    print(f"\n{Fore.YELLOW}Comandos de Banco de Dados:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}listar tabelas{Style.RESET_ALL} - Listar todas as tabelas no banco de dados")
    print(f"  {Fore.WHITE}descrever tabela <nome>{Style.RESET_ALL} - Descrever a estrutura de uma tabela")
    print(f"  {Fore.WHITE}SQL: <consulta>{Style.RESET_ALL} - Executar uma consulta SQL")
    print(f"  {Fore.WHITE}operacoes [limite]{Style.RESET_ALL} - Listar operações da tabela fato_operacoes")
    print(f"  {Fore.WHITE}titulos [limite]{Style.RESET_ALL} - Listar títulos em aberto da tabela fato_titulosabertos")
    print(f"  {Fore.WHITE}contar operacoes{Style.RESET_ALL} - Contar o total de registros na tabela fato_operacoes")
    print(f"  {Fore.WHITE}contar titulos{Style.RESET_ALL} - Contar o total de títulos em aberto")
    print(f"  {Fore.WHITE}contar registros titulos{Style.RESET_ALL} - Contar o total de registros na tabela fato_titulosabertos")
    print(f"\n{Fore.YELLOW}Consultas em Linguagem Natural:{Style.RESET_ALL}")
    print(f"  Você também pode fazer perguntas em linguagem natural sobre o banco de dados, como:")
    print(f"  {Fore.WHITE}Quantos títulos em aberto possui o cedente X?{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Qual o valor total dos títulos em aberto?{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Quais são os 5 maiores títulos em aberto?{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Quantas operações foram realizadas no último mês?{Style.RESET_ALL}")
    print(f"{Fore.CYAN}-" * 50 + Style.RESET_ALL)

def interactive_mode(agent):
    """Run the agent in interactive mode."""
    print_header()

    while True:
        try:
            # Get user input
            user_input = input(f"\n{Fore.GREEN}You:{Style.RESET_ALL} ")

            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print(f"\n{Fore.YELLOW}Exiting {config.AGENT_NAME}. Goodbye!{Style.RESET_ALL}")
                break

            # Check for help command
            elif user_input.lower() == 'help':
                print_help()

            # Check for clear command
            elif user_input.lower() == 'clear':
                agent.clear_conversation_history()
                print(f"{Fore.YELLOW}Conversation history cleared.{Style.RESET_ALL}")

            # Check for info command
            elif user_input.lower() == 'info':
                info = agent.get_info()
                print(f"\n{Fore.YELLOW}Agent Information:{Style.RESET_ALL}")
                for key, value in info.items():
                    print(f"  {Fore.WHITE}{key}{Style.RESET_ALL}: {value}")

            # Check for tools command
            elif user_input.lower() == 'tools':
                tools = agent.list_tools()
                print(f"\n{Fore.YELLOW}Available Tools:{Style.RESET_ALL}")
                for tool in tools:
                    print(f"  - {tool}")

            # Check for models command
            elif user_input.lower() == 'models':
                if 'gemini' in agent.tools:
                    models = agent.tools['gemini'].list_models()
                    print(f"\n{Fore.YELLOW}Available Gemini Models:{Style.RESET_ALL}")
                    for model in models:
                        if "name" in model:
                            model_name = model["name"].split("/")[-1]
                            print(f"  - {model_name}")
                else:
                    print(f"{Fore.RED}Gemini tool not available.{Style.RESET_ALL}")

            # Process regular user input
            elif user_input.strip():
                print(f"\n{Fore.BLUE}{config.AGENT_NAME} is thinking...{Style.RESET_ALL}")
                response = agent.process_query(user_input)
                print(f"\n{Fore.MAGENTA}{config.AGENT_NAME}:{Style.RESET_ALL} {response}")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Exiting {config.AGENT_NAME}. Goodbye!{Style.RESET_ALL}")
            break

        except Exception as e:
            print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def main():
    """Main function to run the Agno AI Agent."""
    parser = argparse.ArgumentParser(description=f'{config.AGENT_NAME} AI Agent')
    parser.add_argument('-q', '--query', help='Process a single query and exit')
    args = parser.parse_args()

    # Create the agent
    agent = AgnoAgent()

    # Check if we're processing a single query or running in interactive mode
    if args.query:
        response = agent.process_query(args.query)
        print(response)
    else:
        interactive_mode(agent)

if __name__ == "__main__":
    main()
