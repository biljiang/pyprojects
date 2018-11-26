# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 09:12:42 2018

@author: Feng
"""
from datetime import datetime,time
import threading
import time as tm



#继承Thread类，创建自定义线程类

class mythread(threading.Thread):

    def __init__(self, num, threadname):
        threading.Thread.__init__(self, name=threadname)
        self.num = num

    #重写run()方法

    def run(self):
        tm.sleep(self.num)
        print(self.num)


class mythread_1(threading.Thread):

    def __init__(self, num, threadname,end_time):
        threading.Thread.__init__(self, name=threadname)
        self.num = num
        self.endtime = end_time
        
    def run(self):
        while datetime.now().time() < self.endtime:
            tm.sleep(self.num)
            print(datetime.now())
        

if __name__ == "__main__":

    t1 = mythread(3, 't1')
    t2 = mythread(5, 't2')

    t2.daemon = True #
#如果某个子线程的daemon属性为False，主线程结束时会检测该子线程是否结束，如果该子线程还在运行，则主线程会等待它完成后再退出；
#如果某个子线程的daemon属性为True，主线程运行结束时不对这个子线程进行检查而直接退出，同时所有daemon值为True的子线程将随主线程一起结束，而不论是否运行完成

    #t1.start()
    #t1.join()

    #t2.start()
    #t2.join()
       
    t3 = mythread_1(5,"t3",time(11,43,30))
    #t3.daemon = True

    t3.start()        
    #t3.join()     
        
