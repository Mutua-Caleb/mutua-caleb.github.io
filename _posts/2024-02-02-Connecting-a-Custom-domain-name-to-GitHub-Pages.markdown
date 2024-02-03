---
layout: post
title: "Connecting a Custom Domain name to GitHub Pages"
date: 2024-02-02
---

I made this blog with Jekyll, which was easy to set up. I quickly got the basic structure using **Jekyll -new**, then uploaded it to GitHub and named the repository [calebkivindyo.github.io](http://calebkivindyo.github.io/) because I wanted that to be the web address if I used **GitHub Pages** to host it. But, GitHub gave it a longer, less appealing address: [mutua-caleb.github.io/calebkivindyo.github.io](http://mutua-caleb.github.io/calebekivindyo.github.io). So, I decided to use a domain I bought last year, [calebkivindyo.com](http://calebkivindyo.com/), and I want to talk about how I did that here.

If you're already using GitHub Pages to host your blog (simply navigate to your repository, access the settings, and locate the 'Pages' section), here's what to do next:

**Get a Domain Name:** Consider buying one from GoDaddy, NameCheap, or Google Domains.

![Default Image](/assets/images/Untitled.png)

**Configure your DNS settings:** 

- Go to your domain name provider and find DNS records of your domain.
- The most common DNS record you’ll need is an A record that points to the IP address of the server where your site is located(In this case Github Pages). Set the A record to point to Github’s IP addresses(ie. 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153).

![Default Image](/assets/images/Untitled-1.png)

- You also need to add a CNAME record, especially if you want to use a subdomain like”www”. In this case add the name of the default GitHub pages domain. In my case it was **mutua-caleb.io**

![Default Image](/assets/images/Untitled-2.png)

After doing this go back to GitHub pages home page and add the custom domain.

![Default Image](/assets/images/Untitled-3.png)

![Default Image](/assets/images/Untitled-4.png)

**Update your Jekyll configuration:** In your Jekyll’s site root directory, find the “_config.yml” file and update your url of your custom domain: **calebkivindyo.com**

**Wait for DNS propagation:** DNS changes can take some time to propagate across the internet. This process can take few minutes to up to 48 hours.