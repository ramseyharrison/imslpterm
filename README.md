# imslp-json

Set of methods which interact with data taken from the IMSLP package by jlumbroso(https://github.com/jlumbroso/imslp)

the main method add_new_composer does two things:

1)calls search_works() method from the imslp package, turns the data into a list, and stores it locally as json
2)takes this recently generated json and extracts specific pieces of information - namely title,permlink - assigns an id, serving as the equivalent of a local catalog number for each composition, and writes all this data into another json file

The reason the imslp package json is stored is simply because each call to search_works is lengthy, and so saving a local copy of what the function returns is more efficien.

There's also another json file that stores which composers have been "fetched" from the IMSLP package. Each call creates a record for a new composer, along with a local id.

add_new_composer expects(as does search_works() from imslp) a properly formatted "category name" from IMSLP website.
proper usage looks like add_new_composer("Beethoven, Ludwig van"), or add_new_composer("Schubert, Franz")

