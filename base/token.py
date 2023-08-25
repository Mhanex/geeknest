from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six, time, datetime



class GenerateToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

    def make_token(self, user):
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        return self._make_token_with_timestamp(user, timestamp)
    









#Token Generator with time
# class GenerateToken(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         current_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
#         time_difference = current_timestamp - timestamp
#         if time_difference > 300:  # 300 seconds = 5 minutes
#             return ""
#         return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

#     def make_token(self, user):
#         timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
#         return self._make_token_with_timestamp(user, timestamp)
