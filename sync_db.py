import sys
import requests

from CherryHarvestAPI.models import Picker, Lug, Block, PickerNumber, OrchardLoad, Tag

HEADERS = {'content-type' : 'application/json'}

def sync_db():
    if len(sys.argv)!=4:
        return
    server, username, password = sys.argv[1:]
    auth = (username, password)

    r = requests.get(server, auth=auth)
    if r.status_code != 200:
        raise IOError('server address not valid')
    urls = r.json()

    # for l in Picker.query.all():
    #     j = {'id':l.id,
    #         'first_name': l.first_name,
    #         'last_name': l.last_name}
    #     r = requests.post(urls['pickers'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{} already exists'.format(l.id)

    # for p in PickerNumber.query.all():
    #     j = {'id':p.id,
    #          'picker_id': p.picker_id,
    #          'tag_epcs': [t.epc for t in p.current_cards]}
    #     r = requests.post(urls['picker_numbers'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{} already exists'.format(p.id)
    #         r = requests.patch('{}{}/'.format(urls['picker_numbers'],p.id),json=j, headers=HEADERS, auth=auth)
    #     if r.status_code not in xrange(200,300):
    #         print r.status_code


    # for t in Block.query.all():
    #     j = {'id':t.id,
    #         'variety': t.variety}
    #     r = requests.post(urls['blocks'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{} already exists'.format(t.id)
    #         r = requests.patch('{}{}/'.format(urls['blocks'],t.id),json=j, headers=HEADERS, auth=auth)
    #     if r.status_code not in xrange(200,300):
    #         print r.status_code

    # for l in OrchardLoad.query.all():
    #     j = {'id':l.id,
    #          'lugs' : [{
    #             'id' : lug.id,
    #             'block_id' : lug.block_id,
    #             'weight' : lug.weight,
    #             'lug_pickers' : [{'picker_id':lp.picker_id,
    #                               'contribution':lp.contribution}
    #                              for lp in lug.lug_pickers]}
    #                    for lug in l.lugs],
    #          'arrival_time' : str(l.arrival_time)}
    #     r = requests.post(urls['orchard_loads'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{} already exists'.format(l.id)
    #         r = requests.patch('{}{}/'.format(urls['orchard_loads'],l.id),json=j, headers=HEADERS, auth=auth)
    #     if r.status_code not in xrange(200,300):
    #         print r.status_code
    #         print r.text
    #         break

    # for t in Tag.query.all():
    #     j = {'epc':t.epc,
    #         'current_picker_number_id':t.current_picker_number_id,}
    #     r = requests.post(urls['tags'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{}: {}'.format(t.epc, r.json())
    #         r = requests.patch('{}{}/'.format(urls['tags'],t.epc),json=j, headers=HEADERS, auth=auth)
    #     if r.status_code not in xrange(200,300):
    #         print r.status_code
    #         print r.json()
    #         break


    # for l in Lug.query.all():
    #     j = {'id':l.id,
    #         'weight': l.weight,
    #         'block_id': l.block_id,
    #         'orchard_load_id': l.orchard_load_id}
    #     r = requests.post(urls['lugs'], json=j, headers=HEADERS, auth=auth)
    #     if r.status_code == 409:
    #         print '{} already exists'.format(l.id)



if __name__ == '__main__':
    try:
        sync_db()
    except IOError, e:
        print e.message