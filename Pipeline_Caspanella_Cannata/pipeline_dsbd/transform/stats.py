from prometheus_api_client import MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta, datetime
import datetime as dt
import pandas as pd

def stats_for_minutes(minutes, df): #Viene restituito massimo, minimo, media e deviazione standard di ogni metrica
    df_stat = pd.DataFrame(columns=['metric','max', 'min', 'avg', 'dev_std'])
    df = df.tail(minutes) #dati degli ultimi 'minutes'
    for metric in df.columns:
        max_value = df[metric].max()
        min_value = df[metric].min()
        avg_value = df[metric].mean()
        std_value= df[metric].std()
        df_stat.loc[len(df_stat)] = [metric, max_value, min_value, avg_value, std_value]
        df_statF = df_stat.set_index('metric')
        #print(df_statF)
    return df_statF 