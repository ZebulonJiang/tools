#!/usr/bin/python
#-*-coding:utf-8 -*-
import os
import sys
import ctypes
from PIL import Image,ImageStat
import ConfigParser
import re
from imgInfo import ImgInfo,GetConfig
import numpy as np

def printResult(data):
	print("**********************************");
	print data[0];
	# print("曝光时间:%s",%(data[0]));
	# print("最小值:%f",%(float(data[3]));
	# print("最大值:%s",%(data[4]));
	# print("平均值:%s",%(data[5]));
	# print("标准方差(噪声):%s",%(data[6]));
	


def saveResult(data,item,title,count):
	fp = open(title + '.txt','a')
	bufList = "";
	if count == 0:
		for expTime in xrange(len(data)):
			bufList = bufList + data[expTime][1] + "           ";
		bufList = bufList + "\n";


	for expTime in xrange(len(data)):
		bufList = bufList + data[expTime][5] + "           ";
	bufList = bufList + "\n";
	fp.write(bufList);

	fp.close();
	# print "savedata";

def getExpTime(file):
	if re.search('ms', file, re.IGNORECASE):
		expTime = int(filter(str.isdigit, file));
	elif re.search('us', file, re.IGNORECASE):
		expTime = float(filter(str.isdigit, file))/1000;
	else:
		expTime = int(filter(str.isdigit, file))*1000;
	return expTime;

def setRoi(format,roiMode,size):
	cofig = GetConfig();
	width,height = size;
	if (roiMode == 0):#自动ROI模式，居中取1/3作为ROI
		RoiWidth	= width/3;
		RoiHeight	= height/3;
		RoiOffsetX	= width/3;
		RoiOffsetY	= height/3;
	elif(roiMode == 1):	#ROI位置居中，ROI的宽、高 从配置文件中读出
		RoiWidth	= cofig.getRoiWidth(cofig.getFormat());
		RoiHeight	= cofig.getRoiHeight(cofig.getFormat());
		RoiOffsetX = (width/2) - (RoiWidth/2);
		RoiOffsetY =  (height/2) - (RoiHeight/2);
	elif(roiMode == 2):   #手动ROI模式，ROI的宽、高、offset都是从配置文件中读出
		RoiWidth	= cofig.getRoiWidth(cofig.getFormat());
		RoiHeight	= cofig.getRoiHeight(cofig.getFormat());
		RoiOffsetX	= cofig.getRoiOffsetX(cofig.getFormat());
		RoiOffsetY	= cofig.getRoiOffsetY(cofig.getFormat());
	else:
		RoiWidth	= width;
		RoiHeight	= height;
		RoiOffsetX	= 0;
		RoiOffsetY	= 0;

	#ROI设置越界保护。
	if (RoiWidth > width):
		RoiWidth = width;
		RoiOffsetX = 0;
	elif ((RoiWidth + RoiOffsetX) > width):
		RoiOffsetX = width - RoiWidth;
	else:
		RoiWidth	= RoiWidth;
		RoiHeight	= RoiHeight;
		RoiOffsetX	= RoiOffsetX;
		RoiOffsetY	= RoiOffsetY;

	if (RoiHeight > height):
		RoiHeight = height;
		RoiOffsetY = 0;	
	elif ((RoiHeight + RoiOffsetY) > height):
		RoiOffsetY = height - RoiHeight;
	else:
		# print "ROI is ok"
		RoiWidth	= RoiWidth;
		RoiHeight	= RoiHeight;
		RoiOffsetX	= RoiOffsetX;
		RoiOffsetY	= RoiOffsetY;

	# print size;
	# print RoiWidth,RoiHeight;
	return (RoiOffsetX,RoiOffsetY,(RoiWidth+RoiOffsetX),(RoiHeight+RoiOffsetY))

