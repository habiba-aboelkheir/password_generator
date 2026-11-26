import secrets
import string


def generate_password(
    length: int = 12,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    pools = []
    guaranteed = []

    if use_upper:
        pools.append(string.ascii_uppercase)
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        pools.append(string.ascii_lowercase)
        guaranteed.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        pools.append(string.digits)
        guaranteed.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?"
        pools.append(symbols)
        guaranteed.append(secrets.choice(symbols))

    if not pools:
        raise ValueError("اختر نوعًا واحدًا على الأقل من المحارف.")

    if length < len(guaranteed):
        raise ValueError(
            f"الطول يجب أن يكون {len(guaranteed)} أو أكثر لتشمل كل الأنواع المحددة."
        )

    all_chars = "".join(pools)
    password_chars = guaranteed + [
        secrets.choice(all_chars) for _ in range(length - len(guaranteed))
    ]

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def evaluate_strength(length: int, active_options: int) -> tuple[str, str]:
    if length < 8 or active_options == 1:
        return "القوة: ضعيفة", "#dc2626"
    if length >= 12 and active_options >= 3:
        return "القوة: قوية جدًا", "#15803d"
    return "القوة: متوسطة", "#d97706"