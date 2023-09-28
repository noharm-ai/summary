# NoHarm Discharge Summary
**Improving Care  Transition with LLM**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/noharm-ai/summary/blob/main/discharge_summary.ipynb)

**Authors:** Henrique Dias, Ana Helena Ulbrich,  Juliana Damasio, Julia Couto, Marcelo Arocha, Arthur Tabbal, Augusto Santos

**Corresponding author:** henrique@noharm.ai

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
