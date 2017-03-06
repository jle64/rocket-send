"Gets astronomy picture of the day from astronomy magazine."
from datetime import date, timedelta

def get_message():
    # actually use yesterday picture as today one might not be available yet
    yesterday = date.today() - timedelta(1)
    base_url = 'http://www.astronomy.com/-/media/' + \
    'Images/Photo%20of%20Day/Large%20Images'
    img_url = '{0}/{1}/{2}/APOD{1}{2}{3}.jpg'.format(base_url,
                                                     yesterday.year,
                                                     yesterday.strftime('%m'),
                                                     yesterday.strftime('%d'))
    img_title = 'Astronomy magazine picture of the day'

    return {'title': img_title, 'text': img_url}
