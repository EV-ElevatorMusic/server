
from keras.models import load_model
from transformers import PreTrainedTokenizerFast
import numpy as np
U_TKN = '<usr>'
S_TKN = '<sys>'
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'



class emotion_analysis():
  def __init__(self,path,max_ids):
    self.model=load_model(path)
    self.max_ids=max_ids
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

    self.tok = TOKENIZER
  def pred(self,words):
    # 0:기쁨
    # 1:분노
    # 2:슬픔
    data=self.word_to_encoded(words)
    pre=self.model.predict(data)
    return np.argmax(pre)

  def word_to_encoded(self,words):
    toks=self.tok.tokenize(words)
    tok_list=token=self.tok.convert_tokens_to_ids(toks)
    zero_list=np.zeros(self.max_ids+1)

    for i in tok_list:
      zero_list[i]=1
      
    zero_list=zero_list.reshape(1,-1,1)  
    return zero_list
  