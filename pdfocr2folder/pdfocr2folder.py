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
    image = cv2.imread(imagePath) #读取图像
    x, y, width, height = (461, 798, 158, 58) #目标区域像素
    roi = image[y:y + height, x:x + width] #裁剪图像
    resultOCR = ocr.ocr(roi)
    resultText = resultOCR[0]['text']
    print(resultText)
    cv2.imwrite((pdfOutPath + "/"+ str(resultText) +".jpg"), roi)
    
def pdf2img(pdfPath, pdfOutPath):
    print("拆分文件输出路径为：" + os.path.abspath(pdfOutPath))
    pdfDoc = fitz.open(pdfPath)
    numPage = pdfDoc.page_count
    page = pdfDoc[0]
    # 此处若是不做设置，默认图片大小为：792X612, dpi=72 我扫描的文件是200dpi
    # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
    zoom_x = 1.6
    zoom_y = 1.6
    mat = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
    pix = page.get_pixmap(matrix = mat, alpha = False)
    pix.save(pdfOutPath + '/1.png')
    ocr =  CnOcr()
    image = cv2.imread(pdfOutPath + '/1.png') #读取图像
    x, y, width, height = (260, 450, 90, 40) #目标区域像素
    roi = image[y:y + height, x:x + width] #裁剪图像
    resultOCR = ocr.ocr(roi)
    resultText = resultOCR[0]['text']
    print(resultText)
    

def splitPDF(pdfPath, pdfOutPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()#开始时间
    print("拆分文件输出路径为：" + os.path.abspath(pdfOutPath))
    pdfDoc = fitz.open(pdfPath)
    numPage = pdfDoc.page_count
    if not os.path.exists(pdfOutPath):#判断存放图片的文件夹是否存在
        os.makedirs(pdfOutPath)# 若pdf文件夹不存在就创建
    if not os.path.exists( imagePath):#判断存放图片的文件夹是否存在
        os.makedirs( imagePath)# 若pdf文件夹不存在就创建   
    for i in range(int(numPage/2)):
        print("正在拆分第" + str(i + 1) + "个人的劳动合同")
        doc2 = fitz.open() # new empty PDF
        doc2.insert_pdf(pdfDoc, from_page = i * 2, to_page = i * 2 + 1) # 提取奇数页
        page = pdfDoc[i * 2] #提取识别关键页
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72 我扫描的文件是200dpi
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。    
        zoom_x = 1.6
        zoom_y = 1.6
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
        pix = page.get_pixmap(matrix = mat, alpha = False)
        pix.save(imagePath + '/' + str(i + 1) + '.png')
        ocr =  CnOcr()
        image = cv2.imread(imagePath + '/' + str(i + 1) + '.png') #读取图像
        x, y, width, height = (260, 450, 90, 40) #目标区域像素
        roi = image[y:y + height, x:x + width] #裁剪图像
        resultOCR = ocr.ocr(roi)
        resultText = resultOCR[0]['text']
        doc2.save(pdfOutPath + "/" + str(resultText) + " 个人劳动合同.pdf") # 生成单个pdf文件
    endTime_pdf2img = datetime.datetime.now()#结束时间_
    print("拆分完毕，共用时" + str((endTime_pdf2img - startTime_pdf2img).seconds) + "s")
 
if __name__ == "__main__":
    pdfPath = "input/云南省农民工劳动合同（已生成）.pdf"
    pdfOutPath = "output"
    imagePath = "input/img"
    splitPDF(pdfPath, pdfOutPath, imagePath)
