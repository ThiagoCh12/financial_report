import logging
import json, logging
from collections import defaultdict
from collections.abc import Iterator, Iterable
from datetime import datetime
from entities.transacao import Transacao
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def load_data(path:Path)->list[dict]:
    """Carrega arquivo json e retorna dicionario
    Args:
        path: caminho do arquivo json
    Returns:
        Dict: dicionario com os dados
    
    """
    logger.info("Load data iniciado")
    if not Path(path).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: '{path}'")
    
    with open(path, "r", encoding="UTF-8") as f:
        dados = json.load(f)
        
    if not dados:
        raise ValueError(f"Arquivo vazio | path='{path}'")
    
    logger.info(f"Dados carregados com sucesso | path='{path}'")
    return dados
    

def filtrar_transacoes(data: list[dict]) -> Iterator[Transacao]:
    """Filtra dados brutos de uma lista de dicionarios iterando 
    sobre cada item que seja compativel com o objeto Transacao, 
    retornando um de cada vez e descartando o anterior, 
    garantindo menos consumo de memória.
    Args:
        data: lista de dicionario com os dados das transacoes
    Returns:
        transacao: objeto válido é retornado e descartado em seguida."""
    
    logger.info(f"Iniciando filtragem de {len(data)} itens.")
    
    itens_validos = 0
    for item in data:
        try:
            transacao = Transacao.from_dict(item) 
            itens_validos += 1
            yield transacao
        except ValueError as e:
            id_item = item.get('id', 'SEM_ID')
            logger.warning(f"Item {id_item} descartado por inconsistência de dados | erro='{e}'")
            
    logger.info(f"Filtragem concluída. {itens_validos} transações processadas com sucesso.")
    
    
def calcular_total_por_pessoa(transacoes: Iterable[Transacao]) -> dict[str, float]:
    """
    Calcula total em valor por pessoa de transações recebidas.
    Args: 
        transacoes:  recebe qualquer objeto iterável do tipo Transacao.
    Returns:
        totais: dicionario com total por pessoa
    """
    logger.info("Iniciando calculo total por pessoa")
    
    totais = defaultdict(dict)
    cont_transacao = 0
    for item in transacoes:
        if item.status.upper() == 'RECEIVED':
            totais[item.customer] = {
                "customer_name":item.customer_name,
                "total": totais.get(item.customer, {}).get('total', 0) + item.value
            }
            cont_transacao += 1
      
    logger.info(f"Calculo de total por pessoa finalizado | trasacoes={cont_transacao}")
    return dict(totais)


def calcular_total_geral_mes(
    transacoes: Iterable[Transacao], 
    mes: int,
    ano: int
    ) -> float:
    """Calcula total de transações recebidas no mês.
    Args:
        transacoes: iterável de objetos Transacao
        mes: mês de referência (1-12)
        ano: ano de referência
    Returns:
        Total em float das transações RECEIVED no período.
    """
    logger.info(f"Iniciando calculo total geral de {ano}/{mes}")
    
    total = 0.0
    count = 0
    for item in transacoes:
        if ano == item.due_date.year and mes == item.due_date.month:
            if item.status.upper() == 'RECEIVED':
                total += item.value 
                count += 1
    logger.info(f"Total geral de {ano}/{mes} calculado com sucesso | {count} transações calculadas")
    return total


def listar_inadimplentes(transacoes: Iterable[Transacao]) -> dict[dict]:
    """
    lista transações inadimplentes.
    Args:
        transacoes: Iteravel do tipo Transacao
    Returns
        inadimplentes: dicionario de transações inadimplentes
    """
    logger.info("Iniciando listagem de inadimplentes")
    inadimplentes = {}
    
    for item in transacoes:
        if item.status.upper() in ('OVERDUE', 'PENDING'):
            inadimplentes[item.id] = {
                'customer':item.customer,
                'customer_name': item.customer_name,
                'value': item.value,
                'billing_type': item.billing_type,
                'status': item.status
            }
    logger.info(f"Listagem de inadimplentes finalizada com sucesso | inadimplentes={len(inadimplentes)}")
    return inadimplentes