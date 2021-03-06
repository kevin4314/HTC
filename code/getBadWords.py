import codecs

# getBadWords.py simply count all word's frequency and output to ../badword/

authors = {'9knife' : 24, 'cityup' : 5, 'love0' : 2}

for (author, num) in authors.items():
	print "> At ", author
	for book_num in range(1, num+1):
		print ">> Book = ", book_num
		f = codecs.open('../format/'+author+'/'+str(book_num)+'.txt', 'r', encoding='utf8')
		fw = codecs.open('../badword/'+author+'_'+str(book_num)+'.txt', 'w', encoding='utf8')
		words = dict()
		for line in f:
			for token in line.strip():# remove the newline character
				if token in words:
					words[token] += 1
				else:
					words[token] = 1
		
		tmp = words.items()
		tmp.sort(key=lambda x:x[1], reverse=True)# sort by the word's frequency (higher -> lower)
		for i in tmp:
			print >> fw, i[0], " ", i[1]