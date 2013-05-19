Horsey Books
=====================

Generates new phrases by scrambling up a bunch of input text using [Markov Chains](http://www.cs.bell-labs.com/cm/cs/pearls/sec153.html).  Lets you choose the best phrases and posts them to Tumblr.

Inspired by [@horse_ebooks](https://twitter.com/horse_ebooks).

Dependencies
---------------------

Python (2.5, maybe?)

Includes a copy of [https://github.com/michaelhelmick/python-tumblpy](https://github.com/michaelhelmick/python-tumblpy).


How to generate text
---------------------

1. Dump a bunch of `.txt` files in the `text/` directory.
2. Run `generate.py` which will generate a bunch of phrases.  Approve or reject each one.  The good ones are saved to `queue.txt`


How to create queued posts on Tumblr
---------------------

1. Rename `tumblr_auth_tokens.example.py` to `tumblr_auth_tokens.py`
2. Get [auth tokens from Tumblr](http://www.tumblr.com/oauth/apps) and put them in `tumblr_auth_tokens.py`
3. Run `queue-entire-file-to-tumblr.py yourfile.txt` which will take each line of text from the text file and put it on Tumblr as a queued text post.


Tips
---------------------

The funniest results happen when you juxtapose text from very different sources.

The longer the input text file, the more often it will show up in the results.  You may need to trim down really long files like ebooks to keep them from drowning out the shorter files.

Try to have at least 50k of input text or the results will be repetitive.


Ideas for input text
---------------------

* New York Times articles
* Wikipedia articles
* Books (check [Project Gutenberg](http://www.gutenberg.org/))
* [Erowid](http://www.erowid.org/experiences/) drug trip reports
* Fan fiction
* Political writing & manifestos
* Sex education material
* Poetry
* Recipes
* [WebMD](http://www.webmd.com/depression/tc/seasonal-affective-disorder-sad-topic-overview)

