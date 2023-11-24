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


#function that preo-process the text and create the dictionary
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
    
    return my_dict
    


#function that call 'dictionary' for every text in a folder and create a dictionary for all the texts
def text_in_directory(dir):
    dizionario_parole_ordinato = {}
    for testo in os.listdir(dir):
        percorso_file = os.path.join(dir, testo)
        with open(percorso_file, 'r', encoding='utf-8') as file:
            testo = file.read()
            dizionario_parole_ordinato = dictionary(testo, dizionario_parole_ordinato)
    return dizionario_parole_ordinato
        
        
        
#deletes all the key that appears in both dictionaries
def bag_of_words(medic_dict, nonmedic_dict):
    dict_copy_medic = medic_dict.copy()
    dict_copy_nonmedic = nonmedic_dict.copy()
    for index in dict_copy_medic:
        for index2 in dict_copy_nonmedic:
            if index2 == index:
                del medic_dict[index]
                del nonmedic_dict[index2]
    
    with open('dizionario_Occorrenze\medici.txt', 'w', encoding='utf-8') as file:
        json.dump(medic_dict , file, indent=4)
        
    with open('dizionario_Occorrenze\ nonmedici.txt', 'w', encoding='utf-8') as file:
        json.dump(nonmedic_dict , file, indent=4)
    
    return medic_dict,nonmedic_dict


#create a dictionary with all the frequency for every word

def frequencies (dict , dir):
    sum = 0
    for index in dict:
        sum += dict[index]
    for index in dict:
        dict[index] = float(dict[index] / sum)
    if dir == 'mediche':
        with open('dizionario_Frequenze\ frequenze_medici.txt', 'w', encoding='utf-8') as file:
            json.dump(dict , file, indent=4)
    else: 
        with open('dizionario_Frequenze\ frequenze_nonmedici.txt', 'w', encoding='utf-8') as file:
            json.dump(dict , file, indent=4)

    return dict


#calculate the prior probability of being a medical/nonmedical using the number of documents in the train set

def prior_probability(cartellamedici, cartellanonmedici):
    num_medici = len(os.listdir(cartellamedici))
    num_nonmedici = len(os.listdir(cartellanonmedici))
    total_docs = num_medici + num_nonmedici
    
    prob_medici = num_medici / total_docs
    prob_nonmedici = num_nonmedici / total_docs
    
    return prob_medici, prob_nonmedici
                
    
    
#open the text in chronological order, for every text it creates the dictionary calling the function and 
#for every word that appears in one of the medical/nonmedical dictionary it sub the log of the frequencies of that word
#in the end it sub the log of prior probability 
#the text is classified based on the higher sum 



#prova
def text_classifier( med_dict, nonmed_dict):
    testo_risultato = {}
    
    prob_prior_medico , prob_prior_nonmedico = prior_probability('testimedici' , 'testinonmedici')
        
    files = [f for f in os.listdir('testi_da_classificare') if f.endswith(".txt")]
    files_ordinati = sorted(files, key=lambda x: os.path.getctime(os.path.join('testi_da_classificare', x)))
    
    for testo in files_ordinati:
        sum_med = 0
        sum_nonmed = 0
        dict_text = {}
        with open(f'testi_da_classificare\{testo}', 'r', encoding='utf-8') as file:
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

            sum_med -= math.log(prob_prior_medico)
            sum_nonmed -= math.log(prob_prior_nonmedico)
            if sum_med > sum_nonmed:
                testo_risultato [testo] = True
        
            else:
                testo_risultato [testo] = False
        
    return testo_risultato


#calculates the accuracy precision and recall using a list called gold_label created when I imported the file that ned to be classified
#it uses the prediction of my classifier and the effective category of the text to calculate all the paramters of my classifier
def accuracy (dict_risultato):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    
    with open('goldlabels.txt', 'r', encoding='utf-8') as file:
        gold_label = [line.strip() for line in file]
    for indice_dict, true_value in zip(dict_risultato, gold_label):
        if dict_risultato[indice_dict] == int(true_value) and dict_risultato[indice_dict] == 1:
            true_positive += 1
        if dict_risultato[indice_dict] == int(true_value) and dict_risultato[indice_dict] == 0:
            true_negative += 1
        if dict_risultato[indice_dict] != int(true_value) and dict_risultato[indice_dict] == 1:
            false_positive += 1
        if dict_risultato[indice_dict] != int(true_value) and dict_risultato[indice_dict] == 0:
            false_negative += 1
            
    accuracy_value = (true_positive + true_negative) / float(true_positive + true_negative + false_positive + false_negative)
    precision = true_positive / float(true_positive + false_positive)
    recall = true_positive / float (true_positive + false_negative)

    return accuracy_value , precision , recall
    


dict_medico = text_in_directory('testimedici')
dict_nonmedical = text_in_directory('testinonmedici')
bag_of_words_med, bag_of_words_nonmed = bag_of_words(dict_medico,dict_nonmedical)
dict_freq_med = frequencies(bag_of_words_med, 'mediche')
dict_freq_nonmed = frequencies (bag_of_words_nonmed, 'non_mediche')

dict_risultato = text_classifier( dict_freq_med,dict_freq_nonmed)
for chiave, valore in dict_risultato.items():
    if valore:
        print(f"{chiave}: testo medico")
    else:
        print(f"{chiave}: testo non medico")

accuracy_value ,precision, recall = accuracy(dict_risultato)
print(accuracy_value*100)
print(recall*100)
print(precision*100)
    



    