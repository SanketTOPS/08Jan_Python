import re

mystr="This is Python!8478498"

#x=re.findall('\w',mystr)
#x=re.findall('\W',mystr)
#x=re.findall('\d',mystr)
#x=re.findall('\D',mystr)
#x=re.findall('\s',mystr)
#x=re.findall('\S',mystr)
#x=re.findall(r'\bThis',mystr)
#x=re.findall('\B64',mystr)
#x=re.findall('\AThis',mystr)
x=re.findall('98\Z',mystr)
print(x)