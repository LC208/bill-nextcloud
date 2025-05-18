#!/usr/bin/env sh

. /usr/local/mgr5/lib/pkgsh/core_pkg_funcs.sh

ExitError() {
	Error "${@}"
	exit 1
}

InstallDeps() {
	Info "Installing dependencies..."

	PKGS="billmanager-plugin-python-libs python3-pip"

	case ${OSTYPE} in
		REDHAT)
			PKGS="$PKGS coremanager-devel"
		;;
		DEBIAN)
			PKGS="$PKGS coremanager-dev"
		;;
		*)
			ExitError "Unknown os type"
		;;
	esac

	PkgInstall "${PKGS}" || ExitError "Failed to install system packages"

	pip3 install --upgrade pip || ExitError "pip upgrade failed"
	pip3 install -r ./requirements.txt || ExitError "Failed to install Python dependencies"
}

InstallNextCloud() {
	Info "Install NextCloud..."

	CURRDIR=$(pwd)
	DESTDIR=/usr/local/mgr5/src/pmnextcloud

	mkdir -p ${DESTDIR} && cp -rfa "${CURRDIR}"/* ${DESTDIR}/
	cd ${DESTDIR} && make install || ExitError "Install NextCloud failed"
	cd ${CURRDIR}

	Info "Install successfuly finished"
}

InstallDeps
InstallNextCloud
