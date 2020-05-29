# Video IR
import cv2
import numpy as np
import imutils



cap = cv2.VideoCapture('IR.mp4')
i = 0
while(True):    


	ret, img = cap.read()	
	if(ret==False):
		break

	image_color = cv2.resize(img,None,fx=0.25,fy=0.25)
	image_color_copy = image_color.copy()

	image_gray = cv2.cvtColor(image_color,cv2.COLOR_BGR2GRAY)
	ret,th1 = cv2.threshold(image_gray,190,255,cv2.THRESH_BINARY)
	medBlur = cv2.medianBlur(th1,3)
	gausBlur = cv2.GaussianBlur(medBlur,(5,5),0)
	edged = cv2.Canny(gausBlur, 245,255)


	out = cv2.hconcat([th1,medBlur,edged,gausBlur])
	cv2.imshow('th1,medBlur,edged,mask',out)
	# cv2.waitKey(0)

	cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
	detectFlag = False
	screenCnt = None
	cxList = []
	cyList = []
	for c in cnts:
		xFlag = False
		yFlag = False
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)
		xx,yy,ww,hh = cv2.boundingRect(approx)
		aspect = ww/hh

		for i in cxList:
			if abs(xx-i)<5:
				# print('same')
				xFlag = True
		for j in cyList:
			if abs(yy-j)<5:
				# print('same')
				yFlag = True

		if xFlag==False and yFlag==False and cv2.contourArea(approx)>45 and cv2.contourArea(approx)<80 and len(approx)<6 and aspect>0.6 and aspect<1.2 and yy>0 and gausBlur.mean()>50:
			print("x:",xx,"\ty:",yy,"\tvertices:",len(approx),"  area:",cv2.contourArea(approx),"\t  aspect:",round(aspect,1) )	
			
			cxList.append(xx)
			cyList.append(yy)
			imbox = image_color_copy[yy-30:yy+30,xx-10:xx+30]		
			# avgrow1 = np.average(imbox, axis=0)
			# avg1 = np.average(avgrow1, axis=0)

			cv2.rectangle(image_color_copy,(xx-ww,yy-hh),(xx+(2*ww),yy+(2*hh)),(0,255,0),2)

			# cv2.imshow('output',image_color_copy)
			# cv2.waitKey(0)
		cv2.imshow('output',image_color_copy)
		# print('mean: ',gausBlur.mean())
	if cv2.waitKey(0) & 0xFF == ord('q'):
		break






