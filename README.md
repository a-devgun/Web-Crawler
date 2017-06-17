# WEB CRAWLER

This script can be used to crawl wikipedia. This script was created keeping the following conditions in mind - 

1. The seed url is - https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher
2. Key phrase is optional. We can either use concordance or go without one.
3. The pages to be crawled should have a prefix - 'https://en.wikipedia.org/wiki/'
4. The main wiki page 'https://en.wikipedia.org/wiki/Main_Page' is not to be crawled.
5. The pages with ':' or '#' are not to be crawled.
6. At max 1000 unique URL's are to be crawled or depth 5 whichever is earliest.
7. There should be a time delay of 1 second between consecutive page requests.

## SETUP

1. Download the latest version of python - "Python 3.5.0".
2. Install PyCharm.
3. Execute code. 

## ABOUT THE CODE

1. This crawler used Breadth First Search approach. That is first it will scan depth 1 and then all links of depth 2 and so on.

2. Relevant pages retreived is '514 of 27743' of the total number of pages.

3. File output is written in a file - 'links.txt' 

## CONTACT

Please contact 'Anirudh Devgun' at 'devgun.a@husky.neu.edu' in case of any issues.