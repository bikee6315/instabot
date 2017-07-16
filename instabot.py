##************ INSTABOT ***********##

import requests                            #importing request module
import urllib                              #importing urllib module
from textblob import TextBlob

#SANDBOX USERS: sntk97, tourism._nepal, insta_bot1996,inta1996
#LATITUDE=28.6129
#LONGITUDE=77.2295

APP_ACCESS_TOKEN = '2171493643.ae2709c.f2266fcdceae49418188a27908541a11'
BASE_URL = 'https://api.instagram.com/v1/'

calamities = ['flood', 'earthquake', 'tsunami', 'landslide', 'soil erosion', 'avalanche', 'cyclones', 'hurricane',
              'thunderstorm', 'drought']
locationid=[]

# Function declaration to get your own info

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):

# Printing the data of own

            print 'Username:%s' %(user_info['data']['username'])
            print 'Number of followers:%s' %(user_info['data']['counts']['followed_by'])
            print 'Number of people you are following:%s' %(user_info['data']['counts']['follows'])
            print 'Number of posts:%s' %(user_info['data']['counts']['media'])
        else:
            print "User doesn\'t exist"                   # Printing message if user doesn't exist
    else:
        print 'Status code other than 200 received'

# Function declaration to get ID of user by username

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()          # Getting information of user in json form

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'User id is:'
            print user_info['data'][0]['id']
            return user_info['data'][0]['id']
        else:
            print 'User not found'
            return None
    else:
        print 'Status code other than 200 received'
        exit()

# Function declaration to get info of user by username

def get_user_info(insta_username):
    user_id=get_user_id(insta_username)
    if user_id==None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()       # Requesting json response

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'Username:%s' % (user_info['data']['username'])
            print 'Number of followers:%s' % (user_info['data']['counts']['followed_by'])
            print 'Number of people you are following:%s' % (user_info['data']['counts']['follows'])
            print 'Number of posts:%s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received'

# Function declaration to get information about your own post

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code']==200:
        if len(own_media['data']):
            image_name=own_media['data'][0]['id']+ '.jpeg'
            print 'IMAGE NAME:%s' %(image_name)                       # Display image name
            image_url=own_media['data'][0]['images']['standard_resolution']['url']
            print 'IMAGE URL:%s' %(image_url)                          # Display image url
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded'
            print 'Post id is:'                                        # Printing post id
            print own_media['data'][0]['id']
            import webbrowser
            webbrowser.open(image_name)                              # Display image on browser
            return own_media['data'][0]['id']
        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'

# Function declaration to get information of user post by username

def get_users_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User doesn\'t exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code']==200:
        if len(user_media['data']):
             image_name = user_media['data'][0]['id'] + '.jpeg'
             print 'IMAGE NAME:%s' %(image_name)                     # Display image name
             image_url = user_media['data'][0]['images']['standard_resolution']['url']
             print 'IMAGE URL:%s' %(image_url)                       # Display image url
             urllib.urlretrieve(image_url, image_name)
             print 'Post id is:'                                     # Display post id
             print user_media['data'][0]['id']
             print 'Your post has been downloaded'
             import webbrowser
             webbrowser.open(image_name)                             # Display image on browser
             return user_media['data'][0]['id']
        else:
            print 'There is no recent post of user'
            exit()
    else:
        print 'Status code other than 200 received'
        exit()

# Function declaration to get ID of post uploaded by user using username

