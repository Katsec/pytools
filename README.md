# pytools

> 项目包含渗透测试过程中常用的python脚本。

## mnScan

通过Python脚本调用masscan进行全端口扫描， 后再使用nmap进行端口识别。  
扫描ip.txt内支持单个IP、IP范围、IP段的形式。  
扫描结果会返回到nmap_result.txt内。  

### usage

```bash
python3 mnScan.py
```



## shiroCheck

该shiro批量检测工具，通过python脚本调用@wyzxxz大佬的检测jar包来批量识别Shiro。  

使用该jar包的原因是检测结果相对较为准确且会出主动寻找利用链,扫描完成后会输出存在漏洞的txt文件（含shiroKey） 

jar包下载地址(https://xz.aliyun.com/forum/upload/affix/shiro_tool.zip)

### usage

```bash
python3 check.py -r url.txt
```



## listFile

主要用于获取源码路径生成字典进行扫描

### usage

```bash
python3 listfile.py #可输入绝对路径或相对路径
```



## crackTomcat

tomcat 管理后台密码爆破,支持批量爆破。  

### usage

```bash
Useage: python3 crack_tomcat.py -u url
Useage: python3 crack_tomcat.py -r url.txt
```

