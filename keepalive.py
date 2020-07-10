# create exe with: pyinstaller --onefile --distpath ./ keepalive.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
import json

app_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
driver_path = app_path + os.path.sep + 'drivers' + os.path.sep
settings_file = app_path + os.path.sep + 'settings.json'

settings = {   
    "refresh_minutes": 10,
    "urls": [
        "http://www.service-now.com",
        "http://www.microsoft.com"
    ]
}
if not os.path.exists(settings_file):
    # Create the settings file
    print('Creating default settings.json file. You can manually edit this file later to change the URLs and refresh time')
    settings['refresh_minutes'] = int(input('How often should the windows refresh (in minutes)? '))
    settings['urls'] = input('Enter the URLs separated by a space. Be sure to include http(s)://\n').split()
    print('Saving file...\n')
    with open(settings_file, 'w') as f:
        f.write(json.dumps(settings, indent=2))

else:
    # Load the settings
    print('Loading Settings')
    try:
        with open(settings_file) as f:
            settings = json.loads(f.read())
    except Exception as e:
        print("ERROR: Could not load JSON file")
        print('  > ' + str(e))
        input('Press ENTER to exit')
        exit()




### FIREFOX:
# browser = webdriver.Firefox(driver_path + 'geckodriver.exe')
# for url in settings.get('urls'):
#     browser.get(url)
#     browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') # Keys.COMMAND
#     browser.switch_to.window(browser.window_handles[-1])
# # keep each tab alive indefinitely
# while True:
#     time.sleep(refresh_frequency * 60)
#     for handle in browser.window_handles:
#         browser.switch_to.window(handle)
#         browser.find_element_by_tag_name('body').send_keys(Keys.F5)


### IE: Open each URL in a new window. Automating tabs doesn't work in IE, but works in other browsers
browsers = []
try:
    for url in settings.get('urls'):
        print('Opening IE 11 Window for {}'.format(url))
        b = webdriver.Ie(driver_path + 'IEDriverServer.exe')
        b.get(url)
        browsers.append(b)
except Exception as e:
    print('ERROR: Make sure all IE zones have the same "protected mode" setting under Internet Options > Security')
    print('  > ' + str(e))
    input('Press ENTER to exit')
    exit()

### keep each tab alive indefinitely
print('\nRefresh will occur every {} minute(s). Press CTRL+C to Pause or Exit'.format(settings.get('refresh_minutes')))
while True:
    try:
        time.sleep(settings.get('refresh_minutes') * 60)
        print('Refreshing Windows...')
        for browser in browsers:
            browser.find_element_by_tag_name('body').send_keys(Keys.F5)
    except KeyboardInterrupt:
        res = input('Refresh loop paused. Press ENTER to continue or "y" to exit: ')
        if res.lower() in ['y', 'x', 'e']:
            break
        else:
            print('\nRefresh will occur every {} minute(s). Press CTRL+C to Pause or Exit'.format(settings.get('refresh_minutes')))
        
### Exit browsers
# print('Closing browser sessions and exiting...')
# for browser in browsers:
#     #browser.close()
#     browser.quit()
