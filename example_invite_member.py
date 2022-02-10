
from use_github3 import github_invite

oname = "Organization_name"

def main():
    inst = github_invite.Invite(oname)

    # Send Invitation
    inst.sendinvitation()

if __name__=="__main__":
    main()