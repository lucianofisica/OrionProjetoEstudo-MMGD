# OrionProjetoEstudo-MMGD

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um pipeline completo de Engenharia de Dados, processando um dataset sobre Micro e Mini Geração Distribuída (MMGD), com foco na geração fotovoltaica. O pipeline seguirá todas as etapas do processo profissional de ETL (Extração, Transformação e Carga), utilizando ferramentas open source amplamente utilizadas no mercado.

## ☀️ O que é Geração Distribuída Fotovoltaica?

A **Geração Distribuída (GD)** é um modelo descentralizado de produção de energia elétrica, regulamentado pela **Resolução Normativa ANEEL nº 482/2012**, que permite aos consumidores brasileiros gerarem sua própria energia a partir de **fontes renováveis** — como a energia solar fotovoltaica — no local ou nas proximidades do ponto de consumo. 

A energia excedente pode ser injetada na rede da distribuidora local, sendo posteriormente compensada na fatura do consumidor por meio do **Sistema de Compensação de Energia Elétrica (SCEE)**. Isso significa que a rede elétrica funciona como uma espécie de "créditos gerados”: durante o dia, o sistema gera energia que pode ser usada à noite ou em outro momento, inclusive em outras unidades consumidoras do mesmo titular, dependendo da modalidade de adesão.

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
| 2    | Upload de Dados Reais no Data Lake       | MinIO / Script de Upload            | Upload de dados da ANEEL no bucket `landing-zone` (camada Bronze).                                                                                    | ✅ Feito       |
| 3    | Exploração e Validação Inicial           | DuckDB / Script Python              | Conexão via S3 para análise exploratória dos dados (contagem, tipos, estatísticas, consistência básica).                                            | ✅ Feito       |
| 4    | Registro de Metadados                    | Hive Metastore / Trino              | Criação de tabelas externas vinculadas ao dataset armazenado no MinIO (definindo esquemas, particionamentos etc).                                     | ✅ Feito       |
| 5    | Consultas SQL Distribuídas               | Trino                               | Execução de queries sobre os dados brutos e transformados, conectando Trino ao Hive Metastore e aos buckets do MinIO.                                 | ✅ Feito       |
| 6    | Transformações e Modelagem de Dados      | dbt (Data Build Tool)               | Criação de modelos em três camadas: `bronze` (fonte), `silver` (staging/limpeza) e `gold` (marts/agregados).                                          | ✅ Feito       |
| 7    | Execução Automatizada do Pipeline        | Apache Airflow                      | Orquestração de todas as etapas anteriores em um DAG com tarefas encadeadas (sensor de arquivo, execução do dbt, testes).                               | ✅ Feito       |
| 8    | Visualização e Análise de Métricas       | Superset                            | Criação de dashboards com métricas extraídas das tabelas da camada Gold para análise de negócio ou exploração interativa.                             | ✅ Feito       |

---

## 🚀 Como Executar o Pipeline

1.  **Pré-requisitos:**
    *   Docker e Docker Compose instalados.
    *   Um arquivo de dados da ANEEL (ex: `dados-aneel.csv`).

2.  **Setup Inicial:**
    *   Clone o repositório.
    *   Crie um arquivo `.env` a partir do `.env.example` e, se desejar, altere as senhas.
    *   Execute `docker-compose up --build -d` para iniciar todos os serviços (MinIO, Trino, Airflow, Superset, etc.). Pode levar alguns minutos na primeira vez.

3.  **Carregar os Dados Brutos:**
    *   Use o script `upload_data.sh` para enviar seu arquivo de dados para o MinIO:
      ```bash
      ./upload_data.sh /caminho/para/seus/dados-aneel.csv
      ```

4.  **Registrar a Tabela Externa:**
    *   Execute o script para criar a tabela no Hive Metastore via Trino:
      ```bash
      pip install -r requirements.txt
      python scripts/criar_tabela_externa.py
      ```

5.  **Executar o Pipeline de Transformação via Airflow:**
    *   Acesse a UI do Airflow em `http://localhost:8081` (login: `admin`, senha: `admin`).
    *   **Configure a Conexão S3:**
        *   Vá para `Admin -> Connections -> Add a new record`.
        *   **Connection ID:** `minio_s3_connection`
        *   **Connection Type:** `Amazon S3`
        *   **Extra:** `{"host": "http://datalake:9000", "aws_access_key_id": "minioadmin", "aws_secret_access_key": "minioadmin"}`
    *   **Configure as Variáveis do Airflow:**
        *   Vá para `Admin -> Variables -> Add a new record`.
        *   Crie a variável `DBT_TRINO_HOST` com o valor `trino-coordinator`.
    *   Ative a DAG `aneel_mmgd_pipeline` e dispare uma execução manual.

## 📊 Visualização e Análise de Métricas (Superset)

Após a execução bem-sucedida do pipeline no Airflow, os dados transformados estarão disponíveis na camada `gold`. Você pode explorá-los usando o Superset.

1.  **Acesse o Superset:**
    *   Abra `http://localhost:8088` no seu navegador.
    *   Faça login com as credenciais padrão: `admin` / `admin`.

2.  **Conecte o Superset ao Trino:**
    *   Vá para `Settings -> Database Connections -> + Database`.
    *   Selecione `Trino` como o banco de dados.
    *   **SQLAlchemy URI:** `trino://admin@trino-coordinator:8080/hive`
    *   Clique em `Test Connection` para verificar se funciona e, em seguida, em `Connect`.

3.  **Adicione um Dataset:**
    *   Vá para `Datasets -> + Dataset`.
    *   **Database:** Selecione a conexão Trino que você acabou de criar.
    *   **Schema:** `gold`
    *   **Table:** `potencia_total_por_fabricante`
    *   Clique em `Add`.

4.  **Crie um Gráfico:**
    *   Você será redirecionado para a página de exploração do novo dataset.
    *   **Visualization Type:** `Bar Chart`
    *   **X-Axis:** `fabricante_modulo`
    *   **Metrics:** `SUM(potencia_total_instalada_kw)`
    *   Clique em `Create Chart`. Agora você pode visualizar a potência total por fabricante e salvar seu gráfico em um dashboard.

## 👥 Autores

### 🧑‍🔧 Magno Hortêncio  
📧 [magno.araujo@ceca.ufal.br](mailto:magno.araujo@ceca.ufal.br)  
🔗 [LinkedIn](https://www.linkedin.com/in/magno-hortencio)

> Me chamo Magno e atualmente sou estudante do curso de Engenharia de Energias pela UFAL. Tenho focado meus estudos e minha carreira como projetista, com especialização em sistemas fotovoltaicos e eficiência energética. Com isso, estou entusiasmado em aplicar meu conhecimento para criar soluções sustentáveis e inovadoras no campo das energias renováveis.

---

### 👨‍💻 Luciano Júnior
📧 [luciano.bezerra@fis.ufal.br](mailto:luciano.bezerra@fis.ufal.br)  
🔗 [LinkedIn](https://www.linkedin.com/in/luciano-j-r-bezerra-jr-002634141/)

> Me chamo Luciano, sou físico e também sou aluno do curso de Engenharia de Software pela Estácio. Tenho experiência em Física da Matéria Condensada, sou usuário linux e programo em C e Fortran desde 2015 no meio acadêmico. Além disso, já utilizei ferramentas Open Source para análise e visualização de dados tais como Python, Gnuplot e Grace. Já participei de outros cursos complementares como uma school de visualização de dados, onde tive um primeiro contato com Tableau e Power BI, Django Girls, Imersão Alura, GCP e New Relic. Tenho interesse na área de Dados, DevOps e em Desenvolvimento.

---
