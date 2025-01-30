## Intro:

This repository contains a backup of the "The Articles Thread 1972-2023" from Backstreets Ticket Exchange forum. A thread started and largely maintained by a user named "Beazle" from 2012 until 2023. The point of the thread was simple, act as a single repository for as many Bruce Springsteen related articles as could be found.

This is a very important resource. Probably close to one thousand unique articles about Bruce going back to the very beginning of his career, until 2023 before his current world tour kicked off. Album and Concert Reviews, Opinion Pieces, Essays, even a college thesis paper or two. Big thanks to Beazle for starting and maintaining the thread for 11 years (which I think could be considered an eternity by internet forum standards.)

Every article in the thread was copied and/or transcribed from the original source. Whether that be a website, newspaper, magazine, transcript of an audio/video interview, etc. In many cases, this thread contains the only version of these articles still on the internet. And not only have they been preserved, but freely accessible for everyone to read. Not locked behind a paywall, or still only available in print (which ranges from easy to near impossible to access today). Also, many of these articles were copied from websites which don't exist anymore. If it wasn't for the efforts of Beazle (and any other contributors to the thread), its safe to say many of these would be lost media.

Sure, many of these articles are still available somewhere online, but nowhere else have they been compiled like this.

Every one of these articles is a little snapshot of history. Whether it is how critics reacted to Bruce's albums at the time of their release, the opinions people had about his music, how his music affected different people, or how his concerts were received at the time. There's articles pondering where Bruce would go after Greetings, or the musician he would become in the future. Even a number of interviews with Bruce, which are an important resource all their own. Its interesting coming across now-famous articles, like the Time and Newsweek articles from 1975, or Jon Landaus now infamous "I have seen the future of rock and roll" review of Cambridge 1974.

## Project History

Back in early 2023, when BTX announced that they were shutting down, I made a backup of a few important threads and pages on the site. It really wasn't a thought out process, and I probably could've done things a bit better. Like the article thread I went page by page and used the print view to save HTML files. Was more tedious than anything, and if I was doing it again I'd probably use some kind of web scraping tool to automate the process.

At the time, I simply took all the HTML files, fixed a few asset paths, and called it a day. Dumping the backup files in a git repo and that was it. I figured it was a "good enough" backup, least the important contents were saved at all.

Of course, I am writing this in January 2025, BTX did _not_ shut down like was advertised. However, at the beginning of this year, the site did go offline for a few days due to a technical issue. Many figured the site was gone for good, all that information now forever lost. It wasn't, but it was motivation enough for me to consider doing something about it.

## Getting to Work

I decided to revisit my backup of the article thread. As mentioned, I saved them as HTML files, which meant that I could use the skills I've picked up from my Databruce project to automate this process a good bit. Not everything could be automated, but most of it could.

Quick note: I likely did much of this wrong. I'm not saying that these tools are the best way to go about this, just that its the tools I know how to use best. So, keep that in mind below.

Using Python, as well as libraries like `BeautifulSoup` and `FTFY`, I set to work parsing all of these pages. The thread was 88 pages long, each containing an unknown number of articles each. Sure, there was an index, but matching that to the pages and articles (especially without direct links to said articles) was going to be a challenge.

I first used `BeautifulSoup` to parse the HTML files and just grab the raw text of each post, and put those into Markdown files. Below is a good description from the ArchiveTeam wiki:

```
Markdown is a human-readable, popular markup language. Even if editors somehow disappear, it is still very human-readable, and so you should still be able to get the gist of it even if there are no tools to open it.
```

In addition, Markdown is an "independent" format for lack of a better term. Most text editors can open and view it, plus it converts somewhat easily back to HTML and other formats. I didn't want to use a "locked" format like DOCX (MS Word) or whatever the Mac version is.

Once the thread was split into posts, I did another pass and split the files up by article. Most of these stuck to "1 article, 1 post", so that was easy enough. Others were split across posts, requiring manual joining. And other posts had a number of articles in one, meaning those had to be split. There are a few I didn't bother splitting, whether they were all the same author, or so short it didn't make sense to split them.

I also added a header to each file, with info like author, source, and date. Having this at the top of each file will make processing much easier. Easy to grab the info and rename files, or generate a new index/table of contents. Also each one is labelled with a "category" for sorting purposes later (Album/Concert Review, News, Commentary, Interview, etc.)

## A Quick Note about Tools

While software tools and libraries have made much of this project possible, they aren't perfect. If everything was consistent formatting wise from the getgo, I likely could've used them more. However, the formatting (to put it nicely) is a mess. These articles were copied as text from whatever source, wrapped to 80 chars, posted in a forum, dumped to HTML, and parsed.

As mentioned, I used a library named `ftfy` to fix many encoding errors. Likely stemming from the HTML step above. The errors would usually show up as pointless gibberish when its actually supposed to be a non-english character or something similiar.

I also used standard python tools like the `re` library to batch fix stuff like the 80 character line length.

In addition, I used the Find and Replace tool in VS Code to fix a ton of other issues like swapping single quotes and backticks for double quotes.

## Alright back to the show

After I had all the articles in their own files, added headers, and fixed as many issues as I could using batch tools. The next step was going to be manually checking the files and fixing any other issues. Stuff that I really didn't want to trust to a program given how wildly inconsistent the source of the articles was. Joining incorrectly split paragraphs, properly formatting interviews to indicate speaker, and using block quotes for chunks of lyrics.

The latter two were personal preference. It makes interviews easier to read, and the lyrics in block quotes make them stand out from the rest of the text. I didn't want to make too many changes, only fix egregious errors and modify the formatting to make them easier to read.

## Some examples of changes

A few articles had to be replaced (either partially or completely).

Bruce's letter about the Stratocaster was a complete mess and nearly gibberish (this is copied directly from the thread without any changes):

```
are mg kinds of people in the world. Those that play
?_t;a;ocasters and those that play Ielgcasters. . .and the twain rarely meet.
Ron Stratocaster. .. Keith Richards. . .Gibsons, Tele's, etc. The
Strokes. . .a young man on a Stratocaster and a young man on a
Nils Lofgren, Steve Van Zandt. . .Strat's. .
```

and the corrected version which I copied from the source

```
There are two kinds of people in the world. Those that play Stratocasters and those that play Telecaster...and the twain rarely meet. Ron Wood...Stratocaster...Keith Richards...Gibsons, Tele's, etc. The Strokes...a young man on a Stratocaster and a young man on a Gibson...Nils Lofgren, Steve Van Zandt...Strat's
```

I dont know how it got this messed up. I can only assume due to HTML formatting? But I really wouldn't know.

In another case, there was a court case Bruce was in back in the early 2000s concerning bootleggers selling stolen studio tapes. Only part of the court case was included, but I dug up the entire thing and used that instead.

One more, the 1998 Charlie Rose interview only had a few paragraphs, I found a transcript and replaced it.

## Conclusion

Once I'm done the final manual pass and renaming, I'll include a final count here. The articles will be organized by type, and renamed with the header info.
