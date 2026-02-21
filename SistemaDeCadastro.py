import customtkinter as ctk
import json
import os
import hashlib

# ==========================
# CONFIGURAÇÕES GERAIS
# ==========================

ctk.set_appearance_mode("dark")

ARQUIVO_USUARIOS = "usuarios.json"


# ==========================
# FUNÇÕES DE DADOS
# ==========================

def carregar_usuarios():
    """Carrega os usuários do arquivo JSON"""
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as arquivo:
            return json.load(arquivo)
    return []


def salvar_usuarios(usuarios):
    """Salva a lista de usuários no arquivo JSON"""
    with open(ARQUIVO_USUARIOS, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ==========================
# FUNÇÕES DO SISTEMA
# ==========================

def abrir_sistema(usuario):
    """Abre a janela principal após login"""

    # Esconde a janela de login
    app.withdraw()

    nova_janela = ctk.CTkToplevel()
    nova_janela.title("Sistema Principal")
    nova_janela.geometry("300x200")

    def fechar_sistema():
        nova_janela.destroy()
        app.deiconify()  # Mostra login novamente

    label_boas_vindas = ctk.CTkLabel(
        nova_janela,
        text=f"Bem-vindo, {usuario}!",
        font=("Arial", 18)
    )
    label_boas_vindas.pack(pady=20)

    botao_fechar = ctk.CTkButton(
        nova_janela,
        text="Sair",
        command=fechar_sistema
    )
    botao_fechar.pack(pady=10)

# ==========================
# FUNÇÕES DE LOGIN
# ==========================

def cadastrar_usuario():
    """Cadastra um novo usuário"""

    usuario = campo_usuario.get()
    senha = campo_senha.get()

    usuarios = carregar_usuarios()

    # Verifica se já existe
    for u in usuarios:
        if u["usuario"] == usuario:
            login_resultado.configure(
                text="Usuário já existe!",
                text_color="orange"
            )
            return

    senha_criptografada = criptografar_senha(senha)

    novo_usuario = {
        "usuario": usuario,
        "senha": senha_criptografada
    }

    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)

    login_resultado.configure(
        text="Usuário cadastrado com sucesso!",
        text_color="green"
    )


def validar_login():
    """Valida usuário e senha"""

    usuario = campo_usuario.get()
    senha = campo_senha.get()

    # Criptografa a senha digitada
    senha_digitada_criptografada = criptografar_senha(senha)

    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha_digitada_criptografada:
            login_resultado.configure(
                text="Login bem-sucedido!",
                text_color="green"
            )
            return

    login_resultado.configure(  
        text="Login falhou. Tente novamente.",
        text_color="red"
    )


# ==========================
# INTERFACE PRINCIPAL
# ==========================

app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("400x400")

# Usuário
label_usuario = ctk.CTkLabel(app, text="Usuário:")
label_usuario.pack(pady=10)

campo_usuario = ctk.CTkEntry(app, placeholder_text="Digite seu usuário")
campo_usuario.pack(pady=10)

# Senha
label_senha = ctk.CTkLabel(app, text="Senha:")
label_senha.pack(pady=10)

campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
campo_senha.pack(pady=10)

# Botões
botao_login = ctk.CTkButton(app, text="Login", command=validar_login)
botao_login.pack(pady=10)

botao_cadastro = ctk.CTkButton(app, text="Cadastrar", command=cadastrar_usuario)
botao_cadastro.pack(pady=5)

# Feedback
login_resultado = ctk.CTkLabel(app, text="")
login_resultado.pack(pady=10)

app.mainloop()

# para criar o usuario, é só rodar o sistema, clicar em "cadastrar", preencher o que pede, pode ser qualquer coisa, e clicar em "cadastrar". Depois disso, é só clicar em "login", preencher o que pediu, e clicar em "login". Se tudo tiver certo, você será redirecionado para o dashboard, onde verá uma mensagem de boas-vindas. Se quiser sair, é só fechar o site ou clicar em "sair".

#ainda em desenvolvimento, pode conter bugs, tipo a janela de login não abrir quando o login for feito. Estou tentando resolver isso.