import csv
import os

import pandas as pd
import ResourcesChatGPT as rChatGPT


def __prepro_diagnostics(diagnostics):
    new_diagnostics, new_set_diagnostics = [], []
    for set_diagnostics in diagnostics:
        splited = set_diagnostics.split("*")

        for diagnostic in splited:
            if diagnostic != "":
                new_set_diagnostics.append("*" + diagnostic)
        new_diagnostics.append(new_set_diagnostics)
        new_set_diagnostics = []

    return new_diagnostics


def prompting(gt, llm, output_file_path):
    responses = []
    gt_to_csv, llm_to_csv = [], []
    i = 1
    for diagnostics_gt, diagnostics_llm in zip(gt, llm):
        txt_gt = "\n".join(diagnostics_gt)
        txt_llm = "\n".join(diagnostics_llm)
        prompt = f"""[Instrução] A tarefa é comparar a lista "referência" com a lista "hipótese". A lista "referência" é curada, anotada por especialistas, e não possui repetições ou diagnósticos similares. Todos os diagnósticos, fatores de risco ou procedimentos da lista "referência" devem estar presentes na lista "hipótese".

Lista “referência”:
{txt_gt}

Lista “hipótese”:
{txt_llm}

Para calcular a precisão e o recall, siga os passos abaixo:

1. Para cada item na lista "referência", verifique se ele está presente na lista "hipótese". Com isso, obtenha o total de elementos pertencentes a True Positives (TP).
2. Com base na verificação da quantidade de TP, calcule o recall.
3. Com base na verificação da quantidade de TP, calcule o precisão.

### Precisão e Recall:
Para calcular a precisão e o recall:
- TP = Número de itens da lista "referência" que estão presentes na lista "hipótese"
- Recall = TP / (Total de itens na lista "referência")
- Precisão = TP / (Total de itens na lista "hipótese")

### Resultados:
Mostre a precisão e o recall no formato: "[[Precisão, Recall]]". Por exemplo, se a precisão for 0.8 e o recall for 0.7, o formato seria "[[0.8, 0.7]]"
"""

        response = rChatGPT.get_response(prompt)
        responses.append(response)

        print(f" :: Processed {i}/{len(gt)}")

        gt_to_csv.append("\n".join(diagnostics_gt))
        llm_to_csv.append("\n".join(diagnostics_llm))

        i += 1

    data = {
        "GT": gt_to_csv,
        "LLM": llm_to_csv,
        "RESPONSES": responses,
    }

    df = pd.DataFrame(data)

    df.to_csv(output_file_path, sep="\t", index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

    print("-----------------------")


if __name__ == "__main__":
    drop_list = [0, 9, 11]

    df_gt = pd.read_csv("./data/gt.tsv", sep="\t")
    gt = df_gt["GT"].values.tolist()
    gt = __prepro_diagnostics(gt)

    for file in os.listdir("./data/"):
        if "diag" in file:
            if os.path.exists("./result-gpt4o/" + file):
                print("[Ignoring] File already processed", file, "...", flush=True)
                continue

            print("Processing file", file, "...", flush=True)

            df_diag = pd.read_csv("./data/" + file, sep="\t")
            df_diag = df_diag.drop(drop_list)

            llm_diag = df_diag["DIAGNOSTICOS_LLM"].values.tolist()

            diagnostics_llm = __prepro_diagnostics(llm_diag)

            prompting(gt, diagnostics_llm, "./result-gpt4o/" + file)
