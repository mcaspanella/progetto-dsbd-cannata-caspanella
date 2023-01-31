from prometheus_api_client import MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import date
import os.path
import datetime as dt
import pandas as pd




def scrape(prom, metrics):  #Viene effettuato lo scrape delle metriche nelle ultime 12 ore da prometheus
    #Verrà restituito un dataframe che avrà come indice il timestamp e come colonne le metriche estratte.
    dataset = pd.DataFrame() 
    current_time, scrape_time = get_time() 
    for metric in metrics:
        metric_df = get_metric(prom,metric, current_time, scrape_time)
        if(dataset.empty):
            dataset[metric] = metric_df[['value']]
        else:
            dataset = pd.concat([dataset, metric_df], axis=1)
            dataset.rename(columns={'value':metric}, inplace=True)
                
    return dataset
    
    


def get_metric(prom, metric, current_time, scrape_time): 
    metric_data = prom.get_metric_range_data(
            metric_name=metric,
            start_time=scrape_time,
            end_time=current_time
        )
    metric_df = MetricRangeDataFrame(metric_data) 
    metric_df=metric_df.resample(rule='T').mean(numeric_only=True) # Viene effettuato un resampling di 1 minuto prendendo i valori medi
    return metric_df




def metrics_to_scrape(prom):
    metrics = []
    all_metrics = prom.all_metrics()  
    for metric in all_metrics:
        if metric.startswith('node_'): #Si effettua un controllo per verificare l'appartenenza al node exporter
            metrics.append(metric)
    
    return metrics




def get_time(): #Viene restituito lo start time e l'end time in cui dev'essere effettuato lo scrape. 
    #Lo scrape impiega circa 2 minuti, pertanto, potrebbero esserci delle incongruenze
    range = dt.timedelta(hours=12)
    current_time = dt.datetime.now()
    scrape_time = current_time - range
    return current_time, scrape_time




def update_csv(dataframe): #Verrà generato un csv con la data attuale. Il CSV, se esistente verrà aggiornato con i nuovi valori.
    date_scrape = date.today()

    file_exists = os.path.exists('/data/dataset_{}.csv'.format(date_scrape))
    #print(file_exists)
    if file_exists:
        dataframe_old = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
        dataframe_csv = pd.concat([dataframe_old, dataframe], join='outer', axis=0)
        
        dataframe_csv.to_csv('/data/dataset_{}.csv'.format(date_scrape))
        
        drop_duplicated_csv(date_scrape) #C'è un incongruenza di tipi, perciò se si dovesse fare il cleaning dal dataframe non cancellerebbe alcun duplicato                             

    else:
        dataframe.to_csv('/data/dataset_{}.csv'.format(date_scrape))
        


def drop_duplicated_csv(date_scrape): #Si effettua il cleaning del CSV
    dataframe_csv = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
    dataframe_csv = dataframe_csv.reset_index()
    dataframe_csv = dataframe_csv.drop_duplicates(subset=['timestamp'])
    dataframe_csv = dataframe_csv.sort_values(by=['timestamp'])
    if 'index' in dataframe_csv.columns:
        dataframe_csv = dataframe_csv.drop('index', axis=1)
    dataframe_csv = dataframe_csv.set_index('timestamp')
    dataframe_csv.to_csv("Prova.csv")
    
    print(dataframe_csv)
    dataframe_csv.to_csv('/data/dataset_{}.csv'.format(date_scrape))