#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GASA - Google Account Security Auditor
Ferramenta Profissional de Auditoria de Credenciais e Postura de Segurança.
"""

import os
import sys
import time
import hashlib
import re
import secrets
import string

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_logo():
    logo = r"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   ██████╗  █████╗ ███████╗ █████╗     [ SECURITY AUDITOR ]            ║
    ║  ██╔════╝ ██╔══██╗██╔════╝██╔══██╗                                    ║
    ║  ██║  ███╗███████║███████╗███████║    Versão: 5.0 - Professional       ║
    ║  ██║   ██║██╔══██║╚════██║██╔══██║    Desenvolvido para Defesa         ║
    ║  ╚██████╔╝██║  ██║███████║██║  ██║                                    ║
    ║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                    ║
    ║                                                                       ║
    ║              GOOGLE ACCOUNT SECURITY AUDITOR (GASA)                   ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    print("\033[94m" + logo + "\033[0m")
    print("\033[93m" + "═" * 75 + "\033[0m")
    print(f"\033[93m[#] Painel Consolidado de Análise de Riscos e Proteção de Identidade\033[0m")
    print("\033[93m" + "═" * 75 + "\033[0m\n")

def verificar_vazamento_senha(senha):
    """Consulta segura via k-Anonymity para verificar vazamentos"""
    sha1_senha = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    prefixo = sha1_senha[:5]
    sufixo = sha1_senha[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefixo}"
    try:
        import requests
        resposta = requests.get(url, timeout=10)
        if resposta.status_code != 200: return None
        linhas = resposta.text.splitlines()
        for linha in linhas:
            hash_visto, contagem = linha.split(':')
            if hash_visto == sufixo: return int(contagem)
        return 0
    except:
        return None

def calcular_tempo_forca_bruta(senha):
    """Módulo matemático de entropia de senha"""
    if not senha: return "Imediato"
    pool = 0
    if any(c.islower() for c in senha): pool += 26
    if any(c.isupper() for c in senha): pool += 26
    if any(c.isdigit() for c in senha): pool += 10
    if any(not c.isalnum() for c in senha): pool += 32
    
    combinacoes = pool ** len(senha)
    tentativas_por_segundo = 100_000_000_000  # Ataque de alta performance offline
    segundos = combinacoes / tentativas_por_segundo
    
    if segundos < 1: return "Imediato (Fraquíssima)"
    minutos = segundos / 60
    if minutos < 60: return f"Cerca de {int(minutos)} minutos"
    horas = minutos / 60
    if horas < 24: return f"Cerca de {int(horas)} horas"
    dias = horas / 24
    if dias < 365: return f"Cerca de {int(dias)} dias"
    anos = dias / 365
    if anos < 1_000_000: return f"Cerca de {int(anos):,} anos".replace(',', '.')
    return "Séculos (Excelente resistência)"

def gerar_senha_segura(comprimento=16):
    """Gera uma senha aleatória usando entropia criptográfica (secrets)"""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*()_+-=[]{}"
    while True:
        senha = ''.join(secrets.choice(caracteres) for _ in range(comprimento))
        # Garante que a senha gerada atenda a todos os requisitos de segurança
        if (any(c.islower() for c in senha)
                and any(c.isupper() for c in senha)
                and any(c.isdigit() for c in senha)
                and any(not c.isalnum() for c in senha)):
            return senha

def auditoria_credenciais():
    limpar_tela()
    mostrar_logo()
    print("\033[96m[ MÓDULO 1: Auditoria Criptográfica de Senha ]\033[0m\n")
    
    email = input("Digite o e-mail para registro do relatório: ").strip()
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        print("\033[91m[!] Formato de e-mail inválido.\033[0m")
        time.sleep(2)
        return
        
    senha = input("Digite a senha atual para avaliar a robustez: ").strip()
    if not senha: return
    
    print("\n[*] Processando dados em nuvem e calculando entropia...")
    vazamentos = verificar_vazamento_senha(senha)
    tempo_quebra = calcular_tempo_forca_bruta(senha)
    
    print("\n" + "─" * 75)
    print(f"\033[96m[ RELATÓRIO DE AUDITORIA PARA: {email} ]\033[0m\n")
    
    if vazamentos is None:
        print("\033[93m[-] Atenção: Não foi possível checar a base global de vazamentos.\033[0m")
    elif vazamentos > 0:
        print(f"\033[91m[✗] CRÍTICO: Esta senha já vazou {vazamentos:,} vezes na internet!".replace(',', '.') + "\033[0m")
        print("\033[91m[!] ALERTA: Troque esta senha imediatamente para evitar Hijacking.\033[0m")
    else:
        print("\033[92m[✓] INTEGRIDADE: Nenhuma exposição pública desta senha foi detectada.\033[0m")
        
    print(f"\033[94m[*] RESISTÊNCIA A FORÇA BRUTA OFFLINE: {tempo_quebra}\033[0m")
    print("─" * 75)
    
    if vazamentos and vazamentos > 0 or "Imediato" in tempo_quebra:
        opcao = input("\nDeseja que o GASA gere uma senha 100% segura e limpa para você? (s/n): ").strip().lower()
        if opcao == 's':
            nova_senha = gerar_senha_segura()
            print(f"\n\033[92m[✓] Nova Sugestão Gerada: {nova_senha}\033[0m")
            print("\033[93m[!] Guarde-a em um gerenciador de senhas seguro offline.\033[0m")
            
    input("\nPressione [Enter] para retornar ao menu...")

def checklist_postura():
    limpar_tela()
    mostrar_logo()
    print("\033[96m[ MÓDULO 2: Checklist de Hardening (Configurações da Conta) ]\033[0m\n")
    
    perguntas = [
        "1. A Verificação em Duas Etapas (MFA) via aplicativo gerador de códigos está ligada?",
        "2. Os códigos de backup impressos estão armazenados em local físico seguro?",
        "3. A 'Proteção Avançada' do Google está habilitada para o seu perfil?",
        "4. Você revisou os aplicativos de terceiros vinculados à sua conta nos últimos 30 dias?"
    ]
    
    pontos = 0
    for p in perguntas:
        resp = input(f"{p} (s/n): ").strip().lower()
        if resp == 's': pontos += 1
        
    print(f"\n\033[94m[*] Pontuação de Defesa Ativa: {pontos}/{len(perguntas)}\033[0m")
    if pontos == 4:
        print("\033[92m[✓] Perfil Blindado: Excelentes práticas de proteção configuradas.\033[0m")
    elif pontos >= 2:
        print("\033[93m[!] Risco Moderado: Recomendamos ativar o MFA por App e remover acessos antigos.\033[0m")
    else:
        print("\033[91m[✗] Risco Alto: A conta depende apenas da senha. Vulnerável a phishing direcionado.\033[0m")
        
    input("\nPressione [Enter] para retornar ao menu...")

def triagem_phishing():
    limpar_tela()
    mostrar_logo()
    print("\033[96m[ MÓDULO 3: Analisador Preventivo de E-mails Suspeitos ]\033[0m\n")
    print("Use este módulo para analisar um e-mail de alerta que você recebeu do Google:\n")
    
    remetente = input("1. Qual o e-mail exato de quem enviou? (Ex: alert@google.com): ").strip().lower()
    contem_link = input("2. O e-mail pressiona você a clicar em um link urgente ou fazer login? (s/n): ").strip().lower()
    pede_codigo = input("3. O texto solicita que você responda com um código de verificação SMS? (s/n): ").strip().lower()
    
    print("\n" + "─" * 75)
    print("\033[96m[ RESULTADO DA TRIAGEM DE PHISHING ]\033[0m\n")
    
    indicadores_risco = 0
    
    # Validação básica de domínios confiáveis do Google
    dominios_validos = ['@google.com', '@support.google.com', '@accounts.google.com']
    if not any(remetente.endswith(dom) for dom in dominios_validos):
        print("\033[91m[!] ALERTA DE REMETENTE: O domínio do remetente NÃO pertence aos servidores centrais da Google.\033[0m")
        indicadores_risco += 1
        
    if contem_link == 's':
        print("\033[93m[!] ALERTA DE LINK: E-mails legítimos de segurança raramente exigem ações imediatas de redefinição via links diretos sem solicitação prévia.\033[0m")
        indicadores_risco += 1
        
    if pede_codigo == 's':
        print("\033[91m[!] ALERTA CRÍTICO: A Google NUNCA solicita códigos de verificação ou senhas por e-mail ou mensagens externas.\033[0m")
        indicadores_risco += 2

    if indicadores_risco == 0:
        print("\033[92m[✓] O e-mail analisado apresenta características iniciais de uma mensagem legítima. Mantenha sempre a cautela.\033[0m")
    else:
        print(f"\n\033[91m[✗] ALERTA: Alto potencial de ataque de Engenharia Social (Phishing). Não clique em nada e delete a mensagem.\033[0m")
        
    print("─" * 75)
    input("\nPressione [Enter] para retornar ao menu...")

def main():
    while True:
        limpar_tela()
        mostrar_logo()
        print("Selecione o módulo de auditoria desejado:")
        print(" \033[92m[1]\033[0m Auditar Robustez e Vazamento de Senha")
        print(" \033[92m[2]\033[0m Executar Checklist de Proteção da Conta (MFA)")
        print(" \033[92m[3]\033[0m Analisar E-mail Suspeito (Anti-Phishing)")
        print(" \033[91m[0]\033[0m Sair do Painel")
        
        try:
            opcao = input("\nOpção desejada > ").strip()
            if opcao == '1':
                auditoria_credenciais()
            elif opcao == '2':
                checklist_postura()
            elif opcao == '3':
                triagem_phishing()
            elif opcao == '0':
                print("\n\033[94m[*] Encerrando Auditoria GASA de forma segura. Até logo!\033[0m")
                break
            else:
                print("\033[91m[!] Opção Inválida.\033[0m")
                time.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("[!] Baixando pacotes de requisição para auditoria segura...")
        os.system(f"{sys.executable} -m pip install requests")
        import requests

    if os.name == 'nt':
        os.system("title GASA v5.0 - Google Account Security Auditor")
        os.system("mode con: cols=85 lines=40")
    main()