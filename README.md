# Turkish-Word-Tokenizer
Tokenize words or given sentence.
Considers Turkish punctuations and abbreviations structure

### Usage
sentence1 = "Senin adını kol saatimin kayışına tırnağımla kazıdım."
print(word_tokenize(sentence))

['Senin', 'adını', 'kol', 'saatimin', 'kayışına', 'tırnağımla', 'kazıdım.']

sentence2 = "T.C. Ankara'dan tüm dünyaya sevgi, saygı vs. çağrısı yaptı ve dolar 1.35 kuruş azaldı."
print(word_tokenize(sentence))

['T.C', "Ankara'dan", 'tüm', 'dünyaya', 'sevgi,', 'saygı', 'vs.', 'çağrısı', 'yaptı', 've', 'dolar', '1.35', 'kuruş', 'azaldı.']
