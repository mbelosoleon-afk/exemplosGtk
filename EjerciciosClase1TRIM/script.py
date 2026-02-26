import json
import sys

pelicula = {"The Big Lebowski":
{
"Director":"Joel Coen y Ethan Coen",
"Anyo":1998,
"Reparto":[
{"Nombre":"Jeff Bridges"},
{"Nombre":"John Goodman"},
{"Nombre":"Julianne Moore"},
{"Nombre":"Steve Buscemi"}
]
}
}

print(json.dumps(pelicula))
sys.exit(0)
