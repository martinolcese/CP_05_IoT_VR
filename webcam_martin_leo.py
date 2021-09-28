#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

#editado por Martin Olcese e Leo Andrade - Grupo CTT - Turma 2TDSJ

import cv2
import os, sys, os.path
import numpy as np

#red filter
img_low_hsv_red = np.array([0, 90, 90])  
img_up_hsv_red = np.array([15, 255, 255])

#cyan filter
img_low_hsv_cyan = np.array([85, 122, 122]) 
img_up_hsv_cyan = np.array([90, 255, 255])

def color_filter(img_bgr, low_hsv, high_hsv):
    img = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask 

def mask_or(mask1, mask2):

    #retorna a mask or
    mask = cv2.bitwise_or(mask1, mask2)
    return mask

def mask_and(mask1, mask2):
     #e esse retorna a mask and
     mask = cv2.bitwise_and(mask1, mask2)
     
     return mask

def cross_one(img, cX,cY, size, color):
     #cruz entre cx e cy
     cv2.line(img,(cX - size,cY),(cX + size,cY),color,5)
     cv2.line(img,(cX,cY - size),(cX, cY + size),color,5)
 

def cross_two(img, cX2 , cY2, size, color):
     #cruz entre cx e cy
     cv2.line(img,(cX2 - size,cY2),(cX2 + size,cY2),color,5)
     cv2.line(img,(cX2,cY2 - size),(cX2, cY2 + size),color,5)    

def write_text(img, text, origin, color):
     #editando o texto
     font = cv2.FONT_HERSHEY_SIMPLEX
     origin = (0,50)
     cv2.putText(img, str(text), origin, font,1,color,2,cv2.LINE_AA)

def draw_line(img,cX,cY,cX2,cY2):
    color = (128,128,0)
    cv2.line(img,(cX , cY),(cX2 , cY2),color,5)

def calc_line(img,cX2,cY2,cX,cY,color):
    p1=(cX2,cY2)
    p2=(cX,cY)
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    ang_straight = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    text=int(ang_straight)
    font = cv2.FONT_HERSHEY_SIMPLEX
    origin = (50,100)
    cv2.putText(img, str(text), origin, font,1,color,2,cv2.LINE_AA)
    
def webcam_img(img):
    """
    ATENÇÃO, BORA FAZER COMO O PROF FALOU NA AULA
    ->>> FECHE A JANELA COM A TECLA ESC <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """  
    mask_hsv1 = color_filter(img, img_low_hsv_red, img_up_hsv_red)
    mask_hsv2 = color_filter(img, img_low_hsv_cyan, img_up_hsv_cyan)
    
    mask_hsv = mask_or(mask_hsv1, mask_hsv2)
    
    contours, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB) 
    contours_img = mask_rgb.copy()
    
    big_one, big_two = None, None
    bigger_area_one, bigger_area_two = 0, 0
    for a in contours:
        area = cv2.contourArea(a)
        if area > bigger_area_one and area > 500:
            bigger_area_two = bigger_area_one
            bigger_area_one = area
            big_two = big_one 
            big_one = a
            
        elif area > bigger_area_two and area > 500:
            bigger_area_two = area
            big_two = a
    
    M1 = cv2.moments(big_one)
    M2 = cv2.moments(big_two)

    # o if para ver se tem algo para calcular. Caso haja, calcule e mostre na tela
    if M1["m00"] != 0:
        cX = int(M1["m10"] / M1["m00"])
        cY = int(M1["m01"] / M1["m00"])
        cv2.drawContours(contours_img, [big_one], -1, [255, 0, 0], 5)
        #faz a cruz no centro do círculo
        cross_one(contours_img, cX,cY, 20, (0,0,255))
        # fonte para o texto
        text = cY , cX
        origin = (0,50)
        write_text(contours_img, text, (0,200), (0,255,0)) 
    if M2["m00"] != 0:
        cX2 = int(M2["m10"] / M2["m00"])
        cY2 = int(M2["m01"] / M2["m00"])
        cv2.drawContours(contours_img, [big_two], -1, [255, 0, 0], 5)
        #faz a cruz no centro do círculo
        cross_two(contours_img, cX2,cY2, 20, (0,0,255))
        # fonte para o texto
        text = cY2 , cX2
        origin = (500,50)
        write_text(contours_img, text, (50,150), (0,255,0))        
        draw_line(contours_img,cX,cY,cX2,cY2)
        calc_line(contours_img,cX2,cY2,cX,cY,(0,255,0))
    else:
        #se não existir nada para segmentar
        cX, cY, cX2 , cY2 = 0, 0 , 0 , 0
        #definir fonte 
        text = 'nao tem nada'
        origin = (0,50)
        write_text(contours_img, text, origin, (0,0,255))
    
    return contours_img

cv2.namedWindow("preview")
#entrada de video para webcam
vc = cv2.VideoCapture(0)
#tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if vc.isOpened(): # pega o primeiro frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    img = webcam_img(frame) 
    # passa o frame para a função webcam_img e recebe em img imagem tratada

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
