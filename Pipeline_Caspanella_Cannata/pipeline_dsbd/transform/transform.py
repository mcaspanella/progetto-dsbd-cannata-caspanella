from ast import literal_eval
import pandas as pd
import snappy
import json
import stats
import metadata
import datetime
from kafka_config import consumer_config, producer



minutes = [60, 180, 720] 
messages = consumer_config.consumer('prometheusdata', 0) #Avvio del consumer
dataset_corr = pd.DataFrame(columns=['Metric', 'Autocorr', 'Correlated', 'AdFuller_Test_p'])



for message in messages:
    start_time = datetime.datetime.now() 


    message_decomp = snappy.decompress(message.value) #Decompressione dataframe

    df_json_dict = json.loads(message_decomp)

    dataset = pd.DataFrame.from_dict(df_json_dict)
    
    dataset_corr = metadata.get_metadata(dataset, dataset_corr) #Viene restituito un daframe contenente le correlazioni e la stazionarietà tramite adfuller_test
    #Il dataframe avrà come indice le metriche, mentre le colonne conterranno i metadati
    #Invio del dataframe con le correlazioni a load
    producer.send_msg(dataset_corr, 1)
    messages.commit()
    #print(dataset_corr) #invece di stampare devo inviare
    
    
    dataset_stats_1h = stats.stats_for_minutes(60, dataset) #Viene restituito il dataset con le statistiche (max, min, avg, dev_std) dell'ultima ora
    dataset_stats_3h = stats.stats_for_minutes(180, dataset) 
    dataset_stats_12h = stats.stats_for_minutes(720, dataset) 
    #I dataframes avranno come indice le metriche, mentre le colonne conterranno i valori statistici

    
    #Invio dei tre dataframe al container Load
    producer.send_msg(dataset_stats_1h, 2) 
    producer.send_msg(dataset_stats_3h, 3)
    producer.send_msg(dataset_stats_12h, 4)
    end_time = datetime.datetime.now()

    runtime = end_time - start_time
    with open("log.txt", "a") as log_file:
        log_file.write("Container transform execution time:" + str(runtime) + "\n")



