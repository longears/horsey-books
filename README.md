Horsey Books
=====================

Generates new phrases by scrambling up a bunch of input text using [Markov Chains](http://www.cs.bell-labs.com/cm/cs/pearls/sec153.html).  Lets you choose the best phrases and posts them to Tumblr.

Inspired by [@horse_ebooks](https://twitter.com/horse_ebooks).

Dependencies
---------------------

Python (2.5, maybe?)


How to use it
---------------------

1. Dump a bunch of `.txt` files in the `text/` directory.
2. Run `generate.py` which will generate a bunch of phrases.  Approve or reject each one.  The good ones are saved to `queue.txt`
3. (coming soon) Run `post-to-tumblr.py` to post the first item from the queue to Tumblr.


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

