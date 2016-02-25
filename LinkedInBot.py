#do: pip install BeautifulSoup4 and Selenium
#Typical LinkedIn Bot that results in increased views based on outgoing job/profile views.
#Clearly, morals are always a dilemma in this situation on if someone should use this.
#I do not recommend this unless extremely desperate. Views obviously will fall to normal 
#levels once the usage is discontinued. Also, I believe bot checks will be run on your account
#following prolonged usage *please see your doctor if ----*

import argparse, os, time #Sets up methods based around arguments passed through cmd, usage of OS, and time
import urllib.parse, random, sys #allows parsing of urls and usage of random library
from selenium import webdriver #allows usage of a webdriver through Selenium
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup

def getPeopleLinks(page): #pulls all links on the current page that link to someones profile --> links array; returns
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if 'profile/view?id=' in url:
				links.append(url)
	return links
def getJobLinks(page): #pulls all links leading to jobs on the current page --> links array; returns them
	links = []
	for link in page.find_all('a'):
		url = linkl.get('href')
		if url:
			if '/jobs' in url:
				links.append(url)
	return links

def getID(url): #parses url for the id number based on a url provided.
	pUrl = urllib.parse.urlparse(url)
	return urllib.parse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser): #browser is defined in main(), such as Firefox or IE
	visited = {} #Defines a set literal variable for all visited pages
	pList = []
	count = 0
	while True:
		#sleep to make sure everything loads.
		#add random to make us look human.
		#time.sleep(random.uniform(12.6,25.2))
		time.sleep(random.uniform(3.6,9.2))
		page = BeautifulSoup(browser.page_source, "html.parser")
		people = getPeopleLinks(page)
		if people:
			for person in people:
				ID = getID(person)
				if ID not in visited:
					pList.append(person)
					visited[ID] = 1
		if pList: #if there's people to view
			person = pList.pop()
			browser.get(person)
			count += 1
		else: #otherwise find people via the job pages
			jobs = getJobLinks(page)
			if jobs:
				job = random.choice(jobs)
				root = 'http://www.linkedin.com'
				roots = 'http://www.linkedin.com'
				if root not in job or roots not in job:
					job = 'https://www.linkedin.com'+job
				browser.get(job)
			else:
				print("Something happened getting job links")
				break
		#output make option for thisulSoup(browser.page_source)
		people = getPeopleLinks(page)
		if people:
			for person in people:
				ID = getID(person)
		print("[+] "+(browser.title).encode('utf8').decode(sys.stdout.encoding)+" Visited! \n ("+str(count)+"/"+str(len(pList))+") Visited/Queue")
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("email",help = "Linkedin email")
	parser.add_argument("password", help = "Linkedin password")
	args = parser.parse_args()

	browser = webdriver.Chrome()
	browser.get("https://linkedin.com/uas/login")

	emailElement = browser.find_element_by_id("session_key-login")
	emailElement.send_keys(args.email)
	passwordElement = browser.find_element_by_id("session_password-login")
	passwordElement.send_keys(args.password)
	passwordElement.submit()
	os.system('cls')
	print("[+] Success! Logged in, Bot Starting!")
	ViewBot(browser)
	browser.close

if __name__ == "__main__":
	main()
