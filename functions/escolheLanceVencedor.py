from queues.filaLances import filaLances
import json

# Caminho para o arquivo JSON da base de dados de lances
baseDadosLances = "./schema/baseDadosRecebedores.json"

def escolheLanceVencedor(produto):
    '''
    Escolhe o lance vencedor para um determinado produto e atualiza a base de dados.
    O lance vencedor será o de maior valor.
    
    Exemplo de uso:
    escolheLanceVencedor("Vaso Histórico")
    '''
    vencedor = None
    maior_valor = 0
    
    try:
        with open(baseDadosLances, 'r') as file:
            lances = json.load(file)
        
        while not filaLances.empty():
            lance = filaLances.get()
            
            if lance['produto'] == produto:
                if lance['valor'] > maior_valor:
                    maior_valor = lance['valor']
                    vencedor = lance

                lances.append(lance)
        
        if vencedor:
            print(f"O vencedor do lance para o produto {produto} é: {vencedor}")
            
            lances_dict = {
                "lances": lances,
                "vencedor": vencedor
            }
            
            with open(baseDadosLances, 'w') as file:
                json.dump(lances_dict, file, indent=4)
            
            return vencedor
        else:
            print(f"Nenhum lance encontrado para o produto {produto}")
            return None
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None