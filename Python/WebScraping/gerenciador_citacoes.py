import shelve
import os
from typing import List, Dict, Optional

# Cores ANSI para o terminal
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    VERMELHO = '\033[91m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    SUBLINHADO = '\033[4m'

# Caminho do arquivo shelve
pasta_dados = "dados_shelve"
arquivo_shelve = os.path.join(pasta_dados, "citacoes.db")

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    """Exibe o cabeçalho do menu"""
    print(f"\n{Cores.CIANO}{Cores.NEGRITO}{'='*60}{Cores.RESET}")
    print(f"{Cores.CIANO}{Cores.NEGRITO}{' '*15}GERENCIADOR DE CITAÇÕES{Cores.RESET}")
    print(f"{Cores.CIANO}{Cores.NEGRITO}{'='*60}{Cores.RESET}\n")

def exibir_menu():
    """Exibe o menu principal"""
    print(f"{Cores.AZUL}{Cores.NEGRITO}MENU PRINCIPAL:{Cores.RESET}\n")
    print(f"{Cores.VERDE}[1]{Cores.RESET} Listar todas as citações")
    print(f"{Cores.VERDE}[2]{Cores.RESET} Buscar citação por ID")
    print(f"{Cores.VERDE}[3]{Cores.RESET} Buscar citações por autor")
    print(f"{Cores.VERDE}[4]{Cores.RESET} Inserir nova citação")
    print(f"{Cores.VERDE}[5]{Cores.RESET} Alterar citação existente")
    print(f"{Cores.VERDE}[6]{Cores.RESET} Deletar citação")
    print(f"{Cores.VERDE}[7]{Cores.RESET} Estatísticas")
    print(f"{Cores.VERMELHO}[0]{Cores.RESET} Sair")
    print(f"\n{Cores.CIANO}{'-'*60}{Cores.RESET}\n")

def carregar_citacoes() -> List[Dict]:
    """Carrega todas as citações do arquivo shelve"""
    try:
        with shelve.open(arquivo_shelve) as db:
            if 'citacoes' in db:
                return db['citacoes'].copy()
            return []
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao carregar citações: {e}{Cores.RESET}")
        return []

def salvar_citacoes(citacoes: List[Dict]):
    """Salva as citações no arquivo shelve"""
    try:
        with shelve.open(arquivo_shelve, writeback=True) as db:
            db['citacoes'] = citacoes
            db['total_citacoes'] = len(citacoes)
        return True
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao salvar citações: {e}{Cores.RESET}")
        return False

def listar_citacoes():
    """Lista todas as citações"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    print(f"{Cores.VERDE}{Cores.NEGRITO}Total de citações: {len(citacoes)}{Cores.RESET}\n")
    print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    for idx, citacao in enumerate(citacoes, 1):
        print(f"{Cores.AZUL}{Cores.NEGRITO}[ID: {idx}]{Cores.RESET}")
        print(f"  {Cores.MAGENTA}Autor:{Cores.RESET} {citacao.get('Autot', 'N/A')}")
        print(f"  {Cores.MAGENTA}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
        print(f"  {Cores.MAGENTA}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def buscar_por_id():
    """Busca uma citação por ID"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    try:
        id_citacao = int(input(f"{Cores.AZUL}Digite o ID da citação (1-{len(citacoes)}): {Cores.RESET}"))
        if 1 <= id_citacao <= len(citacoes):
            citacao = citacoes[id_citacao - 1]
            print(f"\n{Cores.VERDE}{Cores.NEGRITO}CITAÇÃO ENCONTRADA:{Cores.RESET}\n")
            print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}")
            print(f"{Cores.AZUL}{Cores.NEGRITO}[ID: {id_citacao}]{Cores.RESET}")
            print(f"  {Cores.MAGENTA}Autor:{Cores.RESET} {citacao.get('Autot', 'N/A')}")
            print(f"  {Cores.MAGENTA}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
            print(f"  {Cores.MAGENTA}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
            print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
        else:
            print(f"{Cores.VERMELHO}ID inválido!{Cores.RESET}\n")
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def buscar_por_autor():
    """Busca citações por autor"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    autor = input(f"{Cores.AZUL}Digite o nome do autor (ou parte do nome): {Cores.RESET}").strip()
    
    if not autor:
        print(f"{Cores.VERMELHO}Nome do autor não pode estar vazio.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    resultados = []
    for idx, citacao in enumerate(citacoes, 1):
        if autor.lower() in citacao.get('Autot', '').lower():
            resultados.append((idx, citacao))
    
    if not resultados:
        print(f"\n{Cores.AMARELO}Nenhuma citação encontrada para o autor '{autor}'.{Cores.RESET}\n")
    else:
        print(f"\n{Cores.VERDE}{Cores.NEGRITO}Encontradas {len(resultados)} citação(ões):{Cores.RESET}\n")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
        for idx, citacao in resultados:
            print(f"{Cores.AZUL}{Cores.NEGRITO}[ID: {idx}]{Cores.RESET}")
            print(f"  {Cores.MAGENTA}Autor:{Cores.RESET} {citacao.get('Autot', 'N/A')}")
            print(f"  {Cores.MAGENTA}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
            print(f"  {Cores.MAGENTA}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
            print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def inserir_citacao():
    """Insere uma nova citação"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    print(f"{Cores.VERDE}{Cores.NEGRITO}INSERIR NOVA CITAÇÃO:{Cores.RESET}\n")
    
    autor = input(f"{Cores.AZUL}Digite o nome do autor: {Cores.RESET}").strip()
    if not autor:
        print(f"{Cores.VERMELHO}O nome do autor não pode estar vazio.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    frase = input(f"{Cores.AZUL}Digite a frase: {Cores.RESET}").strip()
    if not frase:
        print(f"{Cores.VERMELHO}A frase não pode estar vazia.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    origem = input(f"{Cores.AZUL}Digite a origem (URL): {Cores.RESET}").strip()
    if not origem:
        origem = "Manual"
    
    nova_citacao = {
        'Autot': autor,
        'Frase': frase,
        'Origem': origem
    }
    
    citacoes.append(nova_citacao)
    
    if salvar_citacoes(citacoes):
        print(f"\n{Cores.VERDE}{Cores.NEGRITO}✓ Citação inserida com sucesso!{Cores.RESET}\n")
        print(f"{Cores.CIANO}Nova citação ID: {len(citacoes)}{Cores.RESET}\n")
    else:
        print(f"\n{Cores.VERMELHO}Erro ao salvar a citação.{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def alterar_citacao():
    """Altera uma citação existente"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    try:
        id_citacao = int(input(f"{Cores.AZUL}Digite o ID da citação a alterar (1-{len(citacoes)}): {Cores.RESET}"))
        if not (1 <= id_citacao <= len(citacoes)):
            print(f"{Cores.VERMELHO}ID inválido!{Cores.RESET}\n")
            input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
            return
        
        citacao = citacoes[id_citacao - 1]
        
        print(f"\n{Cores.VERDE}{Cores.NEGRITO}CITAÇÃO ATUAL:{Cores.RESET}\n")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}")
        print(f"  {Cores.MAGENTA}Autor:{Cores.RESET} {citacao.get('Autot', 'N/A')}")
        print(f"  {Cores.MAGENTA}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
        print(f"  {Cores.MAGENTA}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
        
        print(f"{Cores.AMARELO}Deixe em branco para manter o valor atual.{Cores.RESET}\n")
        
        novo_autor = input(f"{Cores.AZUL}Novo autor [{citacao.get('Autot', '')}]: {Cores.RESET}").strip()
        nova_frase = input(f"{Cores.AZUL}Nova frase [{citacao.get('Frase', '')[:50]}...]: {Cores.RESET}").strip()
        nova_origem = input(f"{Cores.AZUL}Nova origem [{citacao.get('Origem', '')}]: {Cores.RESET}").strip()
        
        if novo_autor:
            citacao['Autot'] = novo_autor
        if nova_frase:
            citacao['Frase'] = nova_frase
        if nova_origem:
            citacao['Origem'] = nova_origem
        
        if salvar_citacoes(citacoes):
            print(f"\n{Cores.VERDE}{Cores.NEGRITO}✓ Citação alterada com sucesso!{Cores.RESET}\n")
        else:
            print(f"\n{Cores.VERMELHO}Erro ao salvar as alterações.{Cores.RESET}\n")
    
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def deletar_citacao():
    """Deleta uma citação"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    try:
        id_citacao = int(input(f"{Cores.AZUL}Digite o ID da citação a deletar (1-{len(citacoes)}): {Cores.RESET}"))
        if not (1 <= id_citacao <= len(citacoes)):
            print(f"{Cores.VERMELHO}ID inválido!{Cores.RESET}\n")
            input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
            return
        
        citacao = citacoes[id_citacao - 1]
        
        print(f"\n{Cores.VERMELHO}{Cores.NEGRITO}CITAÇÃO A SER DELETADA:{Cores.RESET}\n")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}")
        print(f"  {Cores.MAGENTA}Autor:{Cores.RESET} {citacao.get('Autot', 'N/A')}")
        print(f"  {Cores.MAGENTA}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
        print(f"  {Cores.MAGENTA}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
        
        confirmacao = input(f"{Cores.VERMELHO}Tem certeza que deseja deletar? (s/n): {Cores.RESET}").strip().lower()
        
        if confirmacao == 's':
            citacoes.pop(id_citacao - 1)
            if salvar_citacoes(citacoes):
                print(f"\n{Cores.VERDE}{Cores.NEGRITO}✓ Citação deletada com sucesso!{Cores.RESET}\n")
            else:
                print(f"\n{Cores.VERMELHO}Erro ao salvar as alterações.{Cores.RESET}\n")
        else:
            print(f"\n{Cores.AMARELO}Operação cancelada.{Cores.RESET}\n")
    
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def exibir_estatisticas():
    """Exibe estatísticas sobre as citações"""
    limpar_tela()
    exibir_cabecalho()
    citacoes = carregar_citacoes()
    
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}\n")
        input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        return
    
    print(f"{Cores.VERDE}{Cores.NEGRITO}ESTATÍSTICAS DAS CITAÇÕES:{Cores.RESET}\n")
    print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    # Estatísticas gerais
    total_citacoes = len(citacoes)
    print(f"{Cores.AZUL}{Cores.NEGRITO}Estatísticas Gerais:{Cores.RESET}\n")
    print(f"  {Cores.MAGENTA}Total de citações:{Cores.RESET} {total_citacoes}")
    
    # Contar autores únicos
    autores = {}
    origens = {}
    total_caracteres = 0
    
    for citacao in citacoes:
        autor = citacao.get('Autot', 'Desconhecido')
        origem = citacao.get('Origem', 'Desconhecida')
        frase = citacao.get('Frase', '')
        
        # Contar por autor
        if autor in autores:
            autores[autor] += 1
        else:
            autores[autor] = 1
        
        # Contar por origem
        if origem in origens:
            origens[origem] += 1
        else:
            origens[origem] = 1
        
        # Contar caracteres
        total_caracteres += len(frase)
    
    total_autores = len(autores)
    print(f"  {Cores.MAGENTA}Total de autores únicos:{Cores.RESET} {total_autores}")
    print(f"  {Cores.MAGENTA}Total de origens únicas:{Cores.RESET} {len(origens)}")
    print(f"  {Cores.MAGENTA}Total de caracteres nas frases:{Cores.RESET} {total_caracteres:,}")
    if total_citacoes > 0:
        media_caracteres = total_caracteres / total_citacoes
        print(f"  {Cores.MAGENTA}Média de caracteres por frase:{Cores.RESET} {media_caracteres:.1f}")
    
    print(f"\n{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    # Top 10 autores com mais citações
    print(f"{Cores.AZUL}{Cores.NEGRITO}Top 10 Autores com Mais Citações:{Cores.RESET}\n")
    autores_ordenados = sorted(autores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for idx, (autor, quantidade) in enumerate(autores_ordenados, 1):
        porcentagem = (quantidade / total_citacoes) * 100
        barra = '█' * int(porcentagem / 2)  # Barra visual
        print(f"  {Cores.VERDE}{idx:2d}.{Cores.RESET} {autor[:40]:<40} {Cores.CIANO}{quantidade:3d}{Cores.RESET} ({porcentagem:5.1f}%) {barra}")
    
    print(f"\n{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    # Distribuição por origem
    print(f"{Cores.AZUL}{Cores.NEGRITO}Distribuição por Origem:{Cores.RESET}\n")
    origens_ordenadas = sorted(origens.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for idx, (origem, quantidade) in enumerate(origens_ordenadas, 1):
        porcentagem = (quantidade / total_citacoes) * 100
        # Truncar URLs longas
        origem_display = origem[:50] + '...' if len(origem) > 50 else origem
        print(f"  {Cores.VERDE}{idx:2d}.{Cores.RESET} {origem_display:<53} {Cores.CIANO}{quantidade:3d}{Cores.RESET} ({porcentagem:5.1f}%)")
    
    print(f"\n{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    # Autor com mais citações
    if autores_ordenados:
        autor_top = autores_ordenados[0]
        print(f"{Cores.AZUL}{Cores.NEGRITO}Autor em Destaque:{Cores.RESET}\n")
        print(f"  {Cores.VERDE}{autor_top[0]}{Cores.RESET} com {Cores.CIANO}{autor_top[1]}{Cores.RESET} citação(ões)")
        porcentagem_top = (autor_top[1] / total_citacoes) * 100
        print(f"  Representa {Cores.MAGENTA}{porcentagem_top:.1f}%{Cores.RESET} do total de citações")
    
    print(f"\n{Cores.CIANO}{'-'*60}{Cores.RESET}\n")
    
    input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def main():
    """Função principal que executa o menu"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu()
        
        opcao = input(f"{Cores.AZUL}Escolha uma opção: {Cores.RESET}").strip()
        
        if opcao == '0':
            limpar_tela()
            print(f"\n{Cores.CIANO}{Cores.NEGRITO}Obrigado por usar o Gerenciador de Citações!{Cores.RESET}\n")
            break
        elif opcao == '1':
            listar_citacoes()
        elif opcao == '2':
            buscar_por_id()
        elif opcao == '3':
            buscar_por_autor()
        elif opcao == '4':
            inserir_citacao()
        elif opcao == '5':
            alterar_citacao()
        elif opcao == '6':
            deletar_citacao()
        elif opcao == '7':
            exibir_estatisticas()
        else:
            print(f"\n{Cores.VERMELHO}Opção inválida! Tente novamente.{Cores.RESET}\n")
            input(f"{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

def arquivo_shelve_existe():
    """Verifica se o arquivo shelve existe (verifica arquivos .dir, .dat ou .bak)"""
    # O shelve cria múltiplos arquivos, verificamos se pelo menos o .dir existe
    arquivos_shelve = [
        arquivo_shelve + '.dir',
        arquivo_shelve + '.dat',
        arquivo_shelve + '.bak'
    ]
    return any(os.path.exists(arq) for arq in arquivos_shelve)

if __name__ == "__main__":
    # Verificar se o arquivo shelve existe
    if not arquivo_shelve_existe():
        print(f"{Cores.VERMELHO}Arquivo shelve não encontrado: {arquivo_shelve}{Cores.RESET}")
        print(f"{Cores.AMARELO}Execute primeiro o app_v2_shelve.py para criar o arquivo.{Cores.RESET}")
        input(f"\n{Cores.CIANO}Pressione ENTER para sair...{Cores.RESET}")
    else:
        main()
