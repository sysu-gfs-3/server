# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class LoginCode(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, js_code: str=None, app_id: str=None, app_secret: str=None, encrypted_data: str=None):  # noqa: E501
        """LoginCode - a model defined in Swagger

        :param js_code: The js_code of this LoginCode.  # noqa: E501
        :type js_code: str
        :param app_id: The app_id of this LoginCode.  # noqa: E501
        :type app_id: str
        :param app_secret: The app_secret of this LoginCode.  # noqa: E501
        :type app_secret: str
        :param encrypted_data: The encrypted_data of this LoginCode.  # noqa: E501
        :type encrypted_data: str
        """
        self.swagger_types = {
            'js_code': str,
            'app_id': str,
            'app_secret': str,
            'encrypted_data': str
        }

        self.attribute_map = {
            'js_code': 'js_code',
            'app_id': 'app_id',
            'app_secret': 'app_secret',
            'encrypted_data': 'encryptedData'
        }

        self._js_code = js_code
        self._app_id = app_id
        self._app_secret = app_secret
        self._encrypted_data = encrypted_data

    @classmethod
    def from_dict(cls, dikt) -> 'LoginCode':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The LoginCode of this LoginCode.  # noqa: E501
        :rtype: LoginCode
        """
        return util.deserialize_model(dikt, cls)

    @property
    def js_code(self) -> str:
        """Gets the js_code of this LoginCode.

        user's js_code  # noqa: E501

        :return: The js_code of this LoginCode.
        :rtype: str
        """
        return self._js_code

    @js_code.setter
    def js_code(self, js_code: str):
        """Sets the js_code of this LoginCode.

        user's js_code  # noqa: E501

        :param js_code: The js_code of this LoginCode.
        :type js_code: str
        """

        self._js_code = js_code

    @property
    def app_id(self) -> str:
        """Gets the app_id of this LoginCode.

        miniprogram app_id  # noqa: E501

        :return: The app_id of this LoginCode.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id: str):
        """Sets the app_id of this LoginCode.

        miniprogram app_id  # noqa: E501

        :param app_id: The app_id of this LoginCode.
        :type app_id: str
        """

        self._app_id = app_id

    @property
    def app_secret(self) -> str:
        """Gets the app_secret of this LoginCode.

        miniprogram app_secret  # noqa: E501

        :return: The app_secret of this LoginCode.
        :rtype: str
        """
        return self._app_secret

    @app_secret.setter
    def app_secret(self, app_secret: str):
        """Sets the app_secret of this LoginCode.

        miniprogram app_secret  # noqa: E501

        :param app_secret: The app_secret of this LoginCode.
        :type app_secret: str
        """

        self._app_secret = app_secret

    @property
    def encrypted_data(self) -> str:
        """Gets the encrypted_data of this LoginCode.

        user's encryptedData when he/she has authensized getUserInfo  # noqa: E501

        :return: The encrypted_data of this LoginCode.
        :rtype: str
        """
        return self._encrypted_data

    @encrypted_data.setter
    def encrypted_data(self, encrypted_data: str):
        """Sets the encrypted_data of this LoginCode.

        user's encryptedData when he/she has authensized getUserInfo  # noqa: E501

        :param encrypted_data: The encrypted_data of this LoginCode.
        :type encrypted_data: str
        """

        self._encrypted_data = encrypted_data