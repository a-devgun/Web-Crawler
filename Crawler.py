from urllib.request import urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
import time
import datetime

__author__ = 'Anirudh'

#################################################################################
#
# LinkParser: Class for calling and processing html page
#
#################################################################################
class LinkParser(HTMLParser):

    __links = []
    __page_source = ""

    def handle_starttag(self, tag, attrs):
        # Only parse 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, append it to class variables
                if name == "href":
                    self.__links.append(urljoin(self.baseURL, value))

    def handle_data(self, data):
        data_string = data.lower().strip()
        self.__page_source = self.__page_source + data_string

    def getLinks(self, url):

        self.__links = []
        self.__page_source = ""
        self.baseURL = url

        response = urlopen(url)
        crawled_time = datetime.datetime.now()

        if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
            self.feed((response.read().decode('UTF-8')))
            return self.__page_source, self.__links, crawled_time

        else:
            return "", [], crawled_time

#################################################################################
#
# crawler: This function takes in the seed url and the key phrase
#
#################################################################################
def crawler(url, word=None):

    max_pages = 1000
    max_depth = 5
    visited_pages = 0
    current_depth = 1
    total_pages = 0

    # totalPagesVisited will contain the total pages that have been parsed
    totalPagesVisited = []
    # pagesPerDepth will contain the pages for the next depth
    pagesPerDepth = []
    # pagesToVisit contains the pages that are yet to be parsed
    pagesToVisit = [url]


    last_time_crawled = datetime.datetime.now()
    parser = LinkParser()

    while visited_pages < max_pages and current_depth <= max_depth:

        if len(pagesToVisit) == 0:

            # Increment current depth when pages to visit becomes zero
            current_depth += 1
            print("Current depth is ", current_depth)

            # If reached the depth greater than 5 then exit the loop
            if current_depth > max_depth:
                break

            # Pages to visit should be updated with links from next depth
            pagesToVisit = list(set(pagesPerDepth) - set(totalPagesVisited))

        urlToVisit = pagesToVisit.pop()

        # Time delay for 1 second
        time_delay(last_time_crawled)

        try:
            data, links, last_time_crawled = parser.getLinks(urlToVisit)
        except:
            print("Error while opening link - ", urlToVisit)

        total_pages = total_pages + 1

        if word is None or data.find(word) > -1:

            # If Match is successful then increment visited pages
            visited_pages += 1
            totalPagesVisited.append(urlToVisit)
            links = url_check(set(links))
            pagesPerDepth = links + pagesPerDepth

        print("Found ", visited_pages, " out of ", total_pages, " pages searched & url is - ", urlToVisit)

    return totalPagesVisited


#################################################################################
#
# url_check: Method to check if url is as per instructions
#
#################################################################################
def url_check(links):

    temp_list = []
    for url in links:
        # If url contains more than one ':' or it contains '#' then ignore
        if url[6:].find(":") > -1 or url.find("#") > -1:
            continue

        # If url starts with 'https://en.wikipedia.org/wiki' then proceed
        # Ignore if the page is the main Page
        if url.startswith("https://en.wikipedia.org/wiki") and not url == "https://en.wikipedia.org/wiki/Main_Page":
            temp_list.append(url)

    return temp_list


#################################################################################
#
# write_to_file: This method is used to write to file "links.txt"
#
#################################################################################
def write_to_file(links):

    f = open("links.txt", "w")
    for url in links:
        f.write(url)
        f.write('\n')
    f.close()


#################################################################################
#
# time_delay: This method is used to give a dealy
#
#################################################################################
def time_delay(last_time_crawled):

    current_time = datetime.datetime.now()
    second_difference = datetime.timedelta.total_seconds(current_time - last_time_crawled)

    # If time difference between the last call and now is less than one second than sleep
    if second_difference < 1:
        time.sleep(1-second_difference)




#################################################################################
#
# THIS IS THE START OF THE PROGRAM
#
#################################################################################

seed_page = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"

keyphrase = input("Please enter the keyphrase to be searched or just press enter to search without one - ")

if keyphrase == "":
    keyphrase = None
    print("Searching without keyphrase")
else:
    print("Searching with - ", keyphrase)


start_time = datetime.datetime.now().replace(microsecond=0)

write_to_file(crawler(seed_page, keyphrase))

end_time = datetime.datetime.now().replace(microsecond=0)
print("Total time taken by the crawler is ", end_time-start_time)

#################################################################################