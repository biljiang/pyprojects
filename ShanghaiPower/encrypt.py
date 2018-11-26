# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:35:36 2018

@author: Feng
"""
import json
import rsa
from binascii import b2a_hex, a2b_hex



class rsacrypt():
    def __init__(self, pubkey, prikey):
        self.pubkey = pubkey
        self.prikey = prikey

    def encrypt(self, text):
        self.ciphertext = rsa.encrypt(text.encode(), self.pubkey)
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), self.prikey)
        return decrypt_text
    
    
    
from Cryptodome.Cipher import AES

AES_LENGTH = 16

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB
        self.cryptor = AES.new(self.pad_key(self.key).encode(), self.mode)

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def pad(self,text):
        while len(text) % AES_LENGTH != 0:
            text += ' '
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def pad_key(self,key):
        while len(key) % AES_LENGTH != 0:
            key += ' '
        return key

    def encrypt(self, text):

        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        # 加密的字符需要转换为bytes
        # print(self.pad(text))
        self.ciphertext = self.cryptor.encrypt(self.pad(text).encode())
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

        # 解密后，去掉补足的空格用strip() 去掉

    def decrypt(self, text):
        plain_text = self.cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip(' ')


if __name__ == '__main__':
    
    pc = prpcrypt('abcdef')  # 初始化密钥
    e = pc.encrypt("0123456789ABCDEF")
    d = pc.decrypt(e)
    print(e.decode(), d)
    e = pc.encrypt("00000000000000000000000000")
    d = pc.decrypt(e)
    print(e.decode(), d) 
    
    pc_1 = prpcrypt('abcdef')
    
    d1=pc_1.decrypt(e)   
    print(e.decode(), d1)
    
    '''
    pubkey, prikey = rsa.newkeys(1024)
    with open('public.pem','w+') as f:
        f.write(pubkey.save_pkcs1().decode())

    with open('private.pem','w+') as f:
        f.write(prikey.save_pkcs1().decode())
    
    '''
    
    with open('public.pem','r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

    with open('private.pem','r') as f:
        prikey = rsa.PrivateKey.load_pkcs1(f.read().encode())    
    
    '''    
    rs_obj = rsacrypt(pubkey,prikey)
    text='hello'
    ency_text = rs_obj.encrypt(text)
    print(ency_text)
    print(rs_obj.decrypt(ency_text))
    '''
#    pubkey1, prikey1 = rsa.newkeys(256)
    rs_obj = rsacrypt(pubkey,prikey)
    text='The license will be expire on Dec 31, 2018'
    ency_text = rs_obj.encrypt(text)
    print(ency_text.decode())
    print(rs_obj.decrypt(ency_text).decode())
    

    lic = {'Company':'Shanghai Power',
           'Producer':'AVARUN.COM',
           'License Number':'avarun201800001',
           'Agreement file':'Attached',
           'Expiration':'2018-12-31'
           }
    
    lic_json_str = json.dumps(lic)

    # encrypt with RSA but need large n=2048 for nbit pool
    # pubkey, prikey = rsa.newkeys(2048)
    rs_obj = rsacrypt(pubkey,prikey)
    ency_text = rs_obj.encrypt(lic_json_str)
    print(ency_text.decode())
    print(rs_obj.decrypt(ency_text).decode())

    # encrypt with AES
    pc_1 = prpcrypt('bill228600')
    e = pc_1.encrypt(lic_json_str)    
    d1=pc_1.decrypt(e)   
    print(e.decode(), d1)



    with open('lic.json','w+') as f:
        json.dump(lic,f)
    
    with open('lic.cryp','w+') as f:
        f.write(ency_text.decode())

    with open('lic.json','r') as f:
        jsonlic=json.load(f)
        
    with open('lic.cryp','r') as f:
        lic_str=f.read()        
        
    r=rs_obj.decrypt(ency_text).decode()    

    lic_1 = json.loads(r)
