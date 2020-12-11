from PIL import Image, ImageFont, ImageDraw,ImageFile,ExifTags
ImageFile.LOAD_TRUNCATED_IMAGES = True
import exifread #获得exif信息
import time
import os



def addText(image_path, text):
    print(os.path.splitext(os.path.basename(image_path))[0])
    im = Image.open(image_path)  # 打开图像
    #print('old',im.size)
    #获取原图片exif分辨率。防止图片旋转。
    try:
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(im._getexif().items())
        if   exif[orientation] == 3 : 
            im=im.rotate(180, expand = True)
        elif exif[orientation] == 6 : 
            im=im.rotate(270, expand = True)
        elif exif[orientation] == 8 : 
            im=im.rotate(90, expand = True)
    except:
        pass
    width, height = im.size
    #print(im.size)
    ttfont = ImageFont.truetype('STLITI.TTF',int(height/20)) #设置字体
    draw = ImageDraw.Draw(im)  # 创建画画对象
    draw.text((int(width*0.01), int(height*0.95)), text, fill='#ff6306', font=ttfont)  # 添加文字
    im.save('./output/'+os.path.basename(image_path), quality = 100)
    im.close()
    
#解析exif信息，获取日期
def getDate(filepath):
    f = open(filepath, 'rb')
    date = exifread.process_file(f)['EXIF DateTimeOriginal'] #获取拍摄日期时间
    date = str(date) #将日期时间转换成字符串
    list = date.split(' ') #分开成日期和时间
    #print(list)
    date = '-'.join(list[0].split(':')) #拍摄日期
    #print(date)
    time = list[1] #拍摄时间
    #print(time)
    return date


def batchImg (srcDir):
	#遍历图片文件
    picFiles = [os.path.join(srcDir,fn) for fn in os.listdir(srcDir) if fn.endswith(('.gif', '.jpg', '.png','.JPG','.jpeg'))]
    for filePath in picFiles:
        #print(filePath)
        addText(filePath, getDate(filePath)) #在此处添加文件路径
        #dealOneFile(filePath)

if __name__ == '__main__':
    #判断输出文件夹是否存在。如果不存在则新建
    if not os.path.exists('./output/'):
    	print('output is not exist,creat output')
    	os.mkdir('./output/')
    else:
    	print('output is exist!')
    batchImg (os.getcwd()) #自动获取可执行文件路径
    print('***********All picture has been added date***********')

