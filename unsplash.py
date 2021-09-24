#!/usr/bin/env python3
""" Allow easier access to the unsplash API """
from typing import Dict, List, Literal, Union
import requests


class UnsplashImage:
    """ Represent an image available via Unsplash """
    img_format = Literal[
        'gif',
        'jp2',
        'jpg',
        'json',
        'jxr',
        'pjpg',
        'mp4',
        'png',
        'png8',
        'png32',
        'webm',
        'webp',
        'blurhash',
        None,
    ]

    crop_type = Literal[
        'top',
        'bottom',
        'left',
        'right',
        'faces',
        'entropy',
        'edges',
        None,
    ]

    edits_type = Dict[str, Union[None, int, str]]

    orientation_type = Literal['landscape', 'portrait', 'squarish', None]

    def __init__(self, raw_url: str, user: str = None):
        self.raw_url = raw_url
        self.edits: UnsplashImage.edits_type = {
            'width': None,
            'height': None,
            'format': None,
            'fit': None,
        }
        self.crop = None
        self.user = user

    def adjust(self, width: Union[int, None] = None,
               height: Union[int, None] = None,
               format_: img_format = None,
               crop: List[crop_type] = None,
               fit: Union[str, None] = None):
        """ Specify adjustments from default for the image """
        if width:
            self.edits['width'] = width
        if height:
            self.edits['height'] = height
        if format_:
            self.edits['format'] = format_
        if crop:
            self.crop = crop
        if fit:
            self.edits['fit'] = fit

    @property
    def url(self):
        """ Generate a url for the current image, with edits """
        image_url = self.raw_url
        for current_edit in self.edits:
            if not self.edits[current_edit]:
                continue
            image_url += f'&{current_edit}={self.edits[current_edit]}'
        if not self.crop:
            return image_url
        image_url += '&crop='
        for current_crop in self.crop:
            image_url += f'{current_crop},'
        return image_url.strip(',')

    def reset(self):
        """ Resets all of the edits on the image """
        self.edits = {
            'width': None,
            'height': None,
            'format': None,
            'fit': None,
        }
        self.crop = []


class Unsplash:
    """ Represent a connection to the Unsplash API """
    def __init__(self, access_key: str, secret_key: str = "",
                 base_url: str = 'https://api.unsplash.com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url

    def get(self, endpoint: str, params: dict = None) -> dict:
        """ Simplify get requests to unsplash API """
        request_url = (f'{self.base_url}/{endpoint}/'
                       f'?client_id={self.access_key}')
        response = requests.get(request_url, params=params)
        if response.ok:
            return response.json()
        return {}

    def get_random_image(
            self, query: str = None,
            orientation: UnsplashImage.orientation_type = None
    ) -> UnsplashImage:
        """ Get a random image via the unsplash API """
        params = {}
        if query:
            params.update({'query': query})
        if orientation:
            params.update({'orientation': orientation})
        response = self.get('photos/random', params=params)
        return UnsplashImage(response['urls']['raw'],
                             user=response['user']['name'])
