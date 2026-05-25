Desenvolvido por Mateus Santana C


```markdown
# 🛡️ Cyber Sentinel v3.0 - Threat Intelligence Tool

O **Cyber Sentinel v3.0** é uma ferramenta em Python desenvolvida para automatizar a consulta e análise de vulnerabilidades diretamente da API oficial do governo americano (**NVD - National Vulnerability Database / NIST**). 

A aplicação possui uma interface gráfica (GUI) intuitiva que permite a profissionais de TI e Cibersegurança buscar detalhes de vulnerabilidades por IDs específicos (CVEs) ou pesquisar por tecnologias/assuntos afetados, gerando relatórios automatizados em PDF.

---

 Principais Funcionalidades

-  **Busca Direta por CVE:** Digite o ID exato (ex: `CVE-2024-1234`) para obter a descrição detalhada e a severidade.
-  **Pesquisa por Tecnologia/Assunto:** Busque por termos como *Windows*, *Apache*, *Zabbix*, *Linux* e liste as últimas vulnerabilidades registradas.
-  **Cálculo de Severidade (Score CVSS):** Exibe a pontuação base do CVSS v3.1/v3.0 para triagem rápida de riscos.
-  **Geração de Manual/Relatório em PDF:** Exporta os resultados da pesquisa por assunto em um relatório estruturado para auditorias ou documentação técnica de *hardening*.
-  **Links Diretos:** Inclui hiperlinks clicáveis direto para a base oficial do NIST de cada vulnerabilidade mapeada.

---

Tecnologias Utilizadas

- **Python 3** (Linguagem base)
- **Tkinter** (Interface Gráfica integrada)
- **Requests** (Consumo da API REST do NVD/NIST)
- **FPDF** (Geração dinâmica dos relatórios em PDF)

---

Como Rodar o Projeto no Linux (Pop!_OS / Ubuntu / Debian)

1. Instalar as dependências do sistema
Abra o terminal na pasta do projeto e instale as bibliotecas necessárias do Python via gerenciador de pacotes APT:
```bash
sudo apt update
sudo apt install python-is-python3 python3-requests python3-fpdf -y
2. Executar a aplicação
Basta rodar o comando abaixo no terminal ou usar o VS Code:

python cyber_sentinel_v3.py

Estrutura do Repositório
Plaintext
├── cyber_sentinel_v3.py   # Script principal da aplicação
└── README.md              # Documentação do projeto
