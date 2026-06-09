# Dashboard_porsche
Projeto de dashboard com dados sanitizado pelo recurso Ia reports utilizado a Porsche como exemplo
Porsche Sales Intelligence 🏁

Executive Analytics & Data Sanitization Pipeline

O Porsche Sales Intelligence é uma plataforma analítica integrada que resolve um dos maiores desafios de concessionárias de luxo: a inconsistência em relatórios manuais de vendas (raw data). Utilizando um Agente Inteligente de Sanitização desenvolvido sob regras rígidas de Schema e uma Dashboard Executiva de Alta Performance inspirada na identidade oficial da Porsche, o projeto transforma registros complexos em insights acionáveis imediatos.

🏛️ O Desafio de Negócio

No mercado de automóveis de alta gama, a precisão das informações reflete a sofisticação da marca. No entanto, planilhas brutas de vendas frequentemente chegam com severas anomalias:

Preços em múltiplos formatos e moedas ($121k, 104,500 USD, 96.800 USD).

Quilometragens misturadas entre Milhas (mi) e Quilômetros (km), além de termos qualitativos (new, zero miles).

Datas incorretas ou impossíveis no calendário (como 2024-02-30 ou April 31st).

Nomes de modelos da Porsche e métodos de pagamento com erros de digitação e espaçamento irregular.

⚙️ Engenharia da Solução

1. O Agente de Sanitização (Pandas Pipeline)

Desenvolvido em Python, este agente atua como um portão de qualidade rigoroso, aplicando as diretrizes exatas de validação corporativa:

Padronização Temporal: Normalização de todas as datas de vendas válidas para o formato ISO YYYY-MM-DD (e marcação cirúrgica de anomalias como INVALID).

Tratamento de Moedas: Extração limpa do valor numérico, tratamento de abreviações financeiras (k) e exportação final em float decimal de precisão (.2f).

Conversão de Métrica de Uso: Conversão dinâmica e inteligente de Km para Milhas ($1 \text{ km} = 0.621371 \text{ mi}$) com arredondamento exato.

Preservação de Integridade: Novas colunas higienizadas são inseridas imediatamente após as originais para facilitar auditorias rápidas (Quality Checks).

2. O Dashboard de Alta Performance (UI/UX Porsche Style)

Inspirado na sofisticação minimalista do portal da Porsche Brasil, o dashboard foi desenvolvido para diretores e analistas de mercado.

Estética Premium: Paleta em Obsidian Black (#0A0A0A), Titanium Gray (#1C1C1C) e o icônico realce vermelho Guards Red (#D5001C).

Filtros Cruzados: Segmentação instantânea por Modelo, Ano do Modelo, Cidade, Método de Pagamento e Período de Venda.

Perguntas de Negócio Respondidas:

Distribuição por Cidade: Quais modelos específicos lideram as vendas em cada praça geográfica?

Análise de Ciclo: Qual ano-modelo (Model Year) registrou maior volume transacionado no período selecionado?

Guia de Preferência Regional (Insight Inteligente): Algoritmo sob demanda que identifica em tempo real o modelo dominante (carro popular de vendas) para cada cidade, moldando estratégias de estoque local.

📊 Arquitetura Tecnológica

A suíte analítica foi construída priorizando portabilidade, leveza e usabilidade:

Backend / Sanitização: Python 3, biblioteca Pandas, RegEx para processamento complexo de padrões textuais.

Frontend / Dashboard: HTML5 semântico, Tailwind CSS (Design System Premium), Chart.js (Gráficos interativos em alta definição) e PapaParse (Leitor e parser de dados em memória do navegador).

🚀 Como Executar o Ecossistema

Executando o Agente de Sanitização (Python)

Instale as dependências básicas:

pip install pandas


Coloque o arquivo bruto (porchet_amostragem.csv) no mesmo diretório do script.

Execute o agente:

python agent_sanitizer.py


O arquivo higienizado porchet_sanitize.csv será gerado automaticamente com as colunas duplicadas e validadas.

Visualizando a Dashboard Executiva (HTML/JS)

Abra o arquivo dashboard.html diretamente em qualquer navegador moderno.

O sistema pré-carregará uma amostra de dados reais para teste de interface.

Para testar o seu próprio volume de dados higienizado, basta arrastar ou fazer o upload do arquivo porchet_sanitize.csv na área indicada no cabeçalho do painel.

📈 Visualizações & Insights Executivos

┌─────────────────────────────────────────────────────────────┐
│                 PORSCHE SALES INTELLIGENCE                  │
├─────────────────────────────────────────────────────────────┤
│  [ Faturamento ]     [ Entregas ]     [ Ticket Médio ]      │
│   R$ 1.631.250,00         14             R$ 116.517,86      │
├─────────────────────────────────────────────────────────────┤
│  ▲ Preferência Regional (Insight Dinâmico por Cidade)       │
│    - Boston: 718 Cayman  - Seattle: 911 Turbo S             │
│    - Austin: Cayenne     - Denver: Macan S                  │
└─────────────────────────────────────────────────────────────┘


Este projeto exemplifica a aplicação de Governança de Dados aplicada à inteligência de vendas de alta performance.
