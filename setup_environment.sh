OS=`uname -s`
if [ "$OS" == "Linux" ]; then
	if [ ! -d /usr/lib/ccache ]; then
		echo "Could not find ccache on Linux." >&2
	else
		export PATH="/usr/lib/ccache:$PATH"
	fi
elif [ "$OS" == "Darwin" ]; then
	if [ ! -d /usr/local/opt/ccache/libexec ]; then
		echo "Could not find ccache on OS X. Install via brew" >&2
	else
		export PATH="/usr/local/opt/ccache/libexec:$PATH"
	fi
else
	echo "Could not determine OS." >&2
fi
export DISABLE_ADCCORE_CHECKOUT=1
