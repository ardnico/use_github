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