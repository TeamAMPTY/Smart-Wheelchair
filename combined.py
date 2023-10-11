
# importing the sys module
import sys    
import subprocess
# import os  
from server import MyServer
# os.system('python yolo-vid.py')
# print('combined.py is running')

# MyServer.connect()


# print('combined.py is finished ............')

# appending the directory of mod.py 
# in the sys.path list
# sys.path.append('D:\Hackathon-Coer\Object-Detection-on-images-using-YOLO\server.py')        
 
# now we can import mod
# import server
 
# calling the hello function of mod.py
# main.py
import multiprocessing

def run_file(file):
    subprocess.run(f'python {file}', shell=True, check=False)

if __name__ == '__main__':
    files = ['yolo-vid.py', 'server.py']
    with multiprocessing.Pool() as pool:
        pool.map(run_file, files)