def openFile(path):
	cofig = GetConfig();
	if(os.path.exists(path)==False):	
		print("\'%s\'  is not exist"%(path))
		return -1
	if os.path.isfile(path): #如果是单个文件直接打开
		if os.path.splitext(path)[1] == '.bmp':
			im = Image.open(path)
			box = setRoi('BMP',cofig.getRoiMode(),im.size);
			roi = im.crop(box)
			r,g,b = roi.split()
			imgInfo = ImgInfo(g);
			roi.show();
			print "bmp info"
			print imgInfo.getPixNum();
			print imgInfo.getPixMin();
			print imgInfo.getPixMax();
			print imgInfo.getPixAver();
			print imgInfo.getPixStdDev();
			im.close();
		elif os.path.splitext(path)[1] == '.raw':
			rawData = open(path,'rb').read();
			imgSize = (cofig.getWidth(),cofig.getHeight());
			box = setRoi('RAW',cofig.getRoiMode(),imgSize);
			im = Image.frombytes('L', imgSize, rawData, 'raw')
			roi = im.crop(box)
			# r,g,b = roi.split()
			imgInfo = ImgInfo(roi);
			# roi.show();
			print "raw info"
			print imgInfo.getPixNum();
			print imgInfo.getPixMin();
			print imgInfo.getPixMax();
			print imgInfo.getPixAver();
			print imgInfo.getPixStdDev();
			im.close();
	else:
		files= os.listdir(path) #得到文件夹下的所有文件名称 
		imgInfoLists = [];
		fileCount = 0;
		for file in files:       #遍历文件夹  
			if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
					if (cofig.getFormat() == 0):
						if os.path.splitext(file)[1] == '.bmp':
							im = Image.open(path+"/"+file)
							width,height = im.size;
							box = setRoi('BMP',cofig.getRoiMode(),im.size);
							roi = im.crop(box)
							r,g,b = roi.split()
							imgInfo = ImgInfo(g);
							expTime = getExpTime(file);
							listTemp = [file,getExpTime(file),imgInfo.getPixNum(),imgInfo.getPixMin(),imgInfo.getPixMax(),
								imgInfo.getPixAver(),imgInfo.getPixStdDev()];
							printResult(listTemp);
							imgInfoLists = imgInfoLists + listTemp;
							fileCount = fileCount +1;
							# print listTemp;
							

							# print file
							# print imgInfo.getPixNum();
							# print imgInfo.getPixMin();
							# print imgInfo.getPixMax();
							# print imgInfo.getPixAver();
							# print imgInfo.getPixStdDev();
							# roi.show();
							im.close();
					elif (cofig.getFormat() == 1): # readraw
						if os.path.splitext(file)[1] == '.raw':
							rawData = open(path+"/"+file,'rb').read();
							imgSize = (cofig.getWidth(),cofig.getHeight());
							box = setRoi('RAW',cofig.getRoiMode(),imgSize);
							im = Image.frombytes('L', imgSize, rawData, 'raw')
							roi = im.crop(box)
							# r,g,b = roi.split()
							imgInfo = ImgInfo(roi);
							fileCount = fileCount +1;
							# roi.show();
							# print "raw info"
							# print imgInfo.getPixNum();
							# print imgInfo.getPixMin();
							# print imgInfo.getPixMax();
							# print imgInfo.getPixAver();
							# print imgInfo.getPixStdDev();
							im.close();
					else:
						print "else"
			# printResult(imgInfoLists);
		# imgInfoList = np.matrix(imgInfoList)
		imgInfoLists = np.reshape(imgInfoLists,(len(imgInfoLists)/7,7));
		imgInfoLists = sorted(imgInfoLists,key=lambda x : float(x[1]))   # sort by expTime 
		fileCount = 0;
		return imgInfoLists;
		# print imgInfoLists;
		# print len(imgInfoLists);



def main():
	debug 			= 0;
	path		= '';
	count = 0;
	#获取程序运行参数
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			path	= sys.argv[i+1];
		if(sys.argv[i]=="-t"):
			title	= sys.argv[i+1];

	config = GetConfig();#获取配置文件
	# fp = open(title + '.txt','w')
	# fp.write("************平均值统计******************\n")
	# fp.close();
	if config.getCompareMode() == 0:   #只处理单个文件夹的数据
		openFile(path);
	elif config.getCompareMode() == 1:  #处理多个文件夹下的数据
		# print config.getComparePath();

		items = config.getComparePath();
		for item in items:
			# printResult(openFile(item[1]));
			result = openFile(item[1]);
			# saveResult(openFile(item[1]),config.getSaveItem(),title,count);
			# count = count + 1;
			# print item[1];
	else:
		print "***** error ****";
	

main();



