# bugly_symbol_thin

无损压缩bugly所产生的符号表

# bugly的符号表

bugly的符号表分为2种，一种是`可读符号表`，另一种是`不可读符号表`。其中不可读符号表在2019年1月22日以后默认生成的都是不可读符号表。如果想要生成可读符号表可以指定参数为-symbol。具体`buglySymboliOS.jar`是如何将DWARF格式转为符号字符串的没有做深究，猜测是通过解析DWARF格式文件提取数据的。可读符号表和不可读符号表经过观察得知，两者在所占空间体积上没有显著差异。本方案针对`可读符号表`进行压缩。

# 如何使用

使用前需要确保安装Python3
准备好物料，bugly的可读符号表：xxxx.symbol.zip

###### 注意，这里的符号表的zip包是指通过 buglySymboliOS.jar 处理后的zip文件，不是dSYM文件zip压缩后的文件


```
 python3 compressed.py -i <bugly符号表的zip包> -o <压缩后的输出路径>
```

![](https://upload-images.jianshu.io/upload_images/4642217-d492a28c0e283421.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


反解：

```
python3 decompress.py -i <经过上步压缩的zip路径> -o <输出路径>
```

![image.png](https://upload-images.jianshu.io/upload_images/4642217-2a3b013573e996d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


