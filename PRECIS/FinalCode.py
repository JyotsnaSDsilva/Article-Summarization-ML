import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import precisToFb

#firebase auth / db reference
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://your-database-link.firebaseio.com'})
root = db.reference('Requests')

stream_count =0

def update_db(Uniquekey,summary): #update the database with summerized content

    if(Uniquekey and summary):
        Requests_ref = root.child(Uniquekey)
        Requests_ref.update({'summaryText': summary})
        return 1

    return 0

def listener(event): #stream handler : invoked whenever changes to the database is detected
    global stream_count 
    stream_count +=1

    event_type_str = event.event_type # put or patch
    path_str = event.path #path to stored data

    print("---Changes Detected---",stream_count)  
  
    if stream_count > 1: #ignores the first time its called since it takes all existing data
        new_request = []
        for key,val in event.data.items():
            new_request.append(key) #store the keys and values in a list to process it later
            new_request.append(val)
            print('\n {0} => {1}'.format(key,val)) #display updated data
    
        #print("New request  : " ,new_request)

        x = new_request[1] in 'Processing' # if not summerized -- returns true

        #send the url to summerize only if its a new request with summer as 'Processing' and url
        if len(new_request) > 2 and x: 
            url_to_summerize = new_request[3] #retrieve the link to be summerized 
            print(" \n This has to be summerized : ",url_to_summerize)
            #summerize
            summerized_content = precisToFb.Process_url(url_to_summerize) #process the url : web scraping
            status = update_db(path_str.strip("/"),summerized_content) #update the database

            if status:
                print(" \n Updation Successful. Response sent \n")

        time.sleep(10)

firebase_admin.db.reference('Requests').listen(listener) #database stream