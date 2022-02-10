# -*- coding:utf-8 -*-
from .encfunc import Enc
import os
import sys
import pandas as pd
import chardet
from getpass import getpass
from datetime import datetime as dt
from github import Github as gh

class Use_github(object):
    def __init__(self,*args,**kwargs):
        os.makedirs("data",exist_ok=True)
        enc = Enc()
        if 'token' in kwargs:
            token = kwargs['token']
        elif 'enc_token' in kwargs:
            token = enc.decrypt(kwargs['token'])
        else:
            if os.path.exists(r"data\token_key"):
                with open(r"data\token_key",mode="r") as f:
                    tmp_txt = f.read()
                token = enc.decrypt(tmp_txt)
            else:
                token = getpass("Please input GITHUB TOKEN:")
                with open(fr"data\token_key",mode="w") as f:
                    tmp_key = enc.encode(token)
                    f.write(tmp_key)
        self.enc_token = enc.encode(token)
        self.g = gh(token)
        self.target_organization = self.get_target_organization()
    
    def set_org(
        self,
        oname:str
    ):
        self.oname = oname
        try:
            self.org = self.g.get_organization(oname)
        except Exception as e:
            print("Please check an organization's name")
            print(e)
            raise Exception
    
    def set_repo(
        self,
        repository_path:str
    ):
        self.repository_path = repository_path
        try:
            self.repo = self.g.get_repo(repository_path)
        except Exception as e:
            print("Please check an organization's name")
            print(e)
            raise Exception
    
    def get_target_organization(
        self,
        target_organization_csv:str = "target_organization.csv"
    ):
        return_list = []
        if os.path.exists(target_organization_csv):
            with open(target_organization_csv,mode="r") as f:
                tmp_txt = f.read()
            target_organization = tmp_txt.replace(" ","").split("\n")
        else:
            with open(target_organization_csv,mode="w") as f:
                f.write("")
            print(f"Please input Organization name to {target_organization_csv}")
            sys.exit()
        for i in target_organization:
            if len(i)!=0:
                return_list.append(i)
        return return_list
    
    def add_update_file(
        self,
        filepath:str,
        target_name:str,
        repository_path:str = "",
        encoding:str = "_"
    ):
        try:
            repository_path = self.repository_path
        except:
            if repository_path != "":
                self.repo = self.g.get_repo(repository_path)
            else:
                print("please use a module 'set_repo'")
                print("set_repo(cls,repository_path,**kwargs)")
                raise Exception
        if os.path.exists(target_name)==False:
            print(f"There is no file {target_name}")
            raise Exception
        if os.path.isfile(target_name)==False:
            print(f"This is a directory: {target_name}")
            return 0
        with open(target_name,mode="rb") as f:
            tmp_cont = f.read()
        encode = chardet.detect(tmp_cont)
        encode = encode['encoding']
        if encoding != "_":
            encode = encoding
        with open(target_name,mode="r",encoding=encode) as f:
            content = f.read()
        filename_to_comment = filepath.replace("\\","_")
        try:
            cont = self.repo.get_dir_contents(filepath)
            self.repo.update_file(filepath,f"[API]Update:{filename_to_comment}",content,cont.sha)
            os.remove(target_name)
        except Exception as e:
            try:
                self.repo.create_file(filepath,f"[API]Create:{filename_to_comment}",content)
                os.remove(target_name)
            except Exception as e:
                print(f"repository_path: {repository_path}  / filepath : {filepath} / target_name : {target_name}")
                print(e)
                raise Exception
        return 1
    
    def delete_file(
        self,
        filepath:str
    ):
        try:
            repository_path = self.repository_path
        except:
            print("please use a module 'set_repo'")
            print("set_repo(cls,repository_path,**kwargs)")
            raise Exception
        cont = self.repo.get_dir_contents(filepath)
        self.repo.delete_file(filepath,"[API]DeleteLogFile",cont.sha)
    
    def write_log(
        self,
        txt:str,
        logname:str = "sendinvitation.log"
    ):
        with open(logname,mode="a") as f:
            time = dt.now().strftime('%Y/%m/%d %H:%M:%S')
            tmp_txt = f'[{time}] {txt}'
            f.write(tmp_txt)
            f.write("\n")
        print(txt)

    def add_new_member2Team(
        self,
        user_name:str,
        team:str
    ):
        for oname in self.target_organization:
            org = self.g.get_organization(oname)
            for i in org.get_members():
                if i.login == user_name:
                    for j in org.get_teams():
                        if j.name == team:
                            j.add_to_members(i)
                            break
                    break
    
    def chk_csv(
        self,
        filepath:str,
        columns:list
    ):
        try:
            df = pd.read_csv(filepath,encoding="shift_jis")
        except:
            try:
                df = pd.read_csv(filepath,encoding="utf-8")
            except:
                self.write_log("failed to read a csv file")
                self.write_log(filepath)
                return ""
        c_d_and = set(columns) & set(df.columns)
        if len(c_d_and)!=len(columns):
            self.write_log(fr"this csv has not enough cokumns: {filepath}")
            return ""
        return df[columns]
    
    def get_permission(
        self,
        repository_name:str,
        teams_permission:dict
    ):
        if len(teams_permission) == 0:
            print("added no group to this repository")
        try:
            oname = self.oname
        except:
            print("please use a module 'set_repo'")
            print("set_repo(cls,repository_path,**kwargs)")
            raise Exception
        repo = self.org.get_repo(repository_name)
        for i in self.org.get_teams():
            if i.name in teams_permission.keys():
                i.add_to_repos(repo)
                i.set_repo_permission(repo,teams_permission[i.name])
        return repo
    