# 3. Python 3.8+ only

Date: 2022-06-03

## Status

Accepted

## Context

Python 3.7 will reach [end of life](https://endoflife.date/python) within a year and
3.8 provides some improvements when it comes to type annotations as well as asynchronous
code.

## Decision

We make an early decision to only support Python 3.8 and above.

## Consequences

We might exclude some users on older platforms but almost everyone should be able to
run virtual environments with any Python version.
