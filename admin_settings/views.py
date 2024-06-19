from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import *
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from gpt_prompts.scheduler import scheduler, gpt_today_job
from django_apscheduler.models import DjangoJob
from kluck_notifications.push_scheduler import send_push_notifications


# api/v1/adms/push/
class Pushtime(APIView):
    serializer_class = Admin_settingsSerializer

    # Get 메소드에 대한 스키마 정의 및 예시 포함
    @extend_schema(tags=['Adms'],
        description="Admin settings에서 push_time 조회",
    )

    def get(self, request):
        try:
            # first()로 row의 존재여부 확인 row가 없으면 예외발생하지 않고 None반환!
            push_time = AdminSetting.objects.first()
            if push_time:
                serializer = Admin_settingsSerializer(push_time)
                response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                return Response(response_serializer.data, status=status.HTTP_200_OK)
                # return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('push_time이 없습니다.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            Response({'Error':'오류가 있습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Post 메소드에 대한 스키마 정의 및 예시 포함
    @extend_schema(tags=['Adms'],
        examples=[
            OpenApiExample(
                'Example',
                value={"push_time": "0100"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="(화면없음): 프론트에서 push_time을 받아 admin_settings의 push_time에 저장"
    )
    def post(self, request):
        try:
            # insert or update
            # target_row의 값을 통해 새로운 row를 생성하는 것이 아닌 기존의 row를 선택
            target_row = AdminSetting.objects.first()

            if target_row:
                # update
                # 관리자 세팅과 관련 값은 하나만 유지하기로 했기에 1번 row로 설정
                # partial=True 옵션으로 row전체 update가 아닌 일부만 update
                serializer = Admin_settingsSerializer(target_row, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                    self.reschedule_push()
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                # 객체가 존재하지 않을 경우
                # insert
                serializer = Admin_settingsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('push_time',))
                    self.reschedule_push()
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error':'오류가 있습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def reschedule_push(self):
        print('reschedule_push 시작')
        logger = logging.getLogger(__name__)

        # AdminSetting 테이블에서 push_time 가져오기
        try:
            push_time = AdminSetting.objects.first().push_time
            # 숫자 네자리를 문자열로 변환하여 분리
            push_time_str = str(push_time).zfill(4)  # 네자리로 맞추기 위해 zfill 사용
            hour = int(push_time_str[:2])  # 앞 두 자리
            minute = int(push_time_str[2:])  # 뒤 두 자리
        except AttributeError:
            # 예외 처리: AdminSetting 객체가 없을 경우 기본값 설정
            logger.warning("AdminSetting 객체가 없어 기본값으로 설정합니다.")
            hour = 8
            minute = 0



        job_id = 'push_scheduler'
        job = scheduler.get_job(job_id)
        print('job',job)

        if job:
            print('aa')
            # DjangoJob 모델에서 동일한 ID를 가진 작업 삭제
            django_job = DjangoJob.objects.filter(id=job_id).first()
            print('django_job:', django_job)
            if django_job:
                django_job.delete()
                print(f'기존 DjangoJob({job_id}) 삭제')
            else:
                print(f'{job_id}에 해당하는 DjangoJob이 존재하지 않습니다.')
            print('jobjob')
            scheduler.add_job(
                send_push_notifications,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id
            )
            logger.info(f"Job {job_id} modified to run {hour}: {minute}.")
            print('bb')
            # 등록된 job정보 출력
            for job in scheduler.get_jobs():
                job_id = job.id
                job_name = job.name
                job_trigger = job.trigger
                print(f"Job ID: {job_id}, Job Name: {job_name}, Job Trigger: {job_trigger}")
            print('bb')
        else:
            print('else')
            logger.warning(f"Job '{job_id}' not found.")

        logger.info("Scheduler updated!")




# api/v1/adms/terms/
class Terms(APIView):
    serializer_class = Admin_settingsSerializer

    # Get 메소드에 대한 스키마 정의 및 예시 포함
    @extend_schema(tags=['Adms'],
        description="Admin settings에서 term_date, term_time 조회",
    )

    def get(self, request):
        try:
            # first()로 row의 존재여부 확인 row가 없으면 예외발생하지 않고 None반환!
            term_date = AdminSetting.objects.first()
            if term_date:
                serializer = Admin_settingsSerializer(term_date)
                response_serializer = Admin_settingsSerializer(serializer.instance, fields=('term_date','term_time'))
                return Response(response_serializer.data, status=status.HTTP_200_OK)
                # return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('term_date 또는 term_time이 없습니다.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            Response({'Error':'오류가 있습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Post 메소드에 대한 스키마 정의 및 예시 포함
    @extend_schema(tags=['Adms'],
        examples=[
            OpenApiExample(
                'Example',
                value={"term_date": "0030",
                        "term_time": "0110"
                },
                request_only=True,  # 요청 본문에서만 예시 사용
            )
        ],
        description="(화면없음): 프론트에서 term_date, term_time을 받아 admin_settings의 term_date, term_time에 저장"
    )
    def post(self, request):
        try:
            # insert or update
            # target_row의 값을 통해 새로운 row를 생성하는 것이 아닌 기존의 row를 선택
            target_row = AdminSetting.objects.first()

            if target_row:
                # update
                # 관리자 세팅과 관련 값은 하나만 유지하기로 했기에 1번 row로 설정
                # partial=True 옵션으로 row전체 update가 아닌 일부만 update
                serializer = Admin_settingsSerializer(target_row, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('term_date', 'term_time'))
                    self.reschedule_term()
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                # 객체가 존재하지 않을 경우
                # insert
                serializer = Admin_settingsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_serializer = Admin_settingsSerializer(serializer.instance, fields=('term_date', 'term_time'))
                    self.reschedule_term()
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Error':'오류가 있습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def reschedule_term(self):
        # AdminSetting 테이블에서 term_time 가져오기
        try:
            scheduler_time = AdminSetting.objects.first().term_time
            # 숫자 네자리를 문자열로 변환하여 분리
            scheduler_time_str = str(scheduler_time).zfill(4)  # 네자리로 맞추기 위해 zfill 사용
            hour = int(scheduler_time_str[:2])  # 앞 두 자리
            minute = int(scheduler_time_str[2:])  # 뒤 두 자리
        except AttributeError:
            # 예외 처리: AdminSetting 객체가 없을 경우 기본값 설정
            hour = 1
            minute = 10


        logger = logging.getLogger(__name__)

        job_id = 'term_scheduler'
        job = scheduler.get_job(job_id)
        print('job',job)

        if job:
            print('aa')
            # DjangoJob 모델에서 동일한 ID를 가진 작업 삭제
            django_job = DjangoJob.objects.filter(id=job_id).first()
            print('django_job:', django_job)
            if django_job:
                django_job.delete()
                print(f'기존 DjangoJob({job_id}) 삭제')
            else:
                print(f'{job_id}에 해당하는 DjangoJob이 존재하지 않습니다.')
            print('jobjob')
            scheduler.add_job(
                gpt_today_job,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id
            )
            logger.info(f"Job {job_id} modified to run {hour}: {minute}.")
            print('bb')
            # 등록된 job정보 출력
            for job in scheduler.get_jobs():
                job_id = job.id
                job_name = job.name
                job_trigger = job.trigger
                print(f"Job ID: {job_id}, Job Name: {job_name}, Job Trigger: {job_trigger}")
            print('bb')
        else:
            print('else')
            logger.warning(f"Job '{job_id}' not found.")

        logger.info("Scheduler updated!")

