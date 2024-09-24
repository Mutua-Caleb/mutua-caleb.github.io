---
layout: post
title: "More Customisation of Jekyll"
date: 2024-02-03
permalink: /posts/:title
categories: [Jekyll]
---

My first blog article was about customizing the footer and using a rather hacky way to prevent the title repeating on the footer. The first home page when you’ve created jekyll skeleton usually shows the title appearing twice on the footer. This is really annoying. I was really naive and thought that solution is just commenting out the lines that mentioned the title in `usr/local/lib/ruby/gems/2.6.0/gems/minima-2.5.1/_includes/footer.html`. By the way to access these files just fire up your terminal and type `bundle info --path minima`

This worked the first time but when I committed my changes to GitHub, the title was still repeating itself. Then I started doing the hacky way of just commenting out any lines that mention the title above. However this didn’t work but I got this ugly error:  `Unable to write file 'vscode-remote://wsl+ubuntu-22.04/var/lib/gems/3.0.0/gems/minima-2.5.1/_includes/footer.html' (NoPermissions (FileSystemError): Error: EACCES: permission denied, open '/var/lib/gems/3.0.0/gems/minima-2.5.1/_includes/footer.html')`

The solution is quite simple really.  Just create the **_includes** folder at the root directory of your project,  copy the **footer.html** file and put it inside the **_includes** folder, then comment out any mention of the title in the footer. This way the Jekyll engine knows to look for the footer files and just apply the changes.