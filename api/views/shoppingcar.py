import json
import redis

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from s11_luffycity.api import models
from s11_luffycity.s11_luffycity import settings
import json
import redis
from s11_luffycity.api.utils.response import BaseResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser



CONN = redis.Redis(host='192.168.11.180', port=6379)


USER_ID = 1
class ShoppingCarView(ViewSetMixin, APIView):
    # 查看购物车信息
    def list (self, request, *args, **kwargs):

        ret = {'code':1000, 'data':None, 'error':None}
        try:
            shopping_car_course_list = []
            pattern = settings.LUFFY_SHOPPING_CAR %(USER_ID, '*')
            # 下面这句话返回一个列表(所有要买的课的列表，应该是两个元素）
            user_key_list = CONN.keys(pattern)
            for key in user_key_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name':CONN.hget(key, 'name').decode('utf-8'),
                    'img':CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id':CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_police_dict':json.loads((CONN.hget(key, 'price_police_dict').decode('utf-8')))
                }
                shopping_car_course_list.append(temp)
            ret['data'] = shopping_car_course_list

        except Exception as e:

            ret['code'] = 10005
            ret['error'] = '获取购物车数据失败'

        return Response(ret)


    def create(self, request, *args, **kwargs):
    # 加入购物车
    # 接受用户的课程id和价格策略id
        course_id = request.data.get('courseid')
        policy_id = request.data.get('policyid')
    # 判断这些id是否在库里（即是否存在）
        course = models.Course.objects.filter(id = course_id).first()
        if not course:
            return Response({'code':500, 'error':'课程不存在'})

        # 判断这个课的价格策略是否合法，course里的price_policy字段
        price_policy_queryset = course.price_policy.all()
        price_policy_dict ={}
        for item in price_policy_queryset:
            temp = {
                'id':item.id,
                'price':item.price,
                'valid_period':item.valid_period,
                'valid_period_display':item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp
        if policy_id not in price_policy_dict:
            return Response({'code':10002,'error':'你改不了的老铁'})

        # 讲商品和价格策略放入购物车
        pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*')
        keys = CONN.keys((pattern))
        if keys and len(keys) > 1000:
            return Response({'code':5011, 'error':'东西太多了'})
        key =settings.LUFFY_SHOPPING_CAR %(USER_ID, course_id)
        # def hset(self, name, key, value)
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'default_price_id', policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))

        CONN.expire(key, 20 * 60)
        return Response({'code':10000,'data':'购买成功'})


    def destroy(self, request, *args, **kwargs):

        response = BaseResponse()
        try:
            courseid = request.GET.get('courseid')
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid)

            CONN.delete(key)
            response.data ='删除成功'

        except Exception as e:
            response.code = 888
            response.error = '没能删除'
        return Response(response.dict)


    def update(self, request, *args, **kwargs):
        # 获取课程id和需要修改的价格策略id
        # 校验合法性（在redis中）
        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None

            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id)

            if not CONN.exists(key):
                response.code = 11141
                response.error = '不存在的课程'
                return Response(response.dict)

            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
            if policy_id not in price_policy_dict:
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)

            CONN.hset(key, 'default_price_id', policy_id)
            CONN.expire(key, 20 * 60)
            response.data = '修改成功'

        except Exception as e:
            response.code = 9999
            response.error = '修改失败'
        return Response(response.dict)
