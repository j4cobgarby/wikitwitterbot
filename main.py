import twitter, wikipediaapi, urllib.request, json, time

configfile = open("config", "r")
config = configfile.readlines()
config = [s.split("=")[1].rstrip() for s in config]
# Amount of minutes for which to sleep
POST_DELAY_MINUTES = int(config[4])

# To access wikipedia
wiki = wikipediaapi.Wikipedia("en")
# To access twitter
api = twitter.Api(
    consumer_key        =config[0],
    consumer_secret     =config[1],
    access_token_key    =config[2],
    access_token_secret =config[3]
)
# To get random pages
req = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&format=json")

def dopost():
    '''
    Make the actual post - randomly selects a page using the wikipedia api directly by querying some data,
    then uses the wikipedia api module I'm importing to get the url from the page name.
    Then, it constructs a string to post to twitter, in the format:

      <Link to the wikipedia page>
      <The summary of the wikipedia page, but cropped to fit a tweet with four characters left> ...
    '''
    # Query the wikipedia api
    random_json_bytes = urllib.request.urlopen(req).read()
    random_json_decoded = random_json_bytes.decode("utf-8")
    random_json = json.loads(random_json_decoded)

    # Get the title of the random wikipedia page
    title = random_json["query"]["random"][0]["title"]
    page = wiki.page(title)

    # Send the actual post
    api.PostUpdate((page.fullurl + "\n" + page.summary)[:276] + " ...")

    # Visual confirmation, could replace this with perhaps a write to a log file, if wanted!
    print("Post good")

def main():
    '''
    Repeatedly posts things, every POST_DELAY_MINUTES minutes.
    '''
    while True:
        # Make a post to twitter
        dopost()
        # time.sleep uses seconds, so convert minutes to seconds
        time.sleep(POST_DELAY_MINUTES * 60)

if __name__ == "__main__":
    main();
