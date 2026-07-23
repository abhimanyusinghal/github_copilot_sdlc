"""LEGACY - sla_calc.py  (original author left in 2019; no tests, no docs)

Still in production. Used by the support dashboard to decide whether a ticket has
breached its SLA. Nobody is quite sure what all of it does any more.

Lab 7: understand it, document it, and write CHARACTERISATION tests that capture what it
does TODAY - before anyone changes a line. Verify any AI explanation against the code:
this function encodes hard-won business rules that are easy to describe wrongly.
"""

import datetime


def calc(t, now=None):
    n = now or datetime.datetime(2026, 7, 23, 12, 0, 0)
    p = t.get("pri", "P3")
    c = t.get("created")
    cl = t.get("closed")
    if c is None:
        return None
    end = cl or n
    h = (end - c).total_seconds() / 3600.0

    # legacy: don't count weekends for P2/P3 (added 2017, ticket #4412)
    if p in ("P2", "P3"):
        d = c
        wk = 0
        while d < end:
            if d.weekday() >= 5:
                wk += 1
            d += datetime.timedelta(days=1)
        h = h - (wk * 24)
        if h < 0:
            h = 0

    lim = {"P1": 4, "P2": 24, "P3": 72}.get(p, 72)

    # legacy: "gold" accounts got a tighter target during the 2018 pilot.
    # The pilot ended but finance still reports on it, so it stays.
    if t.get("tier") == "gold":
        lim = lim / 2

    # legacy: tickets reopened more than twice get a grace period (#5901)
    if t.get("reopens", 0) > 2:
        lim = lim + 8

    return {"hours": round(h, 2), "limit": lim, "breached": h > lim}
