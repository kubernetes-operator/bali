
def DownloadImageFromURL(url, destination):
    """ returns the absolute path of the destination """
    if type(url) != str or type(url) != str:
        raise TypeError("incorrect type.")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("not valid url.")
    
    if "/" not in destination and "\\" not in destination:
        raise ValueError
    
    import requests
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    
    # try:
    #     with open(destination, "xb+") as binaryfile:
    #         binaryfile.write(response.raw.data)
    # except FileExistsError:
    with open(destination, "wb") as binaryfile:
        binaryfile.write(response.raw.data)
    return destination
    
def DownloadFileFromURL(url, folder, headers, name="", extension=""):
    import requests
    response = requests.get(url, headers=headers, stream=True)
    response.raw.decode_content = True
    
    if name == "" and extension == "":
        items = url.split("/")
        filename = items[len(items) - 1]
        fullpath = folder + filename
        del items, filename
    else:
        if folder.endswith("\\"):
            fullpath = folder + name + "." + extension
        else:
            fullpath = folder + "\\" + name + "." + extension
            
    with open(fullpath, "wb") as binaryfile:
        binaryfile.truncate(0)
        binaryfile.write(response.raw.data)
    return fullpath
    
def GetYoutubeVideoThumbnailURL(url):
    if type(url) != str:
        raise TypeError
    
    if not url.startswith("https://www.youtube.com/watch?v="):
        raise ValueError
    
    
    import requests, json
    from bs4 import BeautifulSoup
    from requests_html import HTMLSession
    
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    
    soup = BeautifulSoup(response.html.html, "html.parser")
    webelement = soup.find("script", attrs={"class": "style-scope ytd-player-microformat-renderer"})
    
    data = json.loads(webelement.text)
    return data["thumbnailUrl"][0]