#***** windows字体与文件对应表*****
# 宋体 (TrueType) = SIMSUN.TTF
# 黑体 (TrueType) = simhei.ttf
# 楷体_GB2312 (TrueType) = simkai.ttf
# 仿宋_GB2312 (TrueType) = simfang.ttf
# Arial (TrueType) = ARIAL.TTF
# Arial 粗体 (TrueType) = ARIALBD.TTF
# Arial 粗斜体 (TrueType) = ARIALBI.TTF
# Arial 斜体 (TrueType) = ARIALI.TTF
# Courier New 粗体 (TrueType) = COURBD.TTF
# Courier New 粗斜体 (TrueType) = COURBI.TTF
# Courier New 斜体 (TrueType) = COURI.TTF
# Lucida Console (TrueType) = LUCON.TTF
# Marlett (TrueType) = MARLETT.TTF
# Tahoma = TAHOMA.TTF
# Tahoma 粗体 (TrueType) = TAHOMABD.TTF
# Times New Roman (TrueType) = TIMES.TTF
# Times New Roman 粗体 (TrueType) = TIMESBD.TTF
# Times New Roman 粗斜体 (TrueType) = TIMESBI.TTF
# Times New Roman 斜体 (TrueType) = TIMESI.TTF
# Modern (Plotter) = MODERN.FON
# Comic Sans MS 粗体 (TrueType) = COMICBD.TTF
# Verdana 粗体 (TrueType) = VERDANAB.TTF
# Verdana 斜体 (TrueType) = VERDANAI.TTF
# Verdana 粗斜体 (TrueType) = VERDANAZ.TTF
# Basemic (TrueType) = BASEMIC_.TTF
# Basemic Symbol (TrueType) = BASES___.TTF
# Basemic Times (TrueType) = BASET___.TTF
# Kingsoft Phonetic (TrueType) = Ksphonet.ttf
# SerialNumber = dword:000b6bbc
# MingLiU & PMingLiU (TrueType) = MINGLIU.TTC
# 方正舒体 (TrueType) = FZSTK.TTF
# 方正姚体 (TrueType) = FZYTK.TTF
# 隶书 (TrueType) = SIMLI.TTF
# 华文彩云 (TrueType) = STCAIYUN.TTF
# 华文细黑 (TrueType) = STXIHEI.TTF
# 华文行楷 (TrueType) = STXINGKA.TTF
# 华文新魏 (TrueType) = STXINWEI.TTF
# 华文中宋 (TrueType) = STZHONGS.TTF
# 幼圆 (TrueType) = SIMYOU.TTF
# Arial Black (TrueType) = ARIBLK.TTF
# Arial Narrow (TrueType) = ARIALN.TTF
# Book Antiqua (TrueType) = BKANT.TTF
# Bookman Old Style (TrueType) = BOOKOS.TTF
# Century Gothic (TrueType) = GOTHIC.TTF
# Comic Sans MS (TrueType) = COMIC.TTF
# Courier New (TrueType) = COUR.TTF
# Garamond (TrueType) = GARA.TTF
# Haettenschweiler (TrueType) = HATTEN.TTF
# Impact (TrueType) = IMPACT.TTF
# Monotype Corsiva (TrueType) = MTCORSVA.TTF
# MS Outlook (TrueType) = Outlook.TTF
# Symbol (TrueType) = SYMBOL.TTF
# Trebuchet MS (TrueType) = TREBUC.TTF
# Verdana (TrueType) = VERDANA.TTF
# Wingdings (TrueType) = WINGDING.TTF
# Wingdings 2 (TrueType) = WINGDNG2.TTF
# Wingdings 3 (TrueType) = WINGDNG3.TTF
# Book Antiqua Bold (TrueType) = ANTQUAB.TTF
# Book Antiqua Bold Italic (TrueType) = ANTQUABI.TTF
# Book Antiqua Italic (TrueType) = ANTQUAI.TTF
# Arial Black Italic (TrueType) = ARBLI___.TTF
# Arial Bold (TrueType) = ARIALBD.TTF
# Arial Bold Italic (TrueType) = ARIALBI.TTF
# Arial Italic (TrueType) = ARIALI.TTF
# Arial Narrow Bold (TrueType) = ARIALNB.TTF
# Arial Narrow Bold Italic (TrueType) = ARIALNBI.TTF
# Arial Narrow Italic (TrueType) = ARIALNI.TTF
# Bookman Old Style Bold (TrueType) = BOOKOSB.TTF
# Bookman Old Style Bold Italic (TrueType) = BOOKOSBI.TTF
# Bookman Old Style Italic (TrueType) = BOOKOSI.TTF
# Comic Sans MS Bold (TrueType) = COMICBD.TTF
# Courier New Bold (TrueType) = COURBD.TTF
# Courier New Bold Italic (TrueType) = COURBI.TTF
# Courier New Italic (TrueType) = COURI.TTF
# Garamond Bold (TrueType) = GARABD.TTF
# Garamond Italic (TrueType) = GARAIT.TTF
# Century Gothic Bold (TrueType) = GOTHICB.TTF
# Century Gothic Bold Italic (TrueType) = GOTHICBI.TTF
# Century Gothic Italic (TrueType) = GOTHICI.TTF
# Tahoma (TrueType) = TAHOMA.TTF
# Tahoma Bold (TrueType) = TAHOMABD.TTF
# Times New Roman Bold (TrueType) = TIMESBD.TTF
# Times New Roman Bold Italic (TrueType) = TIMESBI.TTF
# Times New Roman Italic (TrueType) = TIMESI.TTF
# Trebuchet MS Bold (TrueType) = TREBUCBD.TTF
# Trebuchet MS Bold Italic (TrueType) = TREBUCBI.TTF
# Trebuchet MS Italic (TrueType) = TREBUCIT.TTF
# Verdana Bold (TrueType) = VERDANAB.TTF
# Verdana Italic (TrueType) = VERDANAI.TTF
# Verdana Bold Italic (TrueType) = VERDANAZ.TTF
# Webdings (TrueType) = WEBDINGS.TTF
# Tahoma (True Type) = tahoma.ttf