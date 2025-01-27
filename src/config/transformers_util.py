from transformers import BertModel, BertTokenizerFast, OpenAIGPTModel, OpenAIGPTTokenizer
from transformers import GPT2Model, GPT2Tokenizer, CTRLModel, CTRLTokenizer
from transformers import TransfoXLModel, TransfoXLTokenizer, XLNetModel, XLNetTokenizer, DistilBertModel, DistilBertTokenizer
from transformers import RobertaModel, RobertaTokenizerFast, XLMRobertaModel, XLMRobertaTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup
from typing import List, Dict, Any
from src.config import Config
import torch.nn as nn
from termcolor import colored
import torch


context_models = {
    'bert-base-uncased' : {  "model": BertModel,  "tokenizer" : BertTokenizerFast },
    'bert-base-cased' : {  "model": BertModel,  "tokenizer" : BertTokenizerFast },
    'bert-large-cased' : {  "model": BertModel,  "tokenizer" : BertTokenizerFast },
    'openai-gpt': {"model": OpenAIGPTModel, "tokenizer": OpenAIGPTTokenizer},
    'gpt2': {"model": GPT2Model, "tokenizer": GPT2Tokenizer},
    'ctrl': {"model": CTRLModel, "tokenizer": CTRLTokenizer},
    'transfo-xl-wt103': {"model": TransfoXLModel, "tokenizer": TransfoXLTokenizer},
    'xlnet-base-cased': {"model": XLNetModel, "tokenizer": XLNetTokenizer},
    'distilbert-base-cased': {"model": DistilBertModel, "tokenizer": DistilBertTokenizer},
    'roberta-base': {"model": RobertaModel, "tokenizer": RobertaTokenizerFast},
    'roberta-large': {"model": RobertaModel, "tokenizer": RobertaTokenizerFast},
    'xlm-roberta-base': {"model": XLMRobertaModel, "tokenizer": XLMRobertaTokenizerFast},
}

def get_huggingface_optimizer_and_scheduler(config: Config, model: nn.Module,
                                            num_training_steps: int,
                                            weight_decay: float = 0.0,
                                            eps: float = 1e-8,
                                            warmup_step: int = 0):
    """
    Copying the optimizer code from HuggingFace.
    """
    print(colored(f"Using AdamW optimizeer by HuggingFace with {config.learning_rate} learning rate, "
                  f"eps: {eps}, weight decay: {weight_decay}, warmup_step: {warmup_step}, ", 'yellow'))
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=config.learning_rate, eps=eps)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_step, num_training_steps=num_training_steps
    )
    return optimizer, scheduler

