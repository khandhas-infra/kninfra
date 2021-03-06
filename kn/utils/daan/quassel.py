import os.path
import sqlite3
import hashlib
import logging

from django.conf import settings
from kn.base._random import pseudo_randstr


def quassel_setpass(daan, user, password):
    db_path = os.path.join(settings.QUASSEL_CONFIGDIR, 'quassel-storage.sqlite')
    conn = sqlite3.connect(db_path)
    hashed_pw = hashlib.sha1(password).hexdigest()
    c = conn.cursor()
    c.execute("UPDATE quasseluser SET password=? where username=?",
                                    (hashed_pw, user))
    conn.commit()

def apply_quassel_changes(daan, changes):
    if not changes:
        return
    db_path = os.path.join(settings.QUASSEL_CONFIGDIR, 'quassel-storage.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for user in changes['remove']:
        logging.info('quassel: removing %s', user)
        c.execute("DELETE FROM quasseluser WHERE username=?", (user,))
    for user in changes['add']:
        logging.info('quassel: adding %s', user)
        hashed_pw = hashlib.sha1(pseudo_randstr()).hexdigest()
        c.execute("INSERT INTO quasseluser(username, password) VALUES (?, ?)",
                    (user, hashed_pw))
    conn.commit()

# vim: et:sta:bs=2:sw=4:
