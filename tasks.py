# celery.py

from celery import Celery
from fastapi import HTTPException
from azure_client import container_client, model

# app = Celery(
#     'myapp',
#     broker='pyamqp://guest@localhost//',  # Use the RabbitMQ URL here
#     backend='rpc://',
# )

# # Load task modules from all registered Django app configs.
# app.config_from_object('django.conf:settings', namespace='CELERY')


# celery_app.py
BROKER_PORT = 'localhost:5672'
USER = 'guest'
PASS = 'guest'

# def create_celery_app():
celery_app = Celery(__name__)

celery_app.conf.update(
    broker_url=f"amqp://{USER}:{PASS}@{BROKER_PORT}/",
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
)

    # return celery

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)

@celery_app.task(name="transcribe_video")
def transcribe_video(file_id: str):
    print("Transcribing video...")
    try:
        blob_client = container_client.get_blob_client(file_id)
       
        with open(f"videos/{file_id}", "wb") as file:
            file.write(blob_client.download_blob().readall())

        video_transcription = model.transcribe(f"videos/{file_id}")
        print(video_transcription, "DONE")

    except Exception as e:
        print(e)
        return HTTPException(401, "Something went wrong..")
    
    return {
            'message':'Video transcription successful',
            'file_id': file_id,
            'video_transcription': video_transcription['text']
           }