Horsey Books
=====================

A collection of tools for generating weird phrases and auto-posting them to Tumblr.

Inspired by [@horse_ebooks](https://twitter.com/horse_ebooks).


Dependencies
---------------------

Python (2.5+, maybe?)

Includes a copy of [tumblpy (https://github.com/michaelhelmick/python-tumblpy)](https://github.com/michaelhelmick/python-tumblpy)


First, get some interesting text to remix
---------------------

Put some text files in the `text/` directory.  Ideas:

* [Erowid](http://www.erowid.org/experiences/) drug trip reports
 * use the included script `scrape-erowid.py` to download a bunch of trip reports
* New York Times articles
* Wikipedia articles
* Books (check [Project Gutenberg](http://www.gutenberg.org/))
* Erotic fan fiction
* Political writing & manifestos
* Sex education material
* Poetry
* Recipes
* [WebMD](http://www.webmd.com/depression/tc/seasonal-affective-disorder-sad-topic-overview)
* Chat logs
* Email (your own, or a mailing list)
* Plays and scripts

It's best to remove extra junk like tables of contents, footnotes, and timestamps.

The system needs to know where sentences begin and end.  It uses these rules, so format your text appropriately:

* Certain characters are sentence boundaries: `.` `!` `?`
* Sentences can span from one line to the next
* Blank lines are sentence boundaries

For example, if you have a file full of short single-line phrases and you want them to be treated as sentences instead of running together, you should end each line in a period or add a blank line between each line.

Then, generate new phrases
---------------------

Run `generate.py`.  It generates new phrases by scrambling up everything in the `text/` directory using [Markov Chains](http://www.cs.bell-labs.com/cm/cs/pearls/sec153.html) on a word-by-word basis.  It will ask you to approve or reject each result.  You can also enter your own phrases if you want a tweaked version of something the program suggested.

The results are appended to `queue.txt`.


Finally, create queued posts on Tumblr
---------------------

Set up Tumblr authentication:

1. Get [auth tokens from Tumblr](http://www.tumblr.com/oauth/apps)
2. Rename `tumblr_auth_tokens.example.py` to `tumblr_auth_tokens.py` and put your auth tokens in it.  Also set your username in there.

Now you can run `queue-entire-file-to-tumblr.py queue.txt` which will take each line of text from the text file and put it on Tumblr as a queued text post.  After that, you should delete `queue.txt` so you can generate new phrases without re-posting old phrases.

In your Tumblr account, make sure the queue is turned on so it will automatically publish a post every once in a while.


Tips
---------------------

The funniest results happen when you juxtapose text from very different sources.

The longer the input text file, the more often it will show up in the results.  You may need to trim down really long files to keep them from drowning out the shorter files.

If you have less than 40k of input text the results can be repetitive.


