# Databricks notebook source
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, PretrainedConfig

tokenizer_name = "/dbfs/tmp/curb/checkpoint-80500"
model_name = "/dbfs/tmp/curb/checkpoint-80500"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir="/tmp/cache/")
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir="/tmp/cache/")

# COMMAND ----------

import os
import mlflow
from huggingface_wrapper import HuggingFaceWrapper

def save_model(
    model_name_or_path: str,
    tokenizer_name_or_path: str,
    model_name: str = "curb",
    artifact_path = "/tmp/hugging_face/artifacts"
):
    model_path = artifact_path + "model"
    tokenizer_path = artifact_path + "tokenizer"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    model = AutoModelForCausalLM.from_pretrained(tokenizer_name_or_path)
    tokenizer.save_pretrained(tokenizer_path)
    model.save_pretrained(model_path)

    artifacts = {
      "hf_model_path": model_path,
      "hf_tokenizer_path": tokenizer_path
    }
    mlflow_pyfunc_model_path = model_name

    model_info = None
    
    with mlflow.start_run() as run:
        model_info = mlflow.pyfunc.log_model(
            artifact_path = mlflow_pyfunc_model_path,
            python_model = HuggingFaceWrapper(),
            code_path = ["./huggingface_wrapper.py"],
            artifacts=artifacts,
            pip_requirements=["numpy==1.20.1", "transformers==4.16.2", "torch==1.10.2"]
        )
        
    return model_info

# COMMAND ----------

info = save_model(model_name_or_path = model_name, tokenizer_name_or_path = tokenizer_name)

# COMMAND ----------

model_name = "gpt_chatbot_curb"
version_info = mlflow.register_model(model_uri = info.model_uri, name = model_name)

# COMMAND ----------

from mlflow.tracking import MlflowClient
client = MlflowClient()
stage = "Production"

client.transition_model_version_stage(
    name=version_info.name,
    version=version_info.version,
    stage=stage
)

# COMMAND ----------

loaded_model = mlflow.pyfunc.load_model(model_uri=f"models:/{version_info.name}/{stage}")

# COMMAND ----------

chat_history_ids = []

model_input = {
  "question": "hi, are you buck dancer?",
  "chat_history_ids": chat_history_ids
}
reply = loaded_model.predict(model_input)
print(reply["answer"])

# COMMAND ----------

model_input = {
  "question": "I'm not sammy.",
  "chat_history_ids": [reply["chat_history_ids"]]
}

reply = loaded_model.predict(model_input)
print(reply["answer"])

# COMMAND ----------

model_input = {
  "question": "I know, genious.",
  "chat_history_ids": [reply["chat_history_ids"]]
}

reply = loaded_model.predict(model_input)
print(reply["answer"])

# COMMAND ----------


