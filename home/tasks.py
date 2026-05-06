from celery import shared_task
from .models import Objective

@shared_task
def delete_completed_tasks_worker():
    num_of_objective_deleted, _ = Objective.objects.filter(status=True).delete()
    return f"{num_of_objective_deleted} objectives deleted"