from inc import *
import requests
import time
import mechanize, cookielib

def startTheParser(irc):
    # sleep to allow time for the bot to join the channel...
    # Should modify this and make it check for when it is in the channel
    time.sleep(30)
    cookie = login(username='', password='')
    print cookie
    session = requests.session()
    last = ""
    while True:
        try:
#            print 'Getting ez posts'
            r = session.get(url='https://evilzone.org/recent', cookies=cookie)
            html = r.text
	    print html
            start = html.find('<div class="counter">1</div>') + 28
            end = html.find('</div>', start)
            source = html[start:end]
            urlstart = source.find('/ <a href="') + 11
            urlend = source.find('</a>', urlstart)
            url = source[urlstart:urlend]
            userstart = source.find('Last post by <strong><a href="')
            userend = source.find('</a> </strong> on<em>', urlstart)
            user = source[userstart:userend]
            user = '">'.join(user.split('">')[1:])
            sesstart = url.find('PHPSESSID') +9
            sesend = url.find('#', sesstart)
            sestag = url[sesstart:sesend]
            sestag = "?PHPSESSID"+sestag
            url = url.replace(sestag, '')
            endurlstart = url.find('" rel=') + 6
            text = url[endurlstart:]
            text = text.replace('"nofollow">', '')
            url = url.replace('" rel='+url[endurlstart:] ,'').replace('(', '%28').replace(')', '%29')
            output = text+" - [ "+url+" ]"  
            if output != last:
                ircFunc.ircSay('#forum', "User: %s - %s" % (user, output), irc)
                last = output
            time.sleep(5)
        except Exception as e:
            errorhandling.inputError('critical', e, 'forum parser')

def login(username, password):
	login_url = 'https://evilzone.org/login'
	agent = mechanize.Browser()
	agent.set_handle_robots(False)
	cj = cookielib.LWPCookieJar()

	agent.set_cookiejar(cj)
	agent.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	agent.open(login_url)

	#login
	agent.select_form(name='frmLogin')
	agent.form['user'] = username
	agent.form['passwrd'] = password
	response = agent.submit()
#	print response
	return cj

