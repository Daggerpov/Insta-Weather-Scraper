from selenium import webdriver
import tkinter as tk 
from time import sleep 
from sys import platform
from tkinter import ttk
import requests
from random import randint 
import random
import os
from selenium.webdriver.common.keys import Keys

#I'm using this resolution for the window, since I have two screens that are 
#high in resolution (1080p & 1440p) but I want it to be compatible with older systems
#and not take up the entirety of my screens
HEIGHT = 768
WIDTH = 1366


class web_scraper():
    """links = []

    comments = [
        'So cool!', 'Wow!', 'Awesome!'
    ]

    accounts = [
        'google', 'twitter', 'googledevs', 'instagram'
    ]
    """
    
    #will be run for both bot instances
    def __init__(self):
        #tells Python where to look for the chrome web driver
        PATH = "/Users/daggerpov/Documents/GitHub/Insta-Weather-Scraper/chromedriver"
        self.driver = webdriver.Chrome(PATH)
        
    #enters in the credentials and navigates through to the homepage of instagram
    def instagram_login(self, username, password):
        #navigates to this base url
        self.driver.get("https://instagram.com")
        #need to sleep after every request, or else the browser will sense a bot
        #also need to give the browser time to load or it can't fetch
        sleep(2)
        
        #enters the username & password by simulating the presses of keys
        username_input = self.driver.find_element_by_xpath(
            "//input[@name='username']")
        username_input.send_keys(username)
        
        
        password_input = self.driver.find_element_by_xpath(
            "//input[@name='password']")
        password_input.send_keys(password)
        
        
        #clicks on these 3 buttons by finding their x paths
        submit_btn = self.driver.find_element_by_xpath(
            "//button[@type='submit']")
        submit_btn.click()
        sleep(4)
        
        
        not_now_button_1 = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]")
        not_now_button_1.click()
        sleep(2)
        
        
        not_now_button_2 = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]")
        not_now_button_2.click()
        sleep(2)
        

    #randomizing sleep times to avoid being detected as a bot
    def random_number_generator(self, x, y):
        random_number = random.randrange((x * 100), (y * 100)) / 100
        return random_number

    def nav_user(self, user, nav_without_follow=True):
        sleep(self.random_number_generator(2, 6))
        self.driver.get('https://instagram.com/' + user)
        
        #will quit the driver if all the operation does is navigate
        if nav_without_follow == True:
            sleep(3)
            self.driver.quit()
        else:
            sleep(3)

    def follow_user(self, user):
        self.nav_user(user, False)
        
        try:
            follow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0]
            follow_button.click()
        except:
            pass
        
        sleep(self.random_number_generator(3, 5))
        self.driver.quit()

    '''def unfollow_user(self, user):
        try:
            self.nav_user(user, False)
            sleep(self.random_number_generator(3, 5))
            following_btn = self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")[0]
            following_btn.click()
            sleep(self.random_number_generator(2, 4))
            unfollow_btn = self.driver.find_elements_by_xpath("//button[contains(text(), 'Unfollow')]")[0]
            unfollow_btn.click()
        except:
            pass'''


    def get_weather(self, city):
        try:
            #using requests module in Python to find current weather
            
            #this is my own weather key that I got from signing up for free
            #to this weather api
            weather_key = '91cdb307c9f5815eb1149aeb01834886'

            url = 'https://api.openweathermap.org/data/2.5/weather'
            
            #I'll be passing in these parameters to specify my search query
            params = {'APPID': weather_key, 'q': city, 'units': 'metric'}
            
            #getting the full response as lists/dictionaries
            response = requests.get(url, params=params)
            
            #if there is a response retrieved in JSON, then I'll query 
            #for what I want to extract in my 3 variables through 
            #these data structures
            if response.json():
                weather = response.json()
                

                name = weather['name']
                description = weather['weather'][0]['description']
                temperature = weather['main']['temp']
                

                #formatting these as one string with symbols and label text like 'Conditions:'
                current = f'\nCity: {name}\n\nConditions: {description}\n\nTemperature: {temperature}°C' 
            
        except:
            #quitting the chrome driver and returning a custom error message to the 
            #labels instead of the weather
            self.driver.quit()
            
            return 'Something went wrong. \nPlease enter a proper city name.', \
                'Either Type:', \
                '1. (1 word city name)', \
                '2. (1 word city name), (two letter region code)', \
                '3. (2 word city name)', \
                '4. (2 word city name), (two letter region code)'

        city = city.replace(' ', '-')
        city = city.replace(',-', ', ')
        city = city.split(', ')[0]

        try:
            #using selenium bot to find overall description of weather
            #only one request being done, so sleep not required
            self.driver.get("https://www.weather-forecast.com/locations/"+city+"/forecasts/latest")
            
            forecast = self.driver.find_elements_by_class_name("b-forecast__table-description-content")[0].text
        
        except:
            #same as last error message for the other weather scraping attempt
            self.driver.quit()
            
            return 'Something went wrong. \nPlease enter a proper city name.', \
                'Either Type:', \
                '1. (1 word city name)', \
                '2. (1 word city name), (two letter region code)', \
                '3. (2 word city name)', \
                '4. (2 word city name), (two letter region code)'
        
        self.driver.quit()
        
        
        #separating the forecast lines, then defining 3 variables with them
        lines = forecast.split('. ')
        line_one, line_two, line_three = lines
       
       
        #rearranging them, since their sizes in length aren't ideal currently
        line1 = '• ' + line_three
        line2 = '• ' + line_two
        line3 = '• ' + line_one

        #lines 1 and two should be the longest, with 3 never really 
        #exceeding too many characters to go off this window's screen
        
        #splitting lines up if they're too long in character length
        #moving them all down so that if there are any blank lines, 
        #they'll always be towards the top of the 5 forecast labels
        if len(line1) > 75 and len(line2) > 75:
            line1_, line_1 = line1.split(', ')
            line1_ += ','
            line2_, line_2 = line2.split(', ')
            line2_ += ','
        
        elif len(line1) > 75 and len(line2) <= 75:
            line1_  = '' 
            line_1, line2_ = line1.split(', ')
            line_1 += ','
            line_2 = line2
        
        elif len(line1) <= 75 and len(line2) > 75:
            line1_, line_1 = '', line1
            line2_, line_2 = line2.split(', ')
            line2_ += ','

        else:
            line1_, line_1 = '', ''
            line2_ = line1
            line_2 = line2 

        return current, line1_, line_1, line2_, line_2, line3       


