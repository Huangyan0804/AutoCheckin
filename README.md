# AutoCheckin
# 学习通自动签到（小白勿用）

## ！！！仅支持普通签到
学习通自动签到，针对早起不能学生，需要自行提供参数和cookie
目前未知cookie的有效时间
小白勿用

~因为匆忙制作的签到脚本，我的身体已经菠萝菠萝哒~
---
需要修改的地方有：
``` python
course_list 签到的课程
login_data {
    uname:  # 用户名
    password:  #自行base64加密
}
可选参数：
header {
    Cookie：
}

```



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
 *   *    *   *    *  user  command
分 时 日 月 周 用户 命令
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

