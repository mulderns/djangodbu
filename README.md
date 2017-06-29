# djangodbu
Tools for debugging Django

Currently there is one helper routine to print out django model instances to console, intended to be used in django shell/shell_plus.

The output contains attributes and values with their type information.

## Installation

    $ pip install djangodbu

## Usage

Start Django shell_plus: `python manage.py shell_plus`

    >>> from djangodbu.shell import dorm
    >>> dorm(MyModel.objects.get(id=123))

will produce colorized output:

             instancemethod serializable_value
             instancemethod set_password
             instancemethod set_unusable_password
             instancemethod unique_error_message
             instancemethod validate_unique
                    unicode USERNAME_FIELD: username
                    unicode email: some.one@example.org
                    unicode first_name: Some
                    unicode last_name: One
                    unicode password: pbkdf2_sha256$20000$
                    unicode username: someone
                       list REQUIRED_FIELDS: 1
                       long id: 10780
                       long pk: 10780
    so.mo.na.AccountingUser accountinguser: 651 > 'Some One'
             RelatedManager additionalemail_set: 1
             RelatedManager callback_set: 0
             RelatedManager campaigncode_set: 0
             RelatedManager grouplog: 142
         ManyRelatedManager groups: 0
             RelatedManager log: 379
             RelatedManager logevent_set: 89
             RelatedManager message_set: 11
           lo.pa.to.Payment payment: 510 > 'Bob & Uncle'
             RelatedManager settings_set: 1
             RelatedManager social_auth: 0
         ManyRelatedManager user_permissions: 0
             RelatedManager worker_set: 1
                   NoneType activationcode
                   NoneType auth_token
                   NoneType employee
                       bool is_active: True
                       bool is_superuser: False
          datetime.datetime date_joined: 2016-05-01 08:13:16+00:00
          datetime.datetime last_login: 2016-06-20 07:48:51+00:00
                       type DoesNotExist: DoesNotExist
                   classobj Meta: Meta
                       type MultipleObjectsReturned: MultipleObjectsReturned

