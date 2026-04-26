import logging
from services import load_data, exportar_inadimplentes, exportar_total_por_pessoa,calcular_total_geral_mes, listar_inadimplentes,calcular_total_por_pessoa, filtrar_transacoes
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    encoding="UTF-8",
    format="[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    try:
        dados = load_data("/home/thiago/Projetos-python/praticando/desafio05/data/transacoes.json")
        dados_filtrados = list(filtrar_transacoes(dados))
        total_p = calcular_total_por_pessoa(dados_filtrados)
        exportar_total_por_pessoa(total_p)
        
        inadi = listar_inadimplentes(dados_filtrados)
        exportar_inadimplentes(inadi)
        
    except (ValueError, FileNotFoundError) as e:
        logger.exception(f"Erro ao processar transações | erro='{e}'")
        
    except Exception as e:
        logger.exception(f"Erro inesperado | erro='{e}'")
if __name__ == "__main__":
    main()