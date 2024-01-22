import os
from openai import AzureOpenAI
import time


client = AzureOpenAI(
    azure_endpoint="[azure_endpoint]",
    api_version="[api_version]",
    api_key="[api_key]"
)

user_1 = """A tarefa é comparar a lista “referência” com a lista “hipótese”. Todos os diagnósticos, fatores de risco ou procedimentos da lista “referência” devem estar presentes na lista “hipótese”.

Lista “referência”:
* Hipotireoidismo
* Osteoporose
* Câncer gástrico
* Hipertensão arterial sistêmica (HAS)
* Insuficiência Cardíaca Congestiva (ICC) 
* Angina instável
* AVC
* Delirium hiperativo

Lista “hipótese”:
* Hipotireoidismo
* Osteoporose 
* Câncer gástrico 
* Hipertensão arterial sistêmica (HAS) 
* Insuficiência Cardíaca Congestiva (ICC)
* Angina instável. 
* Anamnese Farmacêutica
* Diabetes Mellitus
* AVC

Para calcular a precisão e o recall, primeiro deve ser listados todos os diagnósticos, fatores de risco ou procedimentos pertencentes aos verdadeiros positivos (VP), os itens falsos positivos (FP), e aos diagnósticos falsos negativos (FN).

- VP (Verdadeiro Positivo): Diagnósticos listados na lista “hipótese” que estão também listados na lista “referência”.
- FP (Falso Positivo): Os diagnósticos listados na lista” hipótese” que não estão listados na lista “referência”. Diagnósticos repetidos na lista hipótese também serão considerados Falsos Positivos. Diagnósticos similares ou menos completos a algum diagnóstico listado na lista hipótese também serão considerados Falsos Positivos.
- FN (Falso Negativo): Os diagnósticos que existem na lista “referência”, mas não foram incluídos na lista “hipótese”.

Qual a precisão e o recall? 
Me dê o resultado, sem explicar o que é precisão e recall.
Mostre a qual grupo (VP, FP, FN) pertence cada resultado.

Apresente o recall, a precisão e o ruído no formato: (Precisão, Recall)
"""

assistant_1 = """Verdadeiros Positivos (VP):
* Hipotireoidismo
* Osteoporose
* Câncer gástrico
* Hipertensão arterial sistêmica (HAS)
* Insuficiência Cardíaca Congestiva (ICC)
* Angina instável
* AVC

Falsos Positivos (FP):
* Anamnese Farmacêutica - não é um diagnóstico
* Diabetes Mellitus - não mencionado no texto original

Falsos Negativos (FN):
* Delirium hiperativo - apesar de presente no texto original, não está presente no resultado

Cálculo de precisão e recall:

Precisão = VP / (VP + FP) = 7 / (7 + 2) = 7 / 9 ≈ 0.777 (77,77%)
Recall = VP / (VP + FN) = 7 / (7 + 1) = 7 / 8 = 0.875 (87,5%)

(Precisão, Recall) = (0.777, 0.875)
"""

user_2 = """A tarefa é comparar a lista “referência” com a lista “hipótese”. Todos os diagnósticos, fatores de risco ou procedimentos da lista “referência” devem estar presentes na lista “hipótese”.

Lista “referência”:
* Meningite pós operatória
* Tumor do Sistema Nervoso Central (D33)
* Claustrofobia
* Fístula liquórica cutânea na região da sutura

Lista “hipótese”: 
* Neoplasia benigna do encéfalo e de outras partes do sistema nervoso central (D33)
* Ependimoma
* Meningite pós-operatoria
* Meningite pós-procedimento
* Meningite pós-operatória
* Tumor do sistema nervoso central
* Ressecção de ependimoma
* Fistula liquorica cutanea
* Transição crânio-cervical

Para calcular a precisão e o recall, primeiro deve ser listados todos os diagnósticos, fatores de risco ou procedimentos pertencentes aos verdadeiros positivos (VP), os itens falsos positivos (FP), e aos diagnósticos falsos negativos (FN).

- VP (Verdadeiro Positivo): Diagnósticos listados na lista “hipótese” que estão também listados na lista “referência”.
- FP (Falso Positivo): Os diagnósticos listados na lista” hipótese” que não estão listados na lista “referência”. Diagnósticos repetidos na lista hipótese também serão considerados Falsos Positivos. Diagnósticos similares ou menos completos a algum diagnóstico listado na lista hipótese também serão considerados Falsos Positivos.
- FN (Falso Negativo): Os diagnósticos que existem na lista “referência”, mas não foram incluídos na lista “hipótese”.

Qual a precisão e o recall? 
Me dê o resultado, sem explicar o que é precisão e recall.
Mostre a qual grupo (VP, FP, FN) pertence cada resultado.

Apresente o recall, a precisão e o ruído no formato: (Precisão, Recall)
"""

