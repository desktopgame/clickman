# clickman
clickman is can emulation mouse movement and click operation.  
this application was created for debug a game in auto.  

# install
````
cd clickman
pip install -r requirements.txt
````

# how to use
in first, should be create mouse operation for your want emulate.  
so, you should mouse operation to window.  
below code is start record your mouse operation.

````
python app/main.py setup
or
python app/main.py setup --output clickman.txt
````

in next, your created mouse operation is should be verify.  
below code is draw your mouse operation for window.

````
python app/main.py test
or
python app/main.py test --input clickman.txt
````

in final, execute mouse operation in actualy.

````
python app/main.py run
or
python app/main.py run --input clickman.txt
````