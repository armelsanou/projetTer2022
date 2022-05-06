import sentencepiece as spm
import re
import pandas as pd
from nltk import word_tokenize

textfile = "inputText.txt"

corpus = open (textfile,encoding="utf-8")
model = "model/sortie.txt"

tok_corp = pd.DataFrame([word_tokenize(sent) for sent in corpus])
#print(tok_corp)

spm.SentencePieceTrainer.train(input=tok_corp, model_prefix = model, vocab_size = 3025, max_sentence_length=10000)

vocab = model+".vocab"
vacabulaire = open (vocab,encoding="utf-8")

liste_vocabulaire = []
for line in vacabulaire:
    words = line.split("    ")
    word2 = re.sub('▁','',words[0])
    liste_vocabulaire.append(word2)