from datetime import datetime
import psycopg2

class Authenticate:
     
     # To authenticate a user
    def check(self,emails,password):
        cur.execute('SELECT * FROM users')
        for record in cur.fetchall():
            if emails == record[1]:
                if password == record[2]:
                    socialobj = Social(emails,password)
                    ans1 = int(input(" 1. To follow \n 2. To unfollow \n 3. Check Profile\n 4. Add post \n 5. delete post \n 6. Check post\n 7. Like post \n 8. Dislike post \n 9. comment post \n 10.List All post \n"))
                    if ans1 == 1:
                        id = input("enter user id\n")
                        print(socialobj.follow(id))
                    elif ans1 == 2:
                        id = input("enter user id\n") 
                        socialobj.unfollow(id)
                    elif ans1 == 3:
                        socialobj.user()
                    elif ans1 == 4:
                        title = input("enter title\n")
                        description = input("enter description\n")
                        print(socialobj.add_post(title,description))   
                    elif ans1 == 5:
                        postid = input("enter user post id\n")
                        socialobj.delete_post(postid) 
                    elif ans1 == 6:
                        post_id = input("enter user post id\n")
                        socialobj.describe_post(post_id) 
                    elif ans1 == 7:
                        postid = input("enter user post id\n")
                        socialobj.like_post(postid)
                    elif ans1 == 8:
                        post_id = input("enter user post id\n")
                        socialobj.dislike_post(post_id)    
                    elif ans1 == 9:
                        post_id = input("enter user post id\n")
                        comment = input("enter comment")
                        print(socialobj.comment_post(post_id,comment))  

                    elif ans1 == 10:
                        socialobj.list_post() 
                    else:
                        print("enter valid option") 
                    break      
                else:
                    print("password doesn't match") 
            else:
                print("user doesn't exist")
#------------------------------------------------------------------------------------------------------------

