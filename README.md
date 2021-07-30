# 根据用户名生成密码

## 使用环境

windows+python3.7

```
pip install -r requirements.txt
```

打包成exe：

```
pyinstaller -c pass.py --noconsole

#把config和xuyaode这2个目录放到打包生成dist\pass目录中。
```



![image-20210730215254431](https://gitee.com/dd123456yybb/img/raw/master/image-20210730215254431.png)

## 原理

输入的用户名会根据config/dynamic_password.txt定义的进行替换，%user%被替换为输入的用户名。



static_password目录下存放的常用字典，可以在生成字典的时候把这些字典也添加进去。



用户名和生成的密码会保存在Tmp中，点击copy可以直接复制文件路径，方便放到超级弱口令检测工具里爆破

