import random

def check_login_details(uname, pwd): # 1 for correct, 0 for wrong
    if uname == "admin" and pwd == "admin" :
        return 1
    else :
        return 0

def fake_movies() :
    movies = [{'name' : ' Avatar', 'idx' : '1'}, {'name' : 'Batman', 'idx' : '2'}]
    return movies