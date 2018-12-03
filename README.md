# Graduation_Project

This present project aims at making a data analysis of Belo Horizonte apartament prices and creating a computer model that is capable of predicting these prices. To do so, over 60 thousand housing ads were collected from August to October of 2018. Then, supervised training was performed on regression algorithms of machine learning that are based on statistic methods, biological systems and decision trees. The data analysise can be found <a href=https://nbviewer.jupyter.org/github/gpass0s/Graduation_Project/blob/master/data_analysis.ipynb>here</a>. Note that the data analysis done in this project is timeless and ignores the variation of apartaments prices within time window previously cited. The final results were successfully validated and they prove that this approach is able to generate useful predictions for the housing market of any Brazilian city.

> To run the project in your command line, type:

$ python3 -W ignore predict.py -e gboost.pickle -c clusters.pickle -z price_zone.csv -s 69.27 -r 3 -b 2  -a 1 -p 2 -t 1.110 -d 0  -l -19.9681 -g -43.9840
347439.234591
