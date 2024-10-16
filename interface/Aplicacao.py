import tkinter as tk
from tkinter import ttk, messagebox
from classes.Tarefa import Tarefa
from interface.JanelaAddSprint import JanelaAddSprint
from interface.JanelaTarefas import JanelaTarefas

class Aplicacao(tk.Tk):

    def __init__(self):
        super().__init__()
        self.janela_tarefas = None
        self.title("Gerenciador de Sprints")
        self.geometry("600x400")
        self.minsize(400, 300)  # Tamanho mínimo para a janela

        # Config. grid principal para ser responsivo
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Config. grid do main_frame para ser responsivo
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Frame para os botões e entrada
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.button_frame.grid_columnconfigure(1, weight=1)  

        # Botão para add Sprint
        self.add_button = ttk.Button(self.button_frame, text="Adicionar Sprint", command=self.abre_janela_add_sprint)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Campo p/ IDs das tarefas
        self.tarefa_entry = ttk.Entry(self.button_frame)
        self.tarefa_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botão para add tarefas
        self.add_tarefa_button = ttk.Button(self.button_frame, text="Adicionar Tarefas", command=self.add_tarefas_sprint)
        self.add_tarefa_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Frame para o grid
        self.grid_frame = ttk.Frame(self.main_frame)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_frame.grid_rowconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(0, weight=1)

        self.cria_grid()

        # Lista de Sprints
        self.sprints = []

        # Duplo clique na linha do grid exibe as tarefas
        self.tree.bind("<Double-1>", self.mostrar_tarefas_sprint)

    # Fim __init__

    def cria_grid(self):
        columns = ('Id', 'Data Inicial', 'Data Final')
        self.tree = ttk.Treeview(self.grid_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        # Config. as colunas para se expandirem proporcionalmente
        self.tree.column('Id', width=50, anchor="center")
        self.tree.column('Data Inicial', width=150, anchor="center")
        self.tree.column('Data Final', width=150, anchor="center")

        # Add arra de rolagem vertical
        scrollbar = ttk.Scrollbar(self.grid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Addd árvore do grid
        self.tree.grid(row=0, column=0, sticky="nsew")

    def abre_janela_add_sprint(self):
        JanelaAddSprint(self, self.tree)

    def add_tarefas_sprint(self):
        sprint_sel = self.tree.focus()
        if sprint_sel:
            sprint_id = int(self.tree.item(sprint_sel)['values'][0])
            ids_tarefas = self.tarefa_entry.get().split(',')

            if not ids_tarefas or ids_tarefas == ['']:
                messagebox.showwarning("Atenção", "Por favor, insira pelo menos um ID de tarefa.")
                return

            tarefas_adicionadas = []
            for tarefa_id in ids_tarefas:
                tarefa_id = tarefa_id.strip()
                if tarefa_id.isdigit():
                    # Cria objeto Tarefa
                    tarefa = Tarefa(int(tarefa_id), "História Exemplo", "Descrição Exemplo", "Desenvolvedor Exemplo", "Teste Exemplo", None)
                    tarefas_adicionadas.append(tarefa)
                else:
                    messagebox.showwarning("Atenção", f"ID de tarefa inválido: {tarefa_id}")

            if tarefas_adicionadas:
                for sprint in self.sprints:
                    if sprint.id == sprint_id:
                        sprint.listaTarefas.extend(tarefas_adicionadas)
                        messagebox.showinfo("Sucesso", f"{len(tarefas_adicionadas)} tarefas adicionadas à sprint {sprint_id}.")
                        self.tarefa_entry.delete(0, tk.END)
                        break
            else:
                messagebox.showwarning("Atenção", "Nenhuma tarefa válida encontrada.")
        else:
            messagebox.showwarning("Atenção", "Por favor, selecione uma sprint.")

    def mostrar_tarefas_sprint(self, event):
        sprint_sel = self.tree.focus()
        if sprint_sel:
            sprint_id = int(self.tree.item(sprint_sel)['values'][0])
            for sprint in self.sprints:
                if sprint.id == sprint_id:
                    # JanelaTarefas(self, sprint)
                    self.janela_tarefas = JanelaTarefas(self, sprint)
                    break