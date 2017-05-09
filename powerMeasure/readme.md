## 概述
- 本脚本主要处理max15301/max15303的功耗数据，硬件工具为i2ctool。读出来的数据如《PMBUS.txt》所示。
- pmbus协议可以参考[PMBus_Specification_Part_II](http://www.pmbus.org/Assets/PDFS/Public/PMBus_Specification_Part_II_Rev_1-2_20100906.pdf),电流和电压数据都是X = Y·2^N的形式，其中指数N用的补码。
- 根据[MAX15303 Datasheet](https://datasheets.maximintegrated.com/en/ds/MAX15303.pdf)P27电流计算公式ILOAD = READ_IOUT x IOUT_CAL_GAIN/DCR,READ_IOUT通过寄存器直接读出，IOUT_CAL_GAIN默认由ADDR1下拉电阻决定，但是根据[xilinx官方提供的XML文件](https://www.xilinx.com/Attachment/FULL_ZCU102_REVD_ONLY_05122016_FINE_CAL.XML)，IOUT_CAL_GAIN被重新设置了。DCR则可以根据电感的参数获得。也可以根据Rl＊Cl＝L/DCR算出来。

## 使用方法
- 在环境变量path增加readCurrent应用程序路径。如果不设置环境变量，请先将终端路径切换到readCurrent目录
- 在终端中输入```readCurrent -f H:\Study\Python\maxIcPowerTool\PMBUS.txt```其中```H:\Study\Python\maxIcPowerTool\PMBUS.txt```为数据存放的路径。如果数据在同级目录，则可以直接用文件名```readCurrent -f PMBUS.txt```
- 结果保存

```
powerNet    addr    voltage(V)    current(A)    power(W)
VCCPSINTFP    0xa    0.849854    1.632896    1.387722
VCCPSINTLP    0xb    0.850098    0.258842    0.220041
VCCOPS    0x10    1.800049    0.077930    0.140277
DDR4_DIMM_VDDQ    0x1d    1.199707    0.382695    0.459121
VCCINT    0x13    0.850098    0.611425    0.519771
VCCBRAM    0x14    0.849854    0.031833    0.027053
VCCAUX    0x15    1.799561    0.112676    0.202767
VCC1V2    0x16    1.199951    0.024441    0.029328
VCC3V3    0x17    3.298584    0.079554    0.262417
VADJ_FMC    0x18    1.799561    0.084473    0.152014
MGTAVCC    0x72    0.031982    0.000000    0.000000
MGTAVTT    0x73    0.046631    0.000000    0.000000
UTIL_3V3    0x1a    3.300049    0.761215    2.512046
UTIL_5V0    0x1b    0.240479    0.150459    0.036182
****** powerTotal=5.948741 W ******

```