# Bank Ozar

A small terminal banking application. A person logs in with a username, is
automatically registered into one of four account "colours" based on rules
evaluated against a personnel directory, and can then deposit, withdraw, and
manage subscriptions from a text menu. Data is persisted to two local SQLite
databases.

## Features

- **Menu-driven session** — view balance, deposit, withdraw, add/remove/list
  subscriptions, close the account, or exit.
- **Colour-based account types** — `Yellow`, `Red`, `Blue`, `Green`, each with
  its own eligibility rule, starting balance, and quirks (see below).
- **Automatic registration** — the first time a known username connects, the
  app finds the matching colour and opens an account with that colour's
  onboarding (e.g. a standing subscription).
- **SQLite persistence** — accounts and subscriptions live in two separate
  local databases, seeded with sample rows on first run.
- **Logging** — actions are written to a log file rather than the terminal,
  so the interactive session stays clean.

## Project structure

```
src/
├── main.py                    entry point: init DB + logging, then run api()
├── api.py                     menu dispatch loop, one handler per option
├── menu.py                    menu rendering, single source of truth for options
├── config.py                  environment-driven configuration
├── log_config.py              logging setup
├── models.py                  AccountType enum, AccountInfo dataclass-like model
├── exceptions.py               domain exception hierarchy
├── utils.py                   date/amount validation helpers
├── logics/
│   ├── logics.py              Logics: validates input, routes to rules + storage
│   ├── base_rules.py          AccountRules: shared default behaviour
│   ├── blue_rules.py          BlueAccountRules
│   ├── red_rules.py           RedAccountRules
│   ├── green_rules.py         GreenAccountRules
│   ├── yellow_rules.py        YellowAccountRules
│   └── services.py            personnel-directory lookup (stubbed)
└── storage/
    ├── storage.py              StorageManager: all SQLite access
    ├── db_setup_accounts.py    creates + seeds the accounts table
    └── db_setup_subscription.py creates + seeds the subscriptions table

tests/                         unittest suite with an in-memory FakeStorage
```

See [`bank_ozar_uml.puml`](bank_ozar_uml.puml) for the full class diagram.

## Account types

| Colour | Starting balance | Qualifies when... | Notable behaviour |
|---|---|---|---|
| Yellow | 0 | has a nickname, or is male in a "ת" organization | Opens with a random recurring charge; balance display is masked; account locks itself once balance goes negative |
| Red | 30,000 | last name contains "ן" and department is אלנקטרוניקה/פסיפס | Opens with a 30‑month standing subscription; capped at 300/deposit on odd days |
| Blue | 1,700 | permanent service ("קבע") and phone contains both "3" and "5" | Withdrawals capped at 100 |
| Green | 0 | rank in {סמל, סמר, רבט} and first name contains "י" | Every balance check adds a 2‑unit bonus |

A person is checked against each colour in turn and registered under the
first one that accepts them; qualifying for none raises
`NoQualifyingAccountTypeError`.

## Getting started

```bash
pip install -r requirements.txt
python -m src.main
```

Configuration is read from the environment, with local defaults:

| Variable | Default | Purpose |
|---|---|---|
| `DB_ACCOUNTS_PATH` | `db.accounts` | SQLite file for accounts |
| `DB_SUBSCRIPTION_PATH` | `db.subscription` | SQLite file for subscriptions |
| `LOG_PATH` | `bank.log` | Log file destination |
| `LOG_LEVEL` | `INFO` | Log verbosity |

On first run, both databases are created and seeded with sample accounts
(`t_osherzi`, `t_shimonv`, `t_idome`, `t_raz_ba`, `t_noabir`), so you can log
in with any of those usernames right away.

## Running tests

```bash
python -m unittest discover tests
```

Tests swap the module-level `STORAGE_MANAGER` singleton for an in-memory
`FakeStorage` (see `tests/support.py`), so no test touches a real database
file.

## Known limitations

- **"Project the next pay day" (menu option 7) is not wired up.** The handler
  in `api.py` is a stub that just prints `"implement"` — it never calls
  `Logics.balance_next_day`. That method also calls `rules.balance_next_day`,
  which doesn't exist on the rule classes (they define
  `balance_next_pay_day`), so it would raise `AttributeError` if it were ever
  reached.
- `GreenAccountRules.balance_next_pay_day` computes an adjusted amount but
  never returns it.
- `YellowAccountRules.get_subscriptions` always returns `None`, since its
  only condition (`SUBSCRIPTION_NAME == "Yellow"`) is always true.
- `StorageManager.is_user_exist` is defined but unused anywhere in the app.
- `logics/services.py.get_people_list_from_web` is a stub that always
  returns an empty list, so no one can currently be registered against a
  real personnel directory — the seeded sample accounts are the only way to
  log in until this is connected.
