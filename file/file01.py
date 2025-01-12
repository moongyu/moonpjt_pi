

file = open('text01.txt','w')
for i in range(1,6):
    data = '%d\n'%i
    file.write(data)

file.close()

