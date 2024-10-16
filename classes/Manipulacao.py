from datetime import datetime, timedelta
from typing import Dict, List

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

class Manipulacao:

    def __init__(self):
        pass

    # Conta dias úteis dentro de um intervalo de tempo
    def contar_dias_uteis(self, data_inicial, data_final):
        inicio = datetime.strptime(data_inicial, "%d/%m/%Y")
        fim = datetime.strptime(data_final, "%d/%m/%Y")
        
        dias_uteis = []
        dia = inicio
        
        while dia <= fim:
            if dia.weekday() < 5:  # 0 é segunda, 1 é terça, ..., 4 é sexta
                dias_uteis.append(dia.strftime("%d/%m/%Y"))
            dia += timedelta(days=1)
        
        return dias_uteis

    # Retorna vetor de qtd. de tarefas planejadas de forma constante até o final da sprint
    def planejado(self, qtdDias: int, qtdTarefas: int) -> List[int]:
        resultado = []
        decremento = qtdTarefas / (qtdDias - 1)  # Para garantir uma distribuição linear

        for i in range(qtdDias):
            valor = round(qtdTarefas - decremento * i)
            resultado.append(max(valor, 0))  # Garantindo valores positivos

        return resultado
    
    # Retorna um tupla com data e qtd de tarefas finalizadas por dia
    def contar_tarefas_finalizadas_por_dia(self, tarefas, data_inicial, data_final):
        inicio = datetime.strptime(data_inicial, "%d/%m/%Y")
        fim = datetime.strptime(data_final, "%d/%m/%Y")
        
        dias_uteis = self.contar_dias_uteis(data_inicial, data_final)
        tarefas_finalizadas_por_dia = {}

        # Converte datas de fechamento para objetos datetime
        fechamentos = {}
        for task_id, task_data in tarefas.items():
            for issue in task_data['issues']:
                closed_on = issue.get('closed_on', '')
                if closed_on:
                    fechamentos[task_id] = datetime.strptime(closed_on, "%Y-%m-%dT%H:%M:%SZ")

        # Classificar os fechamentos por dia útil
        for dia_util in dias_uteis:
            tarefas_finalizadas_por_dia[dia_util] = 0

        # Contabilizar tarefas finalizadas antes da sprint
        primeiro_dia_sprint = datetime.strptime(dias_uteis[0], "%d/%m/%Y")
        for task_id, fechamento in fechamentos.items():
            if fechamento < primeiro_dia_sprint:
                tarefas_finalizadas_por_dia[dias_uteis[0]] += 1
            elif fechamento.date() == primeiro_dia_sprint.date():
                tarefas_finalizadas_por_dia[dias_uteis[0]] += 1
            else:
                dia_util = fechamento.strftime("%d/%m/%Y")
                if dia_util in dias_uteis:
                    tarefas_finalizadas_por_dia[dia_util] += 1

        return sorted(tarefas_finalizadas_por_dia.items(), key=lambda x: x[0])
    
    # Monta gráfico de Burndown
    def grafico(self, df):
        # Criar o gráfico
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(df['dias'], df['planejado'], label='Planejado', color='green')
        ax.plot(df['dias'], df['realizado'], label='Realizado', color='blue')

        ax.set_xlabel('Dias Úteis')
        ax.set_ylabel('Quantidade de Tarefas')
        ax.set_title('Gráfico de Burndown')

        ax.legend()

        # Garantir que ambos os eixos contenham valores inteiros consecutivos
        max_value = max(max(df['planejado']), max(df['realizado']))
        x_values = range(1, len(df) + 1)
        y_values = range(1, max_value + 3)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Limites do eixo x e y
        ax.set_xlim(left=1, right=len(df))
        ax.set_ylim(bottom=0, top=max_value)

        ax.set_xticks(x_values)
        ax.set_yticks(y_values)

        # Atualizar as labels dos ticks
        ax.set_xticklabels(x_values)
        ax.set_yticklabels(y_values)

        plt.tight_layout()
        plt.show()

    # Criar o gráfico de barras - responsáveis
    def grafico_resp(self, df_grupos):
         
        plt.figure(figsize=(10, 6))  # Tamanho da figura
        plt.bar(df_grupos['Nome do Responsável'], df_grupos['Horas Estimadas'])

        # Config. o título e rótulos dos eixos
        plt.title('Total de Horas Estimadas por Responsável')
        plt.xlabel('Responsável')
        plt.ylabel('Total de Horas Estimadas')

        # Adiciona valores nos pontos das barras
        for i, v in enumerate(df_grupos['Horas Estimadas']):
            vlr_formatado = f"{v:.2f}"
            plt.text(i, v, vlr_formatado, ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

    
