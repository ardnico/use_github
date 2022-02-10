# use_github
This module was created for daily work, like to get some auditlog, to invite somebody, and so on.

---

_useGitHub Changing log_

* [2022/02/10] Created in this repository



## Example:
### [Get some log data](example_get_auditlog.py)

"""python
from use_github3 import github_auditlog

log_org = "Organization_name"
log_repo = "Repository_name"

def main():
    inst = github_auditlog.Audit(log_org,log_repo)

    # collect eventlog memberlist
    inst.get_setting_info()

    # collect auditlog
    inst.get_all_audit()

if __name__=="__main__":
    main()
"""
### [invite some members](example_invite_member.py)

"""python
from use_github3 import github_invite

oname = "Organization_name"

def main():
    inst = github_invite.Invite(oname)

    # Send Invitation
    inst.sendinvitation()

if __name__=="__main__":
    main()
"""

### [Copy repository ](example_copy_repository.py)

"""python
from use_github3 import handle_repo


oname = "Destination_Organization_name"
org_path = "Org_Organization_name/Org_repository_name"
repo_name = "new_repository_name"
description = "sample"
teams_permission = {
    "teamname1" : "push",
    "teamname2" : "pull",
    "teamname3" : "push"
}
private = True

def main():
    inst = handle_repo.Treat_repo()
    inst.set_org(oname)
    inst.copy_repo(
        org_path,repo_name,description,teams_permission,private,
        strict = True, # 制限設定の有無
        contexts = [], # 指定の文字列を含むファイルを統合前のチェック対象に設定する
        enforce_admins = True, # adminにも設定を強制
        dismissal_users= [],
        dismissal_teams= ["teamsname2"], # pull requestを解散できるチーム
        dismiss_stale_reviews= False, # 他のcommitがpushされると古いpull requestを削除
        require_code_owner_reviews= False, # レビューにコードオーナーを求める
        required_approving_review_count= 1, # 必要レビュワー数
        user_push_restrictions = [],
        team_push_restrictions = ["teamname1"] # push可能なチーム
    )


if __name__=="__main__":
    main()
"""

### About

1. 

## functions

Usage

"""python

"""

## License

Feel free to use, reuse and abuse the code in this project.
