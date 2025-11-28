from queues.filaLances import filaLances

def efetuaLance(lance):
    '''
    Adiciona um lance à fila de lances.
    Exemplo de lance:
    {"valor": 100, 
    "moeda": "BRL", 
    "produto": "Vaso Histórico"
    }
    '''
    filaLances.put(lance)