"""Shared pytest setup."""

import os

# ht_libs.config reads these at import time, so set dummies before any test imports it.
os.environ.setdefault("HATTRICK_OAUTH_CONSUMER_KEY", "dummy-key")
os.environ.setdefault("HATTRICK_OAUTH_CONSUMER_SECRET", "dummy-secret")
