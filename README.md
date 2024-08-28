# Rossmann Sales Forecast
![Rossmann Store](img/readme_img/rossmann.webp)

A Rossmann é uma das maiores redes de farmácias da Europa, fundada em 1972 na Alemanha. Com mais de 4.000 lojas em diversos países, a empresa se destaca por oferecer uma ampla gama de produtos de saúde e bem-estar. Além da Alemanha, a Rossmann está presente na Polônia, Hungria, Turquia e Albânia. Conhecida por seu compromisso com qualidade e preços acessíveis, a Rossmann é uma escolha popular para consumidores que buscam produtos farmacêuticos e de cuidados pessoais.

## Problema de Negócio

O CFO (Chief Financial Officer) da Rossmann está planejando uma grande reforma em todas as unidades da rede. Para viabilizar esse projeto, uma parcela do faturamento de cada loja será destinada à reforma das suas respectivas unidades durante as próximas 6 semanas. Este esforço visa modernizar as lojas, melhorar a experiência do cliente e garantir que todas as unidades estejam alinhadas com os padrões mais recentes da empresa. O desafio está em implementar essas reformas de forma eficiente, sem comprometer o funcionamento diário das lojas e o fluxo de caixa da empresa.

## Planejamento da Solução

A estratégia de solução adotada neste projeto se baseia no método CRISP-DM (Cross Industry Standard Process for Data Mining), uma metodologia amplamente reconhecida e utilizada na ciência de dados. O CRISP-DM é um modelo cíclico e flexível, projetado para a resolução de problemas que envolvem grandes volumes de dados. Ele se destaca por sua capacidade de se adaptar a diferentes contextos e necessidades, permitindo uma abordagem estruturada e iterativa na análise de dados. A metodologia facilita a entrega rápida de valor para os times de negócio, proporcionando uma compreensão aprofundada dos dados e gerando insights acionáveis. A imagem abaixo ilustra uma adaptação do CRISP-DM, destacando suas fases principais e como elas se inter-relacionam para otimizar o processo de mineração de dados e a tomada de decisões estratégicas.

A seguir, descrevo cada etapa explicando as premissas adotadas e decisões tomadas com o objetivo de obter o melhor resultado para o problema apresentado.

### Questão de Negócio

Como explicitado anteriormente, há uma dificuldade por parte dos funcionários da Rossmann de tentar prever o quanto as lojas irão faturar durante as 6 semanas seguintes. A gerência não possui clareza sobre os fatores que impulsionam as vendas, como a influência de concorrentes e a distância em que esses concorrentes começam a impactar negativamente os resultados.

O objetivo deste projeto é, além da entrega de um modelo, é fornecer insights valiosos para a direção com o intuito de muni-los de informações para que tomem decisões baseadas em dados.

#### Entregas:
- **Análise Exploratória de Dados:** Geração de insights sobre o negócio.
- **APP:** Endpoint para realizar previsões de vendas.
- **BotTelegram**: Interface através da qual o CFO poderá solicitar previsões de faturamento das lojas

### Entendimento do Negócio

Atualmente, a previsão de faturamento é feita com base na média das últimas seis semanas de vendas. Por ser uma abordagem simples, este método não leva em consideração variações sazonais, promoções, feriados ou a influência dos concorrentes. Como resultado, as previsões não tem sido boas, dificultando o planejamento financeiro para as reformas das lojas da rede. A incerteza quanto ao faturamento futuro pode levar a decisões inadequadas.

#### Coleta de Dados