class Social:
    
    def __init__(self,emails,password):
        self.emails = emails
        self.password = password
    
    #To follow a user
    def follow(self,user_id):
        try:  
            #Creating following table to keep the records of people user following 
            create_script = """CREATE TABLE IF NOT EXISTS Following(
                    user_email varchar(200),
                    Following_id varchar(200))""" 
            cur.execute(create_script)        
            cur.execute('SELECT * from following')

            #checking if user already followed particular requested id
            for row in cur.fetchall():
                if row[0] == self.emails:
                    if row[1] == user_id:
                        return 'already followed'   

            #if not following then updating followers and following                                        
            update_script = 'UPDATE users SET followers = followers + 1 WHERE id = %s'
            update_value = (user_id,)
            cur.execute(update_script,update_value)
            update_script1 = 'UPDATE users SET following = following + 1 WHERE email = %s'
            update_value1 = (self.emails,)
            cur.execute(update_script1,update_value1)
            
            #updated the list of followings of user
            insert_script = 'INSERT INTO Following(user_email,Following_id) Values(%s,%s)'
            insert_value = (self.emails,user_id,)    
            cur.execute(insert_script,insert_value)
            conn.commit()
        except Exception as e:
            print('not able to follow')                   

    #To unfollow a user
    def unfollow(self,user_id): 
        try:           
            #checking if user already followed or not if yes then only user can unfollow
            follower=0
            followin=0
            cur.execute('SELECT * from following')
            for row in cur.fetchall():
                if row[0] == self.emails:
                    if row[1] == user_id:
                        cur.execute('SELECT * from users')
                        for record in cur.fetchall():
                            if record[0] == user_id:
                                follower = record[4]
                            if record[1] == self.emails:
                                followin = record[5] 

                        # to check if followers are 1 or less than one assign it to 0 else decrease value      
                        if follower <= 1:
                            update_script = 'UPDATE users SET followers = 0 WHERE id=%s'
                            update_value = (user_id,)
                            cur.execute(update_script,update_value)
                        else:
                            update_script = 'UPDATE users SET followers = followers -1  WHERE id=%s'
                            update_value = (user_id,)
                            cur.execute(update_script,update_value) 
                        if followin <= 1:
                             update_script1 = 'UPDATE users SET following = 0 WHERE email=%s'
                             update_value1 = (self.emails,)
                             cur.execute(update_script1,update_value1) 
                        else:           
                             update_script1 = 'UPDATE users SET following = following - 1 WHERE email=%s'
                             update_value1 = (self.emails,)
                             cur.execute(update_script1,update_value1) 
                        delete_script = 'DELETE FROM following WHERE user_email = %s and following_id = %s'
                        delete_value = (self.emails,user_id,) 
                        cur.execute(delete_script,delete_value) 
                        conn.commit()
                else:
                    print('you must follow first')        
        except Exception as e:
            print(e)  

    # To show the user profile 
    def user(self):
        try:  
            cur.execute('SELECT * from users')
            for row in cur.fetchall():
                if row[1] == self.emails:
                    print("Name : {0} Followers : {1} Following : {2}".format(row[3],row[4],row[5]))       
        except Exception as e:
            print("Not able to show profile")          

    #To add a post
    def add_post(self,title,description):
        #to add post
        try:  
            create_time = datetime.now()
            post = title[0:5].join(description[0:5])
            # To keep post details
            create_script1 = """CREATE TABLE IF NOT EXISTS Posts(
                    post_id varchar(200) PRIMARY KEY,
                    Title varchar(200),
                    Description varchar(200),
                    create_time  varchar(100),
                    likes int,
                    dislikes int,
                    comment varchar(100))""" 
            cur.execute(create_script1)

            # To keep post details and details of user who created
            create_script2 = """CREATE TABLE IF NOT EXISTS PostsUsers(
                    user_email varchar(100),
                    post_id varchar(200))""" 
            cur.execute(create_script2)
            insert_script = 'INSERT INTO Posts(post_id,Title,Description,create_time,likes,dislikes,comment) Values(%s,%s,%s,%s,%s,%s,%s)'
            insert_script1 = 'INSERT INTO PostsUsers(user_email,post_id) Values(%s,%s)'
            insert_value =  (post,title,description,create_time,0,0,'None') 
            insert_value1 = (self.emails,post,)

            cur.execute(insert_script,insert_value)
            cur.execute(insert_script1,insert_value1)
            conn.commit()
            cur.execute('SELECT * from Posts')
            for row in cur.fetchall():
                if row[0] == post:
                    return "Post_id : {0}, Title : {1}, Description : {2}, Creation_Time : {3}".format(row[0],row[1],row[2],row[3])

        except Exception as e:
            print(e)  

    #To delete a post
    def delete_post(self,postid):
        try:
            #To check if user who is deleting the post is the actual owner of post or not.
            cur.execute('SELECT * from PostsUsers')
            for row in cur.fetchall():
                if row[0] == self.emails:
                    if row[1] == postid:
                        delete_script = 'DELETE FROM PostsUsers WHERE user_email = %s and post_id = %s'
                        delete_value = (self.emails,postid,) 
                        cur.execute(delete_script,delete_value) 
                        delete_script1 = 'DELETE FROM Posts WHERE post_id = %s'
                        delete_value1 = (postid,) 
                        cur.execute(delete_script1,delete_value1)
                        conn.commit()       
        except Exception as e:
            print("posts doesn't exist")  

    #To like a post 
    def like_post(self,postid):
        try:
            #To check if user already liked or not
            #IF already liked it will end
            #if already disliked it convert into like and change number of likes and dislikes
            # IF nothing done already it will like and create status in database
            create_script2 = """CREATE TABLE IF NOT EXISTS likestatus(
                    user_email varchar(100),
                    post_id varchar(200),
                    status varchar(10))""" 
            cur.execute(create_script2)
            cur.execute('select * from likestatus')
            for row in cur.fetchall():
                if row[0] == self.emails:
                    if row[1] == postid:
                        if row[2] == 'l':
                            print('already liked')
                            return  
                        elif row[2] == 'u': 
                            update_script = 'UPDATE Posts SET likes = likes + 1 WHERE post_id = %s'
                            update_value = (postid,)
                            cur.execute(update_script,update_value)
                            update_script1 = 'UPDATE Posts SET dislikes = dislikes - 1 WHERE post_id = %s'
                            update_value1 = (postid,)
                            cur.execute(update_script1,update_value1) 
                            update_script1 =  'UPDATE likestatus SET status = %s WHERE user_email = %s and post_id = %s'
                            update_value = ('l',self.emails,postid,)
                            conn.commit()
                            return 
                    else:
                        self.like_exten(postid) 
                        return            
                else:
                    self.like_exten(postid)
                    return  
            
            self.like_exten(postid)                      
            conn.commit()
        except Exception as e:
            print("post doesn't exist")    

    #EXtension of like_post method
    def like_exten(self,postid):
        insert_script = 'INSERT into likestatus(user_email,post_id,status) Values(%s,%s,%s)'
        insert_value = (self.emails,postid,'l')  
        cur.execute(insert_script,insert_value) 
        update_script = 'UPDATE Posts SET likes = likes + 1 WHERE post_id = %s'
        update_value = (postid,)
        cur.execute(update_script,update_value)
        conn.commit()

    #To dislike a post
    def dislike_post(self,postid):
        try: 
             #To check if user already disliked or not
            #IF already disliked it will end
            #if already liked it convert into dislike and change number of likes and dislikes
            # IF nothing done already it will dislike and create status in database
            number_dislike = 0
            cur.execute('select * from likestatus')
            for row in cur.fetchall():
                if row[0] == self.emails:
                    if row[1] == postid: 
                        if row[2] == 'u':
                            print('already unliked')
                            return 
                        elif row[2] == 'l':
                            update_script = 'UPDATE Posts SET dislikes = dislikes + 1 WHERE post_id = %s'
                            update_value = (postid,)
                            cur.execute(update_script,update_value)
                            update_script1 = 'UPDATE Posts SET likes = likes - 1 WHERE post_id = %s'
                            update_value1 = (postid,)
                            cur.execute(update_script1,update_value1)
                            update_script1 =  'UPDATE likestatus SET status = %s WHERE user_email = %s and post_id = %s'
                            update_value = ('u',self.emails,postid,)
                            conn.commit()
                            return
                    else:
                        self.dislike_exten(postid) 
                        return            
                else:
                    self.dislike_exten(postid)
                    return  
            
            self.dislike_exten(postid)                      
            conn.commit()  

        except Exception as e:
            print("Not able to dislike")

    #EXtension of dislike_post method
    def dislike_exten(self,postid):
        insert_script = 'INSERT into likestatus(user_email,post_id,status) Values(%s,%s,%s)'
        insert_value = (self.emails,postid,'u')  
        cur.execute(insert_script,insert_value) 
        update_script = 'UPDATE Posts SET dislikes = dislikes + 1 WHERE post_id = %s'
        update_value = (postid,)
        cur.execute(update_script,update_value)
        conn.commit()


    #To comment on a post 
    def comment_post(self,postid,comments):
        try:
            #To add comment in post and return comment id
            comment_id = postid[0:2].join(comments[0:5])
            update_script = 'UPDATE Posts SET comment = %s WHERE post_id = %s'
            update_value = (comments,postid,)
            cur.execute(update_script,update_value)

            #To keep record of post and comment with comment id
            create_script = """CREATE TABLE IF NOT EXISTS comment(
                    post_id varchar(200),
                    comment_id varchar(200),
                    comment varchar(200) )""" 
            cur.execute(create_script)
            insert_script = 'INSERT INTO comment(post_id,comment_id,comment) Values(%s,%s,%s)'
            insert_value = (postid,comment_id,comments,)
            cur.execute(insert_script,insert_value)
            conn.commit()
            return comment_id
        except Exception as e:
            print('Not able to comment')


    #To check particular post
    def describe_post(self,postid):
        try:
            cur.execute('SELECT * from Posts')
            for row in cur.fetchall():
                if row[0] == postid:
                    print("Title : {0}, Description : {1}, Likes : {2}, Dislikes : {3}".format(row[1],row[2],row[4],row[5]))
        except Exception as e:
            print("Not able to check posts")        
        

    #To check all the post created by user
    def list_post(self): 
        try:
            lis = []   
            cur.execute('SELECT * FROM PostsUsers')
            for record in cur.fetchall():
                if record[0] == self.emails:
                    lis.append(record[1])         
        
            for i in lis:
                cur.execute('SELECT * FROM Posts')
                for row in cur.fetchall(): 
                    if i == row[0]:
                        print("Title : {0}, Description : {1}, Likes : {2}, Dislikes : {3}".format(row[1],row[2],row[4],row[5])) 
        except Exception as e:
            print('Not able to check posts')                   
                   

#------------------------------------------------------------------------------------------------------------                  
#To connect database
def connect_db():
    global conn,cur 
    conn = psycopg2.connect(
             host = hostname,
             dbname = database,
             user = username,
             password = pwd,
             port = port_id)
    cur = conn.cursor()
def main():
    connect_db()
    email = input("enter email to login \n")
    password = input("enter password \n")
    user1 = Authenticate()
    user1.check(email,password)
    
hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 'admin'
port_id = 5432


try: 
    if __name__ == "__main__":
        main()  
except Exception as e:
    print(e)
finally:
    if cur:
        cur.close()
    if conn:
        conn.close() 