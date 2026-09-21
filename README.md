# GitHub-Email-Finder
Identify the email addresses of the users involved from the GitHub commit history.

## overview
**GitHub Email Finder** is a Python CLI tool designed to extract the names and email addresses of commit authors from public GitHub repositories and user profiles. It assists in identifying the email addresses of target accounts during OSINT investigations and security research.

> **Disclaimer**
> This tool is intended solely for educational purposes and authorized security research. The developers assume no responsibility for any unauthorized or malicious use of this tool.

### Key Features
- **Flexible Scope**: Search by GitHub username or specific repository URL.
- **Deep Commit Analysis**: Specify the depth of commits to scan per repository (`-d / --deep`).
- **Fork Filtering**: Choose whether to include or exclude forked repositories (`-f / --fork`).
- **API Limit Bypass**: Supports GitHub Personal Access Tokens for authenticated queries (`-t / --token`).
- **Visual Progress**: Console UI with spinner indicators and colorized logs.


## Installation
1. Clone this repository and navigate to the directory.
```bash
git clone https://github.com/f2nDev/GitHub-Email-Finder.git
cd GitHub-Email-Finder
```
2. Install the dependency libraries.
```bash
pip install -r requirements.txt
```

## Usage
Here is how to run it and the arguments involved:
```bash
./github_email_finder.py [-h] [-l LINK] [-u USER] [-d DEEP] [-t TOKEN] [-f]
```

### Arguments
 - `-h`: show a help message and exit.
 - `-l LINK`: Set the link to the target repository.
 - `-u USER`: Set the target users.
 - `-d DEEP`: Set the number of commits to retrieve per repository. default is 3.
 - `-t TOKEN`: Set a user token. Entering one is optional, but doing so allows you to bypass API limits.
 - `-f`: Decide whether to include forked repositories in the scope of the investigation.

### Usage example
```bash
./github_email_finder.py -t example -u example1 -f

===============================================================
GitHub Email Finder - v1.0.0 - by f2nDev
===============================================================
[+] target user: example1
[+] your token: example
[+] Number of commits received per repository: 3
[+] allow fork Repository: True
===============================================================
[+] Searching the users public repos... Done
[+] Searching commits emails... Done
===============================================================
[+] 1 email found.
[*] example1\'s email: example1@example.com
===============================================================
[+] Exiting...
===============================================================
```

## LICENSE
GitHub Email Finder is released under the **MIT License.**
```
MIT License

Copyright (c) 2026 f1023n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```