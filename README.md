# AutoCheckin
# 学习通自动签到

## ！！！支持普通签到，手势签到，二维码签到，拍照签到，位置签到
学习通自动签到，针对早起不能学生，需要自行提供参数和cookie

**目前已知cookie的有效时间至少为一天**

登录方式：二维码登录，自动保存cookie

## 需要修改的地方有：

### 1.课程参数：

```python
   course_list = [
        {
            'name':  # 你的姓名
            'url':  # 课程的任务页面/活动首页
            'course_name':  # 课程名称，可不填
        }
    ]
```

#### 课程URL为进入课程后右上角的任务

![1](images/2020-03-15-160930.png)



### 2.位置信息

```python
    address = {
        "latitude": "-1",  # 纬度
        'longitude': "-1",  # 经度
        'addr': "",  # 位置名称
        'ifTiJiao': "0"  # 是否开启提交位置信息，默认关闭
    }
```

### 3.拍照签到的图片

请在该文件的目录下存放名字为up_img.jpg的图片

如有拍照签到会自动上传该图片，**否则会自动上传wyz**！

##  二、让Python脚本定时启动

准备好定时启动的脚本auto.py

用root权限编辑以下文件

```bash
sudo vim /etc/crontab
```

在文件末尾添加以下命令

```
2 * * * * root /usr/bin/python3.5 ~/auto.py > ~/auto.log

```

以上代码的意思是每隔两分钟执行一次脚本并打印日志。

**三、crontab编写解释**

基本格式

```
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

```

**四、举例说明**

1、每分钟执行一次

```
* * * * * user command
```

2、每隔2小时执行一次

```
* */2 * * * user command (/表示频率)
```

3、每天8:30分执行一次

```
	
30 8 * * * user command
```

4、每小时的30和50分各执行一次

```
30,50 * * * * user command（,表示并列）
```

4、每个月的3号到6号的8:30执行一次

```
30 8 3-6 * * user command （-表示范围）
```

5、每个星期一的8:30执行一次

```
30 8 * * 1 user command （周的范围为0-7,0和7代表周日）
```

