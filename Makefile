# ⚽ hattrick_libs ops – type `make` for the team sheet
# GNU make >= 3.82. Recipe lines start with ">" instead of a tab (copy-paste safe).

SHELL         := bash
.SHELLFLAGS   := -eu -o pipefail -c
.ONESHELL:
.RECIPEPREFIX := >
.DEFAULT_GOAL := help
MAKEFLAGS     += --no-print-directory

UV        ?= uv
PYPI_NAME := hattrick-libs
VERSION    = $(shell sed -nE 's/^version = "(.*)"/\1/p' pyproject.toml | head -n1)
TAG        = v$(VERSION)
PY         = $(shell cat .python-version 2>/dev/null)

# config.py needs these at import time; dummies unless your shell already has real ones
test smoke ci: export HATTRICK_OAUTH_CONSUMER_KEY    ?= dummy-key
test smoke ci: export HATTRICK_OAUTH_CONSUMER_SECRET ?= dummy-secret

.PHONY: help version kickoff ship referee sync lock upgrade tools fmt lint test hooks \
        yaml actions build smoke ci login login-fresh release untag clean \
        warmup hattrick transfer-window physio assist var penalty sweep

# --- 📋 team sheet ------------------------------------------------------------

help: ## 📋 show all moves
>@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

version: ## 🏷️  show the project version
>@echo "$(PYPI_NAME) $(VERSION)"

# --- 🌿 git workflow ----------------------------------------------------------

kickoff: ## 🌿 fresh feature branch from main: make kickoff NAME=my-feature
>@[[ -n "$(NAME)" ]] || { echo "usage: make kickoff NAME=my-feature"; exit 1; }
>[[ -z "$$(git status --porcelain)" ]] || { echo "❌ uncommitted changes, commit or stash first"; exit 1; }
>git switch main
>git pull --ff-only
>git switch -c "feat/$(NAME)"

ship: ci ## 🚢 local CI, push branch, open PR, auto-merge when ci-ok is green
>@branch="$$(git branch --show-current)"
>[[ "$$branch" != main ]] || { echo "❌ you're on main, use: make kickoff NAME=..."; exit 1; }
>[[ -z "$$(git status --porcelain)" ]] || { echo "❌ uncommitted changes"; exit 1; }
>git push -u origin "$$branch"
>gh pr view --json url --jq .url 2>/dev/null || gh pr create --fill
>gh pr merge --auto --squash --delete-branch
>echo "🚢 auto-merge armed: merges itself once ci-ok is green"

referee: ## 🧑‍⚖️ show every protection rule active on main
>@echo "── rulesets on main (type, ruleset id, required approvals)"
>gh api 'repos/{owner}/{repo}/rules/branches/main' \
>  --jq '.[] | [.type, .ruleset_id, (.parameters.required_approving_review_count // "")] | @tsv'
>echo "── classic branch protection (required approvals)"
>gh api 'repos/{owner}/{repo}/branches/main/protection' \
>  --jq '.required_pull_request_reviews.required_approving_review_count' 2>/dev/null \
>  || echo "none 👍"
>gh api 'repos/{owner}/{repo}/rules/branches/main' \
>  --jq '.[] | select(.type=="required_status_checks") | "required check: " + .parameters.required_status_checks[].context'

# --- 📦 dependencies ----------------------------------------------------------

sync: ## 🏃 install exactly what uv.lock says
>@$(UV) sync --locked

lock: ## 🔒 re-lock after editing pyproject.toml
>@$(UV) lock

upgrade: ## 🔄 uv lock --upgrade + sync (what the Monday bot does)
>@$(UV) lock --upgrade
>$(UV) sync --locked

tools: ## 🩺 update uv + newest Python patch, print versions
>@$(UV) self update || echo "ℹ️  uv not from the standalone installer, update it your usual way"
>$(UV) python upgrade $(PY)
>$(UV) --version
>$(UV) run python --version

# --- 🧪 quality ---------------------------------------------------------------

fmt: ## 💅 format + safe autofixes
>@$(UV) run ruff format .
>$(UV) run ruff check --fix .

lint: ## 🔍 ruff check + format check (no changes)
>@$(UV) run ruff check .
>$(UV) run ruff format --check .

test: ## 🧪 run pytest (extra args: make test ARGS="-k oauth")
>@$(UV) run pytest $(ARGS)

hooks: ## 🪝 install pre-commit hooks and run them on everything
>@$(UV) run pre-commit install
>$(UV) run pre-commit run --all-files

