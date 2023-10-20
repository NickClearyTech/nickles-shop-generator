from celery_settings import app as celery_app


@celery_app.task(bind=True)
def an_example(self):
    print("hello there")
