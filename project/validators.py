from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from users.models import CustomUserPasswordHistory


class CaptialAndSymbolValidator:
    def __init__(self, number_of_capitals=1, number_of_symbols=1, symbols="[~!@#$%^&*()_+{}\":;'[]"):
        self.number_of_capitals = number_of_capitals
        self.number_of_symbols = number_of_symbols
        self.symbols = symbols

    def validate(self, password, user=None):
        capitals = [char for char in password if char.isupper()]
        symbols = [char for char in password if char in self.symbols]
        if len(capitals) < self.number_of_capitals:
            raise ValidationError(
                _("This password must contain at least %(min_length)d capital letters."),
                code='password_too_short',
                params={'min_length': self.number_of_capitals},
            )
        if len(symbols) < self.number_of_symbols:
            raise ValidationError(
                _("This password must contain at least %(min_length)d symbols."),
                code='password_too_short',
                params={'min_length': self.number_of_symbols},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(number_of_capitals)d capital letters and %(number_of_symbols)d symbols."
            % {'number_of_capitals': self.number_of_capitals, 'number_of_symbols': self.number_of_symbols}
        )


class DontRepeatValidator:
    def __init__(self, history=3):
        self.history = history

    def validate(self, password, user=None):
        for last_pass in self._get_last_passwords(user):
            if check_password(password=password, encoded=last_pass):
                self._raise_validation_error()

    def get_help_text(self):
        return _(f'You cannot repeat passwords, History: {str(self.history)}')

    def _raise_validation_error(self):
        raise ValidationError(
            _("This password has been used before."),
            code='password_has_been_used',
            params={'history': self.history},
        )

    def _get_last_passwords(self, user):
        all_history_user_passwords = CustomUserPasswordHistory.objects.filter(username_id=user).order_by('id')
        to_index = all_history_user_passwords.count() - self.history
        to_index = to_index if to_index > 0 else None
        if to_index:
            [u.delete() for u in all_history_user_passwords[0:to_index]]

        return [p.old_pass for p in all_history_user_passwords[to_index:]]