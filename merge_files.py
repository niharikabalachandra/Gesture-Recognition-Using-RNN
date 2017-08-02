import csv
fout=open("./one_file.csv","a")
# first file:
count=0
with open('./CSV/0.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[1]==str(0.0) and row [2]==str(0.0) and row[3]==str(0.0):
            count+=1
        else:
            pass
#Eliminate the samples which had erroneous input recorded
if count==0:
    for line in open("./CSV/0.csv"):
        fout.write(line)
        
# Rest of the files: 
for num in range(1,503):
    count=0
    with open('./CSV/'+str(num)+'.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[1]==str(0.0) and row [2]==str(0.0) and row[3]==str(0.0):
                count+=1
            else:
                pass
    if count==0:
        f = open("./CSV/"+str(num)+".csv")
        for line in f:
            fout.write(line)
        f.close() 
fout.close()

