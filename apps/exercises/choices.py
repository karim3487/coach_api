from django.db import models


class EquipmentType(models.TextChoices):
    BODYWEIGHT = "bodyweight", "Собственный вес"
    DUMBBELLS = "dumbbells", "Гантели"
    BARBELL = "barbell", "Штанга"
    RESISTANCE_BANDS = "resistance_bands", "Эспандеры / Резиновые ленты"
    KETTLEBELL = "kettlebell", "Гиря"
    MACHINE = "machine", "Тренажёры"
    BENCH = "bench", "Скамья"
    CABLE = "cable", "Блочный тренажёр"
    MEDICINE_BALL = "medicine_ball", "Медицинский мяч"
    STABILITY_BALL = "stability_ball", "Фитбол"
    BOSU_BALL = "bosu_ball", "Босу-платформа"
    FOAM_ROLLER = "foam_roller", "Массажный ролик (Foam Roller)"
    BOX = "box", "Плиометрическая тумба"
    PULL_UP_BAR = "pull_up_bar", "Турник"
    ROPE = "rope", "Канат"
    TRX = "trx", "TRX-петли"
    SMITH_MACHINE = "smith_machine", "Силовая рама (Смит-машина)"
    MAT = "mat", "Коврик"
    OTHER = "other", "Другое"


class MuscleGroup(models.TextChoices):
    CHEST = "chest", "Грудные мышцы"
    BACK = "back", "Спина"
    SHOULDERS = "shoulders", "Плечи"
    ARMS = "arms", "Руки"
    LEGS = "legs", "Ноги"
    CORE = "core", "Пресс / Корпус"
    FULL_BODY = "full_body", "Всё тело"
    FLEXIBILITY = "flexibility", "Гибкость / Подвижность"
    OTHER = "other", "Другое"