def weather_bot(city, label, label0, label1, label2, label3, label4):
    weather_bot = web_scraper()
    
    #this function call will return 6 items, so I'm using multi variable assignment
    label['text'], label0['text'], label1['text'], label2['text'], label3['text'], label4['text'] = weather_bot.get_weather(city)


def instagram_bot(operation, hashtag, user, username_entry_text, password_entry_text):
    instagram_bot = web_scraper()
    username = str(username_entry_text)
    password = str(password_entry_text)
    instagram_bot.instagram_login(username, password)

    #if operation == 'get_unfollowers':
    #    instagram_bot.get_unfollowers(username)
    #elif operation == 'comment_on_account':
    #    instagram_bot.comment_on_account()
    #elif operation == 'like_comment_by_hashtag':
    #    instagram_bot.like_comment_by_hashtag(hashtag)
    if operation == 'nav_user':
        instagram_bot.nav_user(user)
    elif operation == 'follow_user':
        instagram_bot.follow_user(user)
    #elif operation == 'unfollow_user':
    #    instagram_bot.unfollow_user(user)




def main():
    #initializing module
    root = tk.Tk()
    
    #setting the current screen to start menu
    app = start_menu_screen(root)
    
    #overall GUI loop which will run constantly, accepting input and such
    root.mainloop()


