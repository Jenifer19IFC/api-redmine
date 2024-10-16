import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from request.Request import Request
from datetime import datetime
from classes.Manipulacao import Manipulacao
import pandas as pd

class JanelaTarefas(tk.Toplevel):

    def __init__(self, parent, sprint):   
        super().__init__(parent)
        self.on_close = self.close_window
        
        # Título
        self.title(f"Detalhes da Sprint {sprint.id} - {sprint.dataIni} à {sprint.dataFim}")
        self.geometry("800x600")
        self.resizable(True, True)

        # Flag para indicar se a janela está aberta
        self.is_open = True

        # Armazena sprint
        self.sprint = sprint

        self.total_tarefas = 0
        self.diasUteis = 0
        self.nome_projeto = ''
    
        # Inicializar a classe Request
        self.request = Request(
            base_url="http://fabtec.ifc-riodosul.edu.br/issues.json",
            key="****"
        )

        # Config. grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame para o Treeview
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Treeview p/  as tarefas
        self.columns = ('Id', 'Data Fechamento')
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show='headings')
        
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        # self.tree.column('Id', width=50, anchor="center")
        # self.tree.column('Data Fechamento', width=140, anchor="center")

        # Barra de rolagem vertical para o Treeview
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.dados = {}

         # Frame para exibir os resultados escritos
        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)

         # Atualizar o frame para exibir o nome do projeto
        self.sprint_frame = ttk.Frame(self.result_frame)
        self.sprint_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Label com o nome do projeto
        self.nome_projeto_label = ttk.Label(self.sprint_frame, text=f"Nome do Projeto: {self.nome_projeto}", font=("Arial", 12), wraplength=300)
        self.nome_projeto_label.pack(fill="x")
        self.nome_projeto_label.grid(row=0, column=0, padx=10, sticky="w")

        # Frame para exibir as quantidades de tarefas
        self.qtd_tarefas_frame = ttk.Frame(self.result_frame)
        self.qtd_tarefas_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Config. o grid para o qtd_tarefas_frame
        self.qtd_tarefas_frame.grid_columnconfigure(0, weight=1)
        self.qtd_tarefas_frame.grid_columnconfigure(1, weight=1)

        # Label para Tarefas Finalizadas
        self.finalizadas_label = ttk.Label(self.qtd_tarefas_frame, text="Tarefas Finalizadas: 0", font=("Arial", 12))
        self.finalizadas_label.grid(row=0, column=0, padx=10, sticky="w")

        # Label para Tarefas Não Finalizadas
        self.nao_finalizadas_label = ttk.Label(self.qtd_tarefas_frame, text="Tarefas Não Finalizadas: 0", font=("Arial", 12))
        self.nao_finalizadas_label.grid(row=0, column=1, padx=10, sticky="w")

        # Iniciar a thread para fazer as requisições
        # self.thread = threading.Thread(target=self.realizar_requisicoes, daemon=True)
        # self.thread.start()
        self.realizar_requisicoes()

        # Vincular o evento de fechar a janela para interromper as requisições (se necessário)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def realizar_requisicoes(self):
        json_respostas = {}
        for tarefa in self.sprint.listaTarefas:
            if not self.is_open:
                print("Janela fechada antes de concluir as requisições.")
                return
            tarefa_id = tarefa.id
            print(f"Iniciando requisição para Task ID: {tarefa_id}")  
            resposta = self.request.fazer_requisicao(tarefa_id)
            if resposta:
                json_respostas[tarefa_id] = resposta
                print(f"Requisição bem-sucedida para Task ID: {tarefa_id}")  
            else:
                json_respostas[tarefa_id] = {"error": "Falha na requisição ou dados não disponíveis."}
                print(f"Requisição falhou para Task ID: {tarefa_id}")  

        self.total_tarefas = len(self.sprint.listaTarefas)
        print('\nTOTAL DE TAREFAS NA SPRINT: ', self.total_tarefas, '\n')

        # Criar uma nova thread para exibir o JSON e atualizar o Treeview
        import pandas as pd

        def processa_resultados():
            # self.exibir_json(json_respostas)
            self.after(0, self.atualizar_treeview, json_respostas)
            
            manipulacao = Manipulacao()
            print('\nQTD. DE TAREFAS FINALIZADAS POR DIA:')
            finalizadasPorDia = manipulacao.contar_tarefas_finalizadas_por_dia(json_respostas, self.sprint.dataIni, self.sprint.dataFim)
            print(finalizadasPorDia)
            print('\n')
            
            print('QTD. DE DIAS ÚTEIS:')
            self.diasUteis = manipulacao.contar_dias_uteis(self.sprint.dataIni, self.sprint.dataFim)
            print(len(self.diasUteis))
            print('\n')
            
            print('PLANEJADO: ')
            planejado = manipulacao.planejado(len(self.diasUteis), self.total_tarefas)
            for i, valor in enumerate(planejado):
                print(f"Dia {i+1}: {valor} tarefas")
            
            print('\nDias úteis:')
            print(self.diasUteis)

            finalizadasPorDia.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))
            
            print('------- DATAFRAME PARA burndown--------------\n')

            df = pd.DataFrame({
                'dias': range(1, len(self.diasUteis) + 1),
                'planejado': planejado,
                'finalizado': [x[1] for x in finalizadasPorDia]  # Somente os valores finalizados
            })
            
            # Calcula e add coluna 'realizado'
            total_tarefas = self.total_tarefas
            df['realizado'] = total_tarefas - df['finalizado'].cumsum()
            
            print(df)


            print('---------------------\n')

            # Calcular tarefas finalizadas e não finalizadas
            total_finalizado = df['finalizado'].sum()
            tarefas_nao_finalizadas = self.total_tarefas - total_finalizado


            # Extrair o nome do projeto da resposta JSON
            self.nome_projeto = self.obter_nome_do_projeto(resposta)
            self.after(0, lambda: self.nome_projeto_label.config(text=f"Nome do Projeto: {self.nome_projeto}"))

            # Atualizar as labels com as contagens
            self.after(0, lambda: self.finalizadas_label.config(text=f"Tarefas Finalizadas: {total_finalizado}"))
            self.after(0, lambda: self.nao_finalizadas_label.config(text=f"Tarefas Não Finalizadas: {tarefas_nao_finalizadas}"))

            # POR RESPONSÁVEL
            print('DF POR RESPONSÁVEL')
            df_detalhado = self.cria_df_responsaveis(json_respostas)
            print(df_detalhado)

            # Agrupa pelo responsável e somar as horas estimadas
            df_grupos = df_detalhado.groupby('Nome do Responsável')['Horas Estimadas'].sum().reset_index()

            # manipulacao.grafico(df)
            self.after(0, manipulacao.grafico(df)) # Gráfico de burndown
            self.after(0, manipulacao.grafico_resp(df_grupos)) # Gráfico de responsáveis

            # -----------------------------------------------------------------------------------


        # threading.Thread(target=processa_resultados).start()
        processa_resultados()


    def close_window(self):
        self.is_open = False
        self.destroy()

    def atualizar_treeview(self, dados):
        print('Atualizando Treeview')
        print('\nRESPOSTA GERAL JSON:', dados)
        print('\n')
        if not self.winfo_exists():
            print("JanelaTarefas foi fechada antes de atualizar o Treeview.")
            return
        try:
            # Limpar os itens existentes para evitar duplicação
            for item in self.tree.get_children():
                self.tree.delete(item)

            for task_id, task_data in dados.items():
                for issue in task_data['issues']:
                    closed_on = issue.get('closed_on', '')
                    print(f"Atualizando item {issue['id']} com data de fechamento: {closed_on}")
                    if closed_on:
                        # Converter a data para o formato dd/mm/aaaa
                        data_formatada = datetime.strptime(closed_on, "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                        self.tree.insert('', tk.END, values=(issue['id'], data_formatada))
            print("Treeview atualizado com sucesso")
        except Exception as e:
            print(f"Erro ao atualizar Treeview: {e}")

    def cria_df_responsaveis(self, dados):
        lista_dados = []
        
        for task_id, task_data in dados.items():
            for issue in task_data['issues']:
                assigned_to = issue.get('assigned_to', {}).get('name', 'Não atribuído')
                total_estimated_hours = issue.get('total_estimated_hours', 0)
                
                lista_dados.append({
                    'ID da Tarefa': issue['id'],
                    'Nome do Responsável': assigned_to,
                    'Horas Estimadas': total_estimated_hours
                })
        
        df = pd.DataFrame(lista_dados)
        return df

    def obter_nome_do_projeto(self, resposta):
        issues = resposta.get('issues', [])
        if issues:
            return issues[0].get('project', {}).get('name', 'Não informado')
        return 'Não informado'
