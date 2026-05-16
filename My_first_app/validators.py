import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# OopCompanion:suppressRename


class StrongPasswordValidator:
    """
    Custom password validator that enforces strong password requirements:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    
    def validate(self, password, user=None):
        errors = []

        if len(password) < 8:
            errors.append(_("Password must be at least 8 characters long."))
        

        if not re.search(r'[A-Z]', password):
            errors.append(_("Password must contain at least one uppercase letter."))
        

        if not re.search(r'[a-z]', password):
            errors.append(_("Password must contain at least one lowercase letter."))

        if not re.search(r'\d', password):
            errors.append(_("Password must contain at least one digit."))
        

        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', password):
            errors.append(_("Password must contain at least one special character."))
        

        if re.search(r'(.)\1{2,}', password):  # Three or more consecutive same characters
            errors.append(_("Password cannot contain three or more consecutive identical characters."))
        

        if self.is_sequential(password):
            errors.append(_("Password cannot contain sequential characters (e.g., '123', 'abc')."))
        
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long and contain at least "
            "one uppercase letter, one lowercase letter, one digit, and one special character. "
            "It cannot contain three or more consecutive identical characters or sequential characters."
        )
    
    def is_sequential(self, password):

        password_lower = password.lower()

        for i in range(len(password_lower) - 2):
            if (password_lower[i].isdigit() and 
                password_lower[i+1].isdigit() and 
                password_lower[i+2].isdigit()):
                if (int(password_lower[i+1]) == int(password_lower[i]) + 1 and
                    int(password_lower[i+2]) == int(password_lower[i+1]) + 1):
                    return True
        

        for i in range(len(password_lower) - 2):
            if (password_lower[i].isalpha() and 
                password_lower[i+1].isalpha() and 
                password_lower[i+2].isalpha()):
                if (ord(password_lower[i+1]) == ord(password_lower[i]) + 1 and
                    ord(password_lower[i+2]) == ord(password_lower[i+1]) + 1):
                    return True
        
        return False


class CommonPasswordValidator:

    
    COMMON_PASSWORDS = {
        'password', '123456', '123456789', '12345678', '12345', '1234567',
        '1234567890', 'qwerty', 'abc123', 'password123', 'admin', 'letmein',
        'welcome', 'monkey', '1234', 'dragon', 'master', 'hello', 'freedom',
        'whatever', 'qazwsx', 'trustno1', '123qwe', '1q2w3e4r', 'zxcvbnm',
        'iloveyou', 'adobe123', '123123', 'sunshine', 'princess', 'azerty',
        'trustno1', '000000', '111111', '222222', '333333', '444444',
        '555555', '666666', '777777', '888888', '999999'
    }
    
    def validate(self, password, user=None):
        if password.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                _("This password is too common. Please choose a more secure password.")
            )
    
    def get_help_text(self):
        return _("Your password cannot be a commonly used password.")


class UsernamePasswordValidator:

    
    def validate(self, password, user=None):
        if not user:
            return
        
        username = getattr(user, 'username', '')
        email = getattr(user, 'email', '')
        

        email_username = email.split('@')[0] if email else ''
        
        password_lower = password.lower()
        
        if username and username.lower() in password_lower:
            raise ValidationError(
                _("Password cannot contain your username.")
            )
        
        if email_username and email_username.lower() in password_lower:
            raise ValidationError(
                _("Password cannot contain part of your email address.")
            )
    
    def get_help_text(self):
        return _("Your password cannot contain your username or email address.")
