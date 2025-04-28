import re
from collections.abc import Callable, Iterable

import requests
from decouple import config
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.common.choices import ExerciseType
from apps.exercises.choices import EquipmentType, MuscleGroup
from apps.exercises.models import Exercise

MUSCLE_GROUP_MAPPING = {
    "chest": MuscleGroup.CHEST,
    "back": MuscleGroup.BACK,
    "shoulders": MuscleGroup.SHOULDERS,
    "upper arms": MuscleGroup.ARMS,
    "lower arms": MuscleGroup.ARMS,
    "upper legs": MuscleGroup.LEGS,
    "lower legs": MuscleGroup.LEGS,
    "waist": MuscleGroup.CORE,
    "glutes": MuscleGroup.LEGS,
    "abs": MuscleGroup.CORE,
    "hamstrings": MuscleGroup.LEGS,
    "quads": MuscleGroup.LEGS,
    "adductors": MuscleGroup.LEGS,
    "calves": MuscleGroup.LEGS,
    "lats": MuscleGroup.BACK,
    "spine": MuscleGroup.BACK,
    "traps": MuscleGroup.SHOULDERS,
    "flexibility": MuscleGroup.FLEXIBILITY,
}

# Для equipment → EquipmentType
EQUIPMENT_MAPPING = {
    "body weight": EquipmentType.BODYWEIGHT,
    "dumbbell": EquipmentType.DUMBBELLS,
    "barbell": EquipmentType.BARBELL,
    "resistance band": EquipmentType.RESISTANCE_BANDS,
    "kettlebell": EquipmentType.KETTLEBELL,
    "cable": EquipmentType.MACHINE,
    "leverage machine": EquipmentType.MACHINE,
    "stability ball": EquipmentType.MAT,
    "medicine ball": EquipmentType.MAT,
    "bench": EquipmentType.BENCH,
    "sled machine": EquipmentType.MACHINE,
    "smith machine": EquipmentType.MACHINE,
    "bosu ball": EquipmentType.MAT,
    "band": EquipmentType.RESISTANCE_BANDS,
    "none": EquipmentType.BODYWEIGHT,
}

DEFAULT_EXERCISE_TYPE = ExerciseType.STRENGTH

API_URL = "https://exercisedb.p.rapidapi.com/exercises"
HEADERS = {
    "X-RapidAPI-Key": config("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
}

Rule = Callable[[dict], bool]


def _make_name_rule(*keywords: str) -> Rule:
    """Создаёт правило, проверяющее наличие целых слов из `keywords` в поле 'name'."""
    pattern = re.compile(
        r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", flags=re.I
    )
    return lambda data: bool(pattern.search(data.get("name", "")))


def _body_part_is(*parts: str) -> Rule:
    parts_lower = {p.lower() for p in parts}
    return lambda data: data.get("bodyPart", "").lower() in parts_lower


RULES: dict[ExerciseType, Iterable[Rule]] = {
    ExerciseType.CARDIO: (
        _body_part_is("cardiovascular system"),
        _make_name_rule("run", "jog", "cardio"),
    ),
    ExerciseType.STRETCHING: (_make_name_rule("stretch"),),
    ExerciseType.YOGA: (_make_name_rule("yoga", "asana"),),
    ExerciseType.MIXED: (
        _make_name_rule("burpee", "thruster", "complex", "amrap", "emom"),
    ),
    # STRENGTH идёт в «по умолчанию»
}


def infer_exercise_type(api_exercise: dict) -> ExerciseType:
    for ex_type, rules in RULES.items():
        if any(rule(api_exercise) for rule in rules):
            return ex_type
    return ExerciseType.STRENGTH


def fetch_all_exercises(limit: int = 100) -> list[dict]:
    """Fetches all exercises from API, paginated by limit."""
    all_exercises = []
    offset = 0

    while True:
        params = {
            "limit": limit,
            "offset": offset,
        }
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        exercises = response.json()
        if not exercises:
            break

        all_exercises.extend(exercises)

        if len(exercises) < limit:
            break

        offset += limit

    return all_exercises


def map_exercise(api_exercise: dict) -> dict:
    body_part = api_exercise.get("bodyPart", "").lower()
    equipment = api_exercise.get("equipment", "").lower()

    return {
        "name": api_exercise.get("name", "").capitalize(),
        "type": infer_exercise_type(api_exercise),
        "muscle_group": MUSCLE_GROUP_MAPPING.get(body_part, MuscleGroup.OTHER),
        "equipment": EQUIPMENT_MAPPING.get(equipment, EquipmentType.OTHER),
        "difficulty": "beginner",
        "description": api_exercise.get("target", ""),
        "media_url": api_exercise.get("gifUrl"),
    }


class Command(BaseCommand):
    help = "Imports exercises from RapidAPI ExerciseDB"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Fetching exercises..."))

        try:
            exercises_data = fetch_all_exercises()
        except requests.RequestException as exc:
            self.stderr.write(self.style.ERROR(f"Failed to fetch exercises: {exc}"))
            return

        created_count = 0

        with transaction.atomic():
            for api_exercise in exercises_data:
                mapped_data = map_exercise(api_exercise)

                if not Exercise.objects.filter(name=mapped_data["name"]).exists():
                    Exercise.objects.create(**mapped_data)
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"✅ Successfully created {created_count} exercises.")
        )
