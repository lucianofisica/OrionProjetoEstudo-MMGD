# OrionProjetoEstudo-MMGD

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um pipeline completo de Engenharia de Dados, processando um dataset sobre Micro e Mini Geração Distribuída (MMGD), com foco na geração fotovoltaica. O pipeline seguirá todas as etapas do processo profissional de ETL (Extração, Transformação e Carga), utilizando ferramentas open source amplamente utilizadas no mercado.

## ☀️ O que é Geração Distribuída Fotovoltaica?

A **Geração Distribuída (GD)** é um modelo descentralizado de produção de energia elétrica, regulamentado pela **Resolução Normativa ANEEL nº 482/2012**, que permite aos consumidores brasileiros gerarem sua própria energia a partir de **fontes renováveis** — como a energia solar fotovoltaica — no local ou nas proximidades do ponto de consumo. 

A energia excedente pode ser injetada na rede da distribuidora local, sendo posteriormente compensada na fatura do consumidor por meio do **Sistema de Compensação de Energia Elétrica (SCEE)**. Isso significa que a rede elétrica funciona como uma espécie de “bateria virtual”: durante o dia, o sistema gera energia que pode ser usada à noite ou em outro momento, inclusive em outras unidades consumidoras do mesmo titular, dependendo da modalidade de adesão.

Esse modelo promove benefícios como:
- Redução na conta de energia;
- Maior autonomia e sustentabilidade;
- Menor sobrecarga nas redes de transmissão;
- Incentivo ao uso de fontes limpas e renováveis.

### ⚡ O que é Micro e Minigeração Distribuída (MMGD)?

A **Microgeração** e a **Minigeração Distribuída (MMGD)** são categorias específicas da Geração Distribuída, definidas com base na **potência instalada** do sistema gerador:

- **Microgeração Distribuída**: sistemas com potência instalada de até **75 kW**.
- **Minigeração Distribuída**: sistemas com potência superior a **75 kW** e menor ou igual a **3 MW** (ou até **5 MW** em casos especiais, conforme a Lei nº 14.300/2022).

Ambas devem estar conectadas à rede de distribuição por meio de instalações de unidades consumidoras.

Além do **autoconsumo local**, há outras modalidades de participação no SCEE, como:
- **Autoconsumo remoto** (compensação em outra unidade do mesmo titular);
- **Geração compartilhada** (por consórcio ou cooperativa);
- **Empreendimentos com múltiplas unidades consumidoras** (ex: condomínios).

A MMGD é uma alternativa moderna à geração centralizada e incentiva a autossuficiência energética, promovendo consciência ambiental e economia de longo prazo.

🔗 Saiba mais sobre Geração Distribuída em:  
[https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida](https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida)

## 🗂️ Contexto dos Dados

Originalmente, a proposta do projeto previa o desenvolvimento, em dupla (com supervisão do ORION), de um pipeline baseado em um dataset com 1 bilhão de linhas de dados fictícios gerados por script Python. Entretanto, **Magno**, meu parceiro de projeto, sugeriu o uso de dados reais fornecidos publicamente pela **ANEEL (Agência Nacional de Energia Elétrica)**. A proposta foi bem recebida e **apoiada pelos supervisores**, o que enriquece ainda mais a relevância e aplicabilidade do projeto.

🔗 Os dados utilizados neste projeto podem ser acessados diretamente através do portal de dados abertos da ANEEL:  
[https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida)

## 📊 Sobre o Dataset

O arquivo `.csv` utilizado neste projeto contém **12 colunas** e **3.643.608 de linhas**, com informações detalhadas sobre unidades de geração distribuída de energia elétrica fotovoltaica no Brasil.

### 📁 Estrutura das Colunas

| Nº | Nome da Coluna              | Descrição                                                                                  |
|----|-----------------------------|--------------------------------------------------------------------------------------------|
| 0  | `_id`                       | Identificador único de cada linha no dataset.                                              |
| 1  | `Data_Geracao_Dados`        | Data de geração e publicação dos dados pela plataforma pública.                           |
| 2  | `Codigo_Unidade_Geradora`   | Identificador único da unidade geradora (como um "CPF" da usina).                         |
| 3  | `Total_Area_Arranjo`        | Área total ocupada pelos módulos fotovoltaicos (em m²).                                   |
| 4  | `Potencia_Instalada`        | Potência nominal total instalada da unidade (em kW).                                      |
| 5  | `Fabricante_Modulo`         | Nome do fabricante dos módulos fotovoltaicos.                                             |
| 6  | `Fabricante_Inversor`       | Nome do fabricante dos inversores (equipamento que converte corrente contínua em alternada). |
| 7  | `Data_conexao_Unidade`      | Data de conexão à rede elétrica (início efetivo da operação).                             |
| 8  | `Potencia_Modulos`          | Potência somada de todos os módulos instalados (em kW).                                   |
| 9  | `Potencia_Inversor`         | Potência somada de todos os inversores conectados (em kW).                                |
| 10 | `Quantidade_Modulos`        | Quantidade total de módulos/painéis instalados.                                           |
| 11 | `Nome_Modelo_Modulo`        | Nome técnico do modelo dos módulos fotovoltaicos.                                         |
| 12 | `Nome_Modelo_Inversor`      | Nome técnico do modelo dos inversores.                                                    |

---

## 🔄 Etapas do Pipeline de Dados

| Fase | Etapa                                    | Ferramenta(s)                       | Descrição                                                                                                                                             | Status Atual   |
|------|------------------------------------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| 1    | Coleta de Dados Reais sobre MMGD         | [Download em Site](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida) | Dados reais com grande volume (3.643.608 linhas), com estrutura definida e salva em `.csv`.                                                          | ✅ Feito       |
| 2    | Upload de Dados Reais no Data Lake       | MinIO                               | Upload de dados da ANEEL no bucket `landing-zone` (camada Bronze).                                                                                    | ✅ Feito       |
| 3    | Exploração e Validação Inicial           | DuckDB                              | Conexão local ou via S3 para análise exploratória dos dados (contagem, tipos, estatísticas, consistência básica).                                     | 🔄 Em andamento |
| 4    | Registro de Metadados                    | Hive Metastore                      | Criação de tabelas externas vinculadas ao dataset armazenado no MinIO (definindo esquemas, particionamentos etc).                                     | ⚠ Não iniciada |
| 5    | Consultas SQL Distribuídas               | Trino (Presto)                      | Execução de queries sobre os dados brutos e transformados, conectando Trino ao Hive Metastore e aos buckets do MinIO.                                 | ⚠ Não iniciada |
| 6    | Transformações e Modelagem de Dados      | DBT                                 | Criação de modelos em três camadas: `staging` (tipos), `intermediate` (limpeza/enriquecimento) e `mart` (fatos/dimensões).                            | ⚠ Não iniciada |
| 7    | Execução Automatizada do Pipeline        | Apache Airflow                      | Orquestração de todas as etapas anteriores em um DAG com tarefas encadeadas (geração, upload, validação, DBT etc.).                                   | ⚠ Não iniciada |
| 8    | Visualização e Análise de Métricas (op.) | Superset/Metabase                   | Criação de dashboards com métricas extraídas das tabelas da camada Gold para análise de negócio ou exploração interativa.                             | ⚠ Não iniciada |
