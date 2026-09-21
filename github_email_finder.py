#!/usr/bin/env python3

import argparse
import sys
from time import sleep
import threading
import re

#print horizon
def horizon():
    print("=" * 63)

horizon()
print("GitHub Email Finder - v1.0.0 - by f2nDev")
horizon()

try:
    from github import Github, Auth
    from github.Repository import Repository
except:
    print("\033[31m\033[1m[-] \033[0mCannot import github. plz pip install pygithub.")
    horizon()
    print("\033[32m\033[1m[+] \033[0mExiting...")
    horizon()
    exit(1)

#Create new error
class NotFoundError(Exception):
    pass

class Log():
    # setting the text color
    def __init__(self):
        self.RED = "\033[31m"
        self.YELLOW = "\033[33m"
        self.CYAN = "\033[36m"
        self.GREEN = "\033[32m"
        self.BOLD = "\033[1m"
        self.END = "\033[0m"

    # text prints
    def error(self,log):
        print(self.RED + self.BOLD + "[-] " + self.END + log)
        horizon()
        self.starting("Exiting...")
        horizon()
        exit(1)

    def warning(self,log):
        print(self.YELLOW + self.BOLD + "[!] " + self.END + log)

    def starting(self,log):
        print(self.GREEN + self.BOLD + "[+] " + self.END + log)

    def notice(self,log):
        print(self.CYAN + self.BOLD + "[*] " + self.END + log)

    def normal(self,log):
        print(log)
    #print progress spinner
    def spinner(self, stop_event, message):
        chars = ["|", "/", "-", "\\"]
        idx = 0

        while not stop_event.is_set():
            sys.stdout.write(f"\r{self.GREEN}{self.BOLD}[+] {self.END}{message} {chars[idx % len(chars)]}")
            sys.stdout.flush()
            idx += 1
            sleep(0.2)
    #run function with spinner function
    def run_with_spinner(self, func, *args, message, **kwargs):
        stop_event = threading.Event()

        spinner_thread = threading.Thread(target=self.spinner, args=(stop_event, message))
        spinner_thread.start()
        
        try:
            result = func(*args, **kwargs)

        except Exception as e:
            stop_event.set()
            spinner_thread.join()
            sys.stdout.write(f"\r{self.GREEN}{self.BOLD}[+] {self.END}{message} Error\n")
            sys.stdout.flush()

            self.error(str(e))

        else:
            stop_event.set()
            spinner_thread.join()
            sys.stdout.write(f"\r{self.GREEN}{self.BOLD}[+] {self.END}{message} Done\n")
            sys.stdout.flush()
            return result


def argument(log):
    # setting arguments
    global parser
    parser = argparse.ArgumentParser(
        add_help=False
    )

    # 1. arguments
    parser.add_argument("-h", "--help", action="store_true", help="show this help message and exit")
    parser.add_argument("-l", "--link", type=str, help="Specify the repository link")
    parser.add_argument("-u", "--user", type=str, help="Specify the target username")
    parser.add_argument("-d", "--deep", type=int, default=3, help="Sets the number of commits to retrieve per repository.(default is 3)")
    parser.add_argument("-t", "--token", type=str, help="Specify an access token. While not mandatory, providing one allows you to bypass API limits.")
    parser.add_argument("-f", "--fork", action="store_true", help="include forked repositories in the scope of the investigation")
    args = parser.parse_args()

    # 2. conditions
    if args.help:
        print("Identify user's email address from the GitHub logs.")
        log.warning("DO NOT MISUSE THIS!!!")
        log.warning("The creator assumes no liability for any damages arising from this.")
        horizon()
        parser.print_help()
        horizon()
        exit(0)

    if args.user is None and args.link is None:
        log.error(
            "You must specify a username or a link."
        )

    return args

#Consolidate duplicate keys and values ​​into a single entry
#like -> [("foo", "foo"), ("foo", "foo"), ("baz", "foo")] -> [("foo", "foo"), ("baz", "foo")]
def match_dict(data):
    result = set()

    for d in data:
        result.add(d)

    return list(result)


class git_repos:
    #set values and make github settings
    def __init__(self, username, link, token, fork, deep):
        self.username = username
        self.link = link
        self.token = token
        self.fork = fork
        self.deep = deep

        if self.token is not None:
            self.auth = Auth.Token(self.token)
            self.g = Github(auth = self.auth)
        else:
            self.g = Github()

    #Find the public repositories belonging to the target user
    def get_Users_Public_repos(self):
        try:
            user = self.g.get_user(self.username)
        except:
            raise NotFoundError(f"User {self.username} not found.")
        return user.get_repos()

    #Shorten the GitHub repository link
    def extract_repo_fullname(self, link):
        clean_url = link.rstrip("/").removesuffix(".git")
        pattern = r"github\.com/([^/]+/[^/]+)"
        match = re.search(pattern, clean_url)
        if match:
            return match.group(1)
        
        raise ValueError(f"Unexpected link name: {link}")

    #find the link to the public repository
    def get_link_to_Public_repos(self):
        try:
            repo_name = self.extract_repo_fullname(self.link)
            repo = self.g.get_repo(repo_name)
            return repo
        except:
            raise NotFoundError(f"Link {self.link} is not found.")

    #find the emails from commits
    def get_commit_emails(self, repos):
        emails = []
        if isinstance(repos, Repository):
            if not self.fork and repos.fork:
                return
            try:
                commits = repos.get_commits()
                if commits.totalCount == 0:
                    return

                for commit in commits[:self.deep]:
                    author = commit.commit.author.name
                    email = commit.commit.author.email
                    emails.append((author, email))

            except:
                pass

        else:
            for repo in repos:
                if not self.fork and repo.fork:
                    continue
                try:
                    commits = repo.get_commits()
                    if commits.totalCount == 0:
                        continue

                    for commit in commits[:self.deep]:
                        author = commit.commit.author.name
                        email = commit.commit.author.email
                        emails.append((author, email))

                except:
                    pass

        return match_dict(emails)


def main():
    log = Log()
    args = argument(log)

    if args.link is None:
        log.starting(f"target user: {args.user}")
    else:
        log.starting(f"target link: {args.link}")
    log.starting(f"your token: {args.token}")
    log.starting(f"Number of commits received per repository: {args.deep}")
    log.starting(f"allow fork Repository: {args.fork}")

    horizon()

    git = git_repos(args.user, args.link, args.token, args.fork, args.deep)

    if args.link is None:
        repos = log.run_with_spinner(git.get_Users_Public_repos, message="Searching the users public repos...")
        if repos.totalCount == 0:
            log.warning("The user has no public repos.")

    else:
        repos = log.run_with_spinner(git.get_link_to_Public_repos, message="Searching links repos...")

    emails = log.run_with_spinner(git.get_commit_emails, repos, message="Searching commits emails...")

    emails.sort(key=lambda x: x[0])

    horizon()
    log.starting(f"{len(emails)} email{"s" if len(emails) > 1 else ""} found.")

    for e in emails:
        log.notice(f"{e[0]}'s email: {e[1]}")

    horizon()
    log.starting("Exiting...")
    horizon()

if __name__ == "__main__":
    main()
