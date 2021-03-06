# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserInfoWithoutId(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, nick_name: str = None, avatar_url: str = None):  # noqa: E501
        """UserInfoWithoutId - a model defined in Swagger

        :param nick_name: The nick_name of this UserInfoWithoutId.  # noqa: E501
        :type nick_name: str
        :param avatar_url: The avatar_url of this UserInfoWithoutId.  # noqa: E501
        :type avatar_url: str
        """
        self.swagger_types = {"nick_name": str, "avatar_url": str}

        self.attribute_map = {"nick_name": "nickName", "avatar_url": "avatarUrl"}

        self._nick_name = nick_name
        self._avatar_url = avatar_url

    @classmethod
    def from_dict(cls, dikt) -> "UserInfoWithoutId":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserInfoWithoutId of this UserInfoWithoutId.  # noqa: E501
        :rtype: UserInfoWithoutId
        """
        return util.deserialize_model(dikt, cls)

    @property
    def nick_name(self) -> str:
        """Gets the nick_name of this UserInfoWithoutId.


        :return: The nick_name of this UserInfoWithoutId.
        :rtype: str
        """
        return self._nick_name

    @nick_name.setter
    def nick_name(self, nick_name: str):
        """Sets the nick_name of this UserInfoWithoutId.


        :param nick_name: The nick_name of this UserInfoWithoutId.
        :type nick_name: str
        """

        self._nick_name = nick_name

    @property
    def avatar_url(self) -> str:
        """Gets the avatar_url of this UserInfoWithoutId.


        :return: The avatar_url of this UserInfoWithoutId.
        :rtype: str
        """
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, avatar_url: str):
        """Sets the avatar_url of this UserInfoWithoutId.


        :param avatar_url: The avatar_url of this UserInfoWithoutId.
        :type avatar_url: str
        """

        self._avatar_url = avatar_url
