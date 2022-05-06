import re
from collections import Counter

val = '<seg id="13"> and how high has your <term id="212" type="src_original_and_tgt_original" src="fever" tgt="fièvre"> fever </term> been </seg> <seg id="14"> and i have a <term id="328" type="src_original_and_tgt_original" src="cough" tgt="toussez|toussent|tousser|tousse|toussé|toux"> cough </term> too </seg><seg id="15"> and i have a little cold and a <term id="328" type="src_original_and_tgt_original" src="cough" tgt="toussez|toussent|tousser|tousse|toussé|toux"> cough </term> </seg>'
cleaned = re.sub('<[^>]*>', '', val)
print(cleaned)

split_it = cleaned.split()

# Pass the split_it list to instance of Counter class.
Counters_found = Counter(split_it)
#print(Counters)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counters_found.most_common(4)
print(most_occur)