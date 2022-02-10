# -*- coding:utf-8 -*-
from .use_github import Use_github
import os
import shutil
from glob import glob
from datetime import datetime as dt
import time
import subprocess

class Treat_repo(Use_github):
    def __init__(self,*args,**kwargs):
        super(Treat_repo, self).__init__(*args,**kwargs)
    
    def create_repo(
        self,
        repo_name:str,
        description:str,
        teams_permission:dict,
        private = True,
        **kwargs
    ):
        try:
            oname = self.oname
        except:
            print("please use a module 'set_repo'")
            print("set_repo(cls,repository_path,**kwargs)")
            raise Exception
        self.org.create_repo(
            name = repo_name,
            description = description,
            private = private,
            **kwargs
        )
        time.sleep(5)
        repo = self.get_permission(repo_name,teams_permission)
        return repo
    
    def protect_branch(
        self,
        repo_name:str,
        branch_name:str = "main",
        **kwargs
        ):
        try:
            oname = self.oname
        except:
            print("please use a module 'set_repo'")
            print("set_repo(cls,repository_path,**kwargs)")
            raise Exception
        target = f'{oname}/{repo_name}'
        repo = self.g.get_repo(target)
        bra = repo.get_branch(branch_name)
        bra.edit_protection(**kwargs)
    
    def repo_clone(self,path):
        dir_name = path.replace("\\","/").split("/")[-1]
        rcode = rcode = subprocess.run(["git","--version"]).returncode
        if rcode != 0:
            print("Please install 'Git'")
            raise Exception
        subprocess.run(["git","clone",fr"https://github.com/{path}"])
        time.sleep(3)
        if os.path.exists(dir_name)==False:
            print(rcode)
            print("please check the org_path param.below repository may not exist")
            print(fr"https://github.com/{path}")
            print(path)
            raise Exception
        return dir_name
        
    def copy_repo(
        self,
        org_path:str,
        repo_name:str,
        description:str,
        teams_permission:dict,
        private:bool,
        **kwargs
    ):
        try:
            oname = self.oname
        except:
            print("please use a module 'set_repo'")
            print("set_repo(cls,repository_path,**kwargs)")
            raise Exception
        tmp_dir = dt.now().strftime('workdir_%Y%m%d%H%M%S')
        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)
        org_dir = self.repo_clone(org_path)
        files = glob(fr"./{org_dir}/**",recursive=True)
        time.sleep(3)
        repo = self.create_repo(repo_name,description,teams_permission,private)
        self.repo_clone(f"{oname}/{repo_name}")
        time.sleep(3)
        for i in files:
            if i.find(".git")>-1:
                continue
            filepath = i.replace(os.getcwd(),"./").replace(f"./{org_dir}",f"./{repo_name}")
            if os.path.isdir(i):
                os.makedirs(filepath,exist_ok=True)
            else:
                shutil.copy(i,filepath)
        os.chdir(repo_name)
        subprocess.run(["git","add","-A"])
        subprocess.run(["git","commit","-m","[new]repositorycreation"])
        subprocess.run(["git","push","origin","main"])
        time.sleep(3)
        self.protect_branch(repo_name,**kwargs)
        os.chdir(r"../../")
        try:
            shutil.rmtree(tmp_dir)
        except:
            pass
        return repo