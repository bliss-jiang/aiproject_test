(base) PS D:\AI\DocumentChat> conda activate aiservice
(aiservice) PS D:\AI\DocumentChat> git config --global user.name "bliss-jiang"
(aiservice) PS D:\AI\DocumentChat> git config --global user.email "lansrhaitun@163.com"
(aiservice) PS D:\AI\DocumentChat> git init
Initialized empty Git repository in D:/AI/DocumentChat/.git/
(aiservice) PS D:\AI\DocumentChat> git remote add origin https://github.com/bliss-jiang/aiproject_test.git
(aiservice) PS D:\AI\DocumentChat> git commit -m "Initial commit：上传项目初始代码"
(aiservice) PS D:\AI\DocumentChat> git branch -M main
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
(aiservice) PS D:\AI\DocumentChat> git add .
(aiservice) PS D:\AI\DocumentChat> git status
(aiservice) PS D:\AI\DocumentChat> git commit -m "Initial commit: 上传项目初始代码"
(aiservice) PS D:\AI\DocumentChat> git push -u origin main

(aiservice) PS D:\AI\DocumentChat> git rm -r --cached
(aiservice) PS D:\AI\DocumentChat> git add .
warning: in the working copy of 'html/js/jquery-4.0.0.js', LF will be replaced by CRLF the next time Git touches it
(aiservice) PS D:\AI\DocumentChat> git status
(aiservice) PS D:\AI\DocumentChat> git commit -m "Fix 更新.gitingore"
(aiservice) PS D:\AI\DocumentChat> git push -u origin main

(aiservice) PS D:\AI\DocumentChat> git add .
(aiservice) PS D:\AI\DocumentChat> git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    "attachments/\351\225\277\345\205\2642025-2026\345\271\264\345\221\230\345\267\245\345\225\206\344\277\235\347\246\217\345\210\251\346\211\213\345\206\214.pdf"

(aiservice) PS D:\AI\DocumentChat> git commit -m "Fix更新.gitingore"
[main f336d14] Fix更新.gitingore
 1 file changed, 0 insertions(+), 0 deletions(-)
 delete mode 100644 "attachments/\351\225\277\345\205\2642025-2026\345\271\264\345\221\230\345\267\245\345\225\206\344\277\235\347\246\217\345\210\251\346\211\213\345\206\214.pdf"
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
fatal: unable to access 'https://github.com/bliss-jiang/aiproject_test/': Failed to connect to github.com port 443 after 21078 ms: Could not connect to server
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 16 threads
Compressing objects: 100% (13/13), done.
Writing objects: 100% (14/14), 942.99 KiB | 28.58 MiB/s, done.
Total 14 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 1 local object.
To https://github.com/bliss-jiang/aiproject_test
   c52f91d..f336d14  main -> main
branch 'main' set up to track 'origin/main'.
(aiservice) PS D:\AI\DocumentChat> (aiservice) PS D:\AI\DocumentChat> git push -u origin main


git add .
git commit -m "你的修改说明"
git push