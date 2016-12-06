#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import subprocess
import shutil
import time
import os
__author__ = 'jkk'

back_not_used_dir = "not_use"
auto_delete = 0
auto_move = 1

def do_find_command(search_dir,file_type):

    if len(search_dir) == 0 or len(file_type) == 0:
        return set()

    search_dir = search_dir.replace('\n','')
    print('search_dir:%s' % search_dir)
    all_names_set = set()
    command = "dir \"{}\" /b/s | findstr \"\<*.{other}\>\"".format(search_dir,other = file_type)
    print('command:%s' % command)
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = s.communicate()[0].split()
    for name in results:

        if not name.endswith(file_type):
            continue

        head, tail = os.path.split(name)
        tail = os.path.splitext(tail)[0]
        
        if "@" in tail:
            all_names_set.add(tail.split('@')[0])
        else:
            all_names_set.add(tail)

    return all_names_set

def do_grep(path,key_word):

    if not is_available_file_path(path):
        print ('path:%s is not available' % path)
        return

    command = "find \"%s![a-zA-Z]\" %s" %(key_word,path)
    if subprocess.call(command, shell=False) == 0:
        return 1
    else:
        return 0

def goal_file(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
                                    for fname in fileList:
                                            if is_available_file_path(fname):
                                                path = '%s/%s' % (dirName,fname)
                                                files.append(path)
    return files

def is_available_file_path(path):
    available = 0

    if path.endswith('.m'):
       available = 1
    if path.endswith('.h'):
       available = 1
    if path.endswith('.lua'):
        available = 1
    if path.endswith('.json'):
        available = 1
    if path.endswith('.xml'):
        available = 1

    return available

def support_types():
    types = []
    types.append('png')
    types.append('jpg')
    #types.append('jpeg')
    #types.append('gif')
    return types

def delete_not_used_image(image):
    if len(image) == 0:
        return

    command = "dir \"{}\" /b/s | findstr \"\<{other}\>\"".format(res_dir,other = image)
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = s.communicate()[0].split()
    for path in results:

        valid = 0
        for type in support_types():
            if path.endswith(type):
                valid = 1
                break
        if valid:
            os.remove(path)
            print ('\r\n ========%s is deleted========' % image)

def move_not_used_image(image):
    if len(image) == 0:
        return
    
    command =  "dir \"{}\" /b/s | findstr \"\<{other}\>\"".format(res_dir,other = image)
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = s.communicate()[0].split()
    for path in results:
        valid = 0
        for type in support_types():
            if path.endswith(type):
                valid = 1
                break
        if valid:
            filename, file_extension = os.path.splitext(path)
            des_dir = os.path.join(back_not_used_dir,"{}{}".format(image,file_extension))
            shutil.move(path,des_dir)
            print ('\r\n ========%s is moved========' % image)

def start_find_task():
    print("\nstart finding task...\nbelows are not used images:\n")
    global project_dir
    global res_dir
    if len(sys.argv) > 2:
        project_dir = sys.argv[1]
        res_dir = sys.argv[2]
    else:
        project_dir = "E:\\sprite\\mobile\\client\\KouDai_LUA\\win32\\Debug.win32\\Lua\\ui"
        res_dir = os.path.join(os.getcwd(),"GUI")

    start = time.time()
    i = 0

    results = set()
    for type in support_types():
        results = results | do_find_command(res_dir,type)

    #goal_files = list(set(goal_file(project_dir)).union(set(goal_file(res_dir))) )
    goal_files = goal_file(project_dir)
    
    if auto_move:
        path_to_move = os.path.join(".",back_not_used_dir)
        if os.path.exists(path_to_move):
            print('path_to_move is exit:')
        else:
            os.makedirs(path_to_move)
            
    for image_name in results:
        used = 0
        for file_path in goal_files:
            if do_grep(file_path,image_name):
                used = 1
                break
        
        if used == 0:
            print(image_name)
            i = i + 1
            if auto_delete:
                delete_not_used_image(image_name)
            elif auto_move:
                move_not_used_image(image_name)





    c = time.time() - start
    print('\nsearch finish,find %s results,total count %0.2f s'%(i,c))

start_find_task()