# -*- coding:utf-8 -*-
from .use_github import Use_github
import json
import os
import requests
import pandas as pd
from  datetime import datetime
from glob import glob
from .encfunc import Enc
from datetime import datetime as dt
from datetime import timedelta

class Audit(Use_github):
    def __init__(
        self,
        log_org:str,
        log_repo:str,
        *args,
        **kwargs
    ):
        """[summary]
        This module collect auditlogs
        [example]
        inst = github_auditlog.audit(log_org,log_repo)
        inst.get_setting_info()
        inst.get_all_audit()
        
        Args:
            log_org (str): [description]specify a organization to put logs
            log_repo (str): [description]specify a repository to put logs
        """
        super(Audit, self).__init__(*args,**kwargs)
        self.set_org(log_org)
        self.set_repo(f"{log_org}/{log_repo}")
        self.team_columns = [
            '"name":','"id":','"privacy":','"permission":',
            '"created_at":','"updated_at":','"members_count":',
            '"repos_count":'
        ]
        self.collabo_columns = [
            '"login":','"id":','"node_id":',
            '"type":','"site_admin":','"name":',
            '"updated_at":'
        ]
        self.member_columns = [
            "login","name","id","role","email",
            "location","company","twitter_username",
            "owned_private_repos","public_repos",
            "private_gists","private_gists","created_at",
            "last_modified","updated_at","suspended_at",
            "bio","team_count","permissions","type",
            "site_admin","collaborators"
        ]
    
    def orginfo(
        self,
        target_oname,
        log_dir:str="OrganizationLog"
    ):
        try:
            tmp_org = self.g.get_organization(target_oname)
        except Exception as e:
            print("Please check an organization's name")
            print(e)
            raise Exception        # get_organization_info
        logname = f"orgainfo_{target_oname}.log"
        with open(logname,mode="w") as f:
            tmp_text = json.dumps(tmp_org.raw_data).split(",")
            tmp_text = [i for i in tmp_text if i.find('"temp_clone_token":')==-1]
            tmp_text = [i for i in tmp_text if i.find('"disk_usage":')==-1]
            tmp_text = ",\n".join(tmp_text)
            f.write(tmp_text)
            f.write(f"\nTeams-------------\n")
            for j in tmp_org.get_teams():
                f.write("\n")
                team_list = []
                tmp_text = json.dumps(j.raw_data).split(",")
                for k in tmp_text:
                    for l in self.team_columns:
                        if k.find(l) > -1:
                            team_list.append(k)
                team_list = ",\n".join(tmp_text)
                f.write(team_list)
        filepath = f"{log_dir}/{logname}"
        self.add_update_file(filepath,logname)
        
        return tmp_org
    
    def repoinfo(
        self,
        tmp_org,
        log_dir:str="RepositoryLog"
    ):
        for i in tmp_org.get_repos():
            repo_name = i.name
            tmp_oname = i.organization.login
            logname = f"repoinfo_{tmp_oname}_{repo_name}.log"
            with open(logname,mode="w") as f:
                tmp_text = json.dumps(i.raw_data).split(",")
                tmp_text = [j for j in tmp_text if j.find('"temp_clone_token":')==-1]
                tmp_text = ",\n".join(tmp_text)
                f.write(tmp_text)
                f.write(f"\nCollaborators-------------\n")
                for j in i.get_collaborators():
                    f.write("\n")
                    collabo_list = []
                    tmp_text = json.dumps(j.raw_data).split(",")
                    for k in tmp_text:
                        for l in self.collabo_columns:
                            if k.find(l) > -1:
                                collabo_list.append(k)
                    tmp_text = collabo_list
                    tmp_text = ",\n".join(tmp_text)
                    f.write(tmp_text)
            filepath = f"{log_dir}/{logname}"
            self.add_update_file(filepath,logname)
            
    
    def get_memberlist(
        self,
        tmp_org,
        log_dir:str="MemberList"
    ):
        orga_array = []
        tmp_oname = tmp_org.name
        csv_name = f"member_list_{tmp_oname}.csv"
        for i in tmp_org.get_members():
            tmp_array = [
                i.login,
                i.name,
                i.id,
                i.role,
                i.email,
                i.location,
                i.company,
                i.twitter_username,
                i.owned_private_repos,
                i.public_repos,
                i.private_gists,
                i.private_gists,
                i.created_at,
                i.last_modified,
                i.updated_at,
                i.suspended_at,
                i.bio,
                i.team_count,
                i.permissions,
                i.type,
                i.site_admin,
                i.collaborators
            ]
            orga_array.append(tmp_array)
        tmp_df = pd.DataFrame(orga_array,columns=self.member_columns)
        tmp_df.to_csv(csv_name,index=False,encoding="shift_jis")
        filepath = f"{log_dir}/{csv_name}"
        self.add_update_file(filepath,csv_name,encoding="shift_jis")
        os.remove(csv_name)
        tmp_df = tmp_df[tmp_df['public_repos']>0]
        return len(tmp_df)
    
    def get_eventlog(
        self,
        tmp_org,
        log_dir:str="Eventlog"
    ):
        tmp_oname = tmp_org.name
        for i in tmp_org.get_repos():
            repo_name = i.name
            logname = f"eventlog_{tmp_oname}_{repo_name}.csv"
            filepath = f"{log_dir}/{logname}"
            df = ""
            columns = ['id','type','created_at','actor','payload','public']
            for tmp_j in i.get_events():
                tmp_j = tmp_j.raw_data
                if len(tmp_j)==0:
                    continue
                tmp_list = [[
                    tmp_j["id"],
                    tmp_j["type"],
                    tmp_j["created_at"],
                    json.dumps(tmp_j["actor"]),
                    json.dumps(tmp_j["payload"]),
                    tmp_j["public"]
                ]]
                tmp_df = pd.DataFrame(tmp_list,columns=columns)
                if len(df)==0:
                    df = tmp_df
                else:
                    df = pd.concat([df,tmp_df])
            if len(df)==0:
                continue
            df.to_csv(logname,index=False)
            self.add_update_file(filepath,logname)
            
    
    def get_setting_info(self):
        # log collection
        err_num = 0
        for tmp_oname in self.target_organization:
            tmp_org = self.orginfo(tmp_oname)
            self.repoinfo(tmp_org)
            tmp_num = self.get_memberlist(tmp_org)
            self.get_eventlog(tmp_org)
            err_num += tmp_num
        if err_num > 0:
            print("MemberListに不審な点あり")
        return err_num
    
    def get_auditlog(
        self,
        oname:str,
        log_dir="AuditLog"
    ):
        print(f"{oname} Auditlog取得開始")
        logname = f"auditlog_{oname}.csv"
        filepath = f"{log_dir}/{logname}"
        param = {
            'per_page': '100',
        }
        df = ""
        latestdate = dt.today().strftime("%Y/%m/%d %H:%M:%S")
        endflag = 0
        enc = Enc()
        token = enc.decrypt(self.enc_token)
        while True:
            URL = f'https://api.github.com/orgs/{oname}/audit-log'
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
                }
            res = requests.get(URL, headers=headers,params=param)
            tmp_data = json.loads(res.text)
            if len(tmp_data) == 0:
                break
            tmp_df = pd.DataFrame(tmp_data)
            tmp_latestdate = latestdate
            for i in range(len(tmp_df.index)):
                try:
                    num = int(tmp_df["created_at"][i])
                    num = int(num*0.001)
                    tmp_df["created_at"][i] = datetime.fromtimestamp(num)
                    tmp_latestdate = str(tmp_df["created_at"][i])
                    if latestdate == tmp_latestdate:
                        endflag = 1
                except:
                    break
            latestdate = tmp_latestdate
            if endflag == 1:
                break
            param = {
                'per_page': '100',
                'phrase' :f'created:<{latestdate}',
            }
            if len(df)==0:
                df = tmp_df
            else:
                df = pd.concat([df,tmp_df])
        if len(df) == 0:
            return 0
        columns = df.columns
        columns.sort_values()
        df = df[columns]
        df.to_csv(logname,index=False)
        print(len(df.index))
        self.add_update_file(filepath,logname)
        self.get_accesslog(oname,log_dir)
        rnum = self.extract_data(oname,df,log_dir)
        if rnum > 0:
            print("Organization上に変更あり")
        return rnum
    
    def extract_data(
        self,
        oname:str,
        df,
        log_dir:str
    ):
        logname = f"importantlog_auditlog_{oname}.csv"
        filepath = f"{log_dir}/{logname}"
        yesterday = dt.today() - timedelta(1)
        yesterday = yesterday.strftime("%Y/%m/%d 00:00:00")
        yesterday = dt.strptime(yesterday,"%Y/%m/%d %H:%M:%S")
        tmp_df = df[df['created_at']>yesterday]
        exclude_key = [
            "repo.","audit_log_export","pull_request.",
            "protected_branch.","team.","project.","profile_picture.",
            "org.restore_member","org.add_member","org_credential_authorization.grant"
            ]
        for exkey in exclude_key:
            tmp_df = tmp_df[~tmp_df['action'].str.contains(exkey)]
        if len(tmp_df) > 0:
            print("Organizationの設定が変更された可能性があります")
            tmp_df.to_csv(logname)
            self.add_update_file(filepath,logname)
            
            return len(tmp_df)
        else:
            return 0
    
    def get_accesslog(
        self,
        oname:str,
        log_dir:str
    ):
        logname = f"access_{oname}.log"
        filepath = f"{log_dir}/{logname}"
        param = {
            'per_page': '100',
            'phrase' : 'action:repo.access',
        }
        df = ""
        latestdate = dt.today().strftime("%Y/%m/%d %H:%M:%S")
        enc = Enc()
        token = enc.decrypt(self.enc_token)
        endflag = 0
        while True:
            URL = f'https://api.github.com/orgs/{oname}/audit-log?include=all'
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
                }
            res = requests.get(URL, headers=headers,params=param)
            tmp_data = json.loads(res.text)
            if len(tmp_data) == 0:
                break
            tmp_df = pd.DataFrame(tmp_data)
            tmp_latestdate = latestdate
            for i in range(len(tmp_df.index)):
                try:
                    num = int(tmp_df["created_at"][i])
                    num = int(num*0.001)
                    tmp_df["created_at"][i] = datetime.fromtimestamp(num)
                    tmp_latestdate = str(tmp_df["created_at"][i])
                    if latestdate == tmp_latestdate:
                        endflag = 1
                except:
                    break
            latestdate = tmp_latestdate
            if endflag == 1:
                break
            param = {
                'per_page': '100',
                'phrase' :f'created:<{latestdate}',
                'phrase' : 'action:repo.access',
            }
            if len(df)==0:
                df = tmp_df
            else:
                df = pd.concat([df,tmp_df])
        if len(df) == 0:
            return
        columns = df.columns
        columns.sort_values()
        df = df[columns]
        df.to_csv(logname,index=False)
        print(len(df.index))
        df.to_csv(logname)
        self.add_update_file(filepath,logname)
        
    
    def get_all_audit(self):
        result_num = 0
        for oname in self.target_organization:
            print(oname)
            num = self.get_auditlog(oname)
            result_num += num




