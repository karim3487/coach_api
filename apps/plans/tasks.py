from celery import shared_task

from apps.plans.services.ai_plans import AIPlanService
from apps.profiles.models import ClientProfile


@shared_task(bind=True)
def create_ai_plan_task(self, profile_id: int) -> int:
    """Async creation of AI training plan."""
    profile = ClientProfile.objects.get(id=profile_id)
    plan = AIPlanService.create_plan(profile)
    return plan.id
