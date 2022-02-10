# -*- coding:utf-8 -*-
import string

class Enc:
    def __init__(self):
        pass
    
    def Base_10_to_n(self,X, n):
        if (int(X/n)):
            return self.Base_10_to_n(int(X/n), n)+str(X%n)
        return str(X%n)

    def Base_n_to_10(self,X,n):
        out = 0
        for i in range(1,len(str(X))+1):
            out += int(X[-i])*(n**(i-1))
        return out#int out

    def decrypt(self,keyword):
        keyword = keyword.replace(".","0").replace("b","1").replace("3","2")
        dec_line = ""
        for i in range(int(len(keyword)/5)):
            tmp_num =f"{keyword[i*5]}{keyword[i*5+1]}{keyword[i*5+2]}{keyword[i*5+3]}{keyword[i*5+4]}"
            tmp_num = self.Base_n_to_10(tmp_num,3) -13
            dec_line += string.printable[tmp_num]
        return dec_line

    def encode(self,keyword):
        enc_line = ""
        for i in range(len(keyword)):
            enc_line += str(self.Base_10_to_n((string.printable.find(keyword[i])+13), 3)).zfill(5)
        enc_line = enc_line.replace("0",".").replace("2","3").replace("1","b")
        return enc_line
