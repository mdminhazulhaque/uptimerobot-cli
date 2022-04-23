#!/usr/bin/env python3

__author__ = "Md. Minhazul Haque"
__version__ = "0.2.0"
__license__ = "GPLv3"

"""
Copyright (c) 2020 Md. Minhazul Haque
This file is part of mdminhazulhaque/uptimerobot-cli
(see https://github.com/mdminhazulhaque/uptimerobot-cli).
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import click
import requests
import json
import os
from tabulate import tabulate as t

if 'UPTIMEROBOT_API_KEY' not in os.environ:
    print("UPTIMEROBOT_API_KEY not exported")
    exit(1)

UPTIMEROBOT_API_KEY = os.environ['UPTIMEROBOT_API_KEY']
UPTIMEROBOT_BASE_URL = 'https://api.uptimerobot.com'
UPTIMEROBOT_HEADERS = {
      'Cache-Control': 'no-cache',
      'Content-Type': "application/x-www-form-urlencoded"
    }

UPTIMEROBOT_API_GET_MONITORS = "/v2/getMonitors"
UPTIMEROBOT_API_NEW_MONITOR = "/v2/newMonitor"
UPTIMEROBOT_API_EDIT_MONITOR = "/v2/editMonitor"
UPTIMEROBOT_API_DELETE_MONITOR = "/v2/deleteMonitor"
UPTIMEROBOT_API_GET_ALERT_CONTACTS = "/v2/getAlertContacts"
UPTIMEROBOT_API_EDIT_ALERT_CONTACTS = "/v2/editAlertContact"
UPTIMEROBOT_PAGE_LEN = 50

def _make_request(api_endpoint, payload):
    payload['api_key'] = UPTIMEROBOT_API_KEY
    payload['format'] = 'json'
    response = requests.post(UPTIMEROBOT_BASE_URL + api_endpoint, data=payload, headers=UPTIMEROBOT_HEADERS)        
    return response.json()

@click.group()
def app():
    pass

@app.command(help="Get all monitors")
@click.option('--all', '-a', is_flag=True, default=False, help="Shows all pages")
@click.option('--offset', '-o', type=click.INT, default=0, help="Offset for pagination")
def get_monitors(all, offset):
    payload = {
        'logs': 0,
        'offset': offset,
        'alert_contacts': 1,
    }
    _data = []
    _headers = ['id', 'friendly_name', 'url', 'interval', 'alert_contacts']
    while True:
        data = _make_request(UPTIMEROBOT_API_GET_MONITORS, payload)
        if data['stat'] == 'ok':            
            for monitor in data['monitors']:
                alert_contacts = ",".join(
                    ac['id'] for ac in monitor['alert_contacts']
                    #ac['value'].split('@')[0] for ac in monitor['alert_contacts']
                )
                _data.append([
                    monitor['id'],
                    monitor['friendly_name'],
                    monitor['url'],
                    monitor['interval'],
                    alert_contacts
                ])
            if not all:
                break
            elif len(data['monitors']) < UPTIMEROBOT_PAGE_LEN:
                break
            else:
                payload['offset'] += UPTIMEROBOT_PAGE_LEN
    print(t(_data, headers=_headers, tablefmt="github"))

@app.command(help="Create a monitor")
@click.option('--url', '-u', type=click.STRING, required=True, help="The URL to monitor")
@click.option('--name', '-n', type=click.STRING, required=True, help="Friendly name for the monitor")
@click.option('--interval', '-i', type=click.INT, required=False, help="Interval in seconds")
@click.option('--alerts', '-a', type=click.STRING, required=False, help="Alert contacts")
def new_monitor(url, name, interval, alerts):
    payload = {
        'type': 1,
        'url': url,
        'interval': interval,
        'friendly_name': name,
    }
    data = _make_request(UPTIMEROBOT_API_NEW_MONITOR, payload)
    if data['stat'] == 'ok':
        print(data['monitor']['id'])
    else:
        print("Failed")
        exit(1)

@app.command(help="Edit a monitor")
@click.option('--id', '-i', type=click.STRING, required=True, help="The ID of the monitor")
@click.option('--url', '-u', type=click.STRING, required=False, help="The URL to monitor")
@click.option('--name', '-n', type=click.STRING, required=False, help="Friendly name for the monitor")
@click.option('--interval', '-f', type=click.INT, required=False, help="Interval in seconds")
@click.option('--alert_contacts', '-a', type=click.STRING, required=False, help="Alert contacts")
def edit_monitor(id, name, url, interval, alert_contacts):
    payload = {
        'id': id
        }
    if name:  payload['friendly_name'] = name
    if alert_contacts:
        if "," in alert_contacts:
            alert_contacts = "-".join([ac + "_0_0" for ac in alert_contacts.split(",")])
            payload['alert_contacts'] = alert_contacts
        else:
            payload['alert_contacts'] = alert_contacts + "_0_0"
    if interval:       payload['interval'] = interval
    if url:            payload['url'] = url
    data = _make_request(UPTIMEROBOT_API_EDIT_MONITOR, payload)
    
    if data['stat'] == 'ok':
        exit(0)
    else:
        print("Failed")
        exit(1)

@app.command(help="Delete a monitor")
@click.option('--id', '-i', type=click.STRING, required=True, help="The URL to monitor")
def delete_monitor(id):
    payload = {
        'id': id
    }
    data = _make_request(UPTIMEROBOT_API_DELETE_MONITOR, payload)
    if data['stat'] == 'ok':
        exit(0)
    else:
        print("Failed")
        exit(1)

@app.command(help="Get Alert contacts")
def get_alert_contacts():
    payload = {}
    data = _make_request(UPTIMEROBOT_API_GET_ALERT_CONTACTS, payload)
    if data['stat'] == 'ok':
        _data = []
        _headers = ['id', 'friendly_name', 'value']

        for ac in data['alert_contacts']:
            _data.append([ac['id'], ac['friendly_name'], ac.get('value')])
        
        print(t(_data, headers=_headers, tablefmt="github"))
        exit(0)
    else:
        print("Failed")
        exit(1)
        
@app.command(help="Edit Alert contacts")
@click.option('--id', '-i', type=click.STRING, required=True, help="ID of alert contact")
@click.option('--name', '-n', type=click.STRING, required=False, help="Friendly name of alert contact")
@click.option('--value', '-v', type=click.STRING, required=False, help="Value of alert contact")
@click.option('--status', '-s', type=click.STRING, required=True, help="Status of alert contact")
def edit_alert_contact(id, name, value, status):
    payload = {
        'id': id,
        'status': status
    }
    if name: payload['friendly_name'] = name
    if value: payload['value'] = value
    data = _make_request(UPTIMEROBOT_API_EDIT_ALERT_CONTACTS, payload)
    if data['stat'] == 'ok':
        exit(0)
    else:
        print("Failed")
        exit(1)

if __name__ == "__main__":
    app()
