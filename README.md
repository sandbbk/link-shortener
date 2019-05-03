# link-shortener

Description
-----------------------------------------------------------------------------------------------------------------------------------------
  Simple link shortener on main page receives a link like 
  *https://some-name.some-domain/some-path...some-path* 
  and returnes a short one like 
  [https://sandbbk.pythonanywhere.com/Wor7nb32](https://sandbbk.pythonanywhere.coom/Wor7nb32)
  You can authenticate yourself to watch statistics about links created by You.
  
  Install and launch!
-----------------------------------------------------------------------------------------------------------------------------------------
 To install app just clone it to your local computer with the commands:
 
     $ git clone https://github.com/sandbbk/link-shortener.git
     $ cd link-shortener
     
 Create the virtual environment and install all requirement modules:
 
     $ python3 -m venv myvenv
     $ source myvenv/bin/activate
     $ pip install -r requirements.txt
     
Kick off the app now with code:

    $ python3 manage.py runserver
    
After that open a new tab in browser with url [http://127.0.0.1:8000](http://127.0.0.1:8000).
That is all!
