script_folder="/mnt/c/Users/Diego/conanws/conan-center-index/recipes/openssl/3.x.x/build-release/conan"
echo "echo Restoring environment" > "$script_folder/deactivate_conanbuildenv-release-x86_64.sh"
for v in PATH
do
   is_defined="true"
   value=$(printenv $v) || is_defined="" || true
   if [ -n "$value" ] || [ -n "$is_defined" ]
   then
       echo export "$v='$value'" >> "$script_folder/deactivate_conanbuildenv-release-x86_64.sh"
   else
       echo unset $v >> "$script_folder/deactivate_conanbuildenv-release-x86_64.sh"
   fi
done

export PATH="/root/.conan2/p/cmakeb5295444178fb/p/bin${PATH:+:$PATH}"