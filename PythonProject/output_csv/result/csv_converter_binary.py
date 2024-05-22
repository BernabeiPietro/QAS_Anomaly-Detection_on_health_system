import os
from types import NoneType
import pandas as pd

summary_field=[
    "Correctly Classified Instances",     
    "Incorrectly Classified Instances",           
    "Kappa statistic",                   
    "Mean absolute error",               
    "Root mean squared error",             
    "Relative absolute error",               
    "Root relative squared error",           
    "Coverage of cases (0.95 level)",   
    "Mean rel. region size (0.95 level)",    
]
detailed_field=['TP Rate', 'FP Rate', 'Precision', 'Recall', 'F-Measure', 'MCC', 'ROC Area', 'PRC Area', 'Class']
confusion_field=['a','b','classified']

def convert_txt_to_csv(txt_file, csv_filename_prefix):
    with open(txt_file, 'r') as f:
        data = f.read().splitlines()
    summary_dict_list=[]
    # Flag per indicare se la sezione "Riepilogo" è attiva
    summary_section = False
    detailed_section = False
    confusion_section=False

    scheme =""
    summary_index=0
    summary_data={}
    detailed_list=[]
    confusion_list=[]
    for row in data:
        
        if row.find("Scheme:")!=-1:
            scheme = row.split()[1]
            summary_data={}
            summary_data["scheme"]=scheme
        
        summary_index, row = summary_extraction(summary_section, summary_index, row, summary_data)
        if summary_index>len(summary_field)-1:
            summary_section=False
            summary_dict_list.append(summary_data)
            summary_index=0

        temp, detailed_section = detailed_extraction(detailed_section, row)
        if temp != []:
            detailed_list.append([scheme]+temp)
        
        temp, confusion_section=confusion_extraction(confusion_section, row)
        if temp != []:
            confusion_list.append([scheme]+temp)

        

        if row == "=== Summary ===":
            summary_section = True
        if row == "=== Detailed Accuracy By Class ===":
            detailed_section=True
        if row == "=== Confusion Matrix ===":
            confusion_section=True


    summary_df=pd.DataFrame(summary_dict_list)
    detailed_df=pd.DataFrame(detailed_list,columns=["scheme"]+detailed_field)
    confusion_df=pd.DataFrame(confusion_list,columns=["scheme"]+confusion_field)
    # Salva il DataFrame in un file CSV
    summary_df.to_csv(f'{csv_filename_prefix}_summary.csv', index=False)
    detailed_df.to_csv(f'{csv_filename_prefix}_detailed.csv', index=False)
    confusion_df.to_csv(f'{csv_filename_prefix}_confusion.csv', index=False)



def summary_extraction(summary_section, summary_index, row, summary_data):
    if summary_section and row!="":
            # Dividi la riga in un elenco di parole
        row=row.removeprefix(summary_field[summary_index])
        words=row.split()
            # Se la riga contiene dati, estrai i valori e le etichette
        if len(words) > 2:
            value = words[1]
            summary_data[summary_field[summary_index]]=value  
        else:
            summary_data[summary_field[summary_index]]=words[0]  
        summary_index=summary_index+1
    return summary_index,row

def detailed_extraction(detailed_section, row):
    words=[]
    if detailed_section and not (row=="" or row=='                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class'):
            # Dividi la riga in un elenco di parole
        words=row.split()
        if words[0]=="Weighted":
            words.append("Weighted Avg.")
            words=words[2:]
            detailed_section=False
    return words, detailed_section

def confusion_extraction(confusion_section, row):
    words=[]
    if confusion_section and not (row=="" or row=='   a   b   <-- classified as'):
            # Dividi la riga in un elenco di parole
        words=row.split()
        if words[3]=="b":
            confusion_section=False
        words.append(words[3]+words[4]+words[5])
        words=words[:2]+words[-1:]
    return words, confusion_section          
       
if __name__ == '__main__':
    for suffice in ["malware","dos","integrity"]:
        isExist = os.path.exists(suffice)
        if not isExist:
            os.mkdir(suffice)
        convert_txt_to_csv(f'result_{suffice}.txt', f'{suffice}/csv_file_{suffice}')
