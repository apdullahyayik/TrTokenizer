# Turkish-Word-Tokenizer
Tokenize words of a given Turkish sentence.

### Usage

sentence_1 = "Saat 10:20 itibariyle, T.C. Merkez Bankası verilerine göre 1.25 oranında faiz indirimi yapıldı."
print(word_tokenize(sentence_1))

['Saat', '10:20', 'itibariyle', ',', 'T.C.', 'Merkez', 'Bankası', 'verilerine', 'göre', '1.25', 'oranında', 'faiz', 'indirimi', 'yapıldı', '.']

sentence_2 = "Senin adını kol saatimin kayışına tırnağımla kazıdım."

print(word_tokenize(sentence_2))

['Senin', 'adını', 'kol', 'saatimin', 'kayışına', 'tırnağımla', 'kazıdım', '.']

sentence_3 = "T.C. Ankara'dan tüm dünyaya sevgi, saygı vs. çağrısı yaptı ve dolar 1.35 kuruş azaldı."

print(word_tokenize(sentence_3))

['T.C', "Ankara'dan", 'tüm', 'dünyaya', 'sevgi,', 'saygı', 'vs.', 'çağrısı', 'yaptı', 've', 'dolar', '1.35', 'kuruş', 'azaldı','.']