yaml: ## 🧾 YAML syntax check for workflows + dependabot
>@for f in .github/workflows/*.yml .github/dependabot.yml; do
>  $(UV) run python -c 'import sys, yaml; yaml.safe_load(open(sys.argv[1]))' "$$f" \
>    || { echo "❌ $$f"; exit 1; }
>  echo "✅ $$f"
>done

actions: ## 🔎 check that every `uses:` ref in the workflows exists
>@fail=0
>while read -r ref; do
>  repo="$${ref%@*}"; tag="$${ref#*@}"
>  [[ "$$repo" == ./* ]] && continue
>  if [[ $${#tag} -eq 40 ]] || git ls-remote --exit-code "https://github.com/$$repo" "$$tag" >/dev/null; then
>    echo "✅ $$ref"
>  else
>    echo "❌ $$ref"; fail=1
>  fi
>done < <(grep -hoE 'uses: *[^ #]+' .github/workflows/*.yml | sed -E 's/uses: *//' | sort -u)
>exit $$fail

# --- 📦 build -----------------------------------------------------------------

build: ## 📦 build sdist + wheel into dist/
>@rm -rf dist
>$(UV) build
>unzip -p dist/*.whl '*/METADATA' | grep '^Requires-Python:'

smoke: build ## 🐤 install the built wheel in a clean env and import it
>@$(UV) run --isolated --no-project --with dist/*.whl \
>  python -c 'import ht_libs.get_flags, ht_libs.do_challenge, ht_libs.do_hattrick_request; print("🐤 wheel ok")'

ci: yaml lint test smoke ## 🏟️  the full CI, locally
>@echo "🏆 all green"

# --- 🔐 real CHPP -------------------------------------------------------------

login: ## 🔐 run __main__.py against CHPP (loads .env, reuses .creds)
>@if [[ -f .env ]]; then set -a; source .env; set +a; fi
>$(UV) run python __main__.py

login-fresh: ## 🆕 full OAuth handshake from scratch (backs up .creds outside the repo)
>@if [[ -f .creds ]]; then mv .creds "$$HOME/.hattrick_libs.creds.bak"; echo "📦 .creds → ~/.hattrick_libs.creds.bak"; fi
>$(MAKE) login

# --- 🚀 release ---------------------------------------------------------------

release: ci ## 🚀 local CI, then tag v<version> on main and push (PyPI waits for your approval)
>@v="$(VERSION)"; tag="$(TAG)"
>[[ "$$(git branch --show-current)" == main ]] || { echo "❌ not on main"; exit 1; }
>[[ -z "$$(git status --porcelain)" ]]       || { echo "❌ working tree not clean"; exit 1; }
>git fetch --quiet origin
>[[ "$$(git rev-parse HEAD)" == "$$(git rev-parse origin/main)" ]] || { echo "❌ main != origin/main, pull first"; exit 1; }
>! git rev-parse -q --verify "refs/tags/$$tag" >/dev/null || { echo "❌ $$tag exists locally"; exit 1; }
>! git ls-remote --exit-code --tags origin "refs/tags/$$tag" >/dev/null || { echo "❌ $$tag exists on GitHub"; exit 1; }
>code=$$(curl -s -o /dev/null -w '%{http_code}' "https://pypi.org/pypi/$(PYPI_NAME)/$$v/json")
>[[ "$$code" == 404 ]] || { echo "❌ $$v already on PyPI (HTTP $$code), bump the version"; exit 1; }
>read -rp "🚀 Tag and push $$tag? [y/N] " ok
>[[ "$$ok" == y ]] || { echo "🙅 aborted"; exit 1; }
>git tag -a "$$tag" -m "$$tag"
>git push origin "$$tag"
>echo "✅ $$tag pushed → Actions → Release to PyPI → Review deployments → Approve"

untag: ## 🟨 delete a tag locally + on GitHub, only if not on PyPI (make untag TAG=v0.21.0)
>@tag="$(TAG)"; v="$${tag#v}"
>code=$$(curl -s -o /dev/null -w '%{http_code}' "https://pypi.org/pypi/$(PYPI_NAME)/$$v/json")
>[[ "$$code" == 404 ]] || { echo "❌ $$v is on PyPI, too late for VAR, bump the version"; exit 1; }
>git tag -d "$$tag" || true
>git push origin --delete "$$tag" || true
>echo "🟨 VAR overturned $$tag"

clean: ## 🧹 remove build output + caches
>@rm -rf dist build .pytest_cache .ruff_cache
>find . -type d -name __pycache__ -not -path './.venv/*' -prune -exec rm -rf {} +
>echo "🧹 pitch swept"

# --- ⚽ catchy aliases --------------------------------------------------------

warmup: sync ## 🏃 alias: sync
hattrick: ci ## ⚽⚽⚽ alias: ci
transfer-window: upgrade ## 💸 alias: upgrade
physio: tools ## 🩺 alias: tools
assist: ship ## 🅰️  alias: ship (you pass, CI scores)
var: untag ## 🟨 alias: untag (Video Assistant Referee)
penalty: release ## 🥅 alias: release
sweep: clean ## 🧹 alias: clean
