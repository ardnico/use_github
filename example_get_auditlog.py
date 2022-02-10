
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