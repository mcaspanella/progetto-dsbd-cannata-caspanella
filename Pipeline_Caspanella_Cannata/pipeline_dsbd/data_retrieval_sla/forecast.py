from prophet import Prophet
import pandas as pd



def forecast(date_scrape, metric_name):
        
    dataset = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
    dataset = pd.DataFrame(dataset[metric_name])
    #print(dataset)
    dataset=dataset.reset_index()

    dataset.columns = ['ds', 'y']
    dataset['ds']= pd.to_datetime(dataset['ds']) #I valori di un csv sono stringhe, pertanto è necessario effettuare un casting
    #print(dataset.tail(10))

    model = Prophet()
    model.fit(dataset) #Addestramento modello
    future_index = model.make_future_dataframe(periods=10, freq='min') #Verranno restituiti i successivi timestamp per i prossimi dieci minuti

    forecast = model.predict(future_index) #Verrà effettuata la predizione dei valori
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10)

    return forecast
    
