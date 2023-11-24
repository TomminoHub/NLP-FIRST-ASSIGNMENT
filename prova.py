import nltk
import math
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
import json

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def leggi_file_e_crea_dizionario(nome_file):
    dizionario = {}
    with open(nome_file, 'r',encoding='utf-8') as file:
        dizionario = json.load(file)
    return dizionario


def prior_probability(cartellamedici, cartellanonmedici):
    num_medici = len(os.listdir(cartellamedici))
    num_nonmedici = len(os.listdir(cartellanonmedici))
    total_docs = num_medici + num_nonmedici
    
    prob_medici = num_medici / total_docs
    prob_nonmedici = num_nonmedici / total_docs
    
    return prob_medici, prob_nonmedici
                



def dictionary (text, my_dict):
    lemmatizzatore = WordNetLemmatizer()
    stoplist = stopwords.words('english')
    parole = word_tokenize(text)
    for parola in parole:
        parola_minuscola = parola.lower()
        parola_minuscola = lemmatizzatore.lemmatize(parola_minuscola)
        if parola_minuscola not in stoplist and parola_minuscola.isalnum() and not parola_minuscola.isnumeric():
            if parola_minuscola not in my_dict:
                my_dict[parola_minuscola] = 1
            else:
                my_dict[parola_minuscola] += 1          
    my_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))
    
    print(text)
    print(dict_text)
    
    return my_dict


files = [f for f in os.listdir('testi_da_classificare') if f.endswith(".txt")]
files_ordinati = sorted(files, key=lambda x: os.path.getctime(os.path.join('testi_da_classificare', x)))
testo_risultato = {}
    
prob_prior_medico , prob_prior_nonmedico = prior_probability('testimedici' , 'testinonmedici')
med_dict = leggi_file_e_crea_dizionario('frequenze_medici.txt')
nonmed_dict = leggi_file_e_crea_dizionario('frequenze_nonmedici.txt')
if 'Bradycardia.txt' in files_ordinati:
    print('ok')

for testo in files_ordinati:
        
    if testo == 'Bradycardia.txt' or testo == 'Brugada syndrome.txt' or testo == 'Cardiac arrest.txt':

    
        sum_med = 0
        sum_nonmed = 0
        dict_text = {}
        with open(f'testi_da_classificare\{testo}', 'r', encoding='utf-8') as file:
            print(testo)
            text = file.read()
            dict_text.clear()
            dict_text = dictionary(text, dict_text)
            
            with open(f'dizionario_da_classificare\{testo}', 'w', encoding='utf-8') as file:
                json.dump(dict_text , file, indent=4)
            for index_1 in dict_text:
                for index_2 in med_dict:
                    if index_1 == index_2:
                        sum_med -= math.log(med_dict[index_2])
                        break

            for index_1 in dict_text:
                for index_2 in nonmed_dict:
                    if index_1 == index_2:
                        sum_nonmed -= math.log(nonmed_dict[index_2])
                        break
                    '''
            if testo == 'Bradycardia.txt':
                print(testo)
                print(dict_text)
                
            if testo == 'Brugada syndrome.txt':
                print(testo)
                print(dict_text)
            
            if testo == 'Cardiac arrest.txt':
                print(testo)
                print(dict_text)
                
            print('---------------------')
            '''
            
            
            sum_med -= math.log(prob_prior_medico)
            sum_nonmed -= math.log(prob_prior_nonmedico)
            if sum_med > sum_nonmed:
                testo_risultato [testo] = True
        
            else:
                testo_risultato [testo] = False
                
            print(testo_risultato[testo])
        
