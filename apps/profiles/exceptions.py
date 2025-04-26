class BackupCodeError(Exception):
    """Base exception for backup code logic."""


class BackupCodeInvalidOrAlreadyUsed(BackupCodeError):
    """Raised when a backup code has already been used."""


class TelegramIDAlreadyLinked(BackupCodeError):
    """Raised when telegram_id is already linked to profile."""


class TelegramIDAlreadyUsed(Exception):
    """Raised when telegram_id is already used."""
