# A simple script that archives any site you pass it
import urllib2, re, sys
import time

if not sys.argv[1]:
    print "Welcome to alexandria.py. I take a sitemap, usually found at <site>/sitemap.xml and submit everything I find there to web.archive.org. Before feeding me a sitemap, check the url in your browser. Sometimes you'll find links to the actual sitemaps in different parts./n"
    site = raw_input("What site would you like to archive? Paste the entire url./n> ")
else:
    site = sys.argv[1]

# this block is to retain progress in case something goes wrong. Like my internet shitting out.
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

try:
    doc = open("progress.txt", 'r')
    print "Finding progress.. ."
    pass
except Exception:
    doc = open("progress.txt", 'a+')
    doc.writelines([site+"\n", '0'])
    pass

doc.seek(0)
lines = doc.readlines()
doc.close()
progress = int(lines[1])
print "Restarting at index: " + str(progress)

# gets the sitemap and extracts all the urls in it to a list
response = urllib2.urlopen(sys.argv[1])
print "Searching: " + sys.argv[1]
html = response.read()
print "Success!"
try:
    urls = re.findall('(?<=<loc>)(.*)(?=</loc>)', html)
except AttributeError:
    urls = 'Did not find any! Did you paste the righ url?'
print "Archiving... ."

# hits the web archive api to save each url

for url in urls:
    progress += 1
    print progress
    urllib2.urlopen('https://web.archive.org/save/'+ url)
    time.sleep(1) # the polite thing to do
    prog_str = str(progress)
    replace_line("progress.txt", 1, prog_str)
    print url
