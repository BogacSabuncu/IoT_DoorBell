#!/usr/bin/env python
import github

def uploadImage():
    g = github.Github("danieloved", "aepooy11")

    user = g.get_user()
    repo = user.get_repo("DoorBellLabs")
    file = repo.get_file_contents("latest.jpg")

    #get image binary
    pic = open('image_with_boxes.jpg','rb')
    jpgData = pic.read()
    
    # update image on github
    repo.update_file("/latest.jpg", "Most recent face recognition image", jpgData, file.sha)
    print("Updated github file")
    pic.close()
uploadImage()