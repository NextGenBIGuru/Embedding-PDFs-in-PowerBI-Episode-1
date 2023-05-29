import base64
import csv
from csv import DictWriter
import os
from os import path

def ProcessPDF(WDir,FName):  


    with open(WDir + FName + ".pdf", "rb") as Tempfile: #Open the PDF file
        my_string=base64.b64encode(Tempfile.read()) #Get the PDF file Contents in base64 format
        my_string=my_string.decode('ascii') #Remove the binary reference from the base64 code

    Data_={} #Creating a dictionary for the CSV headers
    field_names=['Source']
    [field_names.append('B' + str(i)) for i in range(30)] 

    CSV_Dir=WDir + 'PDFs.csv'

    if not path.exists(CSV_Dir): #Create the CSV file and add the headers 
        with open(CSV_Dir, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            f.close()

    with open(CSV_Dir, 'a',encoding="UTF8") as f: #add the PDF base64 code into the CSV file
        NRow = DictWriter(f, fieldnames=field_names, lineterminator = '\n')
        Data_={'Source':FName}
        for j in range(int(len(my_string)/32000)+1):#break the base64 code into portions of 32000 charachters before saving them into the CSV file to avoid the characters length limitation
            Data_['B' + str(j)]=my_string[j*32000:(j+1)*32000]
        NRow.writerow(Data_)

################################################
        
WDir="C:\\Users\\hamze\\Desktop\\NG BI Guru\\Video contents\\PDF Videos\\Video 1 PDF viewer\\PDFS\\" #Make sure to replace / with // for python to treat the text as a directory (Path)
for file in os.listdir(WDir): #iterate through the PDF files in the directory and extract the contents to the CSV file
    if os.path.isfile(os.path.join(WDir, file)) and file.lower().endswith(".pdf"):              
        FN=file.rsplit( ".", 1 )[ 0 ]
        ProcessPDF(WDir,FN)
