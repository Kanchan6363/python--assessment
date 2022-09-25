# Social Media app

## About
 - The Social Media app project can be used by people to connect with other people, where they can follow other people to connect and unfollow then to disconnect. 
 - Users also can add a post to share their status , delete a post.
 - Different users can like other users posts, dislike the post and can add comment on the post as well 
 - User can check their user profile
 - User can list their all posts as well    

## Features
 - Different features to check their posts, followers, followings on a single click.  
 - App can be managed using the API endpoints.
 - Simple and Modular Design

## Thoughts
 - Implemented all the endpoints in as simple way as possible by keeping in mind that the response time is lowest.
 - To have consistency and ease of handling data used the `Postgresql` Database.
 - Tried to cover as much as test edge cases possible.
 - Tried to implement all the functions with minimal use of library.
 - Added primary key constraint to avoid Duplicacy in data.
 - To get the export of Database -> `pg_dump -U postgres postgres > reunion.sql`
  