script_folder="/mnt/c/Users/Diego/conanws/conan-center-index/recipes/openssl/3.x.x/build-release/conan"
echo "echo Restoring environment" > "$script_folder/deactivate_conanautotoolstoolchain.sh"
for v in CPPFLAGS CXXFLAGS CFLAGS LDFLAGS PKG_CONFIG_PATH PERL
do
   is_defined="true"
   value=$(printenv $v) || is_defined="" || true
   if [ -n "$value" ] || [ -n "$is_defined" ]
   then
       echo export "$v='$value'" >> "$script_folder/deactivate_conanautotoolstoolchain.sh"
   else
       echo unset $v >> "$script_folder/deactivate_conanautotoolstoolchain.sh"
   fi
done

export CPPFLAGS="${CPPFLAGS:-}${CPPFLAGS:+ }-DNDEBUG"
export CXXFLAGS="${CXXFLAGS:-}${CXXFLAGS:+ }-m64 -fPIC -O3"
export CFLAGS="${CFLAGS:-}${CFLAGS:+ }-m64 -fPIC -O3"
export LDFLAGS="${LDFLAGS:-}${LDFLAGS:+ }-m64"
export PKG_CONFIG_PATH="$script_folder/../../build-release/conan${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export PERL="perl"