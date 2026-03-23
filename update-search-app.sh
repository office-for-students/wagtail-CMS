#!/bin/bash

if [ -f .env ]; then
  source .env
else
  echo "Error: .env file not found"
  exit 1
fi

if [ -z "$SEARCH_APPLICATION_BUILD_ROOT" ]; then
    echo "Error: SEARCH_APPLICATION_BUILD_ROOT is not set in .env"
    exit 1
fi

cd $SEARCH_APPLICATION_BUILD_ROOT
npm run build-prod

cd -
cd coursefinder/static/search_app/

old_js_file=$(ls *.js | head -n 1)
old_css_file=$(ls *.css | head -n 1)

rm $old_js_file
rm $old_css_file

cp $SEARCH_APPLICATION_BUILD_ROOT/dist/assets/*.js .
cp $SEARCH_APPLICATION_BUILD_ROOT/dist/assets/*.css .
cp $SEARCH_APPLICATION_BUILD_ROOT/src/assets/* .

new_js_file=$(ls *.js | head -n 1)
new_css_file=$(ls *.css | head -n 1)

git add .
git add $new_css_file -f

cd ../../templates/coursefinder/search_app

echo "Replacing $old_js_file with $new_js_file"
echo "Replacing $old_css_file with $new_css_file"

sed -i "" s/$old_js_file/$new_js_file/ search_app.html
sed -i "" s/$old_css_file/$new_css_file/ search_app.html

echo "\033[32mSearch app built and asset files copied successfully.\033[0m"