Este projeto é fictício e os dados utilizados foram extraídos de arquivos _.csv_ disponíveis na plataforma de competições [Kaggle](https://www.kaggle.com/c/rossmann-store-sales). Em um cenário real, esses dados seriam gerados via SQL pelo cientista de dados ou pelo administrador do banco de dados.


#### Dicionário de Dados

##### Arquivos
- **`train.csv`**: Dados históricos incluindo as vendas (`Sales`).
- **`test.csv`**: Dados históricos excluindo as vendas (`Sales`).
- **`sample_submission.csv`**: Um arquivo de submissão de exemplo no formato correto.
- **`store.csv`**: Informações suplementares sobre as lojas.

##### Campos de Dados
| Campo                               | Descrição                                                                                                                                               |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`Id`**                            | Um identificador que representa um par (Loja, Data) no conjunto de teste.                                                                               |
| **`Store`**                         | Um identificador único para cada loja.                                                                                                                  |
| **`Sales`**                         | O faturamento em um determinado dia (este é o alvo que você deve prever).                                                                               |
| **`Customers`**                     | O número de clientes em um determinado dia.                                                                                                             |
| **`Open`**                          | Indicador de se a loja estava aberta: `0` = fechada, `1` = aberta.                                                                                      |
| **`StateHoliday`**                  | Indica um feriado estadual. Normalmente, todas as lojas, com algumas exceções, estão fechadas em feriados estaduais: `a`: Feriado público, - `b`: Feriado de Páscoa, `c`: Natal e `0`: Nenhum                                      |
| **`SchoolHoliday`**                 | Indica se a (Loja, Data) foi afetada pelo fechamento das escolas públicas.                                                                               |
| **`StoreType`**                     | Diferencia entre quatro modelos diferentes de loja: `a`, `b`, `c`, `d`.                                                                                 |
| **`Assortment`**                    | Descreve o nível de sortimento: `a`: Básico, `b`: Extra e `c`: Estendido                                                                                                                                                                                                                                                                      
| **`CompetitionDistance`**           | Distância, em metros, para a loja concorrente mais próxima.                                                                                             |
| **`CompetitionOpenSince[Month/Year]`** | O mês e o ano aproximados em que a concorrência mais próxima foi aberta.                                                                                 |
| **`Promo`**                         | Indica se uma loja estava em promoção naquele dia.                                                                                                      |
| **`Promo2`**                        | Indica uma promoção contínua e consecutiva para algumas lojas: `0` = loja não participa, `1` = loja participa.                                           |
| **`Promo2Since[Year/Week]`**        | Descreve o ano e a semana do calendário em que a loja começou a participar da Promo2.                                                                    |
| **`PromoInterval`**                 | Descreve os meses em que a Promo2 é iniciada novamente. Por exemplo, "Fev,Mai,Ago,Nov" significa que a promoção começa em fevereiro, maio, agosto e novembro de cada ano para essa loja. |

### Limpeza de Dados

Com os dados carregados, a primeira tarefa feita foi renomear e adequar as colunas para que elas ficassem mais confortável e amigável durante a análise. O padrão adotado foi o snake_case.

Abaixo listo estas transformações e o racional por trás destas ações

- #### Valores Nulos
	-   `date` -  A coluna `date` foi convertida para o formato datetime, permitindo uma manipulação mais eficiente de datas, como extração de ano, mês e semana.
    
	-   `competition_distance`: Valores ausentes foram substituídos por um valor elevado (200.000) para indicar ausência de concorrentes próximos.
	- `competition_open_since_month` e `competition_open_since_year`: Meses e anos ausentes foram preenchidos com os respectivos valores da data da observação.
	 -   `promo2_since_week` e `promo2_since_year`: Semanas e anos ausentes foram preenchidos com as respectivas semanas e anos da data da observação.
	    -   `promo_interval`: Valores ausentes foram substituídos por 0, e foi criada a coluna `is_promo` para indicar se uma promoção estava ativa no mês correspondente.

- #### dtypes de variáveis

	-   `Conversão de Tipos de Dados**: As colunas `competition_open_since_month`, `competition_open_since_year`, `promo2_since_week` e `promo2_since_year` foram convertidas para o tipo inteiro (`int`), garantindo a consistência dos dados para análises subsequentes.

### Feature Engineering

Pensando nas próximas etapas (EDA e Modelagem de Dados), foram criadas algumas variáveis a partir de `date`:

- #### Variáveis criadas

	- `year`: ano 
	- `month`: mês
	- `day`: dia
	- `week_of_year`número da semana no ano
	- `year_week`: Combinação das variáveis `year` e `week_of_year`, representando o ano e a semana correspondente.
	- `competition_since`: Data de início da concorrência, calculada a partir do ano e mês em que a concorrência começou.
	- `competition_time_month`: Duração da concorrência em meses, calculada desde a data de início até a data da transação.
	- `promo_since`: Data de início da promoção, combinando o ano e a semana em que a promoção começou.
	- `promo_time_week`: Duração da promoção em semanas, calculada desde a data de início até a data da transação.

- #### Filtragem de Variáveis

	- `customers`: Essa variável foi removida porque, no momento da previsão (6 semanas antes), não é possível saber quantos clientes visitaram a loja.
	- `open`: Os registros que indicavam que a loja estava fechada foram excluídos.
	- `sales`: Mantivemos apenas os registros das lojas que realizaram vendas no dia.

### Análise Exploratória de Dados

Após a etapa de Feature Engineering, a próxima fase deste projeto é analisar cada variável individualmente e entender sua relação com a variável alvo `sales`. Para uma exploração mais estruturada do dataset, esta seção foi dividida em três categorias principais.

#### Análise Univariada

Para esta análise, por ser tratar de um problema de regressão, precisamos conhecer a distribuição da variável resposta `sales`, como estão distribuídas as variaveis numéricas e as variáveis categóricas.

##### Variável `sales`:
![distribuíção da variável Sales](imagem_sales.png)

O gráfico acima expõe que a variável `sales` não possui uma distribuíção normal, pois o histograma possui uma leve assimetria. Se a inspeção visual não for suficiente, podemos utilizar os valores de curtose e de assimetria.

**Aprendizado: A variável `sales` precisa de uma transformação para que os algoritmos de machine learning funcione.**

##### Variáveis Numéricas:
O principal objetivo, nesta parte, é olhar para a distribuições de todas as variáveis numérica e identificar atributos que tenha variabilidade. 

![distribuíção da variável Sales](imagem_sales.png)

##### Variáveis Categóricas:

Nos dados trabalhados, há apenas 3 variáveis categóricas: `state_holiday`, `store_type` e `assortment`. A proposta é fazer uma contagem das categorias e gerar os gráficos de densidade para cada uma delas, com o objetivo de identificar possíveis relações entre categorias e o faturamento das lojas.

**Aprendizado: **


![distribuíção da variável Sales](imagem_sales.png)

- ##### `state_holiday`

No gráfico de barras, a grande maioria da dos feriados estaduais são feriados públicos, com poucos registro para os feriados de Páscoa e Natal. Esta afirmação não é nada reveladora, uma vez que durante o ano só há um feriado de Páscoa e Natal, enquanto há mais feriados públicos em um ano.

O gráfico de densidade revela que as vendas tendem a ser maiores durante o Natal em comparação com as outras categorias de feriados públicos, enquanto a Páscoa apresenta uma densidade de venads mais baixa.

- ##### `store_type`

Não há insights relevantes no gráfico de colunas. Apenas fica claro que temos mais lojas *a*, seguida pelas lojas do tipo *d*, *c* e *b*.

A densidade de vendas indica que, apesar das categorias de tipos de lojas apresentem uma distribuição semelhante de vendas, as lojas do tipo *b* parecem ter uma concentração ligeiramente maior de faturamento diário.

**OBS.: Por se tratar de um projeto fictício, perdemos o contexto desta variável, uma vez que não se sabe o que significa os tipos de lojas. Em um projeto real, isso certamente seria explorado durante a reunião com a equipe de negócio e poderia ser incorporado melhor ao modelo de Machine Learning.**

- ##### `assortment`

A maior parte dos registros nesta variável corresponde ao sortimento básico, com um número menor de lojas oferecendo o sortimento estendido e uma quantidade mínima oferecendo o tipo extra.

O gráfico de densidade sugere que as lojas com sortimento extra tendem a ter uma maior concentração de faturamento diário.

#### Análise Bivariada

Para a Análise Bivariada, foram criadas hipóteses sobre o negócio, com o intuito de criar insights para melhorar o processo de modelagem e de treinamento do algoritmos. Abaixo, listo as 11 hipóteses criadas e verifico se ela é verdadeira ou falsa.

- ##### H1. Lojas com maior sortimento deveriam vender mais
**Falsa**. Apesar de ser algo intuitivo a se pensar, os dados indicaram que lojas com sortimento básico ou estendido apresentam vendas maiores às lojas com sortimento extra. 

- ##### H2. Lojas com competidores próximo deveriam vender menos
**Falsa**. Analisando o gráfico de barras podemos notar um decaimento nas vendas a medida que os competidores estão mais longe. Confirmando esta conclusão com a correlação negativa de -0.23, ou seja, quanto maior a distância do concorrente, menor o faturamento da loja.

- ##### H3. Lojas com competidores a mais tempo deveriam vender mais
**Falsa**. A correlação de 0.11 negativo é muito fraca para validarmos esta hipótese. O que vemos nos gráficos de barras e no gráfico de regressão é que o faturamento decai ligeiramente e fica constante após o  35º mês.

- ##### H4. Lojas com promoções ativas por mais tempo deveriam vender mais
**Falsa**. No curto prazo, há um aumento de crescimento das vendas durante as semanas de promoção. No entanto, no longo prazo, nota-se uma leve queda nas vendas após 150 semanas, com uma correlação negativa de 0.029, indicando que promoções prolongadas podem ter um impacto decrescente.

- ##### H5. Lojas com mais promoções consecutivas deveriam vender mais
**Falsa**. O faturamento das duas categorias (Extendida e "Tradicional & Extendida) é próximo até a 35ª semana do ano. Após este marco, as lojas que permanecem com promoções por mais tempo tem uma queda nas vendas 

- ##### H6. Lojas abertas durante o feriado de Natal deveriam vender mais
**Falsa**. O gráfico mostra que, comparado com os outros feriados, as vendas no Natal são mais baixas, principalmente se compara-lo à feriados públicos, que apresentam um volume significativamente maior. 

**Um ponto a ser levantando no próximo ciclo CRISP é, como o dataset tem informações de 2 anos e 7 meses, temos 3 Páscoas e 2 Natais, o que deve interferir esta comparação**

- ##### H7. Lojas deveriam vender mais ao longo dos anos.
**Falsa**. O gráfico sugere uma leve queda nas vendas totais ano após ano. Mesmo considerando que o ano de 2015 não está completo, não há evidências que esta hipótese seja verdadeira.

- ##### H8. Lojas deveriam vender mais no segundo semestre do ano.
**Falsa**. Os dados mostram que as vendas são consistentemente maiores no primeiro semestre, com uma média de vendas superior. Além disso, a análise por semanas revela que, embora haja flutuações, o primeiro semestre se destaca em termos de volume de vendas na maioria das semanas.

- ##### H9. Lojas deveriam vender mais depois do dia 10 de cada mês
**Verdadeira**.  As vendas tendem a ser maiores após o dia 10 de cada mês, como evidenciado pelo volume de vendas mais alto. A correlação negativa entre o dia do mês e as vendas sugere que os consumidores podem estar mais dispostos a gastar após o recebimento de salários ou benefícios, confirmando a hipótese de que as lojas vendem mais após o dia 10.

- ##### H10. Lojas deveriam vender menos aos finais de semana.
**Verdadeira**. A forte correlação negativa entre o dia da semana e as vendas reforça a hipótese de que as vendas são significativamente menores nos finais de semana em comparação aos outros finais de semana

- ##### H11. Lojas deveriam vender menos durante feriados escolares.
**Verdadeira**. O gráfico mostra que as vendas durante feriados escolares são consistentemente mais baixas em comparação com períodos sem feriados escolares, em quase todos os meses. 

### Modelagem de Dados

Antes de iniciar a etapa de teste dos algoritmos de Machine Learning, é fundamental realizar a preparação das variáveis para garantir que os algoritmos possam processá-las adequadamente. Essa preparação foi estruturada em três principais etapas: Rescaling, Encoding e Transformation. A seguir, detalho as ações realizadas sobre as variáveis.

#### Variáveis Numéricas
Como a maioria das variáveis numéricas não apresenta uma distribuição normal, foram aplicados métodos de Rescaling. O `RobustScaler` foi utilizado para variáveis com outliers significativos, enquanto o `Min-Max Scaler` foi aplicado às demais, normalizando-as entre 0 e 1.

#### Variáveis Categóricas
As variáveis categóricas, como `store_type` e `assortment`, foram tratadas com `Label Encoding` e `Ordinal Encoding`, respectivamente. Além disso, aplicamos o `One Hot Encoding` para variáveis categóricas como `state_holiday`, criando colunas binárias para cada categoria.

#### Tranformação de Grandeza
Como a variável de resposta, `sales`, não segue uma distribuição normal, aplicamos uma transformação logarítmica para reduzir a assimetria e melhorar a capacidade de aprendizagem dos algoritmos.

#### Seleção de Features
O algoritmo Boruta foi o escolhido para selecionar as variáveis mais relevantes para o modelo. As variáveis menos importantes foram descartadas, o que ajuda a melhorar a performance do modelo e reduzir o overfitting. As variáveis que permaneceram no dataset foram:
```python
[ 'store', 'promo', 'store_type', 'assortment', 'competition_distance',
 'competition_open_since_month', 'competition_open_since_year',
 'promo2', 'promo2_since_week', 'promo2_since_year',
 'competition_time_month', 'promo_time_week', 'day_of_week_sin',
 'day_of_week_cos', 'month_cos', 'month_sin', 'day_sin', 'day_cos',
 'week_of_year_cos', 'week_of_year_sin', 'date', 'sales']
```
### Algoritmos de Machine Learning

#### Testando Modelos
Com as variáveis selecionadas e transformadas, é o momento de treinar os modelos e identificar quais terão os melhores resultados. Para que não ficasse muito tempo testando modelos, escolhi 2 modelos lineares e 2 modelos não-lineares: Regressão Linear, Lasso, Random Forest e XGBoost. Abaixo o resultado dos primeiro treinamentos.

| Id | Model Name                 | MAE     | MAPE     | RMSE    |
|----|----------------------------|---------|----------|---------|
|  1 | Random Forest Regressor    | 679.966 | 0.099976 | 1011.74 |
|  2 | Average Model              | 1354.8  | 0.2064   | 1835.14 |
|  3 | XGBoost Regressor          | 1686.97 | 0.2506   | 2463.36 |
|  4 | Linear Regression          | 1867.09 | 0.292694 | 2671.05 |
|  5 | Linear Regression Lasso    | 2190.78 | 0.342891 | 3093.9  |

Como dito na seção de *Entendimento de Negócio*, a Rossmann estimava as vendas das próximas 6 semanas fazendo uma média das vendas passadas. Esta era nossa baseline.

#### Cross Validation

Aplicando a técnica de Cross Validation Time Series nos algoritmos, temos os resultados

| Id | Model Name             | MAE               | MAPE             | RMSE               |
|----|------------------------|-------------------|------------------|--------------------|
|  1 | LinearRegression        | 2081.73 ± 295.63  | 0.3026 ± 0.0166  | 2952.52 ± 468.37    |
|  2 | Lasso                   | 2382.74 ± 370.4   | 0.3351 ± 0.0134  | 3369.36 ± 522.76    |
|  3 | RandomForestRegressor   | 838.1 ± 219.01    | 0.1161 ± 0.0232  | 1256.98 ± 319.62    |
|  4 | XGBRegressor            | 1058.52 ± 146.61  | 0.1485 ± 0.0153  | 1513.92 ± 206.74    |

Os resultados indicam que o **Random Forest Regressor** apresentou o melhor desempenho, porém, o modelo gerado é muito grande, o que pode aumentar os custos operacionais. Assim, o **XGBoost** se mostrou uma alternativa viável, oferecendo resultados semelhantes, mas com um modelo significativamente mais leve que o Random Forest.

#### Hyperparameter Fine Tuning

Nesta etapa , foi realizada a otimização dos parâmetros do modelo **XGBoost Regressor**. Um conjunto de valores possíveis para hiperparâmetros como `n_estimators`, `eta`, `max_depth`, `subsample`, `colsample_bytree` e `min_child_weight` foi definido aleatoriamente. 
O melhor conjunto encontrado, após validação cruzada, foi ajustado e aplicado ao modelo final, resultando em um desempenho otimizado para a predição. O modelos final ficou:

| Model Name          | MAE        | MAPE     | RMSE      |
|---------------------|------------|----------|-----------|
| XGBoost Regressor   | 641.005971 | 0.092994 | 939.689364|

### Avaliação do Algoritmo

Com o modelo final definido e os resultados em mãos, é fundamental comunicar essas métricas técnicas de forma acessível ao time de negócios. Compararemos o novo modelo com a baseline previamente utilizada pela equipe e desenvolveremos cenários, tanto otimistas quanto pessimistas, baseados nas métricas do modelo.

Para demonstrar com mais clareza o quão próximo o modelo está dos resultados reais, selecionamos as últimas 6 semanas de dados e somamos o faturamento total de todas as lojas. Realizamos essa análise comparativa tanto para o modelo baseline, utilizado anteriormente, quanto para o novo modelo proposto. O resultado dessa comparação foi

| Sum of Sales    | Baseline (Mean Model) | ML Model       |
|-----------------|-----------------------|----------------|
| R$ 289.571.750  | R$ 324.608.344         | R$ 283.041.088 |

Essa comparação evidencia que o uso de um modelo de machine learning é justificado em relação à projeção da receita futura, pois o desvio do modelo foi significativamente menor do que o do baseline

Com base no erro do modelo, podemos estimar cenários para cada loja com o intuito de facilitar a análise por parte da equipe de negócio. Abaixo alguns temos o exemplo de algumas lojas.

| Store | Sales       | ML Predict  | Worst Scenario | Best Scenario | MAE     | MAPE |
|-------|-------------|-------------|----------------|---------------|---------|------|
| 251   | R$ 690.220,0 | R$ 650.210,0 | R$ 648.380,0   | R$ 652.040,0  | R$ 1.830,0 | 0.09 |
| 192   | R$ 487.998,0 | R$ 400.844,0 | R$ 398.374,0   | R$ 403.313,0  | R$ 2.469,0 | 0.18 |
| 178   | R$ 370.073,0 | R$ 423.960,0 | R$ 352.799,0   | R$ 354.543,0  | R$ 871,0   | 0.08 |
| 34    | R$ 309.543,0 | R$ 285.755,0 | R$ 285.083,0   | R$ 286.428,0  | R$ 672,0   | 0.07 |

### Deploy do Modelo

Com o modelo escolhido, treinado e com bom desempenho, o próximo passo foi colocá-lo em produção. Decidimos disponibilizar as previsões de vendas de forma online, utilizando o aplicativo de mensagens Telegram.

A ideia é que o Assistente do Gerente Regional tenha flexibilidade de acessar estes dados de qualquer lugar, trabalhe esta informação em diferentes contextos. Isso permitirá que ele processe e analise as predições e leve insights valiosos para o CFO, contribuindo para a tomada de decisão.

Para viabilizar essa funcionalidade, desenvolvemos duas APIs: a API que fornecerá as previsões de faturamento (handler.py) e a API do telegram, para a interface com o usuário.

#### API Previsão
Essa API é responsável por fornecer a previsão de vendas baseada nos atributos da loja.

O processo funciona da seguinte forma: o usuário fornece os atributos da loja para a API, como assortment, store_type, dia da semana, entre outros. O script handler.py carrega o modelo treinado, realiza as transformações e redimensionamentos necessários nos dados e, em seguida, executa a previsão.

A resposta da API inclui o conjunto de dados de entrada em formato JSON, juntamente com o valor previsto de vendas para a(s) loja(s) e dia(s) solicitado(s).

#### API de Mensagens Telegram

Esta API é responsável pela comunicação com o usuário, gerenciando as mensagens de boas-vindas, erros e respostas às solicitações de previsão.

Quando o usuário consulta o ID de uma loja para obter a previsão, o script rossmann-bot.py carrega os atributos da loja que já estão em produção (não sendo mais necessário que o usuário os informe), transforma os dados em JSON e realiza a consulta na API handler.py.

A API handler.py retorna um JSON contendo os dados de entrada junto com o valor previsto das vendas. Por fim, o rossmann-bot.py processa esse JSON, soma as previsões e informa ao usuário, por meio de uma mensagem, o valor total das vendas previstas para as próximas 6 semanas.

