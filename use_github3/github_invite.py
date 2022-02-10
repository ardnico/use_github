# -*- coding:utf-8 -*-
from .use_github import Use_github
import sys
import os
import pandas as pd
from glob import glob

class Invite(Use_github):
    def __init__(
        self,
        oname:str,
        *args,
        **kwargs
    ):
        super(Invite, self).__init__(*args,**kwargs)
        self.set_org(oname)
        self.csv_columns = ["GitHubuserID","TeamName"]
        os.makedirs("target",exist_ok=True)
    
    def mk_invite_csv(self):
        with open("target/invite_target.csv",mode="w") as f:
            f.write("GitHubuserID,TeamName\n")
        print("Created sample csv")
        print("plaease input information like belows")
        print("*Team name can specify more teams with split '/'")
        print("monalisa,apl/infra")
        print("okta,infra/manage")
        print("cat,development/apl")

    def get_data(self):
        files = glob(r"target\*.csv")
        df = ""
        if len(files)==0:
            self.write_log("There is no csv files in 'target' directory")
            self.mk_invite_csv()
            self.write_log("end this process")
            waiting = input(">>")
            sys.exit()
        for file in files:
            tmp_df = self.chk_csv(file,self.csv_columns)
            if len(tmp_df) == 0:
                continue
            if len(df) == 0:
                df = tmp_df
            else:
                df = pd.concat([df,tmp_df])
        if len(df) == 0:
            self.write_log("There is no data in csv files")
            self.write_log("end this process")
            waiting = input(">>")
            sys.exit()
        return df

    def user_chk(self,df):
        print("Target user's GitHubID-------------")
        for i in range(len(df.index)):
            print(df["GitHubuserID"][i])
        while True:
            waiting = input("Right?(y/n)):")
            if waiting == "y":
                break

    def invite_member(self,df,oname):
        self.write_log(f"Invite some members")
        self.write_log(f"Organization: {oname}")
        for i in range(len(df.index)):
            ghid = df["GitHubuserID"][i]
            try:
                user = self.g.get_user(ghid)
            except:
                self.write_log("GitHubID may be wrong")
                self.write_log(f"please check the ID: {ghid}")
                continue
            username = user.login
            TeamNames = df["TeamName"][i]
            role = "direct_member"
            # role = "admin"
            teams = []
            for TeamName in TeamNames.split("/"):
                for i in self.org.get_teams():
                    if i.name == TeamName:
                        teams.append(i)
            self.write_log(f"Organization: {self.org.name}")
            try:
                self.org.invite_user(user=user,role=role,teams=teams)
            except Exception as e:
                self.write_log(e)
                self.write_log(fr"Failed to invite: {username}")
                self.write_log("please check github token scope or your role")
            self.write_log(fr"Finished: {username}")
        
    # member invitation
    def sendinvitation(self):
        os.makedirs("target",exist_ok=True)
        self.write_log("ProcessStarted")
        df = self.get_data()
        self.user_chk(df)
        for target in self.target_organization:
            self.invite_member(df,target)
        self.write_log("finished to invite to some members")
