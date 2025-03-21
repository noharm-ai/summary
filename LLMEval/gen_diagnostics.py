import csv
import os
from importlib import import_module

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


@hydra.main(config_path="../configs", config_name="default")
def main(cfg: DictConfig):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get list of providers from diagnostics configuration (split by comma)
    providers = [provider.strip() for provider in cfg.diagnostics.llms.split(",")]
    output_dir = os.path.join(current_dir, cfg.diagnostics.output)

    # Read the ground truth TSV file (expects a column "Diagnósticos NER")
    with open(os.path.join(current_dir, cfg.diagnostics.gt_file), "r", encoding="utf-8") as gt_file:
        reader = csv.DictReader(gt_file, delimiter="\t")
        gt_rows = list(reader)

    # Process each provider
    for provider in providers:
        print(f"Running prompt with provider: {provider}")
        llm_client = get_llm_client(provider, cfg.lms)
        print(f"llm client initialized")
        results = []
        # For each ground truth row, create the prompt and get the LLM response
        for row in gt_rows:
            ner_text = row["DIAGNOSTICO_NER"]
            prompt = f"""{cfg.diagnostics.prompt}\n\n{ner_text}"""
            response = llm_client.invoke(prompt)
            results.append({"DIAGNOSTICOS_LLM": response, "DIAGNOSTICOS_NER": ner_text})

        # Save the results into a TSV file named diagnosticos_{provider}.tsv
        output_file = os.path.join(output_dir, f"diagnosticos_{provider}.tsv")
        with open(output_file, "w", encoding="utf-8", newline="") as out_file:
            fieldnames = ["DIAGNOSTICOS_LLM", "DIAGNOSTICOS_NER"]
            writer = csv.DictWriter(out_file, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            for res in results:
                writer.writerow(res)

        print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
