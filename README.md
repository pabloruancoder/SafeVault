# 🔐 SafeVault

**SafeVault** é um gerenciador de senhas moderno, seguro e local, desenvolvido em Python. Com uma interface limpa baseada em *CustomTkinter*, ele oferece criptografia de ponta a ponta para proteger suas credenciais, notas e cartões de crédito.

![Status](https://img.shields.io/badge/Status-Estável-green)
![Python](https://img.shields.io/badge/Made%20with-Python-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## ✨ Funcionalidades

*   **🔒 Segurança Máxima:** Utiliza criptografia **AES-256** (via biblioteca `cryptography` e `Fernet`) e derivação de chave PBKDF2HMAC.
*   **💾 Armazenamento Local:** Seus dados ficam salvos em um banco de dados SQLite (`.db`) no seu próprio computador. Nada vai para a nuvem.
*   **🎨 UI Moderna:** Interface agradável com suporte nativo a **Modo Escuro (Dark Mode)** e Claro.
*   **📂 Organização:** Crie pastas, subpastas e tipos de itens personalizados (Logins, Cartões, Notas, etc).
*   **📝 Editor Rich Text:** Notas seguras com suporte a formatação (Negrito, Cores, Títulos, Código).
*   **🎲 Gerador de Senhas:** Crie senhas fortes e verifique a força das suas senhas atuais.
*   **🗑️ Lixeira:** Sistema de exclusão segura com possibilidade de restauração.

---

## 📥 Download e Instalação (Windows)

Não quer mexer com código? Baixe a versão pronta para uso:

1.  Acesse a aba **[Releases](../../releases)** aqui no GitHub.
2.  Baixe o arquivo `SafeVault.exe` da versão mais recente.
3.  Execute o arquivo. O banco de dados será criado automaticamente na sua pasta de usuário.

> **Nota:** O Windows pode exibir um aviso de "SmartScreen" por ser um aplicativo novo. Clique em "Mais informações" -> "Executar assim mesmo".

---

## 💻 Como executar o código fonte (.py)

Se você é desenvolvedor e deseja rodar o projeto ou modificá-lo:

### Pré-requisitos
*   Python 3.10 ou superior.
*   Git instalado.

### Passo a passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/SafeVault.git
    cd SafeVault
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

---

## 🎨 Contribuindo com Temas e Design

O **SafeVault** foi construído pensando na comunidade! Queremos ver novas paletas de cores e estilos.

### Como criar um Tema:

Atualmente, as cores são definidas nas constantes globais no início do arquivo `main.py`.

1.  Procure pela seção de configuração de cores no código:
    ```python
    C_BG_MAIN = ("#FFFFFF", "#191919")   # (Cor Claro, Cor Escuro)
    C_ACCENT = ("#2383E2", "#0A84FF")    # Cor de destaque
    C_CARD = ("#FFFFFF", "#2B2B2B")      # Fundo dos cartões
    ...
    ```
2.  Crie um *Fork* deste projeto.
3.  Altere essas tuplas de cores para criar sua identidade visual (Ex: Tema Drácula, Cyberpunk, Nord).
4.  Envie um **Pull Request** com o título `[TEMA] Nome do Seu Tema`.
5.  Se aprovado, implementaremos um seletor de temas nas configurações futuras!

---

## 🤝 Contribuições Gerais

Contribuições são muito bem-vindas!
1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua Feature (`git checkout -b feature/NovaFeature`).
3.  Faça o Commit (`git commit -m 'Adicionando nova feature'`).
4.  Faça o Push (`git push origin feature/NovaFeature`).
5.  Abra um Pull Request.

---

## ⚠️ Aviso de Segurança

Embora este software utilize bibliotecas de criptografia padrão da indústria (`cryptography`), ele é fornecido "como está", sem garantias. Recomenda-se manter backups regulares do seu arquivo de banco de dados (`vault_v6.db`) e de sua chave de segurança.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