assistant_2 = """Verdadeiros Positivos (VP):
* Neoplasia benigna do encéfalo e de outras partes do sistema nervoso central (D33) - versão mais completa do D33
* Meningite pós-operatoria  - versão mais completa do ""Meningite pós""
* Fistula liquorica cutanea

Falsos Positivos (FP):
* Ressecção de Ependimoma (1) - procedimento, não é uma condição médica
* Transição crânio-cervical (1)- não é diagnóstico
* Meningite pós-procedimento (1) - sinônimo de Meningite pós-operatoria
* Meningite pós-operatória (1) - repetido apenas uma vez de forma idêntica
* Ependimoma (1) - similar a Neoplasia benigna do encéfalo
* Tumor do sistema nervoso central (1) - sinônimo de Neoplasia benigna do encéfalo

Falsos Negativos (FN):
* Claustrofobia - apesar de presente no texto original, não está presente no resultado

Cálculo de precisão e recall:

Precisão = VP / (VP + FP) = 3 / (3 + 2) = 3 /6 = 0.5 (50%)
Recall = VP / (VP + FN) = 3 / (3 + 1) = 3 / 4 = 0.75 (75%)

(Precisão, Recall) = (0.5, 0.75)
"""

user_3 = """A tarefa é comparar a lista “referência” com a lista “hipótese”. Todos os diagnósticos, fatores de risco ou procedimentos da lista “referência” devem estar presentes na lista “hipótese”.

Lista “referência”:
* Púrpura Trombocitopênica Idiopática (PTI)
* Anemia Aplástica
* Síndrome Mielodisplásica
* Hipertensão Arterial Sistêmica (HAS)
* Diabetes Mellitus (DM)
* Transtorno de adaptação

Lista “hipótese”:
* Trombocitopenia
* Plaquetopenia
* Anemia aplástica
* Hipertensão arterial sistêmica (HAS)
* Plaquetopenia grave a/e - Provavel Sd Mielodisplasica
* Plaquetopenia grave a/e - PTI
* Trombocitopenia NE
* Anemia
* Plaquetopenia
* Plaquetopenia grave a/e
* Plaquetopenia grave a/e - PTI
* Anemia aplástica não grave
* HAS
* Trombocitopenia NE
* Anemia


Para calcular a precisão e o recall, primeiro deve ser listados todos os diagnósticos, fatores de risco ou procedimentos pertencentes aos verdadeiros positivos (VP), os itens falsos positivos (FP), e aos diagnósticos falsos negativos (FN).

- VP (Verdadeiro Positivo): Diagnósticos listados na lista “hipótese” que estão também listados na lista “referência”.
- FP (Falso Positivo): Os diagnósticos listados na lista” hipótese” que não estão listados na lista “referência”. Diagnósticos repetidos na lista hipótese também serão considerados Falsos Positivos. Diagnósticos similares ou menos completos a algum diagnóstico listado na lista hipótese também serão considerados Falsos Positivos.
- FN (Falso Negativo): Os diagnósticos que existem na lista “referência”, mas não foram incluídos na lista “hipótese”.

Qual a precisão e o recall? 
Me dê o resultado, sem explicar o que é precisão e recall.
Mostre a qual grupo (VP, FP, FN) pertence cada resultado.

Apresente o recall, a precisão e o ruído no formato: (Precisão, Recall)
"""

assistant_3 = """Verdadeiros Positivos (VP):
* Anemia aplástica
* Hipertensão arterial sistêmica (HAS)
* Plaquetopenia grave a/e - Provavel Sd Mielodisplasica
* Plaquetopenia grave a/e - PTI


Falsos Positivos (FP):
* Trombocitopenia NE (2) - sinais da Plaquetopenia grave a/e - PTI
* Anemia (2) - similar a Anemia aplástica
* Plaquetopenia (1) -  similar a Plaquetopenia grave a/e - Provavel Sd Mielodisplasica
* Plaquetopenia grave a/e (1)  - similar a Plaquetopenia grave a/e - Provavel Sd Mielodisplasica
* Plaquetopenia grave a/e - PTI (1) - similar a Plaquetopenia grave a/e - Provavel Sd Mielodisplasica
* Anemia aplástica não grave (1) - similar a anemia aplásica
* HAS (1) - similar a Hipertensão arterial sistêmica (HAS)


Falsos Negativos (FN):
* Transtorno de adaptação - apesar de presente no texto original, não está presente no resultado
* Diabetes Mellitus (DM)

Cálculo de precisão, recall:
Precisão = VP / (VP + FP) = 4 / (4 + 9) = 4 / 13 = 0.61 (61%)
Recall = VP / (VP + FN) = 4 / (4 + 2) = 4 / 6 = 0.67 (67%)

(Precisão, Recall) = (0.61, 0.67)
"""

