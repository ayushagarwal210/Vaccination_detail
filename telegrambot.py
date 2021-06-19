import re
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vaccination.settings'
django.setup()

from home.helpers import *
from home.models import *
from telegram.ext import *

API_KEY = '1841445657:AAHl5aYttd-W9WiT2_WfYWnRvvzfqosoJ4w'


def isValidPinCode(pinCode):

    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"

    p = re.compile(regex)

    if (pinCode == ''):
        return False

    m = re.match(p, pinCode)

    if m is None:
        return False
    else:
        return True


def num_there(s):
    return any(i.isdigit() for i in s)


print('bot started')


def handle_message(update, context):
    text = str(update.message.text).lower()

    if num_there(text):
        if isValidPinCode(text):
            cowin_objs = CowinData.objects.filter(pincode=text)

            if not cowin_objs.exists():
                get_cowin_data_by_pincode(text)
                cowin_objs = CowinData.objects.filter(pincode=text)

            message = f"""Total '{cowin_objs.count()}' slots found in you pincode \n\n"""

            for cowin_obj in cowin_objs:
                message += f"""'Place' - {cowin_obj.name}   'Minimum Age Limit' - {cowin_obj.min_age_limit}   'Paid/Free' - {cowin_obj.fee_type} 'Fee' - {cowin_obj.fee}   'Available Capacity' - {cowin_obj.available_capacity}   'Capacity Dose1' - {cowin_obj.available_capacity_dose1}   'Capacity Dose 2' - {cowin_obj.available_capacity_dose2}   'Vaccine' - {cowin_obj.vaccine} \n\n  """

            update.message.reply_text(f"{message}")
            return

        else:
            update.message.reply_text(f"Enter a valid pincode")
            return

    update.message.reply_text(
        f"Hi, {update['message']['chat']['first_name']} Enter your pincode for vaccination details")


if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(1.0)
    updater.idle()
