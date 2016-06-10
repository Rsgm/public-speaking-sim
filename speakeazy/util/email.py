from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from speakeazy.recordings.mixins import OWNER


def send_feedback_email(submission, grader):
    user = submission.recording.project.user
    context = {
        'submission': submission,
        'user': user,
        'grader': grader,
        'link_type': OWNER
    }

    plaintext = get_template('emails/feedback.txt').render(context)
    html = get_template('emails/feedback.html').render(context)

    msg = EmailMultiAlternatives(
        _("New Recording Feedback"),
        plaintext,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
