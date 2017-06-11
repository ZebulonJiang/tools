#!/usr/bin/python
#-*-coding:utf-8 -*-
from PIL import Image,ImageStat
import ConfigParser

def getConfigValue(option,key):
	config = ConfigParser.SafeConfigParser();
	config.read("config.ini");
	return config.get(option,key);

def getItems(section):
	config = ConfigParser.SafeConfigParser();
	config.read("config.ini");
	return config.items(section);

class ImgInfo(object):
	"""docstring for imgInfo"""
	def __init__(self, img):
		#super(imgInfo, self).__init__()
		self.img = img;
		self.stat = ImageStat.Stat(img);
		self.pixAver = 0;
		self.pixMax = 0;
		self.pixMin = 0;
		self.pixNum = 0;
		self.pixStdDev = 0;
		self.imgWidth = 0;
		self.imgHeight = 0;
		# self.stat;

	def getPixNum(self):
		self.pixNum = self.stat.count[0]
		return self.pixNum;

	def getPixMin(self):
		self.pixMin = self.stat.extrema[0][0];
		return self.pixMin;

	def getPixMax(self):
		self.pixMax = self.stat.extrema[0][1];
		return self.pixMax;

	def getPixAver(self):
		self.pixAver = round(self.stat.mean[0],3);
		return self.pixAver;
	
	def getPixStdDev(self):
		self.pixStdDev = round(self.stat.stddev[0],3);
		return self.pixStdDev;




class GetConfig(object):
	"""docstring for GetConfig"""
	def __init__(self):
		# super(GetConfig, self).__init__()
		self.format = 0;
		self.roiMode = 0;
		self.compareMode = 0;
		self.width = 400;
		self.height = 400;
		self.roiWidth = 400;
		self.roiHeight = 400;
		self.roiOffsetX = 0;
		self.roiOffsetY = 0;
		self.pixDepth = 8;
		self.comparePath = "";
		self.saveItem = 5;

	def getFormat(self):
		self.format = int(getConfigValue("MODE","Format"));
		return self.format;

	def getRoiMode(self):
		self.roiMode = int(getConfigValue("MODE","RoiMode"));
		return self.roiMode;
	
	def getCompareMode(self):
		self.compareMode = int(getConfigValue("MODE","CompareMode"));
		return self.compareMode;

	def getWidth(self):
		self.width = int(getConfigValue("RAW","Width"));
		return self.width;

	def getHeight(self):
		self.height = int(getConfigValue("RAW","Height"));
		return self.height;

	def getRoiWidth(self,format):
		if format == 0:
			self.roiWidth = int(getConfigValue("BMP","RoiWidth"));
		else:
			self.roiWidth = int(getConfigValue("RAW","RoiWidth"));
		return self.roiWidth;

	def getRoiHeight(self,format):
		if format == 0:
			self.roiHeight = int(getConfigValue("BMP","RoiHeight"));
		else:
			self.roiHeight = int(getConfigValue("RAW","RoiHeight"));
		return self.roiHeight;

	def getRoiOffsetX(self,format):
		if format == 0:
			self.roiOffsetX = int(getConfigValue("BMP","RoiOffsetX"));
		else:
			self.roiOffsetX = int(getConfigValue("RAW","RoiOffsetX"));
		return self.roiOffsetX;

	def getRoiOffsetY(self,format):
		if format == 0:
			self.roiOffsetY = int(getConfigValue("BMP","RoiOffsetY"));
		else:
			self.roiOffsetY = int(getConfigValue("RAW","RoiOffsetY"));
		return self.roiOffsetY;
	
	def getComparePath(self):
		self.comparePath = getItems("COMPARE");
		return self.comparePath;

	def getSaveItem(self):
		self.saveItem = int(getConfigValue("MODE","SaveItem"));
		return self.saveItem;
	



		



