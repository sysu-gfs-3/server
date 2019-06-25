# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Condition(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, groups: List[str]=None, sex: str=None, credit_score: int=None):  # noqa: E501
        """Condition - a model defined in Swagger

        :param groups: The groups of this Condition.  # noqa: E501
        :type groups: List[str]
        :param sex: The sex of this Condition.  # noqa: E501
        :type sex: str
        :param credit_score: The credit_score of this Condition.  # noqa: E501
        :type credit_score: int
        """
        self.swagger_types = {
            'groups': List[str],
            'sex': str,
            'credit_score': int
        }

        self.attribute_map = {
            'groups': 'groups',
            'sex': 'sex',
            'credit_score': 'creditScore'
        }

        self._groups = groups
        self._sex = sex
        self._credit_score = credit_score

    @classmethod
    def from_dict(cls, dikt) -> 'Condition':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Condition of this Condition.  # noqa: E501
        :rtype: Condition
        """
        return util.deserialize_model(dikt, cls)

    @property
    def groups(self) -> List[str]:
        """Gets the groups of this Condition.


        :return: The groups of this Condition.
        :rtype: List[str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups: List[str]):
        """Sets the groups of this Condition.


        :param groups: The groups of this Condition.
        :type groups: List[str]
        """

        self._groups = groups

    @property
    def sex(self) -> str:
        """Gets the sex of this Condition.


        :return: The sex of this Condition.
        :rtype: str
        """
        return self._sex

    @sex.setter
    def sex(self, sex: str):
        """Sets the sex of this Condition.


        :param sex: The sex of this Condition.
        :type sex: str
        """

        self._sex = sex

    @property
    def credit_score(self) -> int:
        """Gets the credit_score of this Condition.


        :return: The credit_score of this Condition.
        :rtype: int
        """
        return self._credit_score

    @credit_score.setter
    def credit_score(self, credit_score: int):
        """Sets the credit_score of this Condition.


        :param credit_score: The credit_score of this Condition.
        :type credit_score: int
        """

        self._credit_score = credit_score