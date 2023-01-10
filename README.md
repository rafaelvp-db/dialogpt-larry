# Hugging Face GPT Chatbot Example

<div align="center"><img src="https://github.com/rafaelvp-db/dialogpt-larry/blob/master/img/hf.png?raw=true"></div>

## Objective

**TLDR**: NLP models often have quite a specific set of inputs. With Transformers models this is no different. In this project, we create a small Wrapper class (```huggingface_wrapper.py```) which will be used to package a Hugging Face model in ```mlflow.pyfunc``` flavor.

In the inference notebook (```huggingface_inference.py```), we have an example where we:

1. **Download** the pretrained model and tokenizer from Hugging Face
2. **Save** the model into MLflow Model Registry
3. **Promote** the model to Production
4. **Load** the model
5. Get some **predictions** (concretely, we're having a chat with the GPT Bot 😄)

## Context

### A State-of-the-Art Large-scale Pretrained Response generation model (DialoGPT)

This repo contains a basic example of [Hugging Face model](https://huggingface.co/microsoft/DialoGPT-medium) for [Language Modeling using Transformers](https://huggingface.co/docs/transformers/tasks/language_modeling) - most specifically, ```microsoft/DialoGPT-medium```.

From their Hugging Face repo:

DialoGPT is a SOTA large-scale pretrained dialogue response generation model for multiturn conversations. The human evaluation results indicate that the response generated from DialoGPT is comparable to human response quality under a single-turn conversation Turing test. The model is trained on 147M multi-turn dialogue from Reddit discussion thread.

Multi-turn generation examples from an interactive environment:

| **Role** | **Response**                                                                                                       |
|------|----------------------------------------------------------------------------------------------------------------|
| User | Does money buy happiness?                                                                                      |
| Bot  | Depends how much money you spend on it .                                                                       |
| User | What is the best way to buy happiness ?                                                                        |
| Bot  | You just have to be a millionaire by your early 20s, then you can be happy .                                   |
| User | This is so difficult !                                                                                         |
| Bot  | You have no idea how hard it is to be a millionaire and happy . There is a reason the rich have a lot of money |


## Components

1. Databricks + MLflow
2. FastAPI
3. NGINX
4. ReactJS

## Instructions

### Databricks Serverless ML Endpoints

* Clone this repo into your Databricks workspace.
* Make sure to use a cluster running an `LTS ML` runtime.
* In the `databricks` folder, run the `hf_ingest_nb.py` notebook. This will generate our dataset for further fine tuning our `DialoGPT` model.
* Run the `hf_finetune_nb.py` notebook. This will finetune our model with the dataset generated in the previous step.
* Run the `hf_register_and_inference_nb.py` notebook. Doing so will register our model into MLflow Model Registry, and generate some predictions.
* Once the model is registered, use it to create a REST Realtime Endpoint (Model Serving V2).
### User Interface

* Be sure to have Docker installed.
* Clone this repo.
* Build the `backend` container image by running `make backend`.
* Build the `frontend` container image by running `make frontend`.
* Create a Databricks PAT Token on your workspace.
* Copy the `.env.example` file into `.env` and fill in the parameters. Use the info from your workspace and the Model Serving V2 created in the previous section.
* Run both containers by executing `make run`.
* On your browser, go to [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Demo

<div align="center"><img src="https://github.com/rafaelvp-db/dialogpt-larry/blob/master/img/demo3.gif?raw=true"></div>

## TODO

See the [issues](https://github.com/rafaelvp-db/dialogpt-larry/issues) section

## Credits

* **ReactJS** app theme by [Ritesh Sharma](https://github.com/ritesh-sharma33)
* [Fine-Tuning GPT-based Models for Conversational Chatbots](https://github.com/ncoop57/i-am-a-nerd/blob/master/_notebooks/2020-05-12-chatbot-part-1.ipynb)
