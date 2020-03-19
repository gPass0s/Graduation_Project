#!/usr/bin/python3.6

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 07 20:28:51 2018
Edited on Mon 24 11:42:09 2020

@author: guilherme passos |twiiter: @gpass0s
"""

import pandas as pd
import numpy as np
import pickle
import sklearn
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from scipy.special import boxcox1p


def cors_enabled_function_auth(request):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }
    parameters = request.get_json()
    response = main(parameters)

    return (response, 200, headers)


def main(parameters):

    with open("source/gboost.pickle", 'rb') as handle:
        gboost = pickle.load(handle)

    with open("source/clusters.pickle", 'rb') as handle:
        clusters = pickle.load(handle)

    with open("source/price_zone.csv", 'rb') as handle:
        zone_prices = pd.read_csv(handle, sep=',', encoding='utf-8')

    try:
        area = boxcox1p(float(parameters['tamanho']), 0.5)
    except TypeError:
        return "Parameter size not passed"

    try:
        qtde_quartos = float(parameters['quartos'])
    except TypeError:
        return "Parameter rooms not passed"
    
    try:
        qtde_banheiros = boxcox1p(float(parameters['banheiros']), 0.5)
    except TypeError:
        return "Parameter bathrooms not passed"
    
    try:
        qtde_suites = boxcox1p(float(parameters['suites']), 0.5)
    except TypeError:
        return "Parameter suite not passed"
    
    try:
        qtde_vagas_garagem = boxcox1p(float(parameters['vagas']), 0.5)
    except TypeError:
        return "Parameter parking not passed"

    try:
        valor_cond = boxcox1p(float(parameters['condominio']), 0.5)
    except TypeError:
        return "Parameter condominum price not passed"
    
    try:
        valor_IPTU = boxcox1p(float(parameters['iptu']), 0.5)
    except:
        return "Parameter IPTU not passed"
    
    try:
        latitude = float(parameters['lat'])
        longitude = float(parameters['lng'])
    except:
        return "Parameter location not passed"

    response = predict(
        gboost,
        clusters,
        zone_prices,
        area,
        qtde_quartos,
        qtde_banheiros,
        qtde_suites,
        qtde_vagas_garagem,
        valor_cond,
        valor_IPTU,
        latitude,
        longitude
    )
    return str(response)


def transform_test_set(test,clusters,zone_prices):

    clus = clusters.predict(test[['Latitude', 'Longitude']])

    # Concatena a média e o desvio padrão do preços no conjunto de treino
    zonas = pd.DataFrame({"ImovelID":test['ImovelID'],"Zona":clus})
    test = pd.merge(test,
                        pd.merge(zonas,zone_prices, on="Zona", how='left')[["ImovelID",'Mean_PreçoZone',
                                                                        'Std_PreçoZone','Zona']],
                        on="ImovelID", how= 'inner')

    columns = ['ImovelID','Area','Qtde_Quartos','Qtde_Banheiros',
                'Qtde_Suites','Vagas_Garagem','Valor_Cond','Valor_IPTU',
                'Latitude','Longitude','Mean_PreçoZone','Std_PreçoZone']

    test=test[columns]
    
    return test

def predict(
    gboost,
    clusters,
    zone_prices,
    area,
    qtde_quartos,
    qtde_banheiros,
    qtde_suites,
    qtde_vagas_garagem,
    valor_cond,
    valor_IPTU,
    latitude,
    longitude
):


    test = pd.DataFrame({'ImovelID':1,'Area':area,'Qtde_Quartos':qtde_quartos,
                        'Qtde_Banheiros':qtde_banheiros,
                        'Qtde_Suites':qtde_suites,'Vagas_Garagem':qtde_vagas_garagem,
                        'Valor_Cond':valor_cond,'Valor_IPTU':valor_IPTU,
                        'Latitude': latitude, 'Longitude':longitude},index=[0])
    test = transform_test_set(test,clusters,zone_prices)

    response = np.expm1(gboost.predict(test.iloc[:,1:12]))

            
    return response[0]
