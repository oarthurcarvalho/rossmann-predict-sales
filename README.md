# Rossmann Sales Forecast

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

 

### Análise Exploratória de Dados
### Modelagem de Dados
### Algoritmos de Machine Learning
### Avaliação do Algoritmo
### Deploy do Modelo
