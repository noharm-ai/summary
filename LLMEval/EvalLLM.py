import csv
import pandas as pd
import ResourcesChatGPT as rChatGPT


def __prepro_diagnostics(diagnostics):
	new_diagnostics, new_set_diagnostics = [], []
	for set_diagnostics in diagnostics:
		splited = set_diagnostics.split('*')

		for diagnostic in splited:
			if diagnostic != '':
				new_set_diagnostics.append('*'+diagnostic)
		new_diagnostics.append(new_set_diagnostics)
		new_set_diagnostics = []

	return new_diagnostics


def prompting(gt, llm, output_file_path):
	responses = []
	gt_to_csv, llm_to_csv = [], []
	i = 1
	for diagnostics_gt, diagnostics_llm in zip(gt, llm):
		txt_gt = '\n'.join(diagnostics_gt)
		txt_llm = '\n'.join(diagnostics_llm)
		prompt = f"""A tarefa é comparar a lista “referência” com a lista “hipótese”. Todos os diagnósticos, fatores de risco ou procedimentos da lista “referência” devem estar presentes na lista “hipótese”.

Lista “referência”:
{txt_gt}

Lista “hipótese”:
{txt_llm}

Para calcular a precisão e o recall, primeiro deve ser listados todos os diagnósticos, fatores de risco ou procedimentos pertencentes aos verdadeiros positivos (VP), os itens falsos positivos (FP), e aos diagnósticos falsos negativos (FN).

- VP (Verdadeiro Positivo): Diagnósticos listados na lista “hipótese” que estão também listados na lista “referência”.
- FP (Falso Positivo): Os diagnósticos listados na lista” hipótese” que não estão listados na lista “referência”. Diagnósticos repetidos na lista hipótese também serão considerados Falsos Positivos. Diagnósticos similares ou menos completos a algum diagnóstico listado na lista hipótese também serão considerados Falsos Positivos.
- FN (Falso Negativo): Os diagnósticos que existem na lista “referência”, mas não foram incluídos na lista “hipótese”.

Qual a precisão e o recall? 
Me dê o resultado, sem explicar o que é precisão e recall.
Mostre a qual grupo (VP, FP, FN) pertence cada resultado.

Apresente o recall, a precisão e o ruído no formato: (Precisão, Recall)
"""
		
		response = rChatGPT.get_response(prompt)
		responses.append(response)
		
		print(f' :: Processed {i}/{len(gt)}')
		
		gt_to_csv.append('\n'.join(diagnostics_gt))
		llm_to_csv.append('\n'.join(diagnostics_llm))

		i+=1

	data = {
		"GT": gt_to_csv,
		"LLM": llm_to_csv,
		"RESPONSES": responses,
	}

	df = pd.DataFrame(data)
	
	df.to_csv(output_file_path, sep='\t', index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

	print("-----------------------")
	
if __name__ == '__main__':
	drop_list = [0, 9, 11]

	df_gt = pd.read_csv('./data/gt.tsv', sep='\t')
	gt = df_gt['GT'].values.tolist()
	gt = __prepro_diagnostics(gt)


	#GPT-3 Eval
	df_gpt3 = pd.read_csv('./data/diagnosticos_gpt3.tsv', sep='\t')
	df_gpt3 = df_gpt3.drop(drop_list)

	llm_gpt3 = df_gpt3['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_gpt3 = __prepro_diagnostics(llm_gpt3)
	
	prompting(gt, diagnostics_llm_gpt3, './ResultTables/testGPT3.tsv')
	

	#GPT-4.06 Eval
	df_gpt4_6 = pd.read_csv('./data/diagnosticos_gpt_4_6.tsv', sep='\t')
	df_gpt4_6 = df_gpt4_6.drop(drop_list)

	llm_gpt4_6 = df_gpt4_6['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_gpt4_6 = __prepro_diagnostics(llm_gpt4_6)
	
	prompting(gt, diagnostics_llm_gpt4_6, './ResultTables/testGPT4_6.tsv')


	#Maritalk 1 Eval
	df_maritalk1 = pd.read_csv('./data/diagnosticos_maritalk1.tsv', sep='\t')
	df_maritalk1 = df_maritalk1.drop(drop_list)

	llm_maritalk1 = df_maritalk1['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_maritalk1 = __prepro_diagnostics(llm_maritalk1)

	prompting(gt, diagnostics_llm_maritalk1, './ResultTables/testMariTalk1.tsv')


	#Maritalk 2 Eval
	df_maritalk2 = pd.read_csv('./data/diagnosticos_maritalk2.tsv', sep='\t')
	df_maritalk2 = df_maritalk2.drop(drop_list)

	llm_maritalk2 = df_maritalk2['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_maritalk2 = __prepro_diagnostics(llm_maritalk2)

	prompting(gt, diagnostics_llm_maritalk2, './ResultTables/testMaritalk2.tsv')


	#Palm 2 Eval
	df_palm2 = pd.read_csv('./data/diagnosticos_palm2.tsv', sep='\t')
	df_palm2 = df_palm2.drop(drop_list)

	llm_palm2 = df_palm2['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_palm2 = __prepro_diagnostics(llm_palm2)

	prompting(gt, diagnostics_llm_palm2, './ResultTables/testPalm2.tsv')


	#Gemini Pro Eval
	df_gemini_pro = pd.read_csv('./data/diagnosticos_gemini_pro.tsv', sep='\t')
	df_gemini_pro = df_gemini_pro.drop(drop_list)
	
	llm_gemini_pro = df_gemini_pro['DIAGNOSTICOS_LLM'].values.tolist()

	diagnostics_llm_gemini_pro = __prepro_diagnostics(llm_gemini_pro)

	prompting(gt, diagnostics_llm_gemini_pro, './ResultTables/testGeminiPro.tsv')
