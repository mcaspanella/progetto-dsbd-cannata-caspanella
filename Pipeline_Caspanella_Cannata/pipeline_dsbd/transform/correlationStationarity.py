from statsmodels.tsa.stattools import adfuller

import pandas as pd
import numpy as np
import math




def get_autocorrelation(dataset, dataset_corr): #Viene calcolata l'autocorrelazione percentuale delle metriche.
    #Verranno scartate da questo database quelle con NaN, poichè in presenza di deviazione standard nulla, perchè il numero rimane costante nel tempo.
    metric_autoc = {}
    for metric in dataset.columns:
        Autoc = dataset[metric].autocorr()*100  
        if(math.isnan(Autoc)):
            continue
        metric_autoc[metric] = Autoc
        
    dataset_corr['Metric'] = metric_autoc.keys()
    dataset_corr['Autocorr'] = metric_autoc.values()
    dataset_corr = dataset_corr.set_index('Metric')

    return dataset_corr




def get_correlations(dataset, dataset_corr): #Ritorna le metriche correlate con una correlazione del 70%
    for index, rows in dataset.corr().iterrows():
        correlated = set()
        for column in dataset.columns:
            value = rows[column]
            if(column != index and value > 0.7): 
                correlated.add(column)
        
        if correlated and index in dataset_corr.index:
            dataset_corr.at[index,'Correlated'] = list(correlated)
        
    return dataset_corr





def get_stationarity(dataset, dataset_corr): #Viene restituita la stazionarietà utilizzando AdFuller_Test
    dataset = dataset.dropna()

    for metric in dataset.columns:
        if metric in dataset_corr.index:

            np.seterr(divide='ignore')
            result = adfuller(dataset[metric], regression='c')  

            dataset_corr.at[metric, 'AdFuller_Test_p'] = result[1]
                
    return dataset_corr