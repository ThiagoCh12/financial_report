import csv
import logging 

logger = logging.getLogger(__name__)

def exportar_total_por_pessoa(total_p: dict):
    """
    escreve os dados de um dict em um arquivo csv
    Args:
        total_p: dict com dados por pessoa.
    {
        'customer': 
        {
            'customer_name': 'thiago',
            'total': 149,90
        }
    }
    """
    logger.info("Iniciando exportação de total por pessoa.")
    if not total_p:
        raise ValueError("Não foi possivel exportar os dados | dicionario vazio")
    
    fields = ['customer'] + list(next(iter(total_p.values())).keys())
    
    with open('total_por_pessoa.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        
        #Isso é uma Generator Expression, semelhante a uma List Comprehesion, porém mais eficiente
        #Unpacking ** para acessar as chaves do dicionario interno
        linhas = ({'customer': k, **v}for k, v in total_p.items())
        
        writer.writerows(linhas)
    logger.info(f"Exportação de dados concluída com sucesso | {csvfile.name}")
        
        
def exportar_inadimplentes(inadimplentes: dict):
    """
    Exporta as transacoes inadimplentes para .csv
    Args: 
        dict: dados de transacoes inadimplentes
            {
                id:id
                {
                    'customer':customer
                    'customer_name': customer_name,
                    'value': value,
                    'billing_type': billing_type,
                    'status': status
                }
            }
    """
    if not inadimplentes:
        logger.error("Não foi possivel exportar os dados | dicionario vazio")
        
    fields = ['id'] + list(next(iter(inadimplentes.values())).keys())
    
    with open('transacoes_inadimplentes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        
        rows = ({'id': k, **v}for k, v in inadimplentes.items())
        
        writer.writerows(rows)
    logger.info("Exportacao concluida com sucesso.")