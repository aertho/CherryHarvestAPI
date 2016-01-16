import sys

import requests
from CherryHarvestAPI import models
from CherryHarvestAPI.database import db_session, destroy_db, init_db


def populate_model_from_url(url, auth, model, fields):
    try:
        r = requests.get(url, auth=auth)
    except requests.ConnectionError:
        raise IOError('failed to download {}'.format(url))
    if r.status_code != 200:
        IOError('failed to download {}'.format(url))
        return

    for i in r.json():
        field_values = {f : i[f] for f in fields if not('id' in f and i[f] == 0)}
        m = model(**field_values)
        db_session.add(m)
    db_session.commit()

def backup(cha_server, username, password):
    destroy_db()
    init_db()
    auth = (username, password)
    try:
        r = requests.get(cha_server, auth=auth)
    except requests.ConnectionError:
        print 'failed to connect'
        return
    if r.status_code != 200:
        print 'failed to connect'
        return

    urls = r.json()
    try:
        populate_model_from_url(urls['pickers'], auth, models.Picker, ['id','first_name','last_name'])
        populate_model_from_url(urls['blocks'], auth, models.Block, ['id','variety'])
        populate_model_from_url(urls['picker_numbers'], auth, models.PickerNumber, ['id','picker_id'])
        populate_model_from_url(urls['orchard_loads'], auth, models.OrchardLoad, ['id','arrival_time', 'departure_time'])
        populate_model_from_url(urls['lugs'], auth, models.Lug, ['id', 'weight', 'block_id', 'orchard_load_id',
                                                                 'farm_load_id', 'current_status'])
        populate_model_from_url(urls['tags'], auth, models.Tag, ['epc', 'current_picker_number_id', 'current_lug_id'])
        populate_model_from_url(urls['lug_pickers'], auth, models.LugPicker, ['lug_id', 'picker_id', 'contribution'])
    except IOError, e:
        print e.message
        return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'invalid parameters'
        sys.exit()
    cha_server, username, password = sys.argv[1:]
    backup(cha_server, username, password)
