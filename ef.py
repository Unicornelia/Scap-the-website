from flask import Flask
from flask import render_template
from flask import request
import requests
from bs4 import BeautifulSoup
from pygithub3 import Github
import unicodecsv

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def task():
	#Looks for github and twitter name sin html
	githublinks = [] #created a list for the needed social media links
	twitterlinks = []
	url = request.args.get("url") #flask code for getting links definied in a variable called url
	if url: #if condition, it says:
		candidate_homepage = requests.get(url) #lets call the candidate homepage, literally get the homepage using requests
		links = extractlinks(candidate_homepage.text) #lets define links we need, they are extracted from the candidate homepage's content
		#print candidate_homepage.content that has links but for loop is coming!
		print links
		
		for webitem in links: #condition, if there is twitter or github in the link, then add it to the socialmedialinks list
			if "twitter.com" in webitem:
				webitem = webitem.split("/")[3] #splitted the webitem string and definied with / and then we asked for the 3rd item only
				twitterlinks.append(webitem)
			if "github.com" in webitem:
				webitem = webitem.split("/")[3] #github API comes here
				githublinks.append(webitem)
	if len(twitterlinks + githublinks) == 0:
			return render_template("ef.html", error="Not working URL or you need to start typing")

	return render_template("ef.html", links=', '.join(set(twitterlinks + githublinks))) #return the actual html with printed links in it, which are defined


def extractlinks(html):
	soup = BeautifulSoup(html)
	anchors = soup.findAll('a')
	links = []
	for a in anchors:
		if a.attrs.has_key('href'):
			links.append(a.get("href"))
	return links

def github_stars():
	pass


if __name__ == "__main__":    
	app.debug = True
	app.run()