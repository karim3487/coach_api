class PlanError(Exception):
    """Base exception for plan-related errors."""

    pass


class ActivePlanExists(PlanError):
    """Raised when trying to create a new plan while an active one already exists."""

    pass


class ProgramNotCompatible(PlanError):
    """Raised when selected program is not compatible with the user's profile."""

    pass


class NoWorkoutsInProgram(PlanError):
    """Raised when trying to create a plan from a program without any workouts."""

    pass
