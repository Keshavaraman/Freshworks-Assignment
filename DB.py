from threading import Lock
import time
import sys
import json
import pickle
import os
class K:
 def __init__(self,file_name="myfile"):
     self.lock = Lock()
     self.data={}
     self.file=file_name+".txt"
     open(self.file, "a").close()

#data is place where we are going to store data in json formate
#lock is used synchronization of data



#--------------------------------------------CREATE---------------------------------------------------------



#create method is used to add key-value  in data
 def create(self,key,value,timeout=0):
#lock.acuire() is used the lock the data within the function.
     self.lock.acquire()
     with open(self.file) as f:
         if(os.stat(self.file).st_size != 0):
          dataq = f.read()
          self.data= json.loads(dataq)



# first we check the data is present already or not if it presnt means an error message will pop
     if key in self.data:
         print("error: this key already exists")

     else:
#condition check for key data formate
         if(key.isalpha()):
#condition check for size of data and value size-------- size of data <=1GB    and  value size <=16KB
             if os.stat(self.file).st_size<=(1024*1024*1024) and sys.getsizeof(value)<=(16*1024):
                 if timeout==0:
                     l=[value,timeout]
                 else:
                     l=[value,time.time()+timeout]
#memory check for key
                 if len(key)<=32:
                     self.data[key]=l
             else:
                 print("error: Memory limit exceeded!! ")
         else:
             print("error: Invalind key_name!! key_name must contain only alphabets and no special characters or numbers")

     with open(self.file, 'w') as json_file:
         json.dump(self.data, json_file)
#lock.release() is a method used to release the data
     self.lock.release()


#------------------------------------------------READC-------------------------------------------------------------


#readc() method used to read the data completely
 def readc(self):
     self.lock.acquire()
     with open(self.file) as f:
         if(os.stat(self.file).st_size != 0):
          dataq = f.read()
          self.data= json.loads(dataq)

     for a in self.data:
      if(self.data[a][1]==0 or self.data[a][1]>time.time()):
       print(a+":"+str(self.data[a][0]))
     print("file size :"+str(os.stat(self.file).st_size)+"bytes")
     self.lock.release()



#------------------------------------------------READ-------------------------------------------------------------

#read() methods is used read the element of data using the key value

 def read(self,key):
     self.lock.acquire()
#if key is not present in data it will throw an error
     with open(self.file) as f:
         if(os.stat(self.file).st_size != 0):
          dataq = f.read()
          self.data= json.loads(dataq)

     if key not in self.data:
         print("error: given key does not exist in database. Please enter a valid key")
     else:
         self.b=self.data[key]

#it check for time constrain (Time to live property)
         if self.b[1]!=0:
             if time.time()<self.b[1]:
                 stri=str(key)+":"+str(self.b[0])
                 print(stri)
             else:
                 print("error: time-to-live of",key,"has expired")
         else:
             stri=str(key)+":"+str(self.b[0])
             print(stri)
    self.lock.release()


#-------------------------------------DELETE---------------------------------------------------------------------------


#delete() used to delete the element in the data using key name
 def delete(self,key):
     self.lock.acquire()
     with open(self.file) as f:
         if(os.stat(self.file).st_size != 0):
          dataq = f.read()
          self.data= json.loads(dataq)

     time.sleep(0.5)#-----------------------used for testing lock functions
#first check for the availability of the data if the key is not present then it will throw an error
     if key not in self.data:
         print("error: given key does not exist in database. Please enter a valid key")
     else:
         self.b=self.data[key]
         if self.b[1]!=0:
            if time.time()<self.b[1]:
#del method is used to delete an element from data
                del self.data[key]
                print("key is successfully deleted")
            else:
                print("error: time-to-live of",key,"has expired")
         else:
            del self.data[key]

            print("key is successfully deleted")
     with open(self.file, 'w') as json_file:
         json.dump(self.data, json_file)
     self.lock.release()



#----------------------------------------------MODIFY--------------------------------------------------------

#modify data is used to change the the value of the key
 def modify(self,key,value):
     with open(self.file) as f:
         if(os.stat(self.file).st_size != 0):
          dataq = f.read()
          self.data= json.loads(dataq)

     self.lock.acquire()
     self.b=self.data[key]
     if self.b[1]!=0:
         if time.time()<self.b[1]:
             if key not in self.data:
                 print("error: given key does not exist in database. Please enter a valid key")
             else:
                 self.l=[]
                 self.l.append(value)
                 self.l.append(self.b[1])
                 self.data[key]=self.l
         else:
             print("error: time-to-live of",key,"has expired")
     else:
         if key not in self.data:
             print("error: given key does not exist in database. Please enter a valid key")
         else:
             self.l=[]
             self.l.append(value)
             self.l.append(self.b[1])
             self.data[key]=self.l
     with open(self.file, 'w') as json_file:
         json.dump(self.data, json_file)
     self.lock.release()
#In these method lock.acquire and lock.release method is used to achieve Thread safety
