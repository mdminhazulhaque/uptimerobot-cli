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
        'Cche-Control': "no-cache",
        'Content-Type': "application/x-www-form-urlencoded"
    }

UPTIMEROBOT_API_GET_MONITORS = "/v2/getMonitors"
UPTIMEROBOT_API_NEW_MONITOR = "/v2/newMonitor"
UPTIMEROBOT_API_EDIT_MONITOR = "/v2/editMonitor"
UPTIMEROBOT_API_DELETE_MONITOR = "/v2/deleteMonitor"
UPTIMEROBOT_PAGE_LEN = 50

def _make_request(api_endpoint, payload):
    payload['api_key'] = UPTIMEROBOT_API_KEY
    payload['format'] = 'json'
    response = requests.post(UPTIMEROBOT_BASE_URL + api_endpoint, data=payload, headers=UPTIMEROBOT_HEADERS)        
    return response.json()

@click.group()
def app():
    pass

@app.command(help="List all monitors")
@click.option('--all', '-a', is_flag=True, default=False, help="Shows all pages")
@click.option('--offset', '-o', type=click.INT, default=0, help="Offset for pagination")
def list(all, offset):
    payload = {
        'logs': 0,
        'offset': offset
    }
    _data = []
    _headers = ['id', 'friendly_name', 'url', 'interval']    
    while True:
        data = _make_request(UPTIMEROBOT_API_GET_MONITORS, payload)
        if data['stat'] == 'ok':            
            for monitor in data['monitors']:
                _data.append([
                    monitor['id'],
                    monitor['friendly_name'],
                    monitor['url'],
                    monitor['interval']
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
def create(url, name, interval, alerts):
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
@click.option('--id', '-i', type=click.STRING, required=True, help="The URL to monitor")
@click.option('--url', '-u', type=click.STRING, required=False, help="The URL to monitor")
@click.option('--name', '-n', type=click.STRING, required=False, help="Friendly name for the monitor")
@click.option('--interval', '-f', type=click.INT, required=False, help="Interval in seconds")
@click.option('--alert_contacts', '-a', type=click.STRING, required=False, help="Alert contacts")
def edit(id, name, url, interval, alert_contacts):
    payload = {
        'id': id
        }
    if name:  payload['friendly_name'] = name
    if alert_contacts: payload['alert_contacts'] = alert_contacts
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
def delete(id):
    payload = {
        'id': id
    }
    data = _make_request(UPTIMEROBOT_API_DELETE_MONITOR, payload)
    if data['stat'] == 'ok':
        exit(0)
    else:
        print("Failed")
        exit(1)

if __name__ == "__main__":
    app()
