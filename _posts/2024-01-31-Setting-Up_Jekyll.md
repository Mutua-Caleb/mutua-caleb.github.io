---
layout: post
title: "Setting Up Jekyll"
date: 2024-01-31
---
I've been trying to make my own blog for 5 months! Usually, making a blog is the first thing you do when you start learning web development. I made a blog using Rails 3 years ago, but then there was a problem with Heroku. I didn't fix it because I was lazy. But today, I learned about Jekyll and made a new blog in just 2 hours. Jekyll is easy to set up. You can search for Jekyll online or ask ChatGPT for help. Once you set it up, type localhost:4000 in your web browser, and you'll see your blog's home page:
![Default Image](https://kinsta.com/wp-content/uploads/2023/03/minima-jekyll-theme.jpg)

If you want to change the blog title to <b>"Everyday TILs,"</b> open <code> config.yaml </code> in Jekyll's folder. Change <b> title: Your awesome title </b> to <b>title: Everyday TILs.</b>

To delete the About page, go to the folder <code>/mnt/c/personal_blog/Everydaytils/_site/.</code> Find about.markdown and delete it.

If <b>"Your awesome title"</b> shows up twice in the footer and you want to remove it, you need to edit the theme files. Jekyll uses a theme called minima. Find where minima is on your computer by typing bundle info --path minima in a Linux terminal. It will show a path like <code> /usr/local/lib/ruby/gems/2.6.0/gems/minima-2.5.1.</code>

Go to that folder, then to _includes. Open footer.html. Find lines with site.title and put comment marks <!-- --> around them to hide the titles.