# -*- coding: utf-8 -*-
from ..models.model.Task import Task
import datetime
from flask import g, session

from .accessControlSystem import AccessControlSystem as access_control
from swagger_server.utils.utils import load_data, dump_data

class taskManagementSystem(object):
    def __init__(self):
        pass

    """
    发布者
    """
    #{ '0':"未接受", '1':"已经接受", '2': '已经提交证明', '3'：'拒绝', 4:'同意', 5:'已放弃'}
    def commit_task(self, task):
        """
        发布者：提交任务 -> 
        管理员：审核
        tMS: 写入db（任务状态：待审`核）

        :param publisher_id:
        :param task:
        :return:
        """

        user = g.get('user')
        if user.balance < task.money:
            return ('error', 'no enough money')

        payment = user.table.update_info(user.wechat_id, balance=user.balance - task.money)

        if not payment[0]:
            return ('error', 'payment error')

        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # create new task and write it to db
        result = Task.taskTable.create_task(
            publish_id = g.get('persistent').get('user_id'),
            title = task.title,
            type_ =task.type,
            wjx_id=task.wjx_id,
            task_intro=task.desc,
            max_num=task.max_num,
            participants_num=task.part_num,
            money=task.money,
            sign_start_time=start_time,
            sign_end_time=task.time)
        if  isinstance(result, Exception):

            #roll back payment
            print('roll back payment')
            print(user.table.update_info(user.unionid, balance=user.balance))
            return ('error', "error while creating ")
        else:
            return ('success', '成功')
        # admin audit this task
        #AdminPlatform.commit_new_task(task)

    def publish_task(self, task):
        """任务审核成功-> 进行中
            管理平台：正式发布任务
            -> TaskTable 写入database
        """
        #task.taskTable.create_task(task)

    def add_info(self, task_id, content):
        """
        发布者：增加任务说明
        """
        result = Task.taskTable.append_task_intro(task_id, content)
        if not  isinstance(result, Exception):
            return 'success', "增加成功"
        else:
            return ('error', "fail")

    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def get_published_tasks(self, user_id):
        """
        发布者：获取发布的任务
        """
        task = Task.taskTable.get_published_task(user_id)
        return task

    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def abort_task(self, task_id, user_id):
        """
        发布者：终止任务
        """
        result = Task.taskTable.get_task_part_num(task_id=task_id)
        if result is None or result.get('number'):
            return 'error', 'server error'
        
        if str(result.get('number')) ==str(0):
            result = Task.taskTable.abort_task(task_id)
            if not isinstance(result, Exception):
                return ('success')
            else:
                return ('error', 'unknown error')
        else:
            return ('error', 'no such task or participants is not zero')
    

    def agree_job(self, task_id, user_id, state):

        task = Task.taskTable.get_task_info(task_id=task_id)
        if 'publish_id' not in task:
            return 'error', 'no such task'
        elif  str(task.get('publish_id')) == str(user_id):
            return 'error', 'not your task'

        if state == 'agree':
            agree=True
        elif state == 'reject':
            agree=False
        result = Task.taskTable.agree_job(participant_id = user_id, task_id=task_id, agree=agree)
        if isinstance(result, Exception):
            return 'error', 'fail'
        else:
            return result
    
    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def get_task_accepter(self, task_id, user_id):
        """
        获取任务的参与者信息

        """
        accepters = Task.taskTable.get_task_participants(task_id = task_id)
        return accepters
    
    @staticmethod
    def get_task_detail(task_id):
        """
        获取任务信息以及发布者信息
        """
        task_with_user = Task.taskTable.get_task_detail(task_id, user_id=g.user.user_id)

        if task_with_user is None or len(task_with_user) is 0:
            return ('error', 'no such task')
        if task_with_user.get('job') is not None:
            isagree = task_with_user.get('job').get('isagree')
        else:
            isagree =None
        if isagree is None:
            task_with_user['task_job_state'] = 0
        else:
            if isagree  == 'U':
                task_with_user['task_job_state'] = 1
            elif isagree == 'W':
                task_with_user['task_job_state'] = 2
            elif isagree == 'F':
                task_with_user['task_job_state'] = 3
            elif isagree == 'S':
                task_with_user['task_job_state'] = 4
            else :
                task_with_user['task_job_state'] = 5


        return task_with_user

    def get_related_tasks(self, userId, Type):
        if Type =="acceptment":
            result = Task.taskTable.get_accepted_task(user_id=userId)
        elif Type == "publishment":
            result = Task.taskTable.get_published_task(user_id = userId)
        else:
            result=None
        return result

    def get_task_list(self, page_id):
        """
        获取所有任务列表
        :param page_id
        """
        page_size =10
        begin = page_id *page_size
        end = begin + page_size
        tasks = Task.taskTable.get_tasks(task_type = 'succeed',  begin=begin, end =end)
        return tasks

    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def get_accepted_tasks(self, user_id):
        """
        接收者：获取接受的任务
        """
        tasks = Task.taskTable.get_accepted_task(user_id = user_id)

    def get_task_jobs(self, task_id):
        #? 主人判断
        """
        get a task' s all participants' job
        获取某个任务的所有参与者提交的工作信息
        """
        result = Task.taskTable.get_task_jobs(task_id)
        for item in result:
            materials = load_data(item['job'])
            if materials is not None:
                item['remarks'] = materials.get('remarks')
                item['files'] = materials.get('pics')
        return result
    
    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def accept_task(self, user_id,  task_id):
        """
        用户：接受任务
        """

        result = Task.taskTable.participate_task(user_id, task_id)
        if isinstance(result, Exception):
            return 'error', '参加失败'
        return result

    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def abondon_task(self, user_id, task_id):
        """
        接收者：放弃任务
        """
        result = Task.taskTable.abondon_task(user_id, task_id)
        if isinstance(result, Exception):
            return 'error', "放弃失败"
        else:
            return 'success', "放弃任务"

    @access_control.owner_required(user_args='user_id',identity_error=('error', 'identity error'))
    def commit_job(self, user_id, task_id, job):
        """
        接受者：提交工作
        """
        pics = job.files
        materials = {
            'remarks': job.remarks,
            'pics':pics
        }
        file_name = dump_data(materials)

        result = Task.taskTable.commit_job(user_id=user_id, task_id=task_id, file=file_name )
        if isinstance(result, Exception):
            return 'error', "提交工作失败"
        else:
            return 'success', "提交工作"

    @staticmethod
    def audit_task(task_id, audit):
        return Task.taskTable.audit(task_id, audit)


    """
        获取信息模块
    """
    @staticmethod
    def get_task_count(state='all', type='all'):
        return Task.taskTable.task_count(state, type)

    @staticmethod
    def get_tasks(task_type='all', page=0):
        return Task.taskTable.get_tasks(task_type=task_type,
                                        begin=page*100,
                                        end=(page+1)*100)

