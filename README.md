# DjangoDBU
Tools for debugging Django

## Summary

- dorm: Pretty print models, querysets, etc.
- ds: Search dictionaries and lists for string.
- ago: Generate datetimes.

## DORM - Debug Django ORM

Pretty print django objects with syntax highlighting, column layout and shorthands.

Dorm can handle:
- model instances
    + attribute coloring + grouping
    + attribute values
    + print in parallel columns
- querysets
    + print all rows in queryset
    + prints selected values (in values=[] fashion) or value from 'callable'
    + paginate, with skipt to page
- query
    + syntax highlight
- list / dict / tuple through pprint

## Requirements
- Python 2
- Django
- sqlparse

## Installation

    $ pip install djangodbu

## Usage

Start Django shell_plus: `python manage.py shell_plus`
```python
>>> from djangodbu import dorm
>>> dorm(MyModel.objects.get(id=123))
```
```
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
                    long id: 357
                    long pk: 357
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
```

Printing QuerySets:
```python
>>> dorm(MyModel.objects.all())
1: userA
2: userB
4: userD
20: userY
...
```
Selecting values for QuerySet:
```python
>>> dorm(User.objects.all(), v='first_name, email')

    id: firstname  email
------------------------------------------------
    1: abcd       userA@example.org
    2: efghij     userB@example.org
    4: kl         userD@example.org
    20: Mnopqrst  userY@example.org
...
```
Print Query:
```python
>>> dorm(User.objects.filter(email__isnull=False).exclude(first_name='kl').query)
```
```sql
SELECT auth_user.id,
       auth_user.password,
       auth_user.username,
       auth_user.first_name,
       auth_user.last_name,
       auth_user.email
FROM auth_user WHERE (auth_user.email IS NOT NULL
       AND NOT (auth_user.first_name = kl))
```

## DS - Dictionary search

'ds' accepts dictionaries and lists.

### Usage

```python
    >>> from djangodbu import ds
    >>> ds(haystack_dict, 'needle')
```

```python
    >>> from dbu.utils import ds

    >>> test = { 'a' : ['b', 'c'], 'd':3, 'e': { 'f':'g'}, 'h': 'i' }

    >>> ds(test, 'a')
    a: ['b', 'c']
    >>> ds(test, 'b')
    a > 0 : 'b'
    >>> ds(test, 'c')
    a > 1 : 'c'
    >>> ds(test, 'd')
    d: 3
    >>> ds(test, 'e')
    e: {'f': 'g'}
    >>> ds(test, 'f')
    e > f: 'g'
    >>> ds(test, 'g')
    e > f: 'g'
    >>> ds(test, 'h')
    h: 'i'
    >>> ds(test, 'i')
    h: 'i'
```


## Project url

[djangodbu on github](https://github.com/mulderns/djangodbu)

[djangodbu on pypi](https://pypi.python.org/pypi?name=djangodbu)
