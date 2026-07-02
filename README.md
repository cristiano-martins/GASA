# GASA - Google Account Security Auditor 🛡️

O **Google Account Security Auditor (GASA)** é uma ferramenta de linha de comando (CLI) desenvolvida em Python voltada para a auditoria defensiva, conscientização cibernética e hardening de credenciais. O principal objetivo do projeto é capacitar usuários e administradores a avaliarem a resiliência de suas identidades digitais contra ataques de força bruta, engenharia social (phishing) e vazamentos de dados conhecidos.

---

## 🚀 Funcionalidades

O ecossistema do GASA é dividido em três módulos analíticos principais:

1. **Auditoria Criptográfica de Senhas:**
   * Avalia a complexidade estrutural e a entropia da senha digitada.
   * Estima o tempo necessário para quebra da credencial em um ataque de força bruta offline baseado em clusters de GPUs modernos.
   * Consulta a API global do *Have I Been Pwned* utilizando o modelo matemático seguro **k-Anonymity**.
   * Possui um **Gerador de Senhas Fortes** integrado que utiliza o módulo `secrets` do Python para garantir entropia criptográfica segura.

2. **Checklist de Hardening de Conta:**
   * Questionário técnico interativo para avaliar o nível de resiliência e a postura de defesa ativa do perfil do usuário (MFA, chaves de backup, proteção avançada).

3. **Triagem Preventiva de Phishing:**
   * Motor de regras simples para avaliar as características de e-mails suspeitos recebidos, ajudando a mitigar ataques de Engenharia Social.

---

## 🔒 Segurança e Privacidade (k-Anonymity)

A privacidade do usuário é a prioridade número um do GASA. Ao verificar se uma senha foi vazada, **a sua senha real nunca é enviada para a internet**. 

O script utiliza o princípio de anonimato $k$:
1. A senha é convertida localmente em um hash SHA-1 completo.
2. Apenas os **5 primeiros caracteres** do hash (o prefixo) são enviados para a API do *Have I Been Pwned*.
3. O servidor retorna uma lista de todos os hashes vazados na história que começam com aquele mesmo prefixo.
4. O script compara localmente o restante do hash (o sufixo) com a lista recebida. Se houver correspondência, o sistema indica quantas vezes ela foi exposta.

---

## 🛠️ Pré-requisitos e Instalação

Para rodar o GASA, você precisará apenas do Python 3 instalado em sua máquina e da biblioteca `requests`.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cristiano-martins/gasa.git
   cd gasa

2. **Instale as dependências:**
   ```bash
   pip install requests
   
3. **Execute a ferramenta:**
   ```bash
   python gasa.py


💻 Tecnologias Utilizadas
Python 3 - Linguagem base do projeto.

Requests - Sincronização e requisições HTTP com APIs de segurança externas.

Hashlib - Processamento e hashing criptográfico local.

Secrets - Geração de criptografia aleatória forte com nível de sistema operacional.

Re - Expressões regulares para validação estrutural de e-mails.

📄 Licença
Este projeto está sob a licença MIT. Isso significa que você pode modificar, distribuir e utilizar o código livremente, desde que inclua os créditos originais. Veja o arquivo LICENSE no repositório para mais detalhes.

Disclaimer: Esta ferramenta possui finalidade estritamente educacional, preventiva e de auditoria defensiva (Blue Team). Use para proteger suas próprias credenciais e conscientizar sua equipe.
