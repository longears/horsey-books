#!/usr/bin/env python

# Fetch random Erowid experience reports and save them into the "text/" folder.
# Runs forever until you hit control-C to quit it

from __future__ import division

import os, sys, time, urllib2, random, re, glob


#-------------------------------------------------------------------------------------------
# HELPERS AND SETUP

def writeFile(fn,data):
    f = file(fn,'w'); f.write(data); f.close()

def removeHTML(s):
    htmlRegexes = ['</?.{1,30}?>']
    for htmlRegex in htmlRegexes:
        s = re.sub(htmlRegex, '', s)
    return s

baseurl = 'http://www.erowid.org/experiences/exp.php?ID=%s'
maxID = 67000
dir = 'text/'
if not os.path.exists(dir):
    os.mkdir(dir)


#-------------------------------------------------------------------------------------------
# MAIN

print '---------------------------------------------------------------------------------\\'
print
print 'Downloading random Erowid experience reports'
print
print 'Hit control-C to quit'
print
while True:
    print '-----'
    time.sleep(1)
    id = random.randint(1,maxID)
    url = baseurl % id

    if glob.glob('%s%s *.txt'%(dir,id)):
        print 'We already downloaded that one.  Skipping.'
        continue

    print 'Fetching url: %s'%url
    page = urllib2.urlopen(url).read()

    if 'Unable to read experience ' in page:
        print 'No report at that ID number.'
        continue

    # find the list of substances
    dosechart = page.split('DoseChart')[1]
    lines = dosechart.splitlines()
    substances = []
    for line in lines:
        if '<td><a ' in line:
            substance = line.split("'>")[1].split('<')[0]
            substanceUrl = line.split("href='")[1].split("'")[0]
            substanceUrl = substanceUrl.split('/')[-2]
            substances.append(substanceUrl)
    substances = sorted(list(set(substances)))
    fn = dir + 'erowid ' + ' '.join([str(id)]+substances)
    title = page.split('class="title">')[1].split('</div>')[0]

    print 'Substances: %s'%substances
    print 'Filename: %s'%fn
    print 'Title: %s'%title

    # get main text and remove common unicode characters
    body = page.split('Start Body -->')[1].split('<!-- End Body')[0]
    body = body.replace('\r','')
    body = body.replace('\x92',"'")
    body = body.replace('\x93','"')
    body = body.replace('\x94','"')
    body = body.replace('\x97',' -- ')
    body = removeHTML(body)
    body = body.strip()

    writeFile(fn, title + '\n\n' + body + '\n')



