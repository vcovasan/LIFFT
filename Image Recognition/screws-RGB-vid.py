# Video IR
import cv2
import numpy as np
import imutils

def getScrews(img):
	img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,img2 = cv2.threshold(img1,140,255,cv2.THRESH_BINARY)
	img3 = cv2.medianBlur(img2,3)
	img4 = cv2.GaussianBlur(img3,(5,5),0)
	img5 = cv2.Canny(img4, 174,255)

	out = cv2.hconcat([img2,img3,img4,img5])
	# cv2.imshow('th1,medBlur,edged,mask',out)
	# cv2.waitKey(0)

	cnts1 = cv2.findContours(img5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts1 = imutils.grab_contours(cnts1)
	cnts1 = sorted(cnts1, key = cv2.contourArea, reverse = True)[:6]
	cxList1 = []
	cyList1 = []
	cwList1 = []
	chList1 = []	
	for c1 in cnts1:
		xFlag1 = False
		yFlag1 = False
		peri1 = cv2.arcLength(c1, True)
		approx1 = cv2.approxPolyDP(c1, 0.05 * peri1, True)
		xx1,yy1,ww1,hh1 = cv2.boundingRect(approx1)
		aspect1 = ww1/hh1
		# print('cxList: ', cxList, " cyList: " , cyList)
		# print('x', xx, 'y', yy)

		for i in cxList1:
			if abs(xx1-i)<5:
				# print('same')
				xFlag1 = True
		for j in cyList1:
			if abs(yy1-j)<5:
				# print('same')
				yFlag1 = True

		# print("x:",xx1,"y:",yy1,"vertices:",len(approx1),"  area:",cv2.contourArea(approx1),"\t  aspect:",round(aspect1,1) )	
		if xFlag1==False and yFlag1==False and cv2.contourArea(approx1)>2 and cv2.contourArea(approx1)<200 and aspect1>0.8:
			print("x:",xx1,"y:",yy1,"vertices:",len(approx1),"  area:",cv2.contourArea(approx1),"\t  aspect:",round(aspect1,1) )	
			cxList1.append(xx1)
			cyList1.append(yy1)		
			cwList1.append(ww1)
			chList1.append(hh1)		
			cv2.rectangle(img,(xx1,yy1),(xx1+(ww1),yy1+(hh1)),(0,255,0),2)
			if cv2.contourArea(approx1)>130 and cv2.contourArea(approx1)<200 and aspect1>1.05 and aspect1<1.25:
				img6 = cv2.putText(img,'3',(xx1+ww1+3,yy1+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2, cv2.LINE_AA)
			if cv2.contourArea(approx1)>95 and cv2.contourArea(approx1)<130 and aspect1>1.15 and aspect1<1.45:
				img6 = cv2.putText(img,'2',(xx1+ww1+3,yy1+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2, cv2.LINE_AA)
			if cv2.contourArea(approx1)>70 and cv2.contourArea(approx1)<95 and aspect1>0.85 and aspect1<1.45:
				img6 = cv2.putText(img,'1',(xx1+ww1+3,yy1+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2, cv2.LINE_AA)
			# cv2.imshow('outScrews or img in func',img)
			# cv2.waitKey(0)
	return img









cap = cv2.VideoCapture('fuelProbe2.m4v')
i = 0
while(True):    

	ret, img = cap.read()	
	if(ret==False):
		break

	image_color = cv2.resize(img,None,fx=0.6,fy=0.6)
	image_color_orig = image_color.copy()
	image_color_copy = image_color.copy()
	# cv2.imshow('orig',image_color)
	# cv2.waitKey(0)

	boundaries = [ ([155, 90, 110], [200, 200, 200]) ]
	for (lower, upper) in boundaries:
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
		mask = cv2.inRange(image_color, lower, upper)
		out = cv2.bitwise_and(image_color, image_color, mask = mask)		

	# cv2.imshow('out',out)
	# cv2.waitKey(0)

	kernel = np.ones((3, 3), np.uint8)
	mask = cv2.erode(out, kernel, iterations=2)
	mask = cv2.dilate(mask, kernel, iterations=5)
	# cv2.imshow('mask',mask)
	# cv2.waitKey(0)

	medBlur = cv2.medianBlur(mask,3)

	edged = cv2.Canny(medBlur, 245,255)
	# cv2.imshow('edged',edged)
	# cv2.waitKey(0)

	gausBlur = cv2.GaussianBlur(medBlur,(5,5),0)
	# cv2.imshow('gblur',gausBlur)
	# cv2.waitKey(0)


	cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)
		vertices = len(approx)
		xx,yy,ww,hh = cv2.boundingRect(approx)
		aspect = round(ww/hh,1)
		area = cv2.contourArea(approx)

		print("===================================")
		print("x:",xx,"y:",yy,"vertices:",vertices,"  area:",area,"\t  aspect:",aspect )	
		print("===================================")

		if area>11000 and area<14000 and aspect>0.45 and aspect<0.75 and vertices==4:
			# print("x:",xx,"y:",yy,"vertices:",vertices,"  area:",area,"\t  aspect:",aspect )	
			# cv2.rectangle(image_color_copy,(xx,yy),(xx+ww,yy+hh),(0,255,0),1)			
			# cv2.imshow('output',image_color_copy)
			# cv2.waitKey(0)

			outScrews = getScrews(image_color_copy[yy+1:yy+hh,xx+1:xx+ww])
			image_color_orig[yy+1:yy+hh,xx+1:xx+ww] = outScrews
			
			# cv2.imshow('image_color_orig',image_color_orig)

			break
		
	cv2.imshow('image_color_orig',image_color_orig)
			
	# out = cv2.hconcat([image_color,image_color_copy])
	# cv2.imshow('out',out)
	# cv2.imshow('edged',edged)



	if cv2.waitKey(0) & 0xFF == ord('q'):
		break









	# for i in cxList:
	# 	if abs(xx-i)<5:
	# 		# print('same')
	# 		xFlag = True
	# for j in cyList:
	# 	if abs(yy-j)<5:
	# 		# print('same')
	# 		yFlag = True

	# if xFlag==False and yFlag==False and cv2.contourArea(approx)>4 and cv2.contourArea(approx)<404:
		# cxList.append(xx)
		# cyList.append(yy)
		# imbox = image_color_copy[yy-30:yy+30,xx-10:xx+30]		
		# avgrow1 = np.average(imbox, axis=0)
		# avg1 = np.average(avgrow1, axis=0)
		# if avg1[2]>130:



