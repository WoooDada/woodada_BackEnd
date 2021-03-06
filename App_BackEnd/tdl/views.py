from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from .serializers import monthly_serializer, weekly_serializer, daily_serializer
from .models import Monthly_tdl, Weekly_tdl, Daily_tdl
import jwt


class monthly_tdl(views.APIView):


    #계획 작성
    def post(self, request):

        data = request.data
        serializer = monthly_serializer(data=data)


        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])


        if not serializer.is_valid(raise_exception=False):
            return Response({"message":"mtdl post fail"}, status=status.HTTP_400_BAD_REQUEST)


        else:

            obj = serializer.save(uid=user)
            #return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"m_todo_id" : obj.m_todo_id}, status=status.HTTP_200_OK)
            #return JsonResponse({"m_todo_id" : serializer.validated_data['m_todo_id']}, status=status.HTTP_200_OK)

    #계획 가져오기
    def get(self, request):

        try:

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

  #          current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
   #         user = User.objects.get(uid=current_user_uid)

            if user :
                #queryset = user.Monthly_tdl.all().values()
                queryset = user.Monthly_tdl_uid.all().values('m_todo_id','stt_date',
                                                             'end_date','m_content')

                return Response({"m_todo_list":queryset}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)

        except :
            return Response({"message":"no uid"}, status=status.HTTP_400_BAD_REQUEST)

    #계획 수정하기
    def put(self, request):
        try:
            m_todo_id = request.data.get("m_todo_id")
            m_obj = Monthly_tdl.objects.get(m_todo_id = m_todo_id)

            serializer = monthly_serializer(data=request.data, instance=m_obj)

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"m_todo_id":m_todo_id}, status=status.HTTP_200_OK)

            else :
                return Response({"message":"mtdl update fail"},status=status.HTTP_400_BAD_REQUEST)

        except :
            return Response({"message": "mtdl update fail"}, status=status.HTTP_400_BAD_REQUEST)



      #계획 삭제하기
    def delete(self, request):

        try:
            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            if user:
                m_todo_id = request.data.get("m_todo_id")
                m_obj = Monthly_tdl.objects.get(m_todo_id=m_todo_id)
                m_obj.delete()
                return Response({"m_todo_id":m_todo_id}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "mtdl delete fail"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"message": "mtdl delete fail"}, status=status.HTTP_400_BAD_REQUEST)


class weekly_tdl(views.APIView):

    def get(self, request):

        w_todo_list = []


        try:

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            #dates_param = request.GET.getlist('dates')
            dates_param = self.request.query_params.get('dates')
            dates_param = dates_param.split("|")

            for date in dates_param:
                date_qs = {"w_date": date}
                qs = user.Weekly_tdl_uid.filter(w_date=date).values('w_todo_id', 'w_content', 'w_check')
                data_qs = {"w_todos": list(qs)}

                fin = {**date_qs, **data_qs}
                w_todo_list.append(fin)

                # queryset = user.Weekly_tdl_uid.all()['w_date','w_content','w_check']
            return Response({"w_todo_list": w_todo_list}, status=status.HTTP_200_OK)


        except :
            return Response({"message":"no uid"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):

       try:
            data = request.data
            serializer = weekly_serializer(data=data)

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            if not serializer.is_valid(raise_exception=False):
                return Response({"message": "wtdl post fail"}, status=status.HTTP_400_BAD_REQUEST)


            else:

                obj = serializer.save(uid=user)

                return Response({"w_todo_id": obj.w_todo_id}, status=status.HTTP_200_OK)

       except:
            return Response({"message":"wdtl post fail"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        try:
            w_todo_id = request.data.get("w_todo_id")
            w_obj = Weekly_tdl.objects.get(w_todo_id = w_todo_id)
            w_date = w_obj.w_date
            serializer = weekly_serializer(data=request.data, instance=w_obj)

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"w_todo_id":w_todo_id}, status=status.HTTP_200_OK)

            else :
                return Response({"message":"wtdl update fail"},status=status.HTTP_400_BAD_REQUEST)

        except :
            return Response({"message": "wtdl update fail"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):

        try:
            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])


            w_todo_id = request.data.get("w_todo_id")
            w_obj = Weekly_tdl.objects.get(w_todo_id=w_todo_id)
            w_obj.delete()
            return Response({"w_todo_id": w_todo_id}, status=status.HTTP_200_OK)


        except ObjectDoesNotExist:
            return Response({"message": "wtdl delete fail"}, status=status.HTTP_400_BAD_REQUEST)

        except :
            return Response({"message": "wtdl delete fail"}, status=status.HTTP_400_BAD_REQUEST)




class daily_tdl(views.APIView):

    def get(self, request):

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

     #   current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
      #  user = User.objects.get(uid=current_user_uid)

        if user:
            try:
                date = self.request.query_params.get('d_date')
                qs = user.Daily_tdl_uid.filter(d_date=date).values('d_todo_id', 'd_date','d_tag', 'd_content', 'd_check')

                return Response({"d_todo_list": qs}, status=status.HTTP_200_OK)

            except:
                return Response({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)




    def post(self, request):

        try:
            data = request.data
            serializer = daily_serializer(data=data)

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            if not serializer.is_valid(raise_exception=False):
                return Response({"message": "dtdl post fail"}, status=status.HTTP_400_BAD_REQUEST)


            else:

                obj = serializer.save(uid=user)
                return Response({"d_todo_id": obj.d_todo_id}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "dtdl post fail"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        try:
            d_todo_id = request.data.get("d_todo_id")
            d_obj = Daily_tdl.objects.get(d_todo_id=d_todo_id)

            serializer = daily_serializer(data=request.data, instance=d_obj)

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"d_todo_id": d_todo_id}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "dtdl update fail"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"message": "dtdl update fail"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):

        try:

            d_todo_id = request.data.get("d_todo_id")
            d_obj = Daily_tdl.objects.get(d_todo_id=d_todo_id)
            d_obj.delete()
            return Response({"d_todo_id": d_todo_id}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "dtdl delete fail"}, status=status.HTTP_400_BAD_REQUEST)