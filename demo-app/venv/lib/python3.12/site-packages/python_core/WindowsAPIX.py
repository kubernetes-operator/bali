
"""
    @alexzander - 16.11.2020
    python file for accessing windows api
    
    current state: in development
"""

from win10toast import ToastNotifier

def Windows10Notification(title, message, duration, icon, threaded=1):
    notifier = ToastNotifier()
    notifier.show_toast(title=title, msg=message, duration=duration, icon_path=icon, threaded=threaded)