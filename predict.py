import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
import sys, getopt
import pandas as pd
import sklearn
import numpy as np
import pickle
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from scipy.special import boxcox1p


    


def transform_test_set(test,clusters,zone_prices):
    

    clus = clusters.predict(test[['Latitude', 'Longitude']])

    # Concatena a média e o desvio padrão do preços no conjunto de treino
    zonas = pd.DataFrame({"ImovelID":test['ImovelID'],"Zona":clus})
    test = pd.merge(test,
                      pd.merge(zonas,zone_prices,on="Zona",how='left')[["ImovelID",'Mean_PreçoZone',
                                                                        'Std_PreçoZone','Zona']],
                      on="ImovelID", how= 'inner')

    columns = ['ImovelID','Area','Qtde_Quartos','Qtde_Banheiros',
                'Qtde_Suites','Vagas_Garagem','Valor_Cond','Valor_IPTU',
                'Latitude','Longitude','Mean_PreçoZone','Std_PreçoZone']

    test=test[columns]
    
    return test

def predict(gboost,clusters,zone_prices,area,qtde_quartos,
            qtde_banheiros,qtde_suites,qtde_vagas_garagem,
            valor_cond,valor_IPTU,latitude,longitude):
    
    
    try:
        test = pd.DataFrame({'ImovelID':1,'Area':area,'Qtde_Quartos':qtde_quartos,
                            'Qtde_Banheiros':qtde_banheiros,
                            'Qtde_Suites':qtde_suites,'Vagas_Garagem':qtde_vagas_garagem,
                            'Valor_Cond':valor_cond,'Valor_IPTU':valor_IPTU,
                            'Latitude': latitude, 'Longitude':longitude},index=[0])
        test = transform_test_set(test,clusters,zone_prices)
        response = np.expm1(gboost.predict(test.iloc[:,1:12]))
    except:
        print ('wrong arguments passed')
        sys.exit(2)

    
    print (response[0])

def main(argv):
    

    parameters = ["estimator=","cluster=","zone=","sizing=","rooms=",
                    "bathrooms=","apartments=","parking=", "tax=", 
                    "condominium=", "latitude=","longitude=","help"]

    try:
      opts, args = getopt.getopt(argv,"he:c:z:s:r:b:a:p:t:d:l:g:", parameters)
   
    except getopt.GetoptError:
        print ('no arguments passed')
        sys.exit(2)
   
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print ('predict.py -e <estimator> -c <zone_clusters> -z <zone_prices>' +
                    '-s <sizing> -r <rooms> -b <bathrooms> -a <apartments> -p <parking>' +
                    '-t <tax> -d <condominium> -l <latitude> -g <longitude>')
            sys.exit()
        elif opt in ("-e", "--estimator"):
            with open(arg, 'rb') as handle:
                gboost = pickle.load(handle)
        elif opt in ("-c", "--cluster"):
            with open(arg, 'rb') as handle:
                clusters = pickle.load(handle)
        elif opt in ("-z", "--zone"):
            with open(arg, 'rb') as handle:
                zone_prices = pd.read_csv(handle, sep=',',encoding='utf-8')
        elif opt in ("-s", "--sizing"):
            area = boxcox1p(float(arg),0.5)
        elif opt in ("-r", "--rooms"):
            qtde_quartos = arg
        elif opt in ("-b", "--bathrooms"):
            qtde_banheiros = boxcox1p(float(arg),0.5)
        elif opt in ("-a", "--apartments"):
            qtde_suites = boxcox1p(float(arg),0.5)
        elif opt in ("-p", "--parking"):
            qtde_vagas_garagem = boxcox1p(float(arg),0.5)
        elif opt in ("-d", "--condominium"):
            valor_cond = boxcox1p(float(arg),0.5)
        elif opt in ("-t", "--tax"):
            valor_IPTU= boxcox1p(float(arg),0.5)
        elif opt in ("-l", "--latitude"):
            latitude= float(arg)
        elif opt in ("-g", "--longitude"):
            longitude= float(arg)

    predict(gboost,clusters,zone_prices,area,qtde_quartos,qtde_banheiros,qtde_suites,
           qtde_vagas_garagem,valor_cond,valor_IPTU,latitude,longitude)

if __name__ == "__main__":
   main(sys.argv[1:])