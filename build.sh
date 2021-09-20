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

pkgver_from_git() {
	local desc
	if desc="$(git describe --tags --exact-match --match 'v*' 2>/dev/null)"; then
		echo "${desc#v}" | sed 's/[_-]/~/g'
	elif desc="$(git describe --tags --match 'v*' 2>/dev/null)"; then
		echo "$desc" | sed -En 's/^v([^-]+).*/\1~dev/p'
	else
		echo 'v0.0.0'
	fi
}

set_version() {
	local ver="$(echo $PKG_VERSION | tr '~' '-' | tr -d v)"
	sed -r -i'' "s/0\.0\.0/$ver/g" "$1"
}

if [ -z "${PKG_VERSION:-}" ]; then
	PKG_VERSION="$(pkgver_from_git)"
fi

export PATH="$VENV_DIR/bin:$PATH"
unset PYTHONHOME

if [ -z "${TRAVIS_BUILD_DIR:-}" ]; then
	BUILD_DIR="$(pwd)/build"
	echo "$BUILD_DIR"
	rm -rf "$BUILD_DIR"
	mkdir -p "$BUILD_DIR"
	rsync -av --delete --exclude .venv --exclude .git --exclude build . "$BUILD_DIR"
	cd "$BUILD_DIR"
fi

ls -lha

einfo "Set version $PKG_VERSION"
for d in */ ; do
	case $d in *.egg-info/)
		continue
	esac
	set_version "${d}__init__.py"
done

einfo "Run sdist"
python3 setup.py sdist
