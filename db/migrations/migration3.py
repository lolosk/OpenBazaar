#!/usr/bin/env python

import argparse

from pysqlcipher import dbapi2 as sqlite

from node import constants


def upgrade(db_path):
    with sqlite.connect(db_path) as con:
        cur = con.cursor()

        # Use PRAGMA key to encrypt / decrypt database.
        cur.execute("PRAGMA key = 'passphrase';")

        try:
            cur.execute("ALTER TABLE contracts "
                        "ADD COLUMN refund_requested INT DEFAULT 0")
            cur.execute("ALTER TABLE contracts "
                        "ADD COLUMN cancelled INT DEFAULT 0")
            cur.execute("ALTER TABLE contracts "
                        "ADD COLUMN refund_address TEXT")
            print 'Upgraded'
            con.commit()
        except sqlite.Error as e:
            print 'Exception: %s' % e


def downgrade(db_path):
    with sqlite.connect(db_path) as con:
        cur = con.cursor()

        # Use PRAGMA key to encrypt / decrypt database.
        cur.execute("PRAGMA key = 'passphrase';")

        cur.execute("ALTER TABLE contracts DROP COLUMN refund_requested")
        cur.execute("ALTER TABLE contracts DROP COLUMN cancelled")
        cur.execute("ALTER TABLE contracts DROP COLUMN refund_address")

        print 'Downgraded'
        con.commit()


def main():
    parser = argparse.ArgumentParser(description="Migrate the database")
    parser.add_argument("path", help="the location of the database",
                        nargs='?', default=constants.DB_PATH)
    parser.add_argument("action", help="the action you want to perform",
                        choices=["upgrade", "downgrade"])

    args = parser.parse_args()
    if args.action == "upgrade":
        upgrade(args.path)
    else:
        downgrade(args.path)


if __name__ == "__main__":
    main()
