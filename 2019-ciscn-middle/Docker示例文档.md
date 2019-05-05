# 赛题说明

## 题目信息：

- 题目名称：baby_xss
- 预估难度：中等偏难 （简单/中等偏易/中等偏难/困难）
- 题目描述：baby_xss?

### 题目考点：

```
1. XSS绕过
2. XSS读文件
3. SQL注入-union注入
```

### 思路简述：

XSS读取后台内容，配合csrf，打后台接口，进行sql注入，从而拿到数据库中的flag





## 镜像编译与启动

```bash
# 修改flag
sed -i "s/flag{123456}/flag{新的flag}/g" test.sql

# 启动
docker build  -t 5am3_challenges/baby_xss:v1.0 .
docker run -d -p 8233:80 -t 5am3_challenges/baby_xss:v1.0
```



## WriteUp

懒得写，直接给exp了。

```bash
sed -i "s/xssListenerEval.com/你的XSS监听地址（ip+端口即可）/g" exp.py
# 第二个参数必须写域名（IP）+端口
python exp.py auto timu.com:80
# 然后就在XSS监听地址能接到回显
# 此时可以手动解密，也可以用exp直接解密。
python exp.py decode 收到的base64

```











