# coding=gb2312

from pickle import INT
import sys, fitz
import os
import datetime
import cv2
from cnocr import CnOcr
 
def imageOCR(imagePath,pdfOutPath):
    """
    img_fq = imagePath
    ocr = CnOcr()
    resultOCR = ocr.ocr(img_fq)
    return str(resultOCR[0]["text"])
    """
    ocr = CnOcr()
    image = cv2.imread(imagePath) #��ȡͼ��
    x, y, width, height = (461, 798, 158, 58) #Ŀ����������
    roi = image[y:y + height, x:x + width] #�ü�ͼ��
    resultOCR = ocr.ocr(roi)
    resultText = resultOCR[0]['text']
    print(resultText)
    cv2.imwrite((pdfOutPath + "/"+ str(resultText) +".jpg"), roi)
    
def pdf2img(pdfPath, pdfOutPath):
    print("����ļ����·��Ϊ��" + os.path.abspath(pdfOutPath))
    pdfDoc = fitz.open(pdfPath)
    numPage = pdfDoc.page_count
    page = pdfDoc[0]
    # �˴����ǲ������ã�Ĭ��ͼƬ��СΪ��792X612, dpi=72 ��ɨ����ļ���200dpi
    # ÿ���ߴ������ϵ��Ϊ1.3���⽫Ϊ�������ɷֱ������2.6��ͼ��
    zoom_x = 1.6
    zoom_y = 1.6
    mat = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
    pix = page.get_pixmap(matrix = mat, alpha = False)
    pix.save(pdfOutPath + '/1.png')
    ocr =  CnOcr()
    image = cv2.imread(pdfOutPath + '/1.png') #��ȡͼ��
    x, y, width, height = (260, 450, 90, 40) #Ŀ����������
    roi = image[y:y + height, x:x + width] #�ü�ͼ��
    resultOCR = ocr.ocr(roi)
    resultText = resultOCR[0]['text']
    print(resultText)
    

def splitPDF(pdfPath, pdfOutPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()#��ʼʱ��
    print("����ļ����·��Ϊ��" + os.path.abspath(pdfOutPath))
    pdfDoc = fitz.open(pdfPath)
    numPage = pdfDoc.page_count
    if not os.path.exists(pdfOutPath):#�жϴ��ͼƬ���ļ����Ƿ����
        os.makedirs(pdfOutPath)# ��pdf�ļ��в����ھʹ���
    if not os.path.exists( imagePath):#�жϴ��ͼƬ���ļ����Ƿ����
        os.makedirs( imagePath)# ��pdf�ļ��в����ھʹ���   
    for i in range(int(numPage/2)):
        print("���ڲ�ֵ�" + str(i + 1) + "���˵��Ͷ���ͬ")
        doc2 = fitz.open() # new empty PDF
        doc2.insert_pdf(pdfDoc, from_page = i * 2, to_page = i * 2 + 1) # ��ȡ����ҳ
        page = pdfDoc[i * 2] #��ȡʶ��ؼ�ҳ
        # �˴����ǲ������ã�Ĭ��ͼƬ��СΪ��792X612, dpi=72 ��ɨ����ļ���200dpi
        # ÿ���ߴ������ϵ��Ϊ1.3���⽫Ϊ�������ɷֱ������2.6��ͼ��    
        zoom_x = 1.6
        zoom_y = 1.6
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
        pix = page.get_pixmap(matrix = mat, alpha = False)
        pix.save(imagePath + '/' + str(i + 1) + '.png')
        ocr =  CnOcr()
        image = cv2.imread(imagePath + '/' + str(i + 1) + '.png') #��ȡͼ��
        x, y, width, height = (260, 450, 90, 40) #Ŀ����������
        roi = image[y:y + height, x:x + width] #�ü�ͼ��
        resultOCR = ocr.ocr(roi)
        resultText = resultOCR[0]['text']
        doc2.save(pdfOutPath + "/" + str(resultText) + " �����Ͷ���ͬ.pdf") # ���ɵ���pdf�ļ�
    endTime_pdf2img = datetime.datetime.now()#����ʱ��_
    print("�����ϣ�����ʱ" + str((endTime_pdf2img - startTime_pdf2img).seconds) + "s")
 
if __name__ == "__main__":
    pdfPath = "input/����ʡũ���Ͷ���ͬ�������ɣ�.pdf"
    pdfOutPath = "output"
    imagePath = "input/img"
    splitPDF(pdfPath, pdfOutPath, imagePath)
