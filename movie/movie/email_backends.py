# #  In the root of your Django project (next to settings.py),  create email_backends.py
# import smtplib
# from django.core.mail.backends.smtp import EmailBackend

# class SSLUnsafeEmailBackend(EmailBackend):
#     def open(self):
#         try:
#             self.connection = self.connection or smtplib.SMTP(
#                 self.host,  self.port,  **self.connection_params
#             )
#             if self.use_tls:
#                 self.connection.starttls(context=self.ssl_context)
#             if self.use_ssl:
#                 self.connection = smtplib.SMTP_SSL(
#                     self.host,  self.port,  context=self.ssl_context
#                 )
#             if self.username and self.password:
#                 self.connection.login(self.username,  self.password)
#             return True
#         except:
#             self.connection = None
#             if self.fail_silently:
#                 return False
#             raise
