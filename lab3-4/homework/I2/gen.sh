mkdir -p client/gen
slice2py --output-dir client/gen slice/Servants.ice

mkdir -p server/src/gen
slice2java --output-dir server/src/gen slice/Servants.ice