def get_post_id(insta_username):
     user_id=get_user_id(insta_username)
     if user_id==None:
         print "User doesn\'t exists"
         exit()
     request_url=(BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
     print 'GET request url : %s' %(request_url)
     user_media=requests.get(request_url).json()

     if user_media['meta']['code']==200:
         if len(user_media['data']):
             return user_media['data'][0]['id']
         else:
             print 'There is no recent post of user'
             exit()
     else:
         print 'Status code other than 200 received'
         exit()

# Function declaration to like post of user using username

def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()                    # Posting a like on a post
    if post_a_like['meta']['code']==200:
        print 'Your like was successful'
    else:
        print 'Your like was unsuccessful'

# Function declaration to comment on post of user using username

def post_a_comment(insta_username):
    media_id=get_post_id(insta_username)
    comment_text=raw_input('Enter your text:')
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()                  #Commenting on a post through url
    if make_comment['meta']['code']==200:
        print'Comment was successfully added'
    else:
        print 'Unable to comment'

# Function declaration to get list of comments of a post using username

def get_comments(insta_username):
    media_id=get_post_id(insta_username)
    if media_id==None:
        print "User doesn\'t exist"
        exit()
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media= requests.get(request_url).json()
    print user_media
    if user_media['meta']['code']==200:
        if len(user_media['data']):
            print 'Comments Are:'
            position=1
            for text in user_media['data']:
                print'\t%s. from %s: %s' %(position,text['from']['username'],text['text'])          # Printing list of comments of a post
                position=position+1
        else:
            print'No comments found'
            return None

    else:
        print 'Status code other than 200 is received'
        exit()

# Function declaration to get the location where natural calamities has occured
def get_natural_calamities(lat,lng):
    request_url = (BASE_URL + 'media/search?lat=%s&lng=%s&distance=500&access_token=%s') % (lat, lng, APP_ACCESS_TOKEN)
    print 'GET reques url: %s' % (request_url)
    user_location = requests.get(request_url).json()
    print user_location
    if user_location['meta']['code'] == 200:
        if len(user_location['data']):
            image=user_location['data'][0]['images']['standard_resolution']['url']
            print image
            for temp in calamities:
                if user_location['data'][0]['tags']==temp:
                 print user_location['data'][0]['tags']
                 print user_location['data'][0]['location']
            print 'Tags are:%s' % (user_location['data'][0]['tags'])
            print 'Location is:%s' % (user_location['data'][0]['location'])
            print '%s is going on at %s' %(user_location['data'][0]['tags'],user_location['data'][0]['location'])
        else:
            print'media not found'
    else:
        print 'Status code other than 200 received'

# Function declalration to get the post liked by own

def self_liked_media():
    request_url = (BASE_URL + 'users/self/media/liked/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    liked_media = requests.get(request_url).json()

    if liked_media['meta']['code']==200:
        if len(liked_media['data']):
            rang=len(liked_media['data'])
            i=0
            for i in range(rang):
                print liked_media['data'][i]['images']['standard_resolution']['url']         # Printing the post liked by own
        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'




def start_bot():
    print 'HEY! WELCOME TO INSTABOT'
    print locationid
    while True:
        try:
            print '\nMENU OPTIONS:'
            print '\ta.GET YOUR OWN DETAILS'
            print '\tb.GET YOUR OWN POST'
            print '\tc.GET RECENT MEDIA LIKED BY OWN'
            print '\td.WANT TO LIKE,COMMENT AND MANY MORE ON OTHERS POST?'
            print '\t  PRESS: \n\t\t e.FOR YES'
            print '\tf.EXIT\n'
            choice=raw_input('ENTER YOUR CHOICE:')
            if choice=="a":
                self_info()
            elif choice=="b":
                get_own_post()
            elif choice=="c":
                self_liked_media()
            elif choice=="e":
                print '\nWHAT WOULD YOU LIKE TO DO?'
                print '\t1.GET DETAILS OF USER BY USERNAME'
                print '\t2.GET DETAILS OF USER POST'
                print '\t3.LIKE A POST'
                print '\t4.COMMENT ON A POST'
                print '\t5.GET COMMENTS'
                print '\t6.GET INFORMATION ABOUT NATURAL CALAMITIES'
                choice2=int(raw_input("Enter your choice:"))
                if choice2==1:
                   insta_username = raw_input("USERNAME:")
                   get_user_info(insta_username)
                elif choice2==2:
                   insta_username = raw_input("USERNAME:")
                   get_users_post(insta_username)
                elif choice2==3:
                   insta_username = raw_input("USERNAME:")
                   like_a_post(insta_username)
                elif choice2==4:
                   insta_username = raw_input("USERNAME:")
                   post_a_comment(insta_username)
                elif choice2==5:
                   insta_username = raw_input("USERNAME:")
                   get_comments(insta_username)
                elif choice2==6:
                   lat=float(raw_input("Enter the latitude:"))
                   lng=float(raw_input("Enter the longitude"))
                   get_natural_calamities(lat,lng)
            elif choice=='f':
                print '\n\t*****HAVE A GOOD DAY******'
                exit()
            else:
                print 'WRONG CHOICE.PLEASE INPUT AGAIN'
        except ValueError:
            print 'PLEASE INPUT VALID NUMBER'

start_bot()





