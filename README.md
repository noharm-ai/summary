**Improving Care  Transition with LLM**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/noharm-ai/summary/blob/main/discharge_summary.ipynb)

**Authors:** Joaquim santos, Henrique Dias, Ana Helena Ulbrich,  Juliana Damasio, Julia Couto, Marcelo Arocha, Arthur Tabbal, Augusto Santos, Fábio Tabalipa, Manuela Martins, Rodrigo Nogueira

**Corresponding author:** henrique@noharm.ai

## Abstract

During a patient's hospitalization, extensive information is documented in clinical notes. The efficient summarization of this information is vital for keeping healthcare professionals abreast of the patient's status. This paper proposes a methodology to assess the efficacy of six large language models (LLMs) in automating the task of diagnosis summarization, particularly in discharge summaries. Our approach involves defining an automatic metric based on LLMs, highly correlated with human assessments. We evaluate the performance of the six models using the F1-Score and compare the results with those of healthcare specialists. The experiments reveal that there is room for improvement in the medical knowledge and diagnostic capabilities of LLMs. The source code and data for these experiments are available on the project's GitHub page.

## Context

The transition of care is a major challenge for the healthcare system. Physicians have difficulty organizing the most important information about an inpatient's hospitalization. NoHarm Discharge Summary is artificial intelligence, based on large language models. This tool extracts the most important information from inpatients' records then writes the discharge summary for physicians to validate (as a clinical decision support system). 

**Summary Elements:**
- Reason for Admission
- Diagnostics 
- Allergies
- Previously used medications
- Clinical Summary
- Laboratory Tests
- Textual Exams
- Procedures Performed
- Medications used
- Discontinued medications
- Discharge Conditions
- Discharge Plan
- Discharge Prescription

**Benefits of Hybrid Approach:**

- Cost: NER is a faster model and LLM will process fewer amount of texts. From $60K to $2K (for 1K patients)
- Privacy: NER extract only selected information from clinical notes.
- Scalable: LLM only handle up to 60K tokens, NER can extract small sentences from larger texts.
- Safety: Few-shot learning approach eliminate possible hallucination.
- Inclusive: can deliver free of charge for public healthcare.

**Ethical Language Model:**

- NER model ensure that no personal information goes to LLM prompt by selecting pre-trained entities. It decrease gender/race bias probability in LLM generation.
- Few-shot learning narrow LLM output into examples presented, preventing hallucination and improving text generation results.
- Survey with patients and  primary care professionals to evaluate the NER + LLM discharge summaries.

Github link for [Summary Discharge Interface](https://github.com/noharm-ai/frontend/blob/develop/src/features/summary/Summary.jsx)


## Running LLM Evaluation

To run the evaluation of LLMs, follow these steps:

1 - Clone the repository.
2 - Execute the file EvalLLM.py with: python EvalLLM.py

The "Data" folder contains the output files of the LLMs evaluated by our work. That is, each file is a list of diagnoses that each language model evaluated as a response to an output from our NER system.

The "ResultTables" folder stores the metrics calculated by the automatic evaluator (GPT-4).

The python file "EvalLLM.py" is where we preprocess the files from the "Data" folder to match the format of our evaluation prompt; and also where we do the prompting and store the responses in .tsv format.

To configure your connection to the API of an LLM, it should be done in the file "ResourcesChatGPT.py". We use the Azure service, if you use another service, change this part of the code. In this python file are also our prompts for few-shot learning and a definition called "get_response" that queries the LLM via API.
