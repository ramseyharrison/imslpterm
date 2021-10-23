# imslp-json

terminal interface meant for accessing composer information and works from IMSLP composers

As of now, you can fetch the composition lists of any IMSLP composer with : 

```
python3 parser.py "Brahms, Johannes" 
```
where you can replace ```"Brahms, Johannes"``` with any properly formatted IMSLP category name

You can also locally store any of these composers and their information, with :

```
python3 parser.py "Brahms, Johannes" -s 
```
Once this is done, Brahms will get a local id associated to it, which can be found by running
```
python3 parser.py list
```
The output would look like : 
```
0 : Brahms, Johannes
```
Where ```0``` is the local ID for Brahms. After that, running 
```
python3 parser.py 0 
```
will yield the same result as 
```
python3 parser.py "Brahms, Johannes"
```

This project is entirely dependent on the IMSLP package found here https://github.com/jlumbroso/imslp
