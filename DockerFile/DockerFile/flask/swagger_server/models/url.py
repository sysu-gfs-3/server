# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Url(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, url: str=None):  # noqa: E501
        """Url - a model defined in Swagger

        :param url: The url of this Url.  # noqa: E501
        :type url: str
        """
        self.swagger_types = {
            'url': str
        }

        self.attribute_map = {
            'url': 'url'
        }

        self._url = url

    @classmethod
    def from_dict(cls, dikt) -> 'Url':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Url of this Url.  # noqa: E501
        :rtype: Url
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self) -> str:
        """Gets the url of this Url.


        :return: The url of this Url.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Url.


        :param url: The url of this Url.
        :type url: str
        """

        self._url = url
