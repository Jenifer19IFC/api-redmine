import tkinter as tk
from tkinter import ttk, messagebox

from classes.Sprint import Sprint

class JanelaAddSprint(tk.Toplevel):
    
    def __init__(self, parent, tree):   
        super().__init__(parent)
        self.parent = parent
        self.tree = tree
        self.title("Adicionar Sprint")

        ttk.Label(self, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self, text="Data Final:").grid(row=1, column=0, padx=5, pady=5)

        self.data_inicial_entry = ttk.Entry(self)
        self.data_final_entry = ttk.Entry(self)

        self.data_inicial_entry.grid(row=0, column=1, padx=5, pady=5)
        self.data_final_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Adicionar Sprint", command=self.add_sprint).grid(row=2, column=0, columnspan=2, pady=5)

    def add_sprint(self):
        data_inicial = self.data_inicial_entry.get()
        data_final = self.data_final_entry.get()

        if data_inicial and data_final:
            sprint = Sprint(len(self.parent.sprints) + 1, data_inicial, data_final, [])
            self.parent.sprints.append(sprint)
            self.atualiza_grid()
            self.destroy()
        else:
            messagebox.showwarning("Atenção", "Por favor, insira todas as informações válidas.")

    def atualiza_grid(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for sprint in self.parent.sprints:
            self.tree.insert('', tk.END, values=(sprint.id, sprint.dataIni, sprint.dataFim))