# -*- coding: utf-8 -*-
import numpy as np
import torch
from pytorch_lightning.core.lightning import LightningModule
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel

U_TKN = '<usr>'
S_TKN = '<sys>'
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'

TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK) 



class KoGPT2Chat(LightningModule):
    def __init__(self, hparams, **kwargs):
        super(KoGPT2Chat, self).__init__()
        self.kogpt2 = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
    

    def forward(self, inputs):
        # (batch, seq_len, hiddens)
        output = self.kogpt2(inputs, return_dict=True)
        return output.logits

 
    def chat(self,chat, sent='0'):
        tok = TOKENIZER
        sent_tokens = tok.tokenize(sent)
        
        q=chat
        q_tok = tok.tokenize(q)
        a = ''
        while 1:
            input_ids = torch.LongTensor(tok.encode(U_TKN + q + SENT + sent + S_TKN + a)).unsqueeze(dim=0)
            pred = self(input_ids)
            gen = tok.convert_ids_to_tokens(
                torch.argmax(
                    pred,
                    dim=-1).squeeze().numpy().tolist())[-1]
            if gen == EOS:
                break
            a += gen.replace('▁', ' ')
        return a.strip()


if __name__ == "__main__":
    path='model_chp/model_-epoch=27-train_loss=20.78.ckpt'
    model = KoGPT2Chat.load_from_checkpoint(path)
    chat='안녕하세요'
    print(model.chat(chat))
    print(model.chat(chat))
    print(model.chat(chat))
