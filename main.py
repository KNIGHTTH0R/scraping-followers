from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
import time



print("enter user name")
username = input()

print("enter password")
password = input()


print("User id of the page to scrape followrs from")
user_id = input()

class scrapfollowers():
  
    def __init__(self):
        #assigns firefox as  the browser to  use for executing script
        self.browser = webdriver.Firefox()
    
    def login(self):
        #opens instagram login page
        self.browser.get('https://www.instagram.com/')
        time.sleep(4)

        #finds the username and password elements 
        emailinput = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
        passwinput = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
        
        #sends the password and username wich you input and presses ENTER

        emailinput.send_keys(username)
        passwinput.send_keys(password)
        passwinput.send_keys(Keys.ENTER)
        time.sleep(6)
        print("i have signed in")

    def notification(self):

        #As soon as you login a popup shows saying to turn on notification
        #this function handles it

        try:
            notbut = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
            notbut.click()
        
        #sometimes instead of notification save login information page loads
        #below exception is for handling that

        except NoSuchElementException :
            time.sleep(5)
            #in case the notfication pop up loded up slowly
            try:
                notbut = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
                notbut.click()

            #in case save info page loads  up even then notification popup would
            #appear so this would handle both
            except NoSuchElementException :
                notnowbut = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
                notnowbut.click()
                notbut = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
                notbut.click()
        time.sleep(2)

        print("Notification button is off")

    def search(self , user_id):
        #this function opens up the page of user you want to scrap data from
        self.browser.get("https://www.instagram.com/" + str(user_id))
        time.sleep(5)

    def folllis(self):
        
        #this variable stores the number of followers for running the 
        #scroll down until the range of followernumber/2

        follnumbut = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
        follnum = int(follnumbut.text)
        
        #finds and clicks the followers button for followers list to pop up

        folbut = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        folbut.click()
        time.sleep(5)

        #now a file named followerlist opens up where we will be storing our list

        f=open("followerlist.txt" , "a")

        #for loop for scrolling down the list of followers

        for x in range(int(follnum/2)):

            folldiv = self.browser.find_element_by_class_name('isgrP')

            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",folldiv)
            time.sleep(0.25)

        #for loop for scraping all the user names

        for x in range(int(follnum)):

            followers_elems = self.browser.find_elements_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li["+str(x+1)+"]/div/div[1]/div[2]/div[1]/a")
            # Finally, scrape the followers
            
            for value in followers_elems :
                f.write(value.text)
                f.write("\n")

        #file closed and saved

        f.close()
        time.sleep(2)       
        print("followers file ready")

    def closebrowser(self):
        #function for closing browser
        self.browser.close()


x=scrapfollowers()
x.login()
x.notification()
x.search(user_id)
x.folllis()
x.closebrowser()