class start_menu_screen():
    def __init__(self, master):
        #properties of this screen, most of which will stay constant
        #throughout other screens too
        self.master = master
        self.master.title("Daggerpov's Web Scraper")
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        

        #every element will fit into the above canvas like this top frame
        self.top_frame = tk.Frame(self.canvas, bg='#2c2f33', bd=5)
        self.top_frame.place(relx=0.5, rely=0.05, relheight=0.1, relwidth=0.6, anchor='n')

        #displaying text for the title
        self.title = tk.Label(self.top_frame, text="What would you like to check?", bg='#7289da', 
            fg='white')


        #changing font size of title depending on OS and changing window icon
        if platform == "linux" or platform == "linux2":
            #linux
            size = 32
            img = tk.PhotoImage(file='./images/scraper.png')
            self.master.tk.call('wm', 'iconphoto', self.master._w, img)
        elif platform == "win32":
            #windows
            size = 32
            self.master.iconphoto(True, tk.PhotoImage(file="./images/scraper.ico"))
        elif platform == "darwin":
            #macOS
            size = 44
            self.master.iconphoto(True, tk.PhotoImage(file="./images/scraper.gif"))
        
        #setting font and font size 
        self.title.config(font=('Courier', size))
        #takes up entire top frame
        self.title.place(relwidth=1, relheight=1)


        #these two blocks of code are identical other than which buttons they are
        self.left_frame = tk.Frame(self.canvas, bg='#99aab5', bd=5)
        self.left_frame.place(relx=0.05, rely=0.2, relheight=0.7, relwidth=0.4)

        
        #header text saying "Weather"
        self.weather_text = tk.Label(self.left_frame, text="Weather", bg='#99aab5', fg='#23272a')
        self.weather_text.config(font=('Courier', 33))
        self.weather_text.place(relwidth=1, relheight=0.1)

        
        #making the picture into a label
        self.weather_pic = tk.PhotoImage(file='./images/weather_pic.png')
        self.weather_pic_label = tk.Label(self.left_frame, image=self.weather_pic)
        self.weather_pic_label.place(relwidth=1, relheight=0.9, rely=0.1)

        
        #putting a button at the same spot as the label, essentially
        #making it into one
        self.weather_pic_button = tk.Button(self.left_frame, image=self.weather_pic, 
        command=self.go_weather_screen)
        self.weather_pic_button.place(relwidth=1, relheight=0.9, rely=0.1)

        #----------------------------------------------------------------------------
        self.right_frame = tk.Frame(self.canvas, bg='#99aab5', bd=5)
        self.right_frame.place(relx=0.55, rely=0.2, relheight=0.7, relwidth=0.4)


        self.instagram_text = tk.Label(self.right_frame, text="Instagram", bg='#99aab5', fg='#23272a')
        self.instagram_text.config(font=('Courier', 33))
        self.instagram_text.place(relwidth=1, relheight=0.1)


        self.instagram_pic = tk.PhotoImage(file='./images/instagram_pic.png')
        self.instagram_pic_label = tk.Label(self.right_frame, image=self.instagram_pic)
        self.instagram_pic_label.place(relwidth=1, relheight=0.9, rely=0.1)


        self.instagram_pic_button = tk.Button(self.right_frame, image=self.instagram_pic, 
        command=self.go_instagram_login_screen)
        self.instagram_pic_button.place(relwidth=1, relheight=0.9, rely=0.1)

    #both of these redirects are identical
    def go_weather_screen(self):
        #setting the top level window of tkinter as the current screen
        self.weatherScreen = tk.Toplevel(self.master)
        
        #sets its own app (similar to when the program was first initialized 
        # at main) to the previously defined weatherScreen
        self.app = weather_screen(self.weatherScreen)
    
    def go_instagram_login_screen(self):
        self.instagramScreen = tk.Toplevel(self.master)
        self.app = instagram_login_screen(self.instagramScreen)

class PlaceholderEntry(ttk.Entry):
    #initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        
        #runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        #if this argument is given (like for the instagram password, 
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    
    def _clear_placeholder(self, e):
        #deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"
        
        #editing the property of the entry box 'show' to display asterisks ,
        #instead of any of the entered characters
        if self.validation == 'password':
            self['show'] = "*"
        
    def _add_placeholder(self, e):
        #if there isn't any text entered in AND the user isn't focused in 
        #on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"


class weather_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Daggerpov's Web Scraper - Checking Weather")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        
        #making the style of this window compatible with my custom entry class
        self.style = ttk.Style(self.master)
        self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")
        

        #this background picture will take up the entire window
        self.weather_background_pic = tk.PhotoImage(file="./images/weather_background_pic.png")
        self.weather_background_pic_label = tk.Label(self.master, image=self.weather_background_pic)
        self.weather_background_pic_label.place(relwidth=1, relheight=1)

        #fitting the entry and button for weather
        self.weather_frame = tk.Frame(self.master, bg="#99aab5", bd=5)
        self.weather_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')


        #these labels will take the results from the weather_bot 
        #then place that text to the screen
        #this first label is just for the api results (bigger font, more simple)
        label = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 36, 'bold'))
        label.place(relwidth=1, relheight=0.5)


        #these five labels encompass the output from the bot's scraping 
        #from the other website with selenium
        label0 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 22))
        label0.place(rely=0.5, relwidth=1, relheight=0.1)

        label1 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 22))
        label1.place(rely=0.6, relwidth=1, relheight=0.1)

        label2 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 22))
        label2.place(rely=0.7, relwidth=1, relheight=0.1)

        label3 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 22))
        label3.place(rely=0.8, relwidth=1, relheight=0.1)

        label4 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 22))
        label4.place(rely=0.9, relwidth=1, relheight=0.1)


        #entry text box for user input
        self.entry = PlaceholderEntry(self.weather_frame, "City Name", '', font=('Courier', 40))
        self.entry.place(relwidth=0.65, relheight=1)

        #button for weather entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda function that invokes the weather_bot function
        self.button = tk.Button(self.weather_frame, text="Get Weather", font=('Courier', 40), bg='white', 
            command=lambda:weather_bot(self.entry.get(), label, label0, label1, label2, label3, label4))
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)


