import pandas as pd
import snappy
import json
from kafka_config import consumer_config
import datetime
import createDB

messages_metadata = consumer_config.consumer('prometheusdata', 1) 
tables = ["metadata", "stats_1h","stats_3h","stats_12h"]
for table in tables: #Vengono create le tabelle: metadata, stats_1h, ***_3h, ***_12h
    createDB.create_table(table)



for msg_metadata in messages_metadata: #Sarranno aggiunti i valori del dataframe conentente i metadati dentro la tabella 'metadata'
    start_time = datetime.datetime.now()
    msg_metadata_decomp = snappy.decompress(msg_metadata.value)

    # Converti la stringa JSON in un dizionario
    json_dict_metadata = json.loads(msg_metadata_decomp)

    # Crea un dataframe utilizzando il dizionario
    dataset_stat = pd.DataFrame.from_dict(json_dict_metadata)
    dataset_stat.index.name='metrics_name'
    print(dataset_stat)
    
    createDB.add_metrics("metadata", dataset_stat) 
    
    messages_metadata.commit()
    messages_metadata.close()

    

for partition in range(2,5): #Sarranno aggiunti i valori del dataframe contenente i valori statistici dentro la tabella 'stats_(time)'
    messages_stat = consumer_config.consumer('prometheusdata', partition)
    for msg_stat in messages_stat:
        msg_stat_decomp = snappy.decompress(msg_stat.value)

        # Converti la stringa JSON in un dizionario
        json_dict_stat = json.loads(msg_stat_decomp)

        # Crea un dataframe utilizzando il dizionario
        dataset_stat = pd.DataFrame.from_dict(json_dict_stat)
        dataset_stat.index.name='metrics_name'
        
        print(dataset_stat)
        
        if(partition == 2):
            createDB.add_metrics("stats_1h", dataset_stat) 
        elif(partition == 3):
            createDB.add_metrics("stats_3h", dataset_stat) 
        elif(partition == 4):
            createDB.add_metrics("stats_12h", dataset_stat) 
        
        messages_stat.commit()
        end_time = datetime.datetime.now()
        runtime = end_time - start_time
        with open("log.txt", "a") as log_file:
            log_file.write("Container load execution time:" + str(runtime) + "\n")
    
        messages_stat.close()


