from django.shortcuts import render
from django.http import HttpResponse
from .models import Question as QuestionModel
from django.views.decorators.csrf import csrf_exempt 
from json import dumps
import math
import os ,sys
import pandas as pd
from sklearn.linear_model import LinearRegression


def BUI(DMC ,DC):
	if(DMC <= 0.4 * DC):
		return 0.8 * DMC * DC/(DMC + 0.4 * DC)
	else:
		return DMC -(1.00- 0.8 * DC/(DMC + 0.4 * DC)) * (0.92 + (0.0114 * DMC) ** 1.7) 


def FWI(BUI,ISI):
	if(BUI <= 80.00):
		fD = 0.626 * (BUI) ** 0.809 + 2.00
	else:
		fD = 1000.00 / 25.00 +108.64 * math.exp(-0.023 * BUI)
	B = 0.1 * ISI *fD
	if(B > 1.00):
		return math.exp(2.72 *(0.434 * math.log(B)) ** 0.647)	
	else:
		return B

@csrf_exempt
def Question(request):
	if(request.method=="GET"):
		return render(request,'index.html')
	elif(request.method=="POST"):
		FFMC = float(request.POST.get('FFMC'))
		DMC = float(request.POST.get('DMC'))
		DC = float(request.POST.get('DC'))
		ISI = float(request.POST.get('ISI'))
		RH = float(request.POST.get('RH'))
		temp = float(request.POST.get('temp'))
		wind = float(request.POST.get('wind'))
		bui = BUI(DMC , DC)
		fwi = FWI(bui , ISI)
		p = [[temp ,RH ,wind,fwi]]
		r=QuestionModel(
			FFMC =FFMC,
			DMC =DMC,
			DC=DC,
			ISI = ISI,	
			RH = RH, 
			temp = temp,
			wind = wind,
			fwi = fwi,
			)
		r.save()

	link= './Downloads/forestfires.csv'
	data_pandas = pd.read_csv(link)
	i=0
	forestweatherindex= []
	for row in data_pandas.itertuples():
		bui = BUI(data_pandas['DMC'][i] , data_pandas['DC'][i])
		f = FWI(bui,data_pandas['ISI'][i])
		forestweatherindex.insert(i , f)
		i = i+1
	X = list(zip(data_pandas.temp , data_pandas.RH ,  data_pandas.wind , forestweatherindex))
	X_train = X[:-50]
	X_test = X[-50:]
	y_train = data_pandas.area[:-50]
	y_test = data_pandas.area[-50:]
	lm = LinearRegression(X,data_pandas.area[:-50])
	lm.fit(X_train , y_train )
	output =lm.predict(p)
	f =open("xyz.txt" ,"wb")
	f.write(output)
	output= 100
	return render(request, 'index.html', {'area': output, 'ffmc': FFMC,
										'dmc': DMC, 'dc': DC, 'isi': ISI,
										'rh': RH, 'temp': temp, 'wind': wind,
										'fwi': fwi })