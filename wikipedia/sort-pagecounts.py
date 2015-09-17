import sys
freq = {}
for line in sys.stdin:
    word, count = line.strip().split()
    freq.setdefault(word, 0)
    freq[word] += int(count)

pages = reversed(sorted((count, word) for word, count in freq.items()))
for count, word in pages:
    if "List_of" in word or ":" in word: continue
    if count < 5: break
    print count, word
