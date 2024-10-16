# id (autoincrement), data inicial, data final, lista de tarefas

class Sprint:

    def __init__(self, id, dataIni, dataFim, listaTarefas):
        self.id = id
        self.dataIni = dataIni
        self.dataFim = dataFim  
        self.listaTarefas = listaTarefas   

    def adicionar_tarefa(self, tarefa):
        self.listaTarefas.append(tarefa)
