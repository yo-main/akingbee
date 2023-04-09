#!/usr/bin/env sh

next_release="$1"

sed -i "s/\(^version *= *\).*/\1\"${next_release}\"/" Cargo.toml
sed -i "/name = \"cerbes\"/{n;s/.*/version =\"${next_release}\"/}" Cargo.lock
