import sys, re, os

output_dir = "extracted"
try:
    os.mkdir(output_dir)
except:
    pass

doc_id = re.compile(r'(?:</doc>\n)?<doc id=.+?>')
for filename in sys.argv[1:]:
    data = open(filename).read()
    docs = doc_id.split(data)
    for doc in docs[1:]:
        title, content = doc.split("\n\n", 1)
        title = re.sub(r'\W', "_", title.strip())
        print >>sys.stderr, title
        output = open(output_dir + "/" + title + ".txt", "w")
        print >>output, content
        output.close()
