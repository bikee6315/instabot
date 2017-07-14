import requests
import urllib
from textblob import TextBlob

APP_ACCESS_TOKEN = '2171493643.ae2709c.f2266fcdceae49418188a27908541a11'
BASE_URL = 'https://api.instagram.com/v1/'



def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'Username:%s' %(user_info['data']['username'])
            print 'Number of followers:%s' %(user_info['data']['counts']['followed_by'])
            print 'Number of people you are following:%s' %(user_info['data']['counts']['follows'])
            print 'Number of posts:%s' %(user_info['data']['counts']['media'])
        else:
            print "User doesn\'t exist"
    else:
        print 'Status code other than 200 received'



def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received'
        exit()



def get_user_info(insta_username):
    user_id=get_user_id(insta_username)
    if user_id==None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

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



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code']==200:
        if len(own_media['data']):
            image_name=own_media['data'][0]['id']+ '.jpeg'
            print image_name
            image_url=own_media['data'][0]['images']['standard_resolution']['url']
            print image_url
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded'
            import webbrowser
            webbrowser.open(image_name)
            return own_media['data'][0]['id']
        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'



def get_users_post(insta_username):
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "User doesn\'t exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code']==200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            print image_name
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            print image_url
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded'
            import webbrowser
            webbrowser.open(image_name)
            return own_media['data'][0]['id']
        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'



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



def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code']==200:
        print 'Your like was successful'
    else:
        print 'Your like was unsuccessful'



def post_a_comment(insta_username):
    media_id=get_post_id(insta_username)
    comment_text=raw_input('Enter your text:')
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code']==200:
        print'Comment was successfully added'
    else:
        print 'Unable to comment'



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
                print'\t%s. from %s: %s' %(position,text['from']['username'],text['text'])
                position=position+1
        else:
            print'No comments found'
            return None

    else:
        print 'Status code other than 200 is received'
        exit()



def get_location(lat,lng):
    request_url=(BASE_URL + 'locations/search?lat=%s&lng=%s&access_token=%s') %(lat,lng,APP_ACCESS_TOKEN)
    print 'GET reques url: %s' %(request_url)
    user_location=requests.get(request_url).json()
    print user_location
    if user_location['meta']['code']==200:
        if len(user_location['data']):
            return user_location['data'][0]['id']
        else:
            print 'No location found'
            return None
    else:
        print 'Status code other than 200 received'
        exit()



def get_tags(tag_name):
    request_url = (BASE_URL + 'tags/search?q=%s&access_token=%s') % (tag_name, APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    associated_tag = requests.get(request_url).json()
    print associated_tag
    if associated_tag['meta']['code']==200:
        if len(associated_tag['data']):
            return associated_tag['data']
        else:
            print'No tags found'
            return None
    else:
        print 'Status code other than 200 is received'
        exit()



def get_tag_media(tag_name):
    if tag_name==None:
        print "No image exist"
        exit()
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag_name,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    tag_media = requests.get(request_url).json()

    if tag_media['meta']['code']==200:
        if len(tag_media['data']):
            image_name = tag_media['data'][0]['id'] + '.jpeg'
            print image_name
            image_url = tag_media['data'][0]['images']['standard_resolution']['url']
            print image_url
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded'
            import webbrowser
            webbrowser.open(image_name)
            return tag_media['data'][0]['id']
        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'



def self_liked_media():
    request_url = (BASE_URL + 'users/self/media/liked/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    liked_media = requests.get(request_url).json()

    if liked_media['meta']['code']==200:
        if len(liked_media['data']):
            rang=len(liked_media['data'])
            i=0
            for i in range(rang):
                print liked_media['data'][i]['images']['standard_resolution']['url']
            #image_name = liked_media['data'][0]['id'] + '.jpeg'
            #image_url = liked_media['data'][0]['images']['standard_resolution']['url']
            #urllib.urlretrieve(image_url, image_name)
            #print 'POST DOWNLOADED'
            #import webbrowser
            #webbrowser.open(image_name)
            #return liked_media['data'][0]['id']

        else:
            print "Post doesn\'t exist"
            return None
    else:
        print 'Status code other than 200 received'




def start_bot():
    print 'HEY! WELCOME TO INSTABOT'
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
                print '\t6.GET LOCATION'
                choice2=int(raw_input("Enter your choice:"))
                if choice2==1:
                   insta_username = raw_input("USERNAME:")
                   get_user_info(insta_username)
                elif choice==2:
                   insta_username = raw_input("USERNAME:")
                   get_users_post(insta_username)
                elif choice==3:
                   insta_username = raw_input("USERNAME:")
                   like_a_post(insta_username)
                elif choice==4:
                   insta_username = raw_input("USERNAME:")
                   post_a_comment(insta_username)
                elif choice==5:
                   insta_username = raw_input("USERNAME:")
                   get_comments(insta_username)
                elif choice==6:
                   lat=float(raw_input("Enter the latitude:"))
                   lng=float(raw_input("Enter the longitude"))
                   get_location(lat,lng)
                   print 'Tag names are:'
                   print '\ta.FLOOD\n\tb.EARTHQUAKE\n\tc.LANDSLIDE'
                   tag_name=raw_input("Enter the name of tag")
                   if tag_name=='flood' or tag_name=='a':
                     get_tags(tag_name)
                     get_tag_media(tag_name)
                   elif tag_name=='earthquake' or tag_name=='b':
                     get_tags(tag_name)
                     get_tag_media(tag_name)
                   elif tag_name=='landslide' or tag_name=='c':
                     get_tags(tag_name)
                     get_tag_media(tag_name)
                   else:
                     print 'Wrong input'
                else:
                    print 'INVALID ENTRY'
            elif choice=='f':
                print '\n\t*****HAVE A GOOD DAY******'
                exit()
            else:
                print 'WRONG CHOICE.PLEASE INPUT AGAIN'
        except ValueError:
            print 'PLEASE INPUT VALID NUMBER'

start_bot()





