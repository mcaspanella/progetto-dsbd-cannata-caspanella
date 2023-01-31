from flask import Flask, jsonify, render_template
import psycopg2
import connect
import forecast
from datetime import date
import pandas as pd


while True:
    try:
        conn = connect.connect_POSTGRES()
    except psycopg2.OperationalError():
        print("Database non ancora esistente")
   
    else:  
        date_scrape = date.today()
        app = Flask(__name__)



        @app.route('/', methods=['GET'])
        def home():
              return render_template('index.html')


        @app.route('/sla', methods=['GET'])
        def sla():
            return render_template('sla.html')


        @app.route('/all_metrics', methods=['GET']) #Verranno restituite tutte le metriche disponibili nel database, di cui si dispongono i valori statistici
        def get_all_metrics():
            cursor = conn.cursor()
            cursor.execute("SELECT metrics_name FROM stats_1h ")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return jsonify(data)


        @app.route('/all_metadata_metrics', methods=['GET']) #Verranno restituite tutte le metriche disponibili nel database, di cui si dispongono i metadata
        def get_all_metadata_metrics():
            cursor = conn.cursor()
            cursor.execute("SELECT metrics_name FROM metadata")
            rows = cursor.fetchall()
            return jsonify(rows)


        @app.route('/stats_1h/<metrics_name>', methods=['GET']) #Verranno restituite le statistiche della metrica specificata dell'ultima ora
        def get_stats_1h(metrics_name):
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM stats_1h WHERE metrics_name='{metrics_name}'")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return jsonify(data)
            
            
        @app.route('/stats_3h/<metrics_name>', methods=['GET']) 
        def get_stats_3h(metrics_name):
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM stats_3h WHERE metrics_name='{metrics_name}'")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return jsonify(data)


        @app.route('/stats_12h/<metrics_name>', methods=['GET'])
        def get_stats_12h(metrics_name):
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM stats_12h WHERE metrics_name='{metrics_name}'")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return jsonify(data)


        @app.route('/metadata/<metrics_name>', methods=['GET']) #Verranno restituiti i metadata della metrica specificata
        def get_metadata(metrics_name):
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM metadata WHERE metrics_name='{metrics_name}'")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return jsonify(data)
   
   
        @app.route('/sla/1h/<metrics_name>/<max>/<min>', methods=['GET']) #Restituisce il numero di violazioni nell'ultima ora
        def sla_metrics_input_1h(metrics_name, max, min):
            user_max = float(max)
            user_min = float(min)
            dataset = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
            dataset = pd.DataFrame(dataset[metrics_name])
            dataset= dataset.tail(60)
            violazioni_totali_max=0
            violazioni_totali_min=0
            max_violations = dataset[metrics_name] < user_max
            min_violations = dataset[metrics_name] > user_min
            violazioni_totali_max = max_violations.sum()
            violazioni_totali_min = min_violations.sum()
            max_message = ("Ci sono state " + str(violazioni_totali_max)) +" violazioni del massimo "
            min_message = (" e " + str(violazioni_totali_min)) +" violazioni del minimo nell'ultima ora "
            combined_message = max_message + min_message
       
            return combined_message
        
        
        @app.route('/sla/3h/<metrics_name>/<max>/<min>', methods=['GET']) 
        def sla_metrics_input_3h(metrics_name, max, min):
            user_max = float(max)
            user_min = float(min)
            dataset = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
            dataset = pd.DataFrame(dataset[metrics_name])
            dataset= dataset.tail(180)
            violazioni_totali_max=0
            violazioni_totali_min=0
            max_violations = dataset[metrics_name] < user_max
            min_violations = dataset[metrics_name] > user_min
            violazioni_totali_max = max_violations.sum()
            violazioni_totali_min = min_violations.sum()
            max_message = ("Ci sono state " + str(violazioni_totali_max)) +" violazioni del massimo "
            min_message = (" e " + str(violazioni_totali_min)) +" violazioni del minimo nelle ultime 3 ore "
            combined_message = max_message + min_message
       
            return combined_message
        
        
        @app.route('/sla/12h/<metrics_name>/<max>/<min>', methods=['GET'])
        def sla_metrics_input_12h(metrics_name, max, min):
            user_max = float(max)
            user_min = float(min)
            dataset = pd.read_csv('/data/dataset_{}.csv'.format(date_scrape), index_col=[0])
            dataset = pd.DataFrame(dataset[metrics_name])
            dataset= dataset.tail(720)
            violazioni_totali_max=0
            violazioni_totali_min=0
            max_violations = dataset[metrics_name] < user_max
            min_violations = dataset[metrics_name] > user_min
            violazioni_totali_max = max_violations.sum()
            violazioni_totali_min = min_violations.sum()
            max_message = ("Ci sono state " + str(violazioni_totali_max)) +" violazioni del massimo "
            min_message = (" e " + str(violazioni_totali_min)) +" violazioni del minimo nelle ultime 12 ore "
            combined_message = max_message + min_message
       
            return combined_message
      
      
        @app.route('/sla/future/<metrics_name>/<max>/<min>', methods=['GET']) #Viene effettuata la predizione della metrica scelta dall'utente
        def sla_metrics_input_future(metrics_name, max, min):
            violazioni_totali_max=0
            violazioni_totali_min=0
            user_metric = str(metrics_name)
            user_max = float(max)
            user_min = float(min)
            dataset_forecast = forecast.forecast(date_scrape, user_metric) #crea il dataframe che devo iterare
            max_violations = dataset_forecast['yhat'] < user_max
            min_violations = dataset_forecast['yhat'] > user_min
            violazioni_totali_max = max_violations.sum()
            violazioni_totali_min = min_violations.sum()
            max_message = ("Ci potrebbero essere " + str(violazioni_totali_max)) +" violazioni del massimo "
            min_message = (" e " + str(violazioni_totali_min)) +" violazioni del minimo nei successivi 10 minuti"
            combined_message = max_message + min_message
            return combined_message

        if __name__ == '__main__':
            app.run(host="0.0.0.0", port=5000)
