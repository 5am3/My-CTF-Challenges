# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os,re

urlmain='http://localhost'
chdr='/var/www/chromedriver'
def get_url():
	print('[+] begin to checking~')
	path="html/submit_1bce5f764c10b1c3b7e2bf835cf31247"
	filelist=os.listdir(path)
	for files in filelist:
		Olddir=os.path.join(path,files)
		if os.path.isdir(Olddir):
			continue
		filep=path+'/'+files
		if('index.html' in filep):
			continue
		cat_flag(filep)
		os.remove(filep)
		time.sleep(2)

def cat_flag(urlpath):
	global driver
	# url='http://localhost/'+urlpath
	url=open(urlpath).readlines()[0]
	url = re.sub(r'^http://[a-zA-Z0-9\.:]+?/', "http://localhost/", url)
	print('[+] Testing '+url)
	begin_url=urlmain+'/backdoor2bot_dont_delete.php'

	try:
		driver.get(begin_url)
		# driver.add_cookie({'name':'admin','value':'abc','path':'/'})
		driver.get(url)
	except:
		driver.quit()
		driver =webdriver.Chrome(chdr,chrome_options=chrome_options)
		driver.set_page_load_timeout(10)
		driver.set_script_timeout(10)


chrome_options = Options()
# specify headless mode
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

while(1):
	
	print('[-] chrome loading...')
	driver =webdriver.Chrome(chdr,chrome_options=chrome_options)
	driver.set_page_load_timeout(10)
	driver.set_script_timeout(10)
	
	print('[+] chrome is ready...')
	begin_url=urlmain+'/backdoor2bot_dont_delete.php'
	get_url()
	driver.quit()
	time.sleep(10)


