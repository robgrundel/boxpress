Boxpress
========
Blogging using Dropbox + Markdown. Written in Python and built to deploy on [Heroku](http://heroku.com).

As demonstrated on [robgrundel.com](http://www.robgrundel.com).

Thanks to 
* [Letterpress](https://github.com/an0/Letterpress) by [@an0](https://github.com/an0) for inspiration.
* [@michieldegraaf](https://github.com/michieldegraaf) for making his [ultra clean blog design](https://github.com/michieldegraaf/blog) available to the masses.

## Install Boxpress locally
1. Get the source off [Github](http://github.com/robgrundel/boxpress)
1. Install [Heroku Toolbelt](https://toolbelt.heroku.com/)
1. Run virtualenv 
source venv/bin/activate
1. Start foreman in base directory 
foreman start 
1. Hit the homepage http://127.0.0.1:5000
1. Connect up to your Dropbox which will automatically create an Apps folder in Apps/boxpress
1. To create your first post write a Markdown file and save to the Apps/boxpress directory. 

## Install Boxpress on Heroku
1. Ensure [Heroku Toolbelt](https://toolbelt.heroku.com/) is installed
1. Setup an [Heroku](http://heroku.com) account
1. Set Heroku API key in config heroku config:set HEROKU_KEY=<Heroku API key>
1. If you want add analytics heroku config:set ANALYTICS="<analytics script>"


