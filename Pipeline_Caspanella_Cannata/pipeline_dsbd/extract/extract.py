import extract_utils
import connections
import pandas as pd
import time
import datetime
from kafka_config import producer


start_time = datetime.datetime.now() 
prom=connections.connect()
metrics = extract_utils.metrics_to_scrape(prom) #Restituisce tutte le metriche dell'exporter 'node exporter'

dataset = extract_utils.scrape(prom, metrics) #Vengono scaricate le metriche da prometheus delle ultime 12 ore
dataset.index = dataset.index.astype(str)  
extract_utils.update_csv(dataset) #Viene creato un csv, con i dati delle ultime 12 ore. Se il CSV è già esistente, i dati verranno aggiunti a quelli già esistenti.
#Ogni giorno verrà creato un nuovo dataframe
producer.send_msg(dataset, 0) #I messaggi verranno mandati al broker kafka

end_time = datetime.datetime.now()
runtime = end_time - start_time
with open("log.txt", "a") as log_file: #Configurazione del file di log
    log_file.write("Container extract execution time:" + str(runtime) + "\n")
time.sleep(300) #Sleep di 5 minuti

