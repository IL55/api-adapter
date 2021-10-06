rm -Rf build || true
mkdir build
cp *.py build

pip3 install --target=./build requests

cd build
zip -r build *
cd ..

rm -f ./build.zip || true
cp ./build/build.zip ./