import connexion

from swagger_server.models.balance import Balance  # noqa: E501
from swagger_server.models.error_response import ErrorResponse  # noqa: E501
from swagger_server.models.iden_info import IdenInfo  # noqa: E501
from swagger_server.models.iden_info_with_credit import IdenInfoWithCredit  # noqa: E501
from swagger_server.models.login_code import LoginCode  # noqa: E501
from swagger_server.models.prove_state import ProveState  # noqa: E501
from swagger_server.models.user_info import UserInfo  # noqa: E501
from swagger_server.models.user_info_without_id import UserInfoWithoutId  # noqa: E501
from swagger_server.modules.accessControlSystem import (
    AccessControlSystem as accessControlSystem,
)
from swagger_server.modules.userManagementSystem import ManagementSystem

user_manager = ManagementSystem()
access_control = accessControlSystem()

login_response = (ErrorResponse(message="login"), 400)


@access_control.login_required(login_response)
def user_info_put(body):  # noqa: E501
    """User modify his basic info.

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: UserInfo
    """
    if connexion.request.is_json:
        body = UserInfoWithoutId.from_dict(connexion.request.get_json())  # noqa: E501

    nick_name = body.nick_name
    avatar_url = body.avatar_url

    result = user_manager.modify(nick_name=nick_name, avatar_url=avatar_url)
    if result is not None:
        return UserInfo(
            user_id=result.user_id,
            nick_name=result.nickname,
            avatar_url=result.photo,
            prove_state=result.isprove,
        )
    else:
        return ErrorResponse(message="error"), 400


@access_control.login_required(login_response)
def user_proof_get(userId):  # noqa: E501
    """get user&#39;s indentity info

     # noqa: E501

    :param userId: 
    :type userId: str

    :rtype: IdenInfoWithCredit
    """
    info = user_manager.get_user_detail(userId)
    print(info)
    return IdenInfoWithCredit(
        iden_info=IdenInfo(
            name=info.get("name"),
            sex=info.get("gender"),
            iden_type=info.get("identity"),
            tel=info.get("phone_number"),
            school=info.get("school"),
            company=info.get("company"),
            id=info.get("id"),
            cert=info.get("prove"),
        ),
        credit_score=info.get("credit"),
    )


@access_control.login_required(login_response)
def user_proof_post(body):  # noqa: E501
    """User provide his prove identity.

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = IdenInfo.from_dict(connexion.request.get_json())  # noqa: E501
    result = user_manager.prove(body)
    if "error" in result:
        return ErrorResponse(result[1]), 400
    else:
        return "成功", 200


def user_session_post(body):  # noqa: E501
    """Users login

    Users login # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: UserInfo
    """
    if connexion.request.is_json:
        body = LoginCode.from_dict(connexion.request.get_json())  # noqa: E501
    js_code = body.js_code
    app_id = body.app_id
    app_secret = body.app_secret
    result = user_manager.login(js_code=js_code, app_id=app_id, app_secret=app_secret)
    if result is not None:
        return UserInfo(
            user_id=result.user_id,
            nick_name=result.nickname,
            avatar_url=result.photo,
            prove_state=result.isprove,
        )
    else:
        return ErrorResponse(message="登录失败"), 400


@access_control.login_required(login_response)
def user_user_id_balance_get():  # noqa: E501
    """User get the balance.

     # noqa: E501

    :rtype: Balance
    """
    return "do some magic!"


@access_control.login_required(login_response)
def user_user_id_balance_put():  # noqa: E501
    """User recharge.

     # noqa: E501

    :rtype: Balance
    """
    return "do some magic!"


@access_control.login_required(login_response)
def user_user_id_proof_state_get(userId):  # noqa: E501
    """User get his authState.

     # noqa: E501

    :param userId: 
    :type userId: str

    :rtype: ProveState
    """
    info = user_manager.get_user_info(user_id=userId)
    if info is not None:
        return ProveState(prove_state=info.isprove)
    else:
        return ErrorResponse(message="error"), 400
