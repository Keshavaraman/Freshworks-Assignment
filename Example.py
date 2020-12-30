from threading import Thread
import DB as y
x=y.K("json")
#x is an object of k class
x.create("Ram",25)
#it will create an key-value pair
a={"kesh":2,"san":3}
x.create("raman",a,3600)
#it will create a key-value pair where here value is an another dict
x.read("raman")
x.create("raman",26)
#it will throw an error as it was already Existing
x.create("java",50)
#it will create another key-value pair
x.modify("java",55)

#it will modify the value of java key
x.delete("java")
#it will delete  the key -value pair

#thread is used for parallel proccesing
t1=Thread(target= x.delete,args=("java",))
t1.start()
t2=Thread(target= x.read,args=("java",))
t2.start()

x.readc()
#It will read the entire data

#output of this example with synchronized
'''
raman:{'kesh': 2, 'san': 3}
error: this key already exists
key is successfully deleted
error: given key does not exist in database. Please enter a valid key
error: given key does not exist in database. Please enter a valid key
Ram:25
raman:{'kesh': 2, 'san': 3}
file size:70bytes
[Finished in 1.458s]
'''

#otuput of this program without synchronized
'''
raman:{'kesh': 2, 'san': 3}
error: this key already exists
key is successfully deleted
error: given key does not exist in database. Please enter a valid key
Ram:25
raman:{'kesh': 2, 'san': 3}
file size:70bytes
error: given key does not exist in database. Please enter a valid key
[Finished in 1.469s]
'''
