# -*- coding: utf-8 -*-
from ..models.model.User import User as User
from flask import g, session
from ..utils.utils import code2session

from .loginPersistentSystem import PersistentSystem as persistentSystem
from . accessControlSystem import AccessControlSystem as accessControlSystem
"""
   小程序登录过程
       1. 登录时用户端调用login，从微信服务器获取到jscode，
       2. 用户端将jscode发送给小程序服务器
       3. 小程序服务器用jscode 从微信服务器处获取到union等标识信息
       4. 小程序服务器用union唯一认知用户是否存在
       5. 当用户存在则登录成功，服务器生成uuid, 临时存储并返回uuid给用户端，
               用户端用uuid发起其他请求标志处于session期间
               
       6. 用户不存在则转向注册界面
   登录备注：
       1. 是否处于session期间，需要重新登录由小程序服务器根据uuid判断，
               正常情况下小程序不发起登录请求，直接用本地存储的uuid进行其他操作
               在收到服务器端登录过期或者uuid错误的情况下才发起登录
       2. 账号只能与一个小程序id绑定，即不可在第二个微信上登录
"""
class ManagementSystem:

    def __init__(self):
        pass
    

    def login(self, js_code):
        """
            登录模块， 小程序启动即刻调用
            数据库获取【用户简单信息】，并返回
            session保存登录状态
            不存在则注册
        
        Parameters:
            js_code: 小程序端发来的token,用于从微信服务器获取unionid
        
        Returns:
            用户信息 or None

        """
        """test"""
        #wechatresult = code2session(js_code)
        #if 'error' in wechatresult:
        #   return None
        
        wechatresult = {'unionid': js_code, 'openid':1, 'session_key':'12345'}

        unionid =wechatresult.get('unionid')

        if unionid is None:
            return None
        else:
            user = User.table.query_user(unionid=unionid)
            if isinstance(user, User.BasicUser):
                """
                persistent_info
                openid, unionid, session_key, user
                """
                persistant_result = persistentSystem.save(wechat_server_reply= wechatresult, user = user)
                return user
            else:
                user= self.register(unionid=unionid)
                persistant_result = persistentSystem.save(wechat_server_reply= wechatresult, user = user)
                return user
        

    def register(self, unionid=None):
        """
            注册模块,小程序启动时，在用户不存在时使用
            先数据库查询用户【用户简单信息】，存在则返回错误
            数据库添加用户id

        Parameters:
            id: unionid登录时获得

        """
        if unionid is None:
            return None
        user = User.table.query_user(unionid=unionid)
        if user is None:
            User.table.create_new_user(unionid=unionid)
            user = User.table.query_user(unionid=unionid)
            return user
        else:
            return user
    
    
    def prove(self, ident_info):
        """
            用户发起认证请求
        """
        user_id = g.get('persistent').get('user_id')
        user = User.table.query_user(user_id=user_id)
        unionid = g.get('persistent').get('unionid')
        if user is None:
            return  ('error', 'no such user')
        #elif user.isprove is 'P':
        #    return ('error', 'hasproved')
        
        if ident_info.iden_type is 'S':
            result = User.table.prove(
                user_id = user_id, 
                name=ident_info.name,
                gender = ident_info.sex,
                identity = ident_info.iden_type,
                phone_number = ident_info.tel,
                school = ident_info.school,
                id = ident_info.id,
                prove = ident_info.cert)
            User.table.update_info(
                unionid=unionid, 
                identity='S',
                isprove='W' )
            if result is None:
                return ('success', "changed")
        elif ident_info.iden_type is 'P':
            result = User.table.prove(
                user_id = user_id, 
                name=ident_info.name,
                gender = ident_info.sex,
                identity = ident_info.iden_type,
                phone_number = ident_info.tel,
                company = ident_info.company,
                id = ident_info.id,
                prove = ident_info.cert)
            User.table.update_info(
                unionid=unionid, 
                identity='C',
                isprove='W' )
            if result is None:
                return ('success', "changed")
        else:
            return ('error', 'no such user')

    def modify(self, nick_name, avart_url):
        unionid = g.get('persistent').get('unionid')
        user_id = g.get('persistent').get('user_id')
        User.table.update_info(unionid = unionid, nickname=nick_name, photo = avart_url )
        userinfo = User.table.query_user(unionid=unionid)
        return userinfo

    @staticmethod
    def get_user_count(user_type='all'):
        return User.table.user_count(user_type)

    @staticmethod
    def get_users(user_type='all', page=0):
        return User.table.get_users(user_type=user_type,
                                    begin=page*100,
                                    end=(page+1)*100)

    @staticmethod
    def get_user_info(user_id):
        """
        获取信息模块
        """
        user = User.table.query_user(user_id=user_id)
        if isinstance(user, User.BasicUser):
            return user
        else:
            return None
    


    def get_user_detail(self, user_id):
        """
        获取认证信息模块
        """
        detail = User.table.load_detail_user_id(user_id = user_id, identity=g.get('persistent').get('user_type').get('identity'))
        if detail is None:
            detail = {}
        detail['identity'] = g.get('persistent').get('user_type').get('identity')
        if detail['identity'] is 'S':
            detail['id'] = detail.get('student_num')
        elif detail['identity'] is 'C':
            detail['id'] = detail.get('job_num')
        return detail