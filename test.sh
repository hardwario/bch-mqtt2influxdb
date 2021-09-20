#!/bin/sh
# vim: set ts=4:
set -eu

VENV_DIR="$(pwd)/.venv"

die() {
	printf '\033[1;31mERROR:\033[0m %s\n' "$1" >&2
	shift
	printf '  %s\n' "$@"
	exit 2
}

einfo() {
	printf '\033[1;36m> %s\033[0m\n' "$@" >&2
}

if [ "$(id -u)" -eq 0 ] && [ "$ALLOW_ROOT" != 'yes' ]; then
	die 'Do not run this script as root!'
fi

if [ ! -f "$VENV_DIR/bin/python3" ]; then
	einfo 'Initializing Python virtual environment...'

	for pybin in "${PYTHON:-}" python3 python NOT_FOUND; do
		command -v "$pybin" >/dev/null 2>&1 && break
	done
	if [ "$pybin" = 'NOT_FOUND' ]; then
		die 'Could not find python executable! Please install Python 3.'
	fi

	if ! "$pybin" -c 'import sys; exit(not sys.version_info >= (3, 4, 0))'; then
		die "Python 3.4+ is required, but you have $("$pybin" -V 2>&1)!"
	fi

	if ! "$pybin" -c 'import venv' 2>/dev/null; then
		die 'Python module venv is not installed!',
			'TIP: If you are using Debian-based distro, run "apt-get install python3-venv".'
	fi

	if ! "$pybin" -c 'import pip' 2>/dev/null; then
		die 'Python module pip is not installed!',
			'TIP: If you are using Debian-based distro, run "apt-get install python3-pip".'
	fi

	"$pybin" -m venv "$VENV_DIR"
fi

export PATH="$VENV_DIR/bin:$PATH"
unset PYTHONHOME

einfo 'Installing Python modules...'
python3 -m pip install -r requirements-dev.txt 2>&1 \
	| sed -e '/^Requirement already satisfied/d' \
		-e '/don.t match your environment$/d'

einfo 'Test codestyle'
python3 -m pycodestyle --ignore=E501 --exclude .venv .

einfo 'Test setup.py'
python3 setup.py test
