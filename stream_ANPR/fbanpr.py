import os
import cv2
import sys
import pytesseract
import numpy as np
import mmap
import multiprocessing as mp


block = 0

cap = cv2.VideoCapture(4)
cascPath = sys.argv[1]
carplate = cv2.CascadeClassifier(cascPath)
HAAR_FLAGS = cv2.CASCADE_SCALE_IMAGE

#def task(num):
#    #找出最大矩形面積
#    for cnt in contours:
#        lenght = 0.01 * cv2.arcLength(cnt, True)
#        approx = cv2.approxPolyDP(cnt, lenght, True)
#        if len(approx) == 4:                        
#            area = cv2.contourArea(cnt)                        
#            if area > largest_rectangle[0]:                            
#                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
                



try:
    
    while cap.isOpened():  
    
    
        if cap.isOpened() is False:
            exit(0)
            break
        
        ret, frame = cap.read()

        
        frame32 = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)    
        fbframe = cv2.resize(frame32, (1024,600))
        fd = open('/dev/fb0', 'rb+')
        mirro = mmap.mmap(fd.fileno(), 2457600)    
        
        
        
        with mirro as buf:             
            
            
            gray = cv2.cvtColor(fbframe,cv2.COLOR_BGR2GRAY)
            #做自適應二值化
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            
            zoomX = 30
            zoomY = 30
            
            plate = carplate.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(19, 8),
                maxSize=(19 * zoomX, 8 * zoomY),
                flags=HAAR_FLAGS
            )
            
#################
##   加速測試   #
################
#            
#            pool = mp.Pool()
#            res_list = []
#            for i in range(10):
#                res_list.append(pool.apply_async(task, (i,)))
#
#            for res in res_list:
#                print(res.get())
#                
####################
##   加速測試 END  #
###################                
                    
            print('有' + str(len(plate)) + '車牌')
            
#            if len(plate) == 1 & block % 10 == 0:
            if len(plate) == 1:
                
                blurred = cv2.GaussianBlur(thresh, (11, 11), 0)
                binaryIMG = cv2.Canny(blurred, 30, 200)
                contours, h = cv2.findContours(binaryIMG, 1, 2)
            
                largest_rectangle = [0, 0]
                
                    
                #找出最大矩形面積
                for cnt in contours:
                    lenght = 0.01 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, lenght, True)
                    if len(approx) == 4:
                        
                        area = cv2.contourArea(cnt)
                        
                        if area > largest_rectangle[0]:                            
                            largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
                            
                x, y, w, h = cv2.boundingRect(largest_rectangle[1])               
                
                image = fbframe[y:y + h, x:x + w]   #把找到的最大矩形影像獨立出來, 以利 OCR 讀取
                kernel = np.ones((3,3),np.uint8)
                erosion = cv2.erode(fbframe,kernel,iterations = 1)
                
                cv2.drawContours(fbframe, [largest_rectangle[1]], 0, (0, 255, 0), 2)
                
                
                #print(largest_rectangle)
                
                # ocr 圖片文字
                
                pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
            
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gsblur = cv2.GaussianBlur(gray, (3, 3), 0)
                thresh = cv2.threshold(gsblur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]    
            
                #透過侵蝕膨脹, 讓車牌上的字可以更清晰, 再把黑底白字轉成白底黑字, 以利 OCR 抓取
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
                invert = 255 - opening
                
            
                data = pytesseract.image_to_string(invert, lang='eng')
                
                text_size, _ = cv2.getTextSize(data, cv2.FONT_HERSHEY_COMPLEX, 1, 2)
                text_w, text_h = text_size
                cv2.rectangle(fbframe, (x, y), (x + text_w, y + text_h), (204, 188, 98), -1)
                
                cv2.putText(fbframe, data, (x, y + text_h), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            else:
                print('no found plate')
    
            
            fd.write(fbframe)
            
            mirro.close()
            buf.close()
#            pool.close()
#            pool.join()
            
except KeyboardInterrupt:
    os.system('dd if=/dev/zero of=/dev/fb0')

cap.release()
