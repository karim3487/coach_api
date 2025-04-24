import hashlib
import secrets

from apps.profiles.models import BackupCode, ClientProfile, TelegramID


class BackupCodeService:
    def generate_codes(self, profile: ClientProfile, count: int = 10) -> list[str]:
        raw_codes = []
        for _ in range(count):
            raw = secrets.token_urlsafe(8)
            salt = secrets.token_hex(8)
            hashed = self._hash_code(raw, salt)
            BackupCode.objects.create(profile=profile, code_hash=hashed, salt=salt)
            raw_codes.append(raw)
        return raw_codes

    def consume_code(self, raw_code: str) -> BackupCode:
        for code in BackupCode.objects.filter(used_at__isnull=True):
            if self._hash_code(raw_code, code.salt) == code.code_hash:
                code.mark_used()
                return code
        raise Exception("Invalid or already used code.")

    def link_telegram_id(self, code: str, telegram_id: int) -> ClientProfile:
        backup_code = self.consume_code(code)
        profile = backup_code.profile

        if not profile.telegram_ids.filter(telegram_id=telegram_id).exists():
            TelegramID.objects.create(profile=profile, telegram_id=telegram_id)

        return profile

    def _hash_code(self, raw: str, salt: str) -> str:
        return hashlib.sha256((raw + salt).encode()).hexdigest()

    def revoke_unused(self, profile: ClientProfile):
        BackupCode.objects.filter(profile=profile, used_at__isnull=True).delete()