user_4 = """A tarefa é comparar a lista “referência” com a lista “hipótese”. Todos os diagnósticos, fatores de risco ou procedimentos da lista “referência” devem estar presentes na lista “hipótese”.

Lista “referência”:
* Ascite
* Câncer de colo de útero
* Sangramento peri dreno
* Delirium
* EC IV (osso) - Estágio Clínico IV (osso)

Lista “hipótese”:
* Ascite
* Câncer de colo de útero (C53 - NEOPLASIA MALIGNA DO COLO DO UTERO)
* Câncer endometrial (CEC colo de útero)
* Ca de colo de útero
* Sangramento peri dreno
* Sangramento externo ao dreno
* Delirium
* Redução discreta
* Colo de útero (C53)

Para calcular a precisão e o recall, primeiro deve ser listados todos os diagnósticos, fatores de risco ou procedimentos pertencentes aos verdadeiros positivos (VP), os itens falsos positivos (FP), e aos diagnósticos falsos negativos (FN).

- VP (Verdadeiro Positivo): Diagnósticos listados na lista “hipótese” que estão também listados na lista “referência”.
- FP (Falso Positivo): Os diagnósticos listados na lista” hipótese” que não estão listados na lista “referência”. Diagnósticos repetidos na lista hipótese também serão considerados Falsos Positivos. Diagnósticos similares ou menos completos a algum diagnóstico listado na lista hipótese também serão considerados Falsos Positivos.
- FN (Falso Negativo): Os diagnósticos que existem na lista “referência”, mas não foram incluídos na lista “hipótese”.

Qual a precisão e o recall? 
Me dê o resultado, sem explicar o que é precisão e recall.
Mostre a qual grupo (VP, FP, FN) pertence cada resultado.

Apresente o recall, a precisão e o ruído no formato: (Precisão, Recall)
"""

assistant_4 = """Verdadeiros Positivos (VP):
* Ascite
* Câncer de colo de útero (C53 - NEOPLASIA MALIGNA DO COLO DO UTERO) (mais completo e detalhado que outros sinônimos)
* Sangramento peri dreno
* Delirium

Falsos Positivos (FP):
* Redução discreta - não é um diagnóstico
* Câncer endometrial (CEC colo de útero) (1) - É o mesmo que câncer de colo de útero, e a terminologia "endometrial" é incorreta para C53.
* Ca de colo de útero (1) - repetição do diagnóstico mais completo "Câncer de colo de útero".
* Colo de útero (C53) (1) - repetição do diagnóstico mais completo "Câncer de colo de útero".
* Sangramento externo ao dreno (1) - repetição de "Sangramento peri dreno"

Falsos Negativos (FN):
* EC IV (osso) - Estágio Clínico IV (osso)

Cálculo de precisão e recall:

Precisão = VP / (VP + FP) = 4/ (4 + 5) = 4 / 9= 0.44 (44%)
Recall = VP / (VP + FN) = 4 / (4 + 1) = 4 / 5 = 0.8 (80%)

(Precisão, Recall) = (0.44, 0.8)
"""




def get_response(question : str):

    retries = 5
    tentatives = 1
    while retries > 0:
        try:
            time.sleep(0.3)
            response = client.chat.completions.create(
                model="[model]",
                messages=[
                    {"role": "user", "content":user_1},
                    {"role": "assistant", "content":assistant_1},
                    {"role": "user", "content":user_2},
                    {"role": "assistant", "content":assistant_2},
                    {"role": "user", "content":user_3},
                    {"role": "assistant", "content":assistant_3},
                    {"role": "user", "content":user_4},
                    {"role": "assistant", "content":assistant_4},
                    {"role": "user", "content":question},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            if e:
                print(e)
                print(f' :: [Timeout error, retrying...] [TENTATIVE {tentatives}]')
                retries -= 1
                tentatives+=1
                time.sleep(30)
            else:
                raise e