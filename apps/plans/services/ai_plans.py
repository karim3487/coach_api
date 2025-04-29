from __future__ import annotations

import json
from datetime import date, time, timedelta

from django.conf import settings
from g4f import Client

from apps.plans import exceptions
from apps.plans.choices import PlanStatus
from apps.plans.models import Plan, Schedule
from apps.plans.services.plans import PlanService
from apps.profiles.models import ClientProfile
from apps.programs.models import Program
from apps.workouts.models import Workout

SYSTEM_PROMPT = (
    "You are an elite strength-and-conditioning coach. "
    "Return ONLY a valid JSON structure like this:\n"
    "{\n"
    '  "program_id": 2,\n'
    '  "schedule": [\n'
    '    {"date": "2025-05-01", "workout_id": 101},\n'
    '    {"date": "2025-05-03", "workout_id": 103},\n'
    '    {"date": "2025-05-05", "workout_id": 104}\n'
    "  ]\n"
    "}\n\n"
    "Notes:\n"
    "- Prefer strength workouts if goal_id = 1 (muscle gain).\n"
    "- Avoid exercises dangerous for knees.\n"
    "- Use strictly available_days.\n"
    "- Evenly distribute workouts across weeks.\n"
    "- Preferred training time: 18:00 (for reference only).\n"
)


class AIPlanService:
    """LLM-powered training plan generator."""

    MODEL = "gpt-4o-mini"
    TEMPERATURE = 0.3

    @classmethod
    def create_plan(cls, client: ClientProfile, start_date: date | None = None) -> Plan:
        if Plan.objects.filter(
            client_profile=client, status=PlanStatus.ACTIVE
        ).exists():
            raise exceptions.ActivePlanExists("User already has an active plan.")

        start_date = PlanService.get_nearest_available_date(
            client.available_days, start_date
        )

        try:
            response = cls._request_plan_from_llm(client, start_date)
            return cls._build_plan_from_response(client, response, start_date)
        except Exception:
            fallback_program = Program.objects.first()
            return PlanService.create_training_plan(
                client=client, program=fallback_program, start=start_date
            )

    @classmethod
    def _request_plan_from_llm(cls, client: ClientProfile, start_date: date) -> dict:
        if settings.DEBUG:
            return cls._generate_fake_plan(client, start_date)

        prompt = cls._build_prompt(client, start_date)
        llm_client = Client()

        completion = llm_client.chat.completions.create(
            model=cls.MODEL,
            temperature=cls.TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            web_search=False,
        )

        content = completion.choices[0].message.content
        return json.loads(content)

    @staticmethod
    def _generate_fake_plan(client: ClientProfile, start_date: date) -> dict:
        workouts = Workout.objects.only("id").all()
        program = Program.objects.only("id").first()

        if not workouts or not program:
            raise Exception("No test workouts or programs found.")

        schedule = [
            {
                "date": (start_date + timedelta(days=i)).isoformat(),
                "workout_id": workouts[0].id,
            }
            for i in range(3 * len(client.available_days))
        ]

        return {
            "program_id": program.id,
            "schedule": schedule,
        }

    @staticmethod
    def _build_prompt(client: ClientProfile, start_date: date) -> str:
        workouts_summary = "\n".join(
            f"{w.id}: {w.name}" for w in Workout.objects.only("id", "name")[:100]
        )
        programs_summary = "\n".join(
            f"{p.id}: {p.name}. Duration {p.duration_weeks} weeks"
            for p in Program.objects.only("id", "name")[:20]
        )

        return (
            f"Client:\n"
            f"- Age: {client.age}\n"
            f"- Gender: {client.gender}\n"
            f"- Goal ID: {client.goal_id}\n"
            f"- Location: {client.training_location}\n"
            f"- Contraindications: {client.contraindications}\n"
            f"- Available Days: {client.available_days}\n"
            f"- Preferred Time: {client.preferred_time}\n\n"
            f"Start Date: {start_date}\n\n"
            f"Programs:\n{programs_summary}\n\n"
            f"Workouts:\n{workouts_summary}"
        )

    @staticmethod
    def _build_plan_from_response(
        client: ClientProfile, data: dict, start_date: date
    ) -> Plan:
        program = Program.objects.filter(id=data.get("program_id")).first()
        end_date = AIPlanService._calculate_end_date(data["schedule"])

        plan = Plan.objects.create(
            client_profile=client,
            program=program,
            goal=client.goal,
            start_date=start_date,
            end_date=end_date,
            status="active",
            progress_percent=0,
        )

        AIPlanService._create_schedule(plan, data["schedule"], client.preferred_time)
        return plan

    @staticmethod
    def _calculate_end_date(schedule: list[dict]) -> date:
        return max(date.fromisoformat(item["date"]) for item in schedule)

    @staticmethod
    def _create_schedule(
        plan: Plan, schedule_data: list[dict], preferred_time: time
    ) -> None:
        for idx, entry in enumerate(schedule_data, start=1):
            Schedule.objects.create(
                plan=plan,
                date=date.fromisoformat(entry["date"]),
                time=preferred_time,
                workout_id=entry["workout_id"],
                day_number=idx,
            )
