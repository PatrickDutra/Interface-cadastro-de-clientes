import mysql.connector
from tkinter import messagebox, ttk
import tkinter as tk
from PIL import Image, ImageTk  # Para trabalhar com imagens

# Conectar ao banco de dados MySQL usando a porta 3308
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Substitua pelo seu usuário
    password="96647923Tita",  # Substitua pela sua senha
    database="fisioterapia",  # Nome do banco de dados
    port=3308
)

cursor = conn.cursor()

# Definindo cores e fontes
bg_color = "#E0F7FA"  # Cor de fundo suave
font_label = ("Arial", 14)
font_entry = ("Arial", 14)
font_button = ("Arial", 14)

# Variáveis para temporizadores
timer_cpf = None
timer_telefone = None

# Função para formatar o CPF preservando o cursor
def formatar_cpf(event=None):
    global timer_cpf
    if timer_cpf is not None:
        root.after_cancel(timer_cpf)  # Cancelar o temporizador anterior se o usuário continuar digitando
    
    def aplicar_formatacao_cpf():
        cpf = cpf_var.get().replace("-", "").replace(".", "")  # Remover traços e pontos
        novo_cpf = ""

        # Aplicar formatação
        if len(cpf) > 3:
            novo_cpf = cpf[:3] + "."
        if len(cpf) > 6:
            novo_cpf += cpf[3:6] + "."
        if len(cpf) > 9:
            novo_cpf += cpf[6:9] + "-"
        novo_cpf += cpf[9:]

        # Preservar a posição do cursor
        posicao_cursor = entry_cpf.index(tk.INSERT)
        cpf_var.set(novo_cpf[:14])  # Limitar a 14 caracteres
        entry_cpf.icursor(posicao_cursor)

    # Aplicar formatação após 300ms de inatividade
    timer_cpf = root.after(900, aplicar_formatacao_cpf)

# Função para formatar o telefone preservando o cursor
def formatar_telefone(event=None):
    global timer_telefone
    if timer_telefone is not None:
        root.after_cancel(timer_telefone)  # Cancelar o temporizador anterior se o usuário continuar digitando
    
    def aplicar_formatacao_telefone():
        telefone = telefone_var.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")  # Remover formatação
        novo_telefone = ""

        # Aplicar formatação
        if len(telefone) > 2:
            novo_telefone = "(" + telefone[:2] + ") "
        if len(telefone) > 7:
            novo_telefone += telefone[2:7] + "-"
        novo_telefone += telefone[7:]

        # Preservar a posição do cursor
        posicao_cursor = entry_telefone.index(tk.INSERT)
        telefone_var.set(novo_telefone[:15])  # Limitar a 15 caracteres
        entry_telefone.icursor(posicao_cursor)

    # Aplicar formatação após 300ms de inatividade
    timer_telefone = root.after(900, aplicar_formatacao_telefone)

# Função para salvar o cliente no banco
def salvar_cliente():
    nome = entry_nome.get()
    idade = entry_idade.get()
    telefone = entry_telefone.get()  # Captura o telefone formatado
    cpf = entry_cpf.get()  # Captura o CPF formatado
    endereco = entry_endereco.get()
    email = entry_email.get()
    observacoes = text_observacoes.get("1.0", tk.END).strip()

    # Verificação de preenchimento dos campos obrigatórios
    if not nome or not idade or not telefone or not cpf or not endereco or not email or not observacoes:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")
        return

    # Inserir dados no banco
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, idade, telefone, cpf, endereco, email, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, idade, telefone, cpf, endereco, email, observacoes))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        limpar_campos()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    telefone_var.set("")  # Limpar o campo Telefone
    cpf_var.set("")  # Limpar o campo CPF
    entry_endereco.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    text_observacoes.delete("1.0", tk.END)

def listar_clientes():
    list_window = tk.Toplevel(root)
    list_window.title("Lista de Clientes")
    list_window.geometry("1270x720")

    tree = ttk.Treeview(list_window, columns=("ID", "Nome", "Idade", "Telefone", "CPF", "Endereço", "Email", "Observações"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Idade", text="Idade")
    tree.heading("Telefone", text="Telefone")
    tree.heading("CPF", text="CPF")  # Adiciona o CPF na listagem
    tree.heading("Endereço", text="Endereço")
    tree.heading("Email", text="Email")
    tree.heading("Observações", text="Observações")

    tree.column("Observações", width=200)
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(list_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    cursor.execute("SELECT id, nome, idade, telefone, cpf, endereco, email, observacoes FROM clientes")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Clientes - Fisioterapia")
root.geometry("1270x720")
root.configure(bg=bg_color)  # Cor de fundo da janela principal

# Carregar a imagem com o caminho correto
image = Image.open("C:/Users/patrick.silva/Documents/Clientes/imagem/fisioterapiapng.png")  # Substitua pelo nome da sua imagem
# Redimensionar a imagem para ser maior, como 200x200
image = image.resize((200, 200), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(image)

# Exibir a imagem no canto direito
logo_label = tk.Label(root, image=logo, bg=bg_color)
logo_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")  # Mover para o canto direito

# Labels e entradas
tk.Label(root, text="Nome:", font=font_label, bg=bg_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_nome = tk.Entry(root, font=font_entry)
entry_nome.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Idade:", font=font_label, bg=bg_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_idade = tk.Entry(root, font=font_entry)
entry_idade.grid(row=2, column=1, padx=10, pady=10)

# Campo Telefone com formatação
tk.Label(root, text="Telefone:", font=font_label, bg=bg_color).grid(row=3, column=0, padx=10, pady=10, sticky="e")
telefone_var = tk.StringVar()
entry_telefone = tk.Entry(root, textvariable=telefone_var, font=font_entry)
entry_telefone.grid(row=3, column=1, padx=10, pady=10)
entry_telefone.bind("<KeyRelease>", formatar_telefone)  # Monitorar o campo para formatar

# Adicionar o campo CPF com formatação
tk.Label(root, text="CPF:", font=font_label, bg=bg_color).grid(row=4, column=0, padx=10, pady=10, sticky="e")
cpf_var = tk.StringVar()
entry_cpf = tk.Entry(root, textvariable=cpf_var, font=font_entry)
entry_cpf.grid(row=4, column=1, padx=10, pady=10)
entry_cpf.bind("<KeyRelease>", formatar_cpf)  # Monitorar o campo para formatar

tk.Label(root, text="Endereço:", font=font_label, bg=bg_color).grid(row=5, column=0, padx=10, pady=10, sticky="e")
entry_endereco = tk.Entry(root, font=font_entry)
entry_endereco.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="Email:", font=font_label, bg=bg_color).grid(row=6, column=0, padx=10, pady=10, sticky="e")
entry_email = tk.Entry(root, font=font_entry)
entry_email.grid(row=6, column=1, padx=10, pady=10)

tk.Label(root, text="Observações:", font=font_label, bg=bg_color).grid(row=7, column=0, padx=10, pady=10, sticky="e")
text_observacoes = tk.Text(root, height=4, width=40, font=font_entry)
text_observacoes.grid(row=7, column=1, padx=10, pady=10)

# Botões
tk.Button(root, text="Salvar", command=salvar_cliente, font=font_button, bg="#4CAF50", fg="white").grid(row=8, column=1, padx=10, pady=10)
tk.Button(root, text="Listar Clientes", command=listar_clientes, font=font_button, bg="#2196F3", fg="white").grid(row=8, column=0, padx=10, pady=10)

root.mainloop()

# Fechar a conexão com o banco de dados MySQL
conn.close()
