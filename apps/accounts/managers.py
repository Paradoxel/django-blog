from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    Replaces Django's default manager to support email-based authentication
    instead of username-based.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        password=None is intentional — allows creating users without passwords
        (e.g. for future OAuth/social login support).
        """
        if not email:
            raise ValueError("Email is required")

        # normalize_email lowercases the domain part: "User@Gmail.COM" → "User@gmail.com"
        email = self.normalize_email(email)

        # self.model refers to the User class this manager is attached to
        user = self.model(email=email, **extra_fields)

        # set_password hashes the password — never stores plain text
        # set_password(None) sets an unusable password (user can't login with password)
        user.set_password(password)

        # using=self._db supports multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with all permissions enabled.
        Called by: python manage.py createsuperuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Guard clauses — prevent creating a superuser without full permissions
        # These fire if someone explicitly passes is_staff=False or is_superuser=False
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)