class instagram_login_screen():
    def __init__(self, master):
        #same property adjustments as used for the weather screen
        self.master = master
        self.master.title("Daggerpov's Web Scraper - Instagram Login")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        
        self.style = ttk.Style(self.master)
        self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")

        
        #these frames will house the username/password entries, as well as 
        #the submittion button and nothing else in them
        self.username_frame = tk.Frame(self.master, bg="#99aab5", bd=10)
        self.username_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.25, anchor='n')
        
        self.password_frame = tk.Frame(self.master, bg="#99aab5", bd=10)
        self.password_frame.place(relx=0.5, rely=0.40, relwidth=0.75, relheight=0.25, anchor='n')

        self.submit_frame = tk.Frame(self.master, bg="#7289da", bd=10)
        self.submit_frame.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.15, anchor='n')
        
        
        #making these two variables global so they can be passed into the instagram 
        #screen and then used for the scraping functions
        global username_entry 
        username_entry = PlaceholderEntry(self.username_frame, "Username", "", font=('Courier', 100))
        username_entry.place(relheight=1, relwidth=1)

        global password_entry
        password_entry = PlaceholderEntry(self.password_frame, "Password", 'password', font=('Courier', 100))
        password_entry.place(relheight=1, relwidth=1)
        

        #submission button will redirect the user over to the instagram scraping screen upon being pressed
        self.submit = tk.Button(self.submit_frame, text="Login", font=('Courier', 60), bg='white',
            command=self.go_instagram_screen)
        self.submit.place(relheight=1, relwidth=1)
        

    def go_instagram_screen(self):
        self.instagramScreen = tk.Toplevel(self.master)
        
        #passing in the username/password variables so that their states can be 
        #grabbed as values for use later on
        self.app = instagram_screen(self.instagramScreen, username_entry, password_entry)

class instagram_screen():
    def __init__(self, master, username_entry, password_entry):
        #same base window properties
        self.master = master
        self.master.title("Daggerpov's Web Scraper - Checking Instagram")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)


        #sets the style to work with my custom PlaceholderEntry class
        self.style = ttk.Style(self.master)
        self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")

        self.user_frame = tk.Frame(self.master, bg="#99aab5", bd=5)
        self.user_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')


        #setting this to global so that I can use it similarly to the 
        #username/password ones with Instagram links
        global user
        user = PlaceholderEntry(self.user_frame, "Someone's Username", "", font=('Courier', 60))
        user.place(relheight=1, relwidth=1)


        #making a picture/button for the navigation method to be ran by 
        #passing in its 'operation' argument to be 'nav_user'
        self.navigate_pic = tk.PhotoImage(file='./images/navigate_pic.png')
        self.navigate_pic_label = tk.Label(self.user_frame, image=self.navigate_pic)
        self.navigate_pic_label.place(relwidth=0.1, relheight=1, relx=0.8)

        self.navigate_pic_button = tk.Button(self.user_frame, image=self.navigate_pic, 
        command=lambda: instagram_bot('nav_user', '', str(user.get()), username_entry.get(), password_entry.get()))
        self.navigate_pic_button.place(relwidth=0.1, relheight=1, relx=0.8)


        #same as the navigation, this is identical but slid over to the right of it
        self.follow_pic = tk.PhotoImage(file='./images/follow_pic.png')
        self.follow_pic_label = tk.Label(self.user_frame, image=self.follow_pic)
        self.follow_pic_label.place(relwidth=0.1, relheight=1, relx=0.9)

        self.follow_pic_button = tk.Button(self.user_frame, image=self.follow_pic, 
        command=lambda: instagram_bot('follow_user', '', str(user.get()), username_entry.get(), password_entry.get()))
        self.follow_pic_button.place(relwidth=0.1, relheight=1, relx=0.9)

        '''self.unfollow_pic = tk.PhotoImage(file='./images/unfollow_pic.png')
        self.unfollow_pic_label = tk.Label(self.user_frame, image=self.unfollow_pic)
        self.unfollow_pic_label.place(relwidth=0.1, relheight=1, relx=0.9)

        self.unfollow_pic_button = tk.Button(self.user_frame, image=self.unfollow_pic, 
        command=lambda: instagram_bot('unfollow_user', '', str(user.get()), username_entry.get(), password_entry.get()))
        self.unfollow_pic_button.place(relwidth=0.1, relheight=1, relx=0.9)
        '''

if __name__ == '__main__':
    main()