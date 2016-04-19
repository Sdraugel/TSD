
import os
import win32com.client
from win32com.client import Dispatch, constants

DEBUG = 1

class TSD_Email:

    def send_email(machine, value):
        threshold = "0"

        if (value > 94):
            threshold = "97"
        else:
            threshold = "94"

        

        SERVER = "9a8394cd-ddc2-4a3c-9433-3d6185c21c62@us.bosch.com"
        FROM = "fixed-term.Steven.Draugel@us.bosch.com"
        TO = "fixed-term.Steven.Draugel@us.bosch.com"
        SUBJECT = "Test Stand Diagnostics"
        TEXT = "Hello\n This is an email notification. Machine " + machine
        TEXT += "'s first pass percentage has fallen below the threshold of " + threshold
        TEXT += " %.\n \n \n Thank you"

        const=win32com.client.constants
        olMailItem = 0x0
        obj = win32com.client.Dispatch("Outlook.Application")
        newMail = obj.CreateItem(olMailItem)
        newMail.Subject = SUBJECT
        newMail.Body = TEXT
        newMail.To = TO

        # for debugging
        newMail.display()

        # for runtime
        #newMail.Send()
        return

#TSD_Email.send_email("TS2000", 97)
