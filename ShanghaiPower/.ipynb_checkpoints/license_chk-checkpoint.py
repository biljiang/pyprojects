# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 20:39:25 2018

@author: Feng
"""

from datetime import datetime

import urllib3
import certifi
#urllib3.disable_warnings()

def license_check():
    try: 
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        r = http.request('GET', 
                     'https://avarun.cn/static/license/ShangHaiAdressVerification/expirationdate.txt')
        if r.status==200:
            Ex_time=datetime.strptime(r.data.decode(),'%Y-%m-%d %H:%M:%S\n')
            if datetime.now()<Ex_time:
                return("your license status is good!")
            else:
                return("your license is expired!")
                
        else:
            return("fail to get license file.")
    except:
        return("Network error.")


if __name__=='__main__':
   print (license_check())
    
