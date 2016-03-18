
LIST_AUDIENCE = 'list_audience'
VIEW_AUDIENCE = 'view_audience'
ADD_AUDIENCE = 'add_audience'
UPDATE_AUDIENCE = 'update_audience'
DELETE_AUDIENCE = 'delete_audience'

LIST_USER = 'list_user'
VIEW_USER = 'view_user'
UPDATE_USER = 'update_user'
DELETE_USER = 'delete_user'

LIST_INVITE = 'list_invite'
VIEW_INVITE = 'view_invite'
ADD_INVITE = 'add_invite'
UPDATE_INVITE = 'update_invite'
DELETE_INVITE = 'delete_invite'

LIST_SUBMISSION = 'list_submission'
VIEW_SUBMISSION = 'view_submission'
ADD_SUBMISSION = 'add_submission'  # rename to submit, group with evaluate
UPDATE_SUBMISSION = 'update_submission'
DELETE_SUBMISSION = 'delete_submission'
EVALUATE_SUBMISSION = 'evaluate_submission'

# LIST_ = 'list_'
# VIEW_ = 'view_'
# ADD_ = 'add_'
# UPDATE_ = 'update_'
# DELETE_ = 'delete_'


PERMISSIONS = (
    ("Audience", (
        (LIST_AUDIENCE, "List audience"),
        (VIEW_AUDIENCE, "View audience"),
        (ADD_AUDIENCE, "Add audience"),
        (UPDATE_AUDIENCE, "Update audience"),
        (DELETE_AUDIENCE, "Delete audience"),
    )),

    ("User", (
        (LIST_USER, "List user"),
        (VIEW_USER, "View user"),
        (UPDATE_USER, "Update user"),
        (DELETE_USER, "Delete user"),
    )),

    ("Invite", (
        (LIST_INVITE, "List invite"),
        (VIEW_INVITE, "View invite"),
        (ADD_INVITE, "Add invite"),
        (UPDATE_INVITE, "Update invite"),
        (DELETE_INVITE, "Delete invite"),
    )),

    ("Submission", (
        (LIST_SUBMISSION, "List submission"),
        (VIEW_SUBMISSION, "View submission"),
        (ADD_SUBMISSION, "Add submission"),
        (UPDATE_SUBMISSION, "Update submission"),
        (DELETE_SUBMISSION, "Delete submission"),
        (EVALUATE_SUBMISSION, "Evaluate submission"),
    )),
)
