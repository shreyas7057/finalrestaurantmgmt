from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type



class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user,timestamp):

        # this will make token with combination of user active or not then its id and timestamp when email was send
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()