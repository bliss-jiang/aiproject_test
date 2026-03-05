Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.
Try the new cross-platform PowerShell https://aka.ms/pscore6
Loading personal and system profiles took 2445ms.
(base) PS C:\Windows\system32> D:
(base) PS D:\> ls

    Directory: D:\


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          2026/3/3     12:18                AI
d-----         2026/2/26     14:38                ollama-qa-system-main
d-----         2026/2/24     16:32                OpenCode
d-----         2026/1/26      8:33                PyCharm
d-r---         2025/2/10     15:43                ShareDocs
d-----          2025/1/6     20:27                WebSite
d-----         2026/1/27      8:12                初中
d-----          2026/2/3     13:59                工作資料
-a----          2026/3/2     15:42          40969 file-preview.png
-a----         2025/6/17     17:08        5242629 Git教程.pptx
-a----         2026/2/24     10:59         370829 Jetbrains.zip
-a----         2024/7/12     15:27       24604624 SourceTreeSetup-3.4.18.exe

(base) PS D:\> cd AI
(base) PS D:\AI> cd .\DocumentChat\
(base) PS D:\AI\DocumentChat> ls

    Directory: D:\AI\DocumentChat


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          2026/3/3     17:01                .idea
d-----          2026/3/4      8:50                .vscode
d-----          2026/3/3     16:16                attachments
d-----          2026/3/3     16:16                faiss_db
d-----          2026/3/2     15:42                html
d-----          2026/3/2     14:12                qdrant_db
d-----          2026/3/3     12:48                test
d-----          2026/3/3     16:46                tools
d-----          2026/3/3      9:44                __pycache__
-a----         2026/2/25     16:41            247 .env
-a----          2026/3/3     10:45           2494 main.py
-a----         2026/2/27     15:50           5387 ReadMe.md

(base) PS D:\AI\DocumentChat>
(base) PS D:\AI\DocumentChat> conda activate aiservice
(aiservice) PS D:\AI\DocumentChat> git config --global user.name "lansrhaitun@163.com"
(aiservice) PS D:\AI\DocumentChat> git config --global user.name "bliss-jiang"
(aiservice) PS D:\AI\DocumentChat> git config --global user.email "lansrhaitun@163.com"
(aiservice) PS D:\AI\DocumentChat> git init
Initialized empty Git repository in D:/AI/DocumentChat/.git/
(aiservice) PS D:\AI\DocumentChat> git remote add origin https://github.com/bliss-jiang/aiproject_test
(aiservice) PS D:\AI\DocumentChat> git add
Nothing specified, nothing added.
hint: Maybe you wanted to say 'git add .'?
hint: Disable this message with "git config set advice.addEmptyPathspec false"
(aiservice) PS D:\AI\DocumentChat> git commit -m "Initial commit：上传项目初始代码"
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env
        .idea/
        .vscode/
        ReadMe.md
        __pycache__/
        attachments/
        faiss_db/
        html/
        main.py
        qdrant_db/
        test/
        tools/

nothing added to commit but untracked files present (use "git add" to track)
(aiservice) PS D:\AI\DocumentChat> git branch -M main
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/bliss-jiang/aiproject_test'
(aiservice) PS D:\AI\DocumentChat>
(aiservice) PS D:\AI\DocumentChat>
(aiservice) PS D:\AI\DocumentChat>
(aiservice) PS D:\AI\DocumentChat> git add
Nothing specified, nothing added.
hint: Maybe you wanted to say 'git add .'?
hint: Disable this message with "git config set advice.addEmptyPathspec false"
(aiservice) PS D:\AI\DocumentChat> git add .
(aiservice) PS D:\AI\DocumentChat> git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   ReadMe.md
        new file:   main.py
        new file:   test/OpenAIembedding.py
        new file:   "test/llamaindex\350\277\236\346\216\245\345\261\200\345\237\237\347\275\221\345\244\247\346\250\241\345\236\213.py"
        new file:   "test/\346\265\213\350\257\225ollama\350\277\236\346\216\245qdrant.py"
        new file:   tools/faiss_index/index.faiss
        new file:   tools/faiss_index/index.pkl
        new file:   tools/file_tools.py
        new file:   tools/new_tools_test.py
        new file:   tools/rag_langchain_tools.py
        new file:   tools/rag_llamaindex_tools.py

(aiservice) PS D:\AI\DocumentChat> git commit -m "Initial commit: 上传项目初始代码"
[main (root-commit) c52f91d] Initial commit: 上传项目初始代码
 12 files changed, 987 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 ReadMe.md
 create mode 100644 main.py
 create mode 100644 test/OpenAIembedding.py
 create mode 100644 "test/llamaindex\350\277\236\346\216\245\345\261\200\345\237\237\347\275\221\345\244\247\346\250\241\345\236\213.py"
 create mode 100644 "test/\346\265\213\350\257\225ollama\350\277\236\346\216\245qdrant.py"
 create mode 100644 tools/faiss_index/index.faiss
 create mode 100644 tools/faiss_index/index.pkl
 create mode 100644 tools/file_tools.py
 create mode 100644 tools/new_tools_test.py
 create mode 100644 tools/rag_langchain_tools.py
 create mode 100644 tools/rag_llamaindex_tools.py
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
info: please complete authentication in your browser...
Enumerating objects: 17, done.
Counting objects: 100% (17/17), done.
Delta compression using up to 16 threads
Compressing objects: 100% (17/17), done.
Writing objects: 100% (17/17), 22.43 KiB | 11.21 MiB/s, done.
Total 17 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/bliss-jiang/aiproject_test
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
(aiservice) PS D:\AI\DocumentChat> git push
Everything up-to-date
(aiservice) PS D:\AI\DocumentChat> git rm -r --cached
fatal: No pathspec was given. Which files should I remove?
(aiservice) PS D:\AI\DocumentChat> git add .
warning: in the working copy of 'html/js/jquery-4.0.0.js', LF will be replaced by CRLF the next time Git touches it
(aiservice) PS D:\AI\DocumentChat> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        new file:   "attachments/\351\225\277\345\205\2642025-2026\345\271\264\345\221\230\345\267\245\345\225\206\344\277\235\347\246\217\345\210\251\346\211\213\345\206\214.pdf"
        new file:   html/MultiAI_Chat.html
        new file:   html/img/file-preview.png
        new file:   html/js/MultiAI_Chat.css
        new file:   html/js/jquery-4.0.0.js

(aiservice) PS D:\AI\DocumentChat> git commit -m "Fix 更新.gitingore"
[main b1bb3cc] Fix 更新.gitingore
 6 files changed, 10219 insertions(+), 3 deletions(-)
 create mode 100644 "attachments/\351\225\277\345\205\2642025-2026\345\271\264\345\221\230\345\267\245\345\225\206\344\277\235\347\246\217\345\210\251\346\211\213\345\206\214.pdf"
 create mode 100644 html/MultiAI_Chat.html
 create mode 100644 html/img/file-preview.png
 create mode 100644 html/js/MultiAI_Chat.css
 create mode 100644 html/js/jquery-4.0.0.js
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
fatal: unable to access 'https://github.com/bliss-jiang/aiproject_test/': Empty reply from server
(aiservice) PS D:\AI\DocumentChat> git push -u origin main
fatal: unable to access 'https://github.com/bliss-jiang/aiproject_test/': Failed to connect to github.com port 443 after 21068 ms: Could not connect to server
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