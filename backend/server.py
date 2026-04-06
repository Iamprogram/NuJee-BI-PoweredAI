#!/usr/bin/env python3
"""Minimal GDACS RSS proxy API for ReckonLight dashboard.

Endpoints:
- GET /api/gdacs : returns parsed disasters from GDACS RSS 24h feed.
- GET /healthz   : readiness check.
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

GDACS_RSS_URL = os.getenv('GDACS_RSS_URL', 'https://www.gdacs.org/xml/rss_24h.xml')
CACHE_TTL_SECONDS = int(os.getenv('GDACS_CACHE_TTL_SECONDS', '360'))
HOST = os.getenv('GDACS_HOST', '0.0.0.0')
PORT = int(os.getenv('GDACS_PORT', '8000'))

CACHE: dict[str, Any] = {
    'last_fetch_epoch': 0,
    'payload': {
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'source': GDACS_RSS_URL,
        'events': [],
        'summary': {
            'activeDisasters': 0,
            'peopleAffected': 'N/A',
            'mostAffectedRegion': 'N/A',
            'trend': 'Unknown',
        },
        'error': None,
    },
}


def _severity_from_text(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    if 'red alert' in text:
        return 'red'
    if 'orange alert' in text:
        return 'orange'
    return 'green'


def _type_from_text(text: str) -> str:
    low = text.lower()
    if 'cyclone' in low or 'storm' in low:
        return 'cyclone'
    if 'flood' in low:
        return 'flood'
    if 'wildfire' in low or 'fire' in low:
        return 'wildfire'
    if 'earthquake' in low:
        return 'earthquake'
    return 'hazard'


def _extract_affected(description: str) -> str:
    # Best-effort extraction from plain text patterns.
    m = re.search(r'(\d[\d,\.\s]{1,20})\s*(people|persons|population)', description, flags=re.I)
    if not m:
        return 'N/A'
    return m.group(1).strip().replace('  ', ' ')


def _parse_coordinates(item_xml: ET.Element) -> dict[str, float | None]:
    ns = {
        'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    }
    lat = item_xml.findtext('geo:lat', default='', namespaces=ns)
    lon = item_xml.findtext('geo:long', default='', namespaces=ns)
    try:
        return {'lat': float(lat), 'lon': float(lon)}
    except ValueError:
        return {'lat': None, 'lon': None}


def fetch_gdacs_events() -> dict[str, Any]:
    req = Request(GDACS_RSS_URL, headers={'User-Agent': 'ReckonLight/1.0 (+dashboard-feed)'})
    with urlopen(req, timeout=20) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    channel = root.find('channel')
    if channel is None:
        raise ValueError('Invalid RSS payload: channel not found')

    items = channel.findall('item')
    events: list[dict[str, Any]] = []

    for idx, item in enumerate(items):
        title = (item.findtext('title') or '').strip()
        description = (item.findtext('description') or '').strip()
        link = (item.findtext('link') or '').strip() or 'https://www.gdacs.org/'
        pub_date = (item.findtext('pubDate') or '').strip()

        full_text = f'{title} {description}'
        event_type = _type_from_text(full_text)
        severity = _severity_from_text(title, description)
        coords = _parse_coordinates(item)
        location_guess = 'Unknown location'
        title_parts = [x.strip() for x in title.split(' for ', 1)]
        if len(title_parts) > 1:
            location_guess = title_parts[1]

        events.append(
            {
                'id': f'gdacs-{idx}',
                'title': title,
                'summary': description[:220] if description else 'No details provided by feed source.',
                'location': location_guess,
                'severity': severity,
                'type': event_type,
                'timestamp': pub_date,
                'affectedPopulation': _extract_affected(description),
                'gdacsUrl': link,
                'coordinates': coords,
            }
        )

    summary = {
        'activeDisasters': len(events),
        'peopleAffected': 'Live feed',
        'mostAffectedRegion': 'See live incident feed',
        'trend': 'Live',
    }

    return {
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'source': GDACS_RSS_URL,
        'events': events,
        'summary': summary,
        'error': None,
    }


def get_cached_payload() -> dict[str, Any]:
    now = int(time.time())
    age = now - int(CACHE['last_fetch_epoch'])
    if age < CACHE_TTL_SECONDS and CACHE['payload']['events']:
        return CACHE['payload']

    try:
        payload = fetch_gdacs_events()
        CACHE['payload'] = payload
        CACHE['last_fetch_epoch'] = now
    except (URLError, TimeoutError, ET.ParseError, ValueError) as err:
        CACHE['payload'] = {
            **CACHE['payload'],
            'updatedAt': datetime.now(timezone.utc).isoformat(),
            'error': f'Unable to refresh GDACS feed: {err}',
        }
    return CACHE['payload']


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (required by BaseHTTPRequestHandler)
        if self.path == '/healthz':
            self._send_json(200, {'ok': True, 'service': 'gdacs-proxy'})
            return

        if self.path == '/api/gdacs':
            payload = get_cached_payload()
            self._send_json(200, payload)
            return

        self._send_json(404, {'error': 'Not found'})


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'GDACS API listening on http://{HOST}:{PORT}')
    server.serve_forever()


if __name__ == '__main__':
    run()
