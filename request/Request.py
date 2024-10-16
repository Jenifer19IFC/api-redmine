import requests
import json

class Request:
    
    def __init__(self, base_url, key):
        self.base_url = base_url
        self.key = key

    def fazer_requisicao(self, id_tarefa):
        url = f"{self.base_url}?issue_id={id_tarefa}&key={self.key}&status_id=*"

        try:
            resposta = requests.get(url, timeout=15)
            
            if resposta.status_code == 200:
                return resposta.json()
            else:
                print(f"Falha na requisição. Código de status: {resposta.status_code}")
                print(resposta.text)
                return None
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    def imprimir(self, issue_id):
        issues = self.fazer_requisicao(issue_id)
        
        if issues:
            print(json.dumps(issues, indent=2))
        else:
            print("Não foi possível obter os dados das tarefas.")


# # Como usar a classe
# base_url = "http://fabtec.ifc-riodosul.edu.br/issues.json"
# chave = "b7c238adc2c0af943c1f0fa9de6489ce190bd6d5"

# requisicao = Request(base_url, chave)

# ids_tarefas = [103, 104, 105]

# for id_tarefa in ids_tarefas:
#     requisicao.imprimir(id_tarefa)
#     print("\n" + "-"*50 + "\n")  
