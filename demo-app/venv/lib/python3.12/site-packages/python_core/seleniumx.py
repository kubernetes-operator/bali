
from selenium import webdriver
    
def GetChromeDriver(chrdv_path: str, useragent: dict, icognito=1):
    options = webdriver.ChromeOptions()
    
    # only on windows
    options.binary_location = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
    options.add_argument("user-agent={}".format(useragent["User-Agent"]))
    
    if icognito:
        options.add_argument("--incognito")
        
    driver = webdriver.Chrome(executable_path=chrdv_path, options=options)
    return driver