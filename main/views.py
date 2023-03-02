from django.shortcuts import render, redirect
import numpy as np
# import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

# def home(request):
# 	return render(request,"main/index.html")



def home(request):
	context= {
		
		}
	img_size = 100
	class_names = ['cat','dog','parrot']

	if request.method == "POST":
		img_file = request.FILES['animal'] # posted img file
		
		# delete all files in media dir before saving new one
		media_dir = os.getcwd()+'/media/'

		for file in os.listdir(media_dir):
			file_path = media_dir + file
			os.remove(file_path) #delete previously saved files

		# save new file and get path for the new file
		fs = FileSystemStorage()
		filename = fs.save(img_file.name, img_file)

		file_url = fs.url(filename)
		file_url = os.getcwd() + file_url #absolute path to new file

		# load img to arr as grayscale and resize
		img_arr = cv2.imread(file_url,0) # 0  convert RGB to grayscale
		img_arr = cv2.resize(img_arr,(img_size,img_size))
		img_arr = img_arr/255.0  #scale img

		img = np.expand_dims(img_arr,0) # shape img to (1,img_size,img_size)

		#  load model 
		model_path = os.getcwd() + '/animal_model.h5'
		model = load_model(model_path)

		# make prediction
		prediction = model.predict(img)

		predicted_label = class_names[np.argmax(prediction)]
		predicted_probability = round(prediction.max()*100,2)

		context["label"] = predicted_label
		context["prob"] = predicted_probability
		
		
		

	return render(request,"main/index.html",context)



def project_info(request):
	return render(request,"main/project_info.html")