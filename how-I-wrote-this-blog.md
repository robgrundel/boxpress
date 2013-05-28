title: How I wrote this blog (and how you can use it too)
date: 2013-05-28 23:00:00
tags: tech, blog, improvement, heroku, python

I wanted to learn Python and thought the long overdue update on my blog would be an ideal training ground. I looked at [Letterpress](https://github.com/an0/Letterpress/) but was unable to install it on Heroku. So, I thought I'd roll my own. I wrote the following list of requirements.

1. To use the same style as Letterpress courtesy of [Michiel Degraaf's blog](https://github.com/michieldegraaf/blog).
1. Also as with Letterpress I wanted to use [Markdown](http://daringfireball.net/projects/markdown/) which means I can write my blog posts in [iA Writer](http://iawriter.com) which support MD.
1. To read from my Dropbox using the Dropbox API (hence the choice to use Python as there are limited language choices).
1. After failing to get Letterpress working, I was determined to deploy something to [Heroku](http://heroku.com). So, a meaningless technical requirement but a personal goal acheived.

The first task was to serve a static HTML page for which I used [CherryPy](http://www.cherrypy.org/).

Then I deployed the app on [Heroku](http://heroku.com) which meant setting up the appropriate Procfile and requirements.txt files. You can see how easy it is to [deploy a Python app](https://devcenter.heroku.com/articles/python).

Markdown is a piece of cake to use in Python so I served this first post as a static MD file and inserted in my basic index.html file.

I needed to do write some custom metadata for my posts. I thought the following would be enough as the first 3 lines of each Markdown post
	
	title: How I wrote this blog
	date: 2013-05-28 23:00:00
	tags: tech, blog, improvement, heroku, python
