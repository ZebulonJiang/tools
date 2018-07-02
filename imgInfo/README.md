* [概述](#%E6%A6%82%E8%BF%B0)
* [安装步骤](#%E5%AE%89%E8%A3%85%E6%AD%A5%E9%AA%A4)
  * [Step1 python安装配置](#step1-python%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AE)
    * [安装python2\.7](#%E5%AE%89%E8%A3%85python27)
    * [python环境变量设置](#python%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E8%AE%BE%E7%BD%AE)
  * [Step2 cmder 配置](#step2-cmder-%E9%85%8D%E7%BD%AE)
  * [Step3 安装依赖](#step3-%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96)
* [使用说明](#%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)
  * [运行](#%E8%BF%90%E8%A1%8C)
  * [修改配置](#%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE)

# 概述

该工具用于图像信息统计，支持bmp和raw图。可以任意ROI。可以由config.ini配置不同的模式。

# 安装步骤

## Step1 python安装配置

### 安装python2.7

从python[官网](https://www.python.org/downloads/)下载python2.7，如下图所示
![python下载](http://7xq2ld.com1.z0.glb.clouddn.com/github/setup1.jpg)


### python环境变量设置
找到python.exe所在的目录，本人电脑python安装目录为```D:\Program Files (x86)\Python27```
![环境变量配置](http://7xq2ld.com1.z0.glb.clouddn.com/github/env4.jpg)
请将python的安装目录，以及对应的子目录Scripts添加到用户和系统的PATH环境变量，如果系统没有PATH环境变量，请自行新建PATH。
例如python安装目录为```D:\Program Files (x86)\Python27```则将以下两个路径分别添加到PATH环境变量。环境变量之间应该用英文分号隔开

```D:\Program Files (x86)\Python27```

```D:\Program Files (x86)\Python27\Scripts```

![环境变量配置](http://7xq2ld.com1.z0.glb.clouddn.com/github/env1.jpg)
![环境变量配置](http://7xq2ld.com1.z0.glb.clouddn.com/github/env3.jpg)

在终端工具中输入```python```能看到python版本信息，则证明python安装配置成功



## Step2 cmder 配置

Linux或者mac用户请忽略这一步。
由于win自带的cmd工具不是很好用，路径切换/文本复制/文本粘贴都不是很好用。所以我推荐大家使用cmder作为命令行工具，cmder用法请参考[Win下必备神器之Cmder](https://jeffjade.com/2016/01/13/2016-01-13-windows-software-cmder/)

![cmder安装](http://7xq2ld.com1.z0.glb.clouddn.com/github/cmder_setup.jpg)

## Step3 安装依赖

图像分析工具使用了python的第三方工具，如科学计算工具```numpy``` 图像处理工具```Pillow```，首次使用该工具，需要安装这些依赖，在工具目录下，右键打开cmder，终端就自动切换到工具所在的目录，在终端工具中输入下面命令

```pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple```

![cmder here](http://7xq2ld.com1.z0.glb.clouddn.com/github/cmder_here.jpg)


# 使用说明

## 运行

在工具目录下，右键打开cmder，终端就会自动切换到工具所在的目录
![cmder here](http://7xq2ld.com1.z0.glb.clouddn.com/github/cmder_here.jpg)

运行命令```python main.py -f 图片路径```，例如图片路径为```E:\work\tools\imgInfo\test```，则运行

`python main.py -f E:\work\tools\imgInfo\test`

注意：图片路径不能有中文、空格。最好用英文路径。

![imginfo](http://7xq2ld.com1.z0.glb.clouddn.com/github/result.jpg)


## 修改配置

工具支持多种图像格式和多种窗口模式，只需要修改config.ini文件即可

![imginfo](http://7xq2ld.com1.z0.glb.clouddn.com/github/config.jpg)






