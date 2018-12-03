# Graduation_Project
This present project aims at making a data analysis of Belo Horizonte apartament prices and creating a computer model that is capable of predicting these prices. In order to do so, over 15 thousand housing prices ads were collected in August of 2018 to perform the supervised training process of statistical regression models.

You can check the data analysis here: https://nbviewer.jupyter.org/github/gpass0s/Graduation_Project/blob/master/data_analysis.ipynb

To run the project in your command line:

$ python3 -W ignore predict.py -h
predict.py -e <estimator> -c <zone_clusters> -z <zone_prices>-s <sizing> -r <rooms> -b <bathrooms> -a <apartments> -p <parking>-t <tax> -d <condominium> -l <latitude> -g <longitude>
  
$ python3 -W ignore predict.py -e gboost.pickle -c clusters.pickle -z price_zone.csv -s 69.27 -r 3 -b 2  -a 1 -p 2 -t 1.110 -d 0  -l -19.9681 -g -43.9840
347439.234591
