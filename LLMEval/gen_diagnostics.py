import csv
import os
from importlib import import_module
from typing import Callable, Dict, List

import hydra
from omegaconf import DictConfig, OmegaConf

# Register env resolver explicitly
OmegaConf.register_new_resolver("env", lambda x: os.getenv(x))


def get_llm_client(provider: str, lms_config: DictConfig):
    client_config = lms_config.get(provider)
    if client_config is None:
        raise ValueError(f"Provider '{provider}' not found in config.")

    class_path = client_config.get("class")
    if class_path is None:
        raise ValueError(f"No class specified for provider '{provider}'.")

    # Split full path, e.g., "langchain_openai.AzureChatOpenAI"
    try:
        module_path, class_name = class_path.rsplit(".", 1)
    except ValueError:
        raise ValueError(f"Invalid class path: '{class_path}'. Expected format 'module.ClassName'.")

    module = import_module(module_path)
    client_cls = getattr(module, class_name)

    kwargs = client_config.get("args", {})
    return client_cls(**kwargs)


def build_default_prompt(base_prompt: str, ner_text: str) -> str:
    return f"{base_prompt}\n\n{ner_text}"


def build_prompt_repetition_prompt(base_prompt: str, ner_text: str) -> str:
    return f"{base_prompt}\n\n{ner_text}\n\n{base_prompt}\n\n{ner_text}"

def run_diagnostics_experiment(
    cfg: DictConfig,
    current_dir: str,
    gt_rows: List[Dict[str, str]],
    output_relative_dir: str,
    prompt_builder: Callable[[str], str],
    experiment_name: str,
):
    providers = cfg.diagnostics.llms
    output_dir = os.path.join(current_dir, output_relative_dir)
    os.makedirs(output_dir, exist_ok=True)

    for provider in providers:
        output_file = os.path.join(output_dir, f"diagnosticos_{provider}.tsv")
        if os.path.exists(output_file):
            print(f"Skipping provider '{provider}' for '{experiment_name}' (output already exists at {output_file})")
            continue

        print(f"Running '{experiment_name}' with provider: {provider}")
        llm_client = get_llm_client(provider, cfg.lms)
        print("llm client initialized")
        results = []

        for row in gt_rows:
            ner_text = row["DIAGNOSTICO_NER"]
            prompt = prompt_builder(ner_text)
            response = llm_client.invoke(prompt)
            results.append({"DIAGNOSTICOS_LLM": response.content, "DIAGNOSTICOS_NER": ner_text})

        with open(output_file, "w", encoding="utf-8", newline="") as out_file:
            fieldnames = ["DIAGNOSTICOS_LLM", "DIAGNOSTICOS_NER"]
            writer = csv.DictWriter(out_file, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            for res in results:
                writer.writerow(res)

        print(f"Results for '{experiment_name}' saved to {output_file}")


@hydra.main(config_path="../configs", config_name="default")
def main(cfg: DictConfig):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Read the ground truth TSV file (expects a column "Diagnósticos NER")
    with open(os.path.join(current_dir, cfg.diagnostics.gt_file), "r", encoding="utf-8") as gt_file:
        reader = csv.DictReader(gt_file, delimiter="\t")
        gt_rows = list(reader)

    # Original experiment
    run_diagnostics_experiment(
        cfg=cfg,
        current_dir=current_dir,
        gt_rows=gt_rows,
        output_relative_dir=cfg.diagnostics.output,
        prompt_builder=lambda ner_text: build_default_prompt(cfg.diagnostics.prompt, ner_text),
        experiment_name="baseline",
    )

@hydra.main(config_path="../configs", config_name="default")
def main_rep(cfg: DictConfig):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Read the ground truth TSV file (expects a column "Diagnósticos NER")
    with open(os.path.join(current_dir, cfg.diagnostics.gt_file), "r", encoding="utf-8") as gt_file:
        reader = csv.DictReader(gt_file, delimiter="\t")
        gt_rows = list(reader)

    # Prompt repetition experiment
    output_rep = "data_rep/"

    run_diagnostics_experiment(
        cfg=cfg,
        current_dir=current_dir,
        gt_rows=gt_rows,
        output_relative_dir=output_rep,
        prompt_builder=lambda ner_text: build_prompt_repetition_prompt(
            cfg.diagnostics.prompt, ner_text
        ),
        experiment_name="prompt_repetition",
    )

if __name__ == "__main__":
    main_rep()
