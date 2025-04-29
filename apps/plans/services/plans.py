from datetime import date, timedelta

from apps.plans import exceptions
from apps.plans.choices import PlanStatus
from apps.plans.models import Plan, Schedule
from apps.profiles.models import ClientProfile
from apps.programs.models import Program


class PlanService:
    """Service for generating training plans for client profiles."""

    @staticmethod
    def create_training_plan(
        client: ClientProfile,
        program: Program,
        start: date | None = None,
    ) -> Plan:
        """Create a new training plan based on selected program."""
        if Plan.objects.filter(
            client_profile=client, status=PlanStatus.ACTIVE
        ).exists():
            raise exceptions.ActivePlanExists("User already has an active plan.")

        workouts = program.get_workouts_in_order()
        if not workouts:
            raise exceptions.NoWorkoutsInProgram("Program has no workouts to assign.")

        start_date = PlanService.get_nearest_available_date(
            client.available_days, start
        )

        plan = Plan.objects.create(
            client_profile=client,
            program=program,
            goal=client.goal,
            start_date=start_date,
            status=PlanStatus.ACTIVE,
            progress_percent=0,
        )

        end_date = PlanService._generate_schedule(
            plan=plan,
            client_profile=client,
            workouts=workouts,
            start=start_date,
        )

        plan.end_date = end_date
        plan.save(update_fields=["end_date"])

        return plan

    @staticmethod
    def _generate_schedule(
        plan: Plan, client_profile: ClientProfile, workouts: list, start: date
    ) -> date:
        """Generate workout schedule entries for the plan and return calculated end_date."""  # noqa: E501

        available_days = [day.lower() for day in client_profile.available_days]
        preferred_time = client_profile.preferred_time

        current_date = start
        day_number = 1
        workout_index = 0

        while workout_index < len(workouts):
            if current_date.strftime("%a").lower()[:3] in available_days:
                Schedule.objects.create(
                    plan=plan,
                    date=current_date,
                    time=preferred_time,
                    workout=workouts[workout_index],
                    day_number=day_number,
                    completed=False,
                )
                day_number += 1
                workout_index += 1

            current_date += timedelta(days=1)

        return current_date - timedelta(days=1)

    @staticmethod
    def get_nearest_available_date(
        available_days: list[str], from_date: date | None = None
    ) -> date:
        """Return the next closest date matching available_days."""
        from_date = from_date or date.today()
        available_days = [day.lower() for day in available_days]

        weekdays_map = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6,
        }

        target_weekdays = {weekdays_map[day] for day in available_days}

        for offset in range(7):
            candidate = from_date + timedelta(days=offset)
            if candidate.weekday() in target_weekdays:
                return candidate

        return from_date
