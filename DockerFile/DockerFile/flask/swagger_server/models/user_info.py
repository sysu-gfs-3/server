# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, user_id: str=None, nick_name: str=None, avatar_url: str=None, prove_state: str=None):  # noqa: E501
        """UserInfo - a model defined in Swagger

        :param user_id: The user_id of this UserInfo.  # noqa: E501
        :type user_id: str
        :param nick_name: The nick_name of this UserInfo.  # noqa: E501
        :type nick_name: str
        :param avatar_url: The avatar_url of this UserInfo.  # noqa: E501
        :type avatar_url: str
        :param prove_state: The prove_state of this UserInfo.  # noqa: E501
        :type prove_state: str
        """
        self.swagger_types = {
            'user_id': str,
            'nick_name': str,
            'avatar_url': str,
            'prove_state': str
        }

        self.attribute_map = {
            'user_id': 'userId',
            'nick_name': 'nickName',
            'avatar_url': 'avatarUrl',
            'prove_state': 'proveState'
        }

        self._user_id = user_id
        self._nick_name = nick_name
        self._avatar_url = avatar_url
        self._prove_state = prove_state

    @classmethod
    def from_dict(cls, dikt) -> 'UserInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserInfo of this UserInfo.  # noqa: E501
        :rtype: UserInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this UserInfo.


        :return: The user_id of this UserInfo.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this UserInfo.


        :param user_id: The user_id of this UserInfo.
        :type user_id: str
        """

        self._user_id = user_id

    @property
    def nick_name(self) -> str:
        """Gets the nick_name of this UserInfo.


        :return: The nick_name of this UserInfo.
        :rtype: str
        """
        return self._nick_name

    @nick_name.setter
    def nick_name(self, nick_name: str):
        """Sets the nick_name of this UserInfo.


        :param nick_name: The nick_name of this UserInfo.
        :type nick_name: str
        """

        self._nick_name = nick_name

    @property
    def avatar_url(self) -> str:
        """Gets the avatar_url of this UserInfo.


        :return: The avatar_url of this UserInfo.
        :rtype: str
        """
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, avatar_url: str):
        """Sets the avatar_url of this UserInfo.


        :param avatar_url: The avatar_url of this UserInfo.
        :type avatar_url: str
        """

        self._avatar_url = avatar_url

    @property
    def prove_state(self) -> str:
        """Gets the prove_state of this UserInfo.


        :return: The prove_state of this UserInfo.
        :rtype: str
        """
        return self._prove_state

    @prove_state.setter
    def prove_state(self, prove_state: str):
        """Sets the prove_state of this UserInfo.


        :param prove_state: The prove_state of this UserInfo.
        :type prove_state: str
        """

        self._prove_state = prove_state
