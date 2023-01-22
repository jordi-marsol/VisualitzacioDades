import pandas as pd
import os
#pip install xlrd per obrir excel

script_dir = os.path.dirname(__file__) 
rel_path = "CSV\\EPSH_2022.csv"
abs_file_path = os.path.join(script_dir, rel_path)

# llegeixo arxiu csv, el dataframe ja llegirà la primera fila com a capçalera
data = pd.read_csv(abs_file_path, delimiter='\t', dtype='str') 

# llegeixo el excel on està la taula amb la equivalencia entre els noms curts de les variables de la capçalera i la seva descripció
# volem que la descripció quedi com a nom de variable pel Tableau
diccionari = os.path.join(script_dir, 'dr_EPSH_2022.xlsx')
xls = pd.ExcelFile(diccionari)
df0 = pd.read_excel(xls, 'Diseño')

vars2 = pd.DataFrame(df0.iloc[1:323,[0,1,7,8]].values)
varnom=dict(df0.iloc[1:324,[0,8]].values) # llegim de la fila 1 a la 323, les columnes 0 (variables) i 8 (descripcions) i convertim els seus valors en un diccionari al final del programa

#funció per llegir de l'excel els codis corresponents als valors buscats
#retorna un diccionari amb els parells codi:valor
def dic_valors(code,tablas):
    trobat = 0
    i= 0
    df = pd.read_excel(xls, tablas)
    codvar = {}
    for index, row in df.iterrows():
        if index >2:
            if (row[0]==code):
                trobat = 1
            if trobat == 1:
                if pd.isnull(row[0]):
                    break            
                if i > 1:
                    codvar[str(row[0])] = str(row[1]) #faig que tot sigui string perquè la taula de dades també ho he decidit aixi i poder-ho comparar
                i += 1
    return codvar

dfinal = pd.DataFrame ()
dtot = {}
#bucle principal que llegeix del csv de les dades cada variable
#de cada variable en fa la traducció de valors i els va juntant en una gran taula/diccionari
for (columnName, columnData) in data.items():
    keys = columnData.values
    row = vars2[vars2[0]==columnName]
    try:
        if not pd.isnull(row[1].values[0]): #camps que no fan servir diccionari
            values = dic_valors(row[1].values[0],row[2].values[0])
            new_values = []
            for key in keys:
                try:
                    value = values[key]
                    new_values.append(value)
                except KeyError:
                    new_values.append(key)                              
            dtot.setdefault(columnName,new_values)
        else:
            dtot.setdefault(columnName,keys)
    except:
        pass
    
dfinal = pd.DataFrame (dtot)
dfinal.rename(columns=varnom, inplace=True)
sortida =os.path.join(script_dir, 'dfinal.csv')
dfinal.to_csv(sortida,index=False) 
