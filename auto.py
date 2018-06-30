#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from time import sleep
from logbook import Logger, FileHandler
from datetime import datetime as dt

#load the logger
try:
    logger = Logger('Automater')
    log = FileHandler(__file__+'.log')
    log.push_application()
    logger.info('Application initialized at '+str(dt.now()))
    logger.info('Loading users...')
    users = {
        'username':'password'
        #add users details here
        }
    logger.info('users loaded successfullly')
    #Attempt to load the webdriver
    try:
        logger.info('starting webdriver...')
        '''
            For windows users: Replace line 29 with 24 and 25
            Ensure that geckodriver is in path i.e 'C:\Users\USERNAME\geckodriver.exe'
            Edit to use chromedriver or any other webdriver available
            path = os.path.join(os.getenv('USERPROFILE'), 'geckdriver.exe')
            driver = webdriver.Firefox(executable_path=path)
        '''
        driver = webdriver.Firefox()
        logger.info('wedriver started successfully')

    except Exception as exception:
        logger.critical(type(exception).__name__+' Exception occured when loading webdriver')
        try:
            driver.quit()
        except NameError:
            pass
        exit(0)
    #Attempt to login users into url
    try:   
        for user in users:
            url = 'https://www.imlango.co.ke'
            logger.info('loading '+url)
            logger.info('Please wait this might take a while...')
            driver.get(url)
            email = driver.find_element_by_id('TxtUsername1')
            email.send_keys(user)
            password = driver.find_element_by_id('TxtPassword1')
            password.send_keys(users[user])
            password.submit()
            logger.notice(user+' Logged in...')
            #The time setup gives every user 40mins online
            counter = 0
            '''
            Add code here to specify any links to go to
            Depending on your website elements or 
            whichever criteria you opt to use
            '''
            while(counter < 80):
                #Ensure that all pop-ups are suppressed
                try:
                    alert = driver.switch_to_alert()
                    alert.dismiss()
                    logger.notice('Alert dismissed...')
                except NoAlertPresentException:
                    #if no pop-up present carry on
                    pass
                sleep(30)
                counter += 1
                #sleep for 30secs count 1
            logger.warn('Logging out '+user)
            
    except Exception as exception:
        logger.critical(type(exception).__name__+' Exception occured when loading page')
        driver.quit()
        exit(0)
        
    logger.info('Choked on all users successfully')
    logger.notice('Now dying...')
    logger.notice('application terminated at '+str(dt.now()))
    driver.quit()
    exit(0)
except KeyboardInterrupt as KI:
    logger.error('KeyboardInterrupt...Dying')
    try:
        driver.quit()
    except NameError:
        pass
    exit(0)
