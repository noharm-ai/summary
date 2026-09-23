import os
import sys
from types import SimpleNamespace

import pytest
from omegaconf import OmegaConf

# Compute the directory of the current file.
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path relative to this file's location.
target_path = os.path.join(current_dir, "..")

# Append the computed path to sys.path.
sys.path.append(os.path.abspath(target_path))

from LLMEval.gen_diagnostics import get_llm_client


# Mock class for testing
class DummyLLM:
    def __init__(self, foo=None, bar=None):
        self.foo = foo
        self.bar = bar

    def invoke(self, prompt):
        return f"Echo: {prompt}"


def test_get_llm_client_valid(monkeypatch):
    # Register dummy class under a fake module
    import sys

    sys.modules["mock_module"] = SimpleNamespace(DummyLLM=DummyLLM)

    config = OmegaConf.create({"dummy": {"class": "mock_module.DummyLLM", "args": {"foo": "hello", "bar": 123}}})

    client = get_llm_client("dummy", config)
    assert isinstance(client, DummyLLM)
    assert client.foo == "hello"
    assert client.bar == 123
    assert client.invoke("test") == "Echo: test"


def test_get_llm_client_invalid_class_path():
    config = OmegaConf.create({"bad": {"class": "InvalidClassPath", "args": {}}})

    with pytest.raises(ValueError, match="Invalid class path: 'InvalidClassPath'.*"):
        get_llm_client("bad", config)


class DummyBedrockLLM:
    def __init__(self, model_id=None, config=None):
        self.model_id = model_id
        self.config = config


def test_get_llm_client_botocore_config_mapping():
    from botocore.config import Config

    sys.modules["mock_bedrock"] = SimpleNamespace(DummyBedrockLLM=DummyBedrockLLM)
    config = OmegaConf.create({"slow": {"class": "mock_bedrock.DummyBedrockLLM", "args": {"model_id": "x", "config": {"read_timeout": 600}}}})

    client = get_llm_client("slow", config)
    assert isinstance(client.config, Config)
    assert client.config.read_timeout == 600
