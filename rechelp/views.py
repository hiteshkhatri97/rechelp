from django.shortcuts import render, HttpResponse, redirect
from pymongo import MongoClient

def appliedStudentsTest(request):

    try:
        conn = MongoClient()
        print(conn)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # database
    db = conn.rechelp
    db=conn['rechelp']

    # Created or Switched to collection names: my_gfg_collection
    collection = db.post_post
    collection=db['post_post']

    
    
    result = collection.update_many(
        {"id": 1},
        {"$set": {"appliedStudents": ['1519bece30060']},}
    )


    result1 = collection.find({"id": 1}, {"appliedStudents": 1})
    
    
    newStudent = '1519bece30038'
    newList=[]
    # Print the new record
    cursor = collection.find()
    for record in result1:
        newList = record['appliedStudents']
    print('nl',newList)
    newList.append(newStudent)
    print('nl',newList)
    result = collection.update_many(
        {"id": 1},
        {"$set": {"appliedStudents": newList}, }
    )

    return HttpResponse("<p>" +str(result1)+"</p>")

def index(request):
    if request.user.is_authenticated:
        if request.user.userType == 'company':
            return redirect('company/')
        if request.user.userType == 'student':
            return redirect('student/')
    return render(request, 'index.html')
