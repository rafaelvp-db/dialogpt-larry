import torch
import numpy as np
import mlflow.pyfunc

from transformers import AutoModelForCausalLM, AutoTokenizer

class HuggingFaceWrapper(mlflow.pyfunc.PythonModel):
    """
    Class to use HuggingFace Models
    """

    def load_context(self, context):
        """This method is called when loading an MLflow model with pyfunc.load_model(), as soon as the Python Model is constructed.
        Args:
            context: MLflow context where the model artifact is stored.
        """

        self.tokenizer = AutoTokenizer.from_pretrained(context.artifacts["hf_tokenizer_path"])
        self.model = AutoModelForCausalLM.from_pretrained(context.artifacts["hf_model_path"])
        
    def ask_question(
      self,
      question,
      chat_history_ids,
      max_length = 1000,
      temperature = 50.0,
      repetition_penalty = 50.0
    ):
  
        new_user_input_ids = self.tokenizer.encode(
          str(question) + str(self.tokenizer.eos_token),
          return_tensors='pt'
        )
    
        chat_history_ids = torch.from_numpy(np.array(chat_history_ids))
    
        if (len(chat_history_ids) > 0):
          bot_input_ids = torch.cat(
            [chat_history_ids, new_user_input_ids],
            dim=-1
          )
        else:
          bot_input_ids = new_user_input_ids

        """chat_history_ids = self.model.generate(
          bot_input_ids,
          max_length = max_length,
          temperature = temperature,
          repetition_penalty = repetition_penalty,
          pad_token_id = self.tokenizer.eos_token_id,
        )"""
        
        chat_history_ids = self.model.generate(
          bot_input_ids, max_length=200,
          pad_token_id=self.tokenizer.eos_token_id,  
          no_repeat_ngram_size=3,       
          do_sample=True, 
          top_k=100, 
          top_p=0.7,
          temperature=0.8
        )
        
        answer = self.tokenizer.decode(
          chat_history_ids[:, bot_input_ids.shape[-1]:][0],
          skip_special_tokens=True
        )

        return answer, chat_history_ids

    def predict(self, context, model_input):
        """This is an abstract function. We customized it into a method to fetch the Hugging Face model.
        Args:
            context ([type]): MLflow context where the model artifact is stored.
            model_input ([type]): the input data to fit into the model.
        Returns:
            [type]: the loaded model artifact.
        """

        answer, chat_history_ids = self.ask_question(
          question = model_input["question"],
          chat_history_ids = model_input["chat_history_ids"]
        )
        
        result = {
          "answer": answer,
          "chat_history_ids": chat_history_ids[0].tolist()
        }
        
        return result


def _load_pyfunc(data_path):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_pyfunc``.
    """
    return HuggingFaceWrapper(data_path)