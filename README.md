# financial_report

Sistema de análise financeira de transações com exportação CSV.

## O que faz
- Carrega transações de um arquivo JSON
- Agrega total por pessoa (apenas RECEIVED)
- Lista inadimplentes (OVERDUE e PENDING)
- Exporta relatórios em CSV

## Estrutura

financial_report/
├── data/
│   └── transacoes.json
├── entities/
│   └── transacao.py
├── services/
│   ├── load_data.py
│   ├── process_data.py
│   └── export_csv.py
├── main.py
└── requirements.txt


## Como rodar
pip install -r requirements.txt
python main.py
