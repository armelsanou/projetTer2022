import sentencepiece as spm
import re
textfile = "inputText.txt"

text = open (textfile,encoding="utf-8")

spm.SentencePieceTrainer.train(input=textfile,model_prefix="model",vocab_size = 16000)

vocab = "model"+".vocab"
vacabulaire = open (vocab,encoding="utf-8")

liste_vocabulaire = []
for line in vacabulaire:
    words = line.split("    ")
    word2 = re.sub('▁','',words[0])
    liste_vocabulaire.append(word2)