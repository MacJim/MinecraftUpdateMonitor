import os

def showSystemNotification(title, text):
    # Source: https://stackoverflow.com/questions/17651017/python-post-osx-notification
    # Shows a macOS notification with AppleScript.
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
