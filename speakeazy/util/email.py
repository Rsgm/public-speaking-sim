from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from speakeazy.recordings.mixins import GRADER


def send_feedback_email(submission, grader):
    user = submission.recording.project.user
    context = {
        'submission': submission,
        'user': user,
        'grader': grader,
        'link_type': GRADER
    }

    plaintext = get_template('emails/evaluation.txt').render(context)
    html = get_template('emails/evaluation.html').render(context)

    msg = EmailMultiAlternatives(
        _("New Recording Evaluation"),
        plaintext,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
