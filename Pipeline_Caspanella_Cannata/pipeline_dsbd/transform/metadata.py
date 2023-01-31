import pandas as pd
import correlationStationarity

def get_metadata(dataset, dataset_corr):

    dataset_corr = correlationStationarity.get_autocorrelation(dataset, dataset_corr)
    dataset_corr = correlationStationarity.get_correlations(dataset, dataset_corr)
    dataset_corr = correlationStationarity.get_stationarity(dataset, dataset_corr)

    return dataset_corr


