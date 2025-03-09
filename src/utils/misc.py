import billmgr.db as db
import billmgr.misc as misc


def from_muliple_keys(params, keys, default):
    for key in keys:
        if key in params:
            return params[key]
    return default


def get_account_id(item):
    item_info = misc.iteminfo(item)
    return item_info["account_id"]


def get_billaccount_email(item):
    acc_id = get_account_id(item)
    return db.db_query(
        "SELECT email FROM user WHERE account=%s ORDER BY id ASC", acc_id
    )[0]["email"]
