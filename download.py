###
# Dependencies
###
import bs4
import wget
import json
from selenium import webdriver

# URLS array
# List of urls for Adobe Lightroom Shares
# Example urls: https://lightroom.adobe.com/shares/SHAREID or https://adobe.ly/SHAREID
URLS = []

# Chrome Driver Path
# Path to local chromedriver
DRIVER = "/usr/local/bin/chromedriver"

###
# Get HTML from url
#
# @param args
# args.driver: Webdriver to use
# args.url: Url/link for target html
# args.target: Target html container element
# @return html
###
def getHTML(args):

    # Arguments validation
    if 'driver' not in args:
        print('getHTML: Missing driver argument')
        return
    if 'url' not in args:
        print('getHTML: Missing url argument')
        return

    # Try to make request
    try:
        # Set browser options 
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--enable-javascript")

        # Open webdriver
        print('Opening browser...')
        browser = webdriver.Chrome(args['driver'], options=options)

        # Make browser request
        print('Requesting... ' + args['url'])
        browser.get(args['url'])

        # Parse HTML
        print('Parsing html...')
        html = bs4.BeautifulSoup(browser.page_source, 'html.parser')

        # Quit/close driver instance
        print('Closing browser...')
        browser.quit()

    # If error is found
    except Exception as e:
        print(e)
        html = None

    # Return data
    return html


###
# Process url list
# For each URL in URL list
###
for url in URLS:

    # Print status
    print('Now Processing: ' + url)

    # Get base HTML
    html = getHTML({
        "driver": DRIVER,
        "url": url
    })

    # Save variable data
    space_id = html.find(property='og:url').get('content').replace('https://lightroom.adobe.com/shares/', '')
    album_id = html.find(class_='cover').parent.parent.get('id')
    album_name = html.find(class_='cover').get('title')
    assets_url = "https://lightroom.adobe.com/v2/spaces/" + space_id + "/albums/" + album_id + "/assets?embed=asset%3Buser&order_after=-&exclude=incomplete&subtype=image%3Bvideo%3Blayout_segment"

    # Try additonal data requests
    try: 

        # Get ablum data
        data = getHTML({
            "driver": DRIVER,
            "url": assets_url,
        })

        # Convert data to json object
        data = data.find("pre").text.replace("while (1) {}", '')
        data = json.loads(data)

        # For each item in array
        for item in data['resources']:
            # Try to download asset image
            try: 
                # Print status
                print("\n" + "Downloading image " + item['asset']['id'])
                # Download image
                image = wget.download("https://lightroom.adobe.com/v2c/spaces/" + space_id + "/" + item['asset']['links']['/rels/rendition_type/2048']['href'], out=album_name.replace(' ', '-') + '_' + item['asset']['id'] + '.jpg')
            except:
                # Print status
                print('Error with image' + album_name + item['asset']['id'])
                # Continue 
                pass

    except:
        # Print status
        print('Error with json.' + space_id)
        # Continue
        pass

###
# DONE
###
exit('DONE')

