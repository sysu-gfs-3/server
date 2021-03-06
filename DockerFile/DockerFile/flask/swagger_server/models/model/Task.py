# -*- coding: utf-8 -*-
import threading

import datetime
from ...utils.db import Database

print(__name__)


class TaskTable(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(TaskTable, "_instance"):
            with TaskTable._instance_lock:
                if not hasattr(TaskTable, "_instance"):
                    TaskTable._instance = object.__new__(cls)
        return TaskTable._instance

    @staticmethod
    def create_task(**kwargs):
        """
        :param kwargs: {
                 'title',
                 'type',
                 'publish_id',
                 'wjx_id',
                 'task_intro',
                 'max_num',
                 'participants_num',
                 'money',
                 'sign_start_time',
                 'sign_end_time',
                 'audit_administrator_audit_id'
        }
        """
        kwargs.update(
            {"release_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             "state": "W",  # waiting
             "audit_administrator_audit_id": '00227'
             })

        sql = "INSERT INTO task(title, type, publish_id, state, wjx_id, task_intro, max_num, participants_num, money, "\
              "release_time, sign_start_time, sign_end_time, audit_administrator_audit_id) "\
              "VALUES ('{title}', '{type_}', '{publish_id}', '{state}', '{wjx_id}', '{task_intro}', '{max_num}', '{participants_num}',  "\
              "'{money}', '{release_time}', '{sign_start_time}', '{sign_end_time}', '{audit_administrator_audit_id}'); "\
            .format(**kwargs)
        return Database.execute(sql, response=True)

    @staticmethod
    def get_task_info(task_id):
        """
        获取任务的基本信息
        """
        sql = 'SELECT * FROM task WHERE task.task_id=%d;' % (int(task_id))
        result = Database.query(sql, fetchone=True)
        return result

    @staticmethod
    def get_task_detail(task_id, user_id=None):
        """
        获取任务的基本信息task表　以及其创建者的photo, nickname, phone, userid, 还有job state
        """
        sql = 'SELECT * FROM task WHERE task_id=%d;' % int(task_id)
        task = Database.query(sql, fetchone=True)

        if task is None:
            return None
        id = task['publish_id']

        sql2 = 'SELECT * '\
                ' FROM user as u, (select phone_number, user_com_id as id from com_identity where user_user_id={id}  '\
                                 ' UNION ALL '\
                                 ' select phone_number, user_stu_id as id from stu_identity where user_user_id={id} ) as a '\
                ' WHERE u.user_id={id};'.format(id = id)
        
        publisher = Database.query(sql2, fetchone=True)
        if publisher is None:
            return None

        sql3 = "SELECT isagree FROM user_has_task as ut  WHERE ut.user_user_id = {user_id} AND ut.task_task_id={task_id} "\
            .format(user_id=user_id, task_id=task_id)
        
        job = Database.query(sql3, fetchone=True)

        return {
            'task': task,
            'publisher': publisher,
            'job': job}

    ##目前的表查询是错的,还要关联task表，以及获得任务发布者的photo，
    @staticmethod
    def get_accepted_task(user_id):
        """
        获取已经接受的任务的信息
        """
        sql = \
        'SELECT task.*, user.photo FROM user_has_task, task, user  '\
        ' WHERE user_has_task.user_user_id={}  '\
        ' AND task.task_id=user_has_task.task_task_id AND '\
            ' task.publish_id=user.user_id'.format(user_id)

        result = Database.query(sql)
        return result
    
    ##获得任务发布者的photo， 
    @staticmethod
    def get_published_task(user_id):
        """
        获取已发布任务的信息
        """
        sql = \
            'SELECT * FROM task, user  '\
            ' WHERE task.publish_id={user_id} AND user.user_id=task.publish_id'.format(user_id=user_id)

        result = Database.query(sql)
        return result

    @staticmethod
    def abort_task(task_id):
        """
        放弃任务
        """
        sql = "UPDATE task SET state='F' WHERE task_id='{task_id}' ".format(task_id=task_id)
        result = Database.execute(sql)
        return result

    ##需要获得参与者数量，通过user_has_task
    @staticmethod
    def get_task_part_num(task_id):
        sql = 'SELECT COUNT(*) as number FROM user_has_task WHERE task_task_id={task_id};'.format(task_id=task_id)
        return Database.query(sql, fetchone=True)

    @staticmethod
    def get_task_participants(task_id):
        """
        获取某任务的参加用户的信息包括　photo, nickname, phone, userid
        """
        sql="SELECT user.user_id, user.photo, user.nickname, cs.phone as phone "\
            " FROM (SELECT user_user_id FROM user_has_task WHERE task_task_id={id}) as u, "\
                 " (SELECT phone_number as phone, user_user_id as id FROM stu_identity "\
                 " UNION ALL  "\
                 " SELECT phone_number as phone, user_user_id as id FROM com_identity "\
                 ") as cs, "\
                 "user "\
            " WHERE u.user_user_id=user.user_id and cs.id=user.user_id;".format(id=task_id)

        return Database.query(sql)

    @staticmethod
    def get_task_intro(task_id):
        sql = "SELECT  task_intro From task  "\
            "Where task_id={task_id}".format(task_id=task_id)
        result = Database.query(sql)
        return result

    @staticmethod
    def append_task_intro(task_id, content):
        content =  "\n"+content
        sql = "UPDATE task SET task_intro=CONCAT(task_intro,'{content}')  "\
                    "WHERE task_id={task_id} "\
                        .format(content=content, task_id = task_id)
        result = Database.execute(sql, response=True)
        return result

    @staticmethod
    def commit_job(user_id, task_id, file):
        """
            任务参与者上传其工作证明 file xml
        """
        sql = "INSERT INTO user_task_job(task_task_id, user_user_id, job_path, unload_time)  "\
              " VALUES('{task_id}','{user_id}','{job_path}','{unload_time}') "\
            .format(task_id=task_id,
                    user_id=user_id,
                    job_path=file,
                    unload_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        result = Database.execute(sql, response=True)
        if isinstance(result, Exception):
            return result
        sql = "UPDATE user_has_task as ut SET ut.isagree='W' WHERE  ut.task_task_id="\
            "{task_id} AND ut.user_user_id={user_id}".format(task_id=task_id,user_id=user_id)
        return Database.execute(sql, response=True)

    @staticmethod
    def agree_job(participant_id, task_id, agree=True):
        """
        任务发布者接受或者拒绝任务参与者的任务证明
        """
        sql = 'UPDATE user_has_task as uh SET isagree=\'{agree}\' ' \
              'WHERE user_user_id={user_id} and task_task_id={task_id};'.format(
            agree='S' if agree else 'F', user_id=participant_id, task_id=task_id
        )
        return Database.execute(sql, response=True)

    @staticmethod
    def update_task(task_id,  **kwargs):
        """
        根据参数的属性，更改 task_id 对应的task 的属性
        example:
            update_task(task_id=1, audit_id=1, type = 1)
        """
        sql = "UPDATE task SET "
        for key in kwargs:
            if key in Task.__slots__:
                sql += " {key} = {value} ".format(key = key, value= kwargs[key])

        sql += "WHERE task_id = {task_id}".format(task_id=task_id)

        Database.execute(sql)

    @staticmethod
    def participate_task(user_id, task_id):
        """
        user pariticipate a task
        用户参加任务
        isagree: U W S F Q
            Q:QUIT
            U:UN AGREE
            W: WATING
            S: SUCCESS
            F: FAIL
        """
        sql = 'INSERT INTO user_has_task(user_user_id, task_task_id, task_audit_administrator_audit_id, isagree) '\
              'VALUES({user_id}, {task_id}, \'227\', \'U\')'.format(user_id=user_id,task_id= task_id)
        return Database.execute(sql, response=True)

    @staticmethod
    def abondon_task(user_id, task_id):
        """
        user abondon he accept task
        参与者放弃其参加的任务
        """
        sql = 'UPDATE user_has_task SET isagree=\'Q\' WHERE user_user_id={user_id} and task_task_id={task_id}'.format(
            user_id=user_id, task_id=task_id
        )
        return Database.execute(sql, response=True)

    @staticmethod
    def get_task_jobs(task_id):
        """
        get a task' s all participants' job
        获取某个任务的所有参与者提交的工作信息
        """

        sql = 'SELECT jobs.user_user_id as user_id ,jobs.job_path as job  '\
              ' FROM user_has_task AS task, user_task_job AS jobs  '\
              ' WHERE task.task_task_id=%d;' % int(task_id)

        return Database.query(sql)

    @staticmethod
    def task_count(state='all', type='all'):
        if state == 'all':
            state = 'IS NOT NULL'
        elif state == 'waiting':
            state = '= \'W\''

        if type == 'all':
            type = 'IS NOT NULL'
        elif type == 'W':
            type = '= \'W\''
        elif type == 'O':
            type = '= \'O\''



        sql = 'SELECT COUNT(*) as count FROM task WHERE task.state {} and task.type {};'.format(state, type)
        print(sql)
        data = Database.execute(sql, response=True)

        if isinstance(data, Exception):
            return False, data
        else:
            return True, data[0]['count']

    @staticmethod
    def get_tasks(task_type='all', begin=0, end=100):
        if task_type == 'all':
            sql = 'SELECT * FROM task LIMIT %d OFFSET %d;' \
                  % (end - begin, begin)
        elif task_type == 'waiting':
            sql = 'SELECT * FROM task WHERE task.state=\'W\' LIMIT %d OFFSET %d;' \
                  % (end - begin, begin)
        elif task_type == 'succeed':
            # 倒序
            sql = 'SELECT task.*, user.photo as icon FROM task, user WHERE state=\'S\' AND user.user_id=task.publish_id ORDER BY task.task_id DESC LIMIT %d OFFSET %d;' \
                  % (end - begin, begin)
        elif task_type == 'begin':
            # 倒序
            sql = 'SELECT task.*, user.photo as icon FROM task, user WHERE state=\'B\' AND user.user_id=task.publish_id ORDER BY task.task_id DESC LIMIT %d OFFSET %d;' \
                  % (end - begin, begin)
        else:
            raise KeyError('task type error')

        result = Database.query(sql)
        for user in result:
            user['release_time'] = str(user['release_time'])
            user['sign_start_time'] = str(user['sign_start_time'])
            user['sign_end_time'] = str(user['sign_end_time'])

        return result

    @staticmethod
    def audit(task_id, audit):
        audit = 'S' if audit else 'F'
        sql = 'UPDATE task SET state= \'%s\'WHERE task_id=%d;'\
        %(audit, task_id)
        print(sql)

        result = Database.execute(sql, response=True)
        if isinstance(result, Exception):
            print(result)
            return False, 'Database execute error: %s' % result
        else:
            return True, 'success audit'

class Task(object):
    """
    W - waiting
    F - failed
    S - succeed
    B - begin
    E - end
    """
    __slots__ = ['task_id',
                 'title',
                 'type_',
                 'publish_id',
                 'state',
                 'wjx_id',
                 'task_intro',
                 'max_num',
                 'participants_num',
                 'money',
                 'release_time',
                 'sign_start_time',
                 'sign_end_time',
                 'audit_administrator_audit_id'
                 ]
    taskTable = TaskTable()

    def __init__(self, task_id, title, type_, publish_id, state, wjx_id, task_intro, max_num, participants_num, money,
                 release_time, sign_start_time, sign_end_time, audit_administrator_audit_id):
        """
        :param task_id:
        :param title:
        :param type_:
        :param publish_id:
        :param state:
        :param wjx_id:
        :param task_intro:
        :param max_num:
        :param participants_num:
        :param money:
        :param release_time:
        :param sign_start_time:
        :param sign_end_time:
        :param audit_administrator_audit_id:
        """
        self.task_id = task_id
        self.title = title
        self.type_ = type_
        self.publish_id = publish_id
        self.state = state
        self.wjx_id = wjx_id
        self.task_intro = task_intro
        self.max_num = max_num
        self.participants_num = participants_num
        self.money = money
        self.release_time = release_time
        self.sign_start_time = sign_start_time
        self.sign_end_time = sign_end_time
        self.audit_administrator_audit_id = audit_administrator_audit_id


if __name__ =='__main__':

    print(Task.taskTable.task_count())