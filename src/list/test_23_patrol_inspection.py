# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest

class Test_patrol_inspection:
    # @allure.description("暂存巡检单")
    # @allure.suite('暂存巡检单')
    # @allure.title("暂存巡检单")  # 测试用例的标题
    # @allure.testcase('/fsm-platform/taskOrder/temporarySavePatrolInspection')
    # @pytest.mark.two
    def patrol_inspection(self):
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/temporarySavePatrolInspection"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        # 巡检id、任务id
        self.list_sql_search = Read_sql_Data.Conte(survey)
        # 问卷id
        self.list_survey_question = Read_sql_Data.Conte(survey_question % str(self.list_sql_search[0][2]))
        # 门锁检查选项id
        self.list_survey_option1 = Read_sql_Data.Conte(survey_option % \
                                {'1': self.list_sql_search[0][2], '2': self.list_survey_question[0][0]})

        # 门铰链检查选项id
        self.list_survey_option2 = Read_sql_Data.Conte(survey_option % \
                                                      {'1': self.list_sql_search[0][2],  '2': self.list_survey_question[1][0]})

        # 地面清洁度检查选项id
        self.list_survey_option3 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': str(self.list_survey_question[2][0])})
        # 灯光亮度检查选项id
        self.list_survey_option4 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': self.list_survey_question[3][0]})
        data ={
            "questionAnswers": [{
                "id": self.list_survey_question[0][0],
                "createUser": 1,
                "createUser_label": "admin",
                "createTime": "2022-11-18 10:42:51",
                "updateUser": 1,
                "updateUser_label": "admin",
                "updateTime": "2022-11-18 11:20:00",
                "isDelete": 0,
                "title": "门锁检查",
                "number": "true",
                "type": "checkbox",
                "description": None,
                "remark": None,
                "fileSize": 2,
                "fileNumber": 2,
                "inputFormat": None,
                "inputMin": None,
                "inputMax": None,
                "optionSortType": None,
                "requirements": "1、关闭门，查看是否能正常落锁\n2、使用钥匙进行反锁，是否正常关闭且不可打开；\n3、使用钥匙关闭反锁，是否可以正常开锁；\n4、锁具开关是否卡涩；\n5、填写巡检表",
                "useTool": None,
                "needPhoto": "true",
                "needRemark": "true",
                "sort": 1,
                "required": 1,
                "surveyId": self.list_sql_search[0][0],
                "bankId": "645936954327695360",
                "options": [{
                    "id": self.list_survey_option1[0][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 1,
                    "label": "1、门锁开关卡涩",
                    "value": "c6518ee6bf2e4690adca59b09db5f8c2",
                    "questionId": self.list_survey_question[0][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option1[1][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 2,
                    "label": "2、关闭不能落锁",
                    "value": "c486daf881454fb7b630aa6ca82794b6",
                    "questionId": self.list_survey_question[0][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option1[2][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 3,
                    "label": "3、反锁门后依然可以打开",
                    "value": "be510074e9ac4e978bce8e58b061054c",
                    "questionId": self.list_survey_question[0][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option1[3][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 4,
                    "label": "4、无以上情况",
                    "value": "155e2f97a0bc497088f4a65763277db2",
                    "questionId": self.list_survey_question[0][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }],
                "questionRelation": None,
                "group": 0,
                "questions": None,
                "values": [{
                    "content": self.list_survey_option1[0][0],
                    "images": "",
                    "optionId": self.list_survey_option1[0][0],
                    "remarkContent": ""
                }],
                "images": [],
                "remarkContent": "",
                "show": "true"
            }, {
                "id":self.list_survey_question[1][0],
                "createUser": 1,
                "createUser_label": "admin",
                "createTime": "2022-11-18 10:44:09",
                "updateUser": 1,
                "updateUser_label": "admin",
                "updateTime": "2022-11-18 11:20:00",
                "isDelete": 0,
                "title": "门铰链检查",
                "number": "true",
                "type": "checkbox",
                "description": None,
                "remark": None,
                "fileSize": 2,
                "fileNumber": 2,
                "inputFormat": None,
                "inputMin": None,
                "inputMax": None,
                "optionSortType": None,
                "requirements": "1、打开关闭门，铰链是否异响\n2、检查铰链是否锈蚀\n3、检查铰链是否脱落",
                "useTool": None,
                "needPhoto": "true",
                "needRemark": "true",
                "sort": 2,
                "required": 1,
                "surveyId": self.list_sql_search[0][0],
                "bankId": "645937282666201088",
                "options": [{
                    "id": self.list_survey_option2[0][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 1,
                    "label": "1、铰链异响",
                    "value": "a0dc0366b68443b683c0b49a35ba52fa",
                    "questionId": self.list_survey_question[1][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option2[1][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 2,
                    "label": "2、铰链脱落",
                    "value": "93903034c2f44b7eb978fb3e22a67a31",
                    "questionId": self.list_survey_question[1][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option2[2][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 3,
                    "label": "3、铰链锈蚀",
                    "value": "079c8662742b41da99cc9b85dff5db3a",
                    "questionId": self.list_survey_question[1][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option2[3][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 4,
                    "label": "4、无以上情况",
                    "value": "043d9f30b13b4debb7256041c43d8a2b",
                    "questionId": self.list_survey_question[1][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }],
                "questionRelation": None,
                "group": 0,
                "questions": None,
                "values": [{
                    "content": self.list_survey_option2[0][0],
                    "images": "",
                    "optionId": self.list_survey_option2[0][0],
                    "remarkContent": ""
                }],
                "images": [],
                "remarkContent": "",
                "show": "true"
            }, {
                "id": self.list_survey_question[2][0],
                "createUser": 1,
                "createUser_label": "admin",
                "createTime": "2022-11-18 10:45:54",
                "updateUser": 1,
                "updateUser_label": "admin",
                "updateTime": "2022-11-18 11:20:00",
                "isDelete": 0,
                "title": "地面清洁度检查",
                "number": "true",
                "type": "radio",
                "description": None,
                "remark": None,
                "fileSize": None,
                "fileNumber": None,
                "inputFormat": None,
                "inputMin": None,
                "inputMax": None,
                "optionSortType": None,
                "requirements": "1、巡检内容包括门店大厅所有地区的地面\n2、使用纸巾擦拭地面检查灰尘情况\n3、重点检查座位下，家具装饰下的灰尘和油污情况\n4、填写巡检表",
                "useTool": None,
                "needPhoto": "false",
                "needRemark": "false",
                "sort": 3,
                "required": 1,
                "surveyId": self.list_sql_search[0][0],
                "bankId": "645937721038077952",
                "options": [{
                    "id": self.list_survey_option3[0][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 1,
                    "label": "1、清洁度完美，无灰尘或污渍",
                    "value": "6a4f633f2d28479ca7b7195405bea3c9",
                    "questionId": self.list_survey_question[2][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option3[1][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 2,
                    "label": " 2、清洁度较好，少量灰尘或污渍",
                    "value": "b7c641dc2b524f49896770bf2a1a1967",
                    "questionId": self.list_survey_question[2][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option3[2][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 3,
                    "label": "3、清洁度较差，大量灰尘或污渍",
                    "value": "7c0a69f17a45412d965dce4a7b6df8c9",
                    "questionId": self.list_survey_question[2][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }],
                "questionRelation": None,
                "group": 0,
                "questions": None,
                "values": [{
                    "content": self.list_survey_option3[0][0],
                    "images": "",
                    "optionId": self.list_survey_option3[0][0],
                    "remarkContent": ""
                }],
                "images": None,
                "remarkContent": None,
                "show": "true"
            }, {
                "id": self.list_survey_question[3][0],
                "createUser": 1,
                "createUser_label": "admin",
                "createTime": "2022-11-18 10:47:44",
                "updateUser": 1,
                "updateUser_label": "admin",
                "updateTime": "2022-11-18 11:20:00",
                "isDelete": 0,
                "title": "灯光亮度检查",
                "number": "true",
                "type": "select",
                "description": None,
                "remark": None,
                "fileSize": None,
                "fileNumber": None,
                "inputFormat": None,
                "inputMin": None,
                "inputMax": None,
                "optionSortType": None,
                "requirements": "1、使用照度仪检查灯泡或发光体色温\n2、拍摄色温数值\n3、拍摄照度仪数值\n4、填写巡检表",
                "useTool": None,
                "needPhoto": "false",
                "needRemark": "false",
                "sort": 4,
                "required": 1,
                "surveyId": self.list_sql_search[0][0],
                "bankId": "645938184525447168",
                "options": [{
                    "id": self.list_survey_option4[0][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 1,
                    "label": "1、个别灯具色温不在合适范围1",
                    "value": "b42b456901394af2a6f44f193f62b83c",
                    "questionId": self.list_survey_question[3][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option4[1][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 2,
                    "label": "2、大部分灯具色温不在合适范围",
                    "value": "6da9557083af4298885e4b3717b796c1",
                    "questionId": self.list_survey_question[3][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }, {
                    "id": self.list_survey_option4[2][0],
                    "createUser": None,
                    "createTime": "2022-11-18 11:20:00",
                    "updateUser": None,
                    "updateTime": "2022-11-18 11:20:00",
                    "isDelete": 0,
                    "sort": 3,
                    "label": "3、全部灯具色温不在合适范围",
                    "value": "c52d97d626184776b1504c1d16dd0c3d",
                    "questionId": self.list_survey_question[3][0],
                    "parentId": "0",
                    "needPhoto": "false",
                    "needRemark": "false",
                    "description": None,
                    "needDescription": "false"
                }],
                "questionRelation": None,
                "group": 0,
                "questions": None,
                "values": [{
                    "content": self.list_survey_option4[0][0],
                    "images": "",
                    "optionId": self.list_survey_option4[0][0],
                    "remarkContent": ""
                }],
                "images": None,
                "remarkContent": None,
                "show": "true"
            }],
            "surveyId": self.list_sql_search[0][0],
            "id": "",
            "surveyUniqueId": self.list_sql_search[0][1],
            "status": 0,
            "bizId": self.list_sql_search[0][2]
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        # log_show(res, data)
        assert res.status_code == 200
        # 检验选项1的数据是否正确
        self.check_option1 = Read_sql_Data.Conte(check_survey  % \
                                                       {'1': self.list_sql_search[0][0],
                                                        '2': self.list_sql_search[0][2],
                                                        '3': self.list_survey_question[0][0]
                                                        }
                                                      )
        sql_option1=self.check_option1[0][1].replace('"', '', 2)
        assert  str(self.list_survey_option1[0][0]) ==sql_option1
        # 检验选项2的数据是否正确
        self.check_option2 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[1][0]
                                                  }
                                                 )
        sql_option2 = self.check_option2[0][1].replace('"', '', 2)
        assert str(self.list_survey_option2[0][0]) == sql_option2
        # 检验选项3的数据是否正确
        self.check_option3 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[2][0]
                                                  }
                                                 )
        sql_option3 = self.check_option3[0][1].replace('"', '', 2)
        assert str(self.list_survey_option3[0][0]) == sql_option3
        # 检验选项4的数据是否正确
        self.check_option4 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[3][0]
                                                  }
                                                 )
        sql_option4 = self.check_option4[0][1].replace('"', '', 2)
        assert str(self.list_survey_option4[0][0]) == sql_option4
        return str(self.list_sql_search[0][0]),str(self.list_sql_search[0][2])

    @allure.description("提交巡检单")
    @allure.suite('提交巡检单')
    @allure.title("提交巡检单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/submitPatrolInspection')
    @pytest.mark.two
    def test_submit_patrol_inspection(self):
        # 巡检id、任务id
        self.list_sql_search = Read_sql_Data.Conte(survey)
        # 问卷id
        self.list_survey_question = Read_sql_Data.Conte(survey_question % str(self.list_sql_search[0][2]))
        # 门锁检查选项id
        self.list_survey_option1 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': self.list_survey_question[0][0]})

        # 门铰链检查选项id
        self.list_survey_option2 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': self.list_survey_question[1][0]})

        # 地面清洁度检查选项id
        self.list_survey_option3 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': str(self.list_survey_question[2][0])})
        # 灯光亮度检查选项id
        self.list_survey_option4 = Read_sql_Data.Conte(survey_option % \
                                                       {'1': self.list_sql_search[0][2],
                                                        '2': self.list_survey_question[3][0]})
        # 前厅id
        self.list_group1 = Read_sql_Data.Conte(group1 % str(self.list_sql_search[0][0]))
        # 大厅id
        self.list_group2 = Read_sql_Data.Conte(group2 % str(self.list_sql_search[0][0]))

        patrol_inspection = self.patrol_inspection()
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/submitPatrolInspection"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        data = {
	        "surveyAnswerVO": {
		    "questionAnswers": [{
			"id": self.list_group1[0][0],
			"createUser": None,
			"createTime": None,
			"updateUser": None,
			"updateTime": None,
			"isDelete": None,
			"title": "前厅",
			"number": None,
			"type": None,
			"description": None,
			"remark": None,
			"fileSize": None,
			"fileNumber": None,
			"inputFormat": None,
			"inputMin": None,
			"inputMax": None,
			"optionSortType": None,
			"requirements": None,
			"useTool": None,
			"needPhoto": None,
			"needRemark": None,
			"sort": None,
			"required": None,
			"surveyId": None,
			"bankId": None,
			"options": None,
			"questionRelation": None,
			"group": 1,
			"questions": [{
				"id": self.list_survey_question[0][0],
				"createUser": 1,
				"createUser_label": "admin",
				"createTime": "2022-11-18 10:42:51",
				"updateUser": 1,
				"updateUser_label": "admin",
				"updateTime": "2022-11-23 00:00:00",
				"isDelete": 0,
				"title": "门锁检查",
				"number": "true",
				"type": "checkbox",
				"description": None,
				"remark": None,
				"fileSize": 2,
				"fileNumber": 2,
				"inputFormat": None,
				"inputMin": None,
				"inputMax": None,
				"optionSortType": None,
				"requirements": "1、关闭门，查看是否能正常落锁\n2、使用钥匙进行反锁，是否正常关闭且不可打开；\n3、使用钥匙关闭反锁，是否可以正常开锁；\n4、锁具开关是否卡涩；\n5、填写巡检表",
				"useTool": None,
				"needPhoto": "true",
				"needRemark": "true",
				"sort": 1,
				"required": 1,
				"surveyId": self.list_sql_search[0][0],
				"bankId": "645936954327695360",
				"options": [{
					"id": self.list_survey_option1[0][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 1,
					"label": "1、门锁开关卡涩",
					"value": "c6518ee6bf2e4690adca59b09db5f8c2",
					"questionId": self.list_survey_question[0][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option1[1][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 2,
					"label": "2、关闭不能落锁",
					"value": "c486daf881454fb7b630aa6ca82794b6",
					"questionId": self.list_survey_question[0][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option1[2][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 3,
					"label": "3、反锁门后依然可以打开",
					"value": "be510074e9ac4e978bce8e58b061054c",
					"questionId": self.list_survey_question[0][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option1[3][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 4,
					"label": "4、无以上情况",
					"value": "155e2f97a0bc497088f4a65763277db2",
					"questionId": self.list_survey_question[0][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}],
				"questionRelation": None,
				"group": 0,
				"questions": None,
				"values": [{
					"optionId": self.list_survey_option1[0][0],
					"content": self.list_survey_option1[0][0],
					"remarkContent": "",
					"images": None
				}],
				"images": [],
				"remarkContent": ""
			}, {
				"id": self.list_survey_question[1][0],
				"createUser": 1,
				"createUser_label": "admin",
				"createTime": "2022-11-18 10:44:09",
				"updateUser": 1,
				"updateUser_label": "admin",
				"updateTime": "2022-11-23 00:00:00",
				"isDelete": 0,
				"title": "门铰链检查",
				"number": "true",
				"type": "checkbox",
				"description": None,
				"remark": None,
				"fileSize": 2,
				"fileNumber": 2,
				"inputFormat": None,
				"inputMin": None,
				"inputMax": None,
				"optionSortType": None,
				"requirements": "1、打开关闭门，铰链是否异响\n2、检查铰链是否锈蚀\n3、检查铰链是否脱落",
				"useTool": None,
				"needPhoto": "true",
				"needRemark": "true",
				"sort": 2,
				"required": 1,
				"surveyId": self.list_sql_search[0][0],
				"bankId": "645937282666201088",
				"options": [{
					"id": self.list_survey_option2[0][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 1,
					"label": "1、铰链异响",
					"value": "a0dc0366b68443b683c0b49a35ba52fa",
					"questionId": self.list_survey_question[1][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option2[1][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 2,
					"label": "2、铰链脱落",
					"value": "93903034c2f44b7eb978fb3e22a67a31",
					"questionId": self.list_survey_question[1][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option2[2][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 3,
					"label": "3、铰链锈蚀",
					"value": "079c8662742b41da99cc9b85dff5db3a",
					"questionId": self.list_survey_question[1][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option2[3][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 4,
					"label": "4、无以上情况",
					"value": "043d9f30b13b4debb7256041c43d8a2b",
					"questionId": self.list_survey_question[1][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}],
				"questionRelation": None,
				"group": 0,
				"questions": None,
				"values": [{
					"optionId": self.list_survey_option2[0][0],
					"content": self.list_survey_option2[0][0],
					"remarkContent": "",
					"images": None
				}],
				"images": [],
				"remarkContent": ""
			}],
			"values": None,
			"images": None,
			"remarkContent": None
		}, {
			"id": self.list_group2[0][0],
			"createUser": None,
			"createTime": None,
			"updateUser": None,
			"updateTime": None,
			"isDelete": None,
			"title": "大厅",
			"number": None,
			"type": None,
			"description": None,
			"remark": None,
			"fileSize": None,
			"fileNumber": None,
			"inputFormat": None,
			"inputMin": None,
			"inputMax": None,
			"optionSortType": None,
			"requirements": None,
			"useTool": None,
			"needPhoto": None,
			"needRemark": None,
			"sort": None,
			"required": None,
			"surveyId": None,
			"bankId": None,
			"options": None,
			"questionRelation": None,
			"group": 1,
			"questions": [{
				"id": self.list_survey_question[2][0],
				"createUser": 1,
				"createUser_label": "admin",
				"createTime": "2022-11-18 10:45:54",
				"updateUser": 1,
				"updateUser_label": "admin",
				"updateTime": "2022-11-23 00:00:00",
				"isDelete": 0,
				"title": "地面清洁度检查",
				"number": "true",
				"type": "radio",
				"description": None,
				"remark": None,
				"fileSize": None,
				"fileNumber": None,
				"inputFormat": None,
				"inputMin": None,
				"inputMax": None,
				"optionSortType": None,
				"requirements": "1、巡检内容包括门店大厅所有地区的地面\n2、使用纸巾擦拭地面检查灰尘情况\n3、重点检查座位下，家具装饰下的灰尘和油污情况\n4、填写巡检表",
				"useTool": None,
				"needPhoto": "false",
				"needRemark": "false",
				"sort": 3,
				"required": 1,
				"surveyId": self.list_sql_search[0][0],
				"bankId": "645937721038077952",
				"options": [{
					"id": self.list_survey_option3[0][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 1,
					"label": "1、清洁度完美，无灰尘或污渍",
					"value": "6a4f633f2d28479ca7b7195405bea3c9",
					"questionId": self.list_survey_question[2][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option3[1][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 2,
					"label": " 2、清洁度较好，少量灰尘或污渍",
					"value": "b7c641dc2b524f49896770bf2a1a1967",
					"questionId": self.list_survey_question[2][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option3[2][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 3,
					"label": "3、清洁度较差，大量灰尘或污渍",
					"value": "7c0a69f17a45412d965dce4a7b6df8c9",
					"questionId": self.list_survey_question[2][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}],
				"questionRelation": None,
				"group": 0,
				"questions": None,
				"values": [{
					"optionId": self.list_survey_option3[0][0],
					"content": self.list_survey_option3[0][0],
					"remarkContent": "",
					"images": None
				}],
				"images": None,
				"remarkContent": None
			}, {
				"id": self.list_survey_question[3][0],
				"createUser": 1,
				"createUser_label": "admin",
				"createTime": "2022-11-18 10:47:44",
				"updateUser": 1,
				"updateUser_label": "admin",
				"updateTime": "2022-11-23 00:00:00",
				"isDelete": 0,
				"title": "灯光亮度检查",
				"number": "true",
				"type": "select",
				"description": None,
				"remark": None,
				"fileSize": None,
				"fileNumber": None,
				"inputFormat": None,
				"inputMin": None,
				"inputMax": None,
				"optionSortType": None,
				"requirements": "1、使用照度仪检查灯泡或发光体色温\n2、拍摄色温数值\n3、拍摄照度仪数值\n4、填写巡检表",
				"useTool": None,
				"needPhoto": "false",
				"needRemark": "false",
				"sort": 4,
				"required": 1,
				"surveyId": self.list_sql_search[0][0],
				"bankId": "645938184525447168",
				"options": [{
					"id": self.list_survey_option4[0][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 1,
					"label": "1、个别灯具色温不在合适范围1",
					"value": "b42b456901394af2a6f44f193f62b83c",
					"questionId": self.list_survey_question[3][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option4[1][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 2,
					"label": "2、大部分灯具色温不在合适范围",
					"value": "6da9557083af4298885e4b3717b796c1",
					"questionId": self.list_survey_question[3][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}, {
					"id": self.list_survey_option4[2][0],
					"createUser": None,
					"createTime": "2022-11-23 00:00:00",
					"updateUser": None,
					"updateTime": "2022-11-23 00:00:00",
					"isDelete": 0,
					"sort": 3,
					"label": "3、全部灯具色温不在合适范围",
					"value": "c52d97d626184776b1504c1d16dd0c3d",
					"questionId": self.list_survey_question[3][0],
					"parentId": "0",
					"needPhoto": "false",
					"needRemark": "false",
					"description": None,
					"needDescription": "false"
				}],
				"questionRelation": None,
				"group": 0,
				"questions": None,
				"values": [{
					"optionId": self.list_survey_option4[0][0],
					"content": self.list_survey_option4[0][0],
					"remarkContent": "",
					"images": None
				}],
				"images": None,
				"remarkContent": None
			}],
			"values": None,
			"images": None,
			"remarkContent": None
		}],
		"surveyId": self.list_sql_search[0][0],
		"surveyUniqueId": self.list_sql_search[0][1],
		"status": 1,
		"bizId": self.list_sql_search[0][2]
	},
	    "taskOrderVO": {
		"operationType": "FSMTOSOT01",
		"id": self.list_sql_search[0][2],
		"serviceId": "645943433973727232",
		"serviceVersion": ""
	    }
    }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        log_show(res, data)
        assert res.status_code == 200
        # 检验选项1的数据是否正确
        self.check_option1 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[0][0]
                                                  }
                                                 )
        sql_option1 = self.check_option1[0][1].replace('"', '', 2)
        assert str(self.list_survey_option1[0][0]) == sql_option1
        # 检验选项2的数据是否正确
        self.check_option2 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[1][0]
                                                  }
                                                 )
        sql_option2 = self.check_option2[0][1].replace('"', '', 2)
        assert str(self.list_survey_option2[0][0]) == sql_option2
        # 检验选项3的数据是否正确
        self.check_option3 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[2][0]
                                                  }
                                                 )
        sql_option3 = self.check_option3[0][1].replace('"', '', 2)
        assert str(self.list_survey_option3[0][0]) == sql_option3
        # 检验选项4的数据是否正确
        self.check_option4 = Read_sql_Data.Conte(check_survey % \
                                                 {'1': self.list_sql_search[0][0],
                                                  '2': self.list_sql_search[0][2],
                                                  '3': self.list_survey_question[3][0]
                                                  }
                                                 )
        sql_option4 = self.check_option4[0][1].replace('"', '', 2)
        assert str(self.list_survey_option4[0][0]) == sql_option4

