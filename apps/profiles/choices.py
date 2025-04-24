from django.db import models


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Contraindication(models.TextChoices):
    HEART_DISEASE = "heart_disease", "Heart disease"
    HYPERTENSION = "hypertension", "Hypertension"
    DIABETES = "diabetes", "Diabetes"
    ASTHMA = "asthma", "Asthma"
    JOINT_PROBLEMS = "joint_problems", "Joint problems"
    PREGNANCY = "pregnancy", "Pregnancy"
    BACK_PAIN = "back_pain", "Back pain"
    OBESITY = "obesity", "Obesity"
    NONE = "none", "None"


class TrainingDay(models.TextChoices):
    MON = "mon", "Monday"
    TUE = "tue", "Tuesday"
    WED = "wed", "Wednesday"
    THU = "thu", "Thursday"
    FRI = "fri", "Friday"
    SAT = "sat", "Saturday"
    SUN = "sun", "Sunday"
