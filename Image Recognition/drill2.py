# Video IR - Drill 2
import cv2
import numpy as np
import imutils


def getBackground(img):
	maskFlag = False
	out = img
	image_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,th1 = cv2.threshold(image_gray,170,255,cv2.THRESH_BINARY)
	# cv2.imshow('th1',th1)

	kernel = np.ones((2, 2), np.uint8)
	mask = cv2.erode(th1, kernel, iterations=4)
	mask = cv2.dilate(mask, kernel, iterations=2)
	cv2.imshow('mask',mask)
	cv2.moveWindow('mask', 512,440)

	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
	
	cxList = []
	cyList = []
	print("--------")		
	for c in cnts:
		xFlag = False
		yFlag = False
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.05 * peri, True)
		vertices = len(approx)
		area = cv2.contourArea(approx)
		xx,yy,ww,hh = cv2.boundingRect(approx)
		aspect = round(ww/hh,1)
		imgmean = round(mask.mean(),0)
		print( "x:",xx,  "\ty:",yy,  "\tvertices:",vertices, " aspect:",aspect,  "    imgmean:",imgmean, " area:",area )			

		for i in cxList:
			if abs(xx-i)<5:
				xFlag = True
		for j in cyList:
			if abs(yy-j)<5:
				yFlag = True
		if xFlag==False and yFlag==False and vertices<8 and area>5000 and area<7000 and aspect>0.3 and aspect<0.8 and imgmean>8 and imgmean<30:
			maskFlag = True
			cxList.append(xx)
			cyList.append(yy)

			mask2 = np.zeros(img.shape, dtype=np.uint8)
			mask2[:,:,0] = mask
			mask2[:,:,1] = mask
			mask2[:,:,2] = mask
			out = cv2.bitwise_and(img,mask2)
			# cv2.imshow('out',out)
			# cv2.moveWindow('out', 0,440)
			# cv2.rectangle(img,(xx,yy),(xx+ww,yy+hh),(0,255,0),2)

	# cv2.imshow('out',out)
	# cv2.moveWindow('out', 768,440)

	return out,mask,maskFlag


def getScrews(img):
	# cv2.imshow('imgc',imgc)
	# cv2.moveWindow('imgc', 0,440)

	medBlur = cv2.medianBlur(img,5)
	# cv2.imshow('img2',medBlur)
	# cv2.moveWindow('img2', 512,440)

	edged = cv2.Canny(medBlur, 245,255)
	cv2.imshow('img3',edged)
	cv2.moveWindow('img3', 0,440)

	cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
	
	cxList = []
	cyList = []
	print("--------")		
	for c in cnts:
		xFlag = False
		yFlag = False
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.15 * peri, True)
		vertices = len(approx)
		area = round(cv2.contourArea(approx),0)
		xx,yy,ww,hh = cv2.boundingRect(approx)
		aspect = round(ww/hh,1)
		imgmean = round(medBlur.mean(),0)
		cntmean = np.array(cv2.mean(medBlur[yy:yy+hh,xx:xx+ww]))
		cntmean = round(cntmean[0],1)

		print( "x:",xx,  "\ty:",yy,  "\tvertices:",vertices,  "  aspect:",aspect,  "\timgmean:",imgmean,   " area:",area,"\tm:",cntmean )			

		for i in cxList:
			if abs(xx-i)<3:
				xFlag = True
		for j in cyList:
			if abs(yy-j)<5:
				yFlag = True
		if xFlag==False and yFlag==False and vertices<8 and area>5 and area<100 and aspect>0.4 and aspect<1.3 and imgmean>8 and imgmean<40 and cntmean<140:
			cxList.append(xx)
			cyList.append(yy)
			
			cv2.rectangle(image_color_copy,(xx,yy),(xx+ww,yy+hh),(0,255,0),2)

	# cv2.imshow('imgc',imgc)
	# cv2.moveWindow('imgc', 0,440)

	return image_color_copy


def getDrill(img):
	img1_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret1,img1_th = cv2.threshold(img1_gray,60,255,cv2.THRESH_BINARY)
	cv2.imshow('img1_thresh',img1_th)
	imr1 = np.array(img1_th[156,:])
	row_mean = imr1.mean()
	# print('row_mean:',imr1.mean())
	if row_mean<255:
		imr1_min = min(min(np.where(imr1==0)))
		imr1_max = max(max(np.where(imr1==0)))
		w1 = imr1_max-imr1_min
		# print(w1)
		if w1<40 and imr1_min>230 and imr1_max<330:
			cv2.line(img,(imr1_min,156),(imr1_max,156),(0,255,0),3)
			cv2.putText(img,str(w1),(imr1_max+int(w1),156),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,0),1)		
			# cv2.imshow('img1_th',img1_th)
	return img



cap = cv2.VideoCapture('H22.mp4')
i = 0
while(True):    

	ret, img = cap.read()	
	if(ret==False):
		break

	image_color = cv2.resize(img,None,fx=0.4,fy=0.4)
	image_color_copy = image_color.copy()

	img_bkg,thresh,mFlag = getBackground(image_color)
	# cv2.imshow('thresh',thresh)
	# cv2.moveWindow('thresh', 0,440)

	print(mFlag)

	if mFlag == True:	
		img_screws = getScrews(thresh)
		# cv2.imshow('img_screws',img_screws)
		# cv2.moveWindow('img_screws', 512,440)

		img_drill = getDrill(img_screws)
		cv2.imshow('img_drill',img_drill)
		cv2.moveWindow('img_drill', 712,440)
	else:
		img_drill = getDrill(image_color_copy)
		cv2.imshow('img_drill',img_drill)
		cv2.moveWindow('img_drill', 712,440)


	if cv2.waitKey(0) & 0xFF == ord('q'):
		break






