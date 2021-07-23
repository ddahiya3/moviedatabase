import random
from app import db

# def check_login_details(uname, pwd): # 1 for correct, 0 for wrong
#     if uname == "admin" and pwd == "admin" :
#         return True
#     else :
#         return False

def fake_movies() :
    movies = [{'name' : ' Avatar', 'idx' : '1'}, {'name' : 'Batman', 'idx' : '2'}]
    return movies

def check_login_details(uname, pwd): # 1 for correct, 0 for wrong
    conn = db.connect()
    query = f'select COUNT(Username) from USER WHERE Username = "{uname}" AND Password = "{pwd}";'
    exists = conn.execute(query).fetchall()
    conn.close()
    if exists[0][0] == 1 :
        return True
    return False

def add_new_user(uname, pwd):
    conn = db.connect()
    query = f'insert into USER values ("{uname}", "{pwd}");'
    conn.execute(query)
    conn.close()
    return

def check_existing_user(uname):
    conn = db.connect()
    query = f'select COUNT(Username) from USER WHERE Username = "{uname}";'
    exists = conn.execute(query).fetchall()
    conn.close()
    if exists[0][0] == 1 :
        return True
    return False

def advanced_query_1(first_director_letter, second_director_letter):
    conn = db.connect()
    query = f'(SELECT Title, Directors FROM MOVIE m NATURAL JOIN CREW c WHERE Directors LIKE "{first_director_letter}%%") UNION (SELECT Title, Directors FROM MOVIE m NATURAL JOIN CREW c WHERE Directors LIKE "{second_director_letter}%%") ORDER BY Title DESC;'
    # print(query)
    results = conn.execute(query).fetchall()
    # print(results)
    conn.close()
    return results

def advanced_query_2(director_name):
    conn = db.connect()
    query = f'SELECT M.Title, C.Directors, M.Runtime FROM MOVIE M  NATURAL JOIN CREW C WHERE C.Directors LIKE "{director_name}%%" AND M.Runtime >= ALL (SELECT M2.Runtime FROM MOVIE M2 NATURAL JOIN CREW C2 WHERE C.Directors = C2.Directors);'
    # print(query)
    results = conn.execute(query).fetchall()
    # print(results)
    conn.close()
    return results

def user_ratings(uname):
    conn = db.connect()
    query = f'select Title, Score from RATING where Username = "{uname}";'
    ratings = conn.execute(query).fetchall()
    conn.close()
    return ratings

def delete_rating_query(uname, moviename):
    conn = db.connect()
    query = f'delete from RATING where Username = "{uname}" AND Title = "{moviename}";'
    conn.execute(query)
    conn.close()
    return

def update_rating_query(uname, moviename, new_score):
    conn = db.connect()
    query = f'update RATING SET Score = {new_score} WHERE Username = "{uname}" AND Title = "{moviename}";'
    conn.execute(query)
    conn.close()
    return

#TODO: error handling for add new user
#TODO: remove all prints
#TODO: error handling for all querries

