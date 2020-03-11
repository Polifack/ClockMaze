einstein 5 house riddle

//enunciamos lo que hay
//enunciarlo de esta forma no es eficiente, se puede enunciar usando tipos
person(1..5).
person(brit;swede;dane;german;norw).
color(red;blue;green;yellow;white).
drink(tea;coffee;milk;beer;water).
tobaco(pall;dunhill;blends;bluem;prince).
pet(fish;bird;cat;dog;horse).

//Generamos las restricciones
//genera una persona p que vive en una house h
{ lives(P,H): house(H)}:- person(P) 

//genera la restriccino de que solo una persona por casa
//(nota: empeza rpor :- significa prohibido que)
:-lives(P,H), lives(R,H), P!=R.
//añadir esta restriccion nos genera 120 soluciones

//Generamos la restriccion 2
//genera una casa H con color C
{paints (H,C): color(C)}:-house(H)
//pintame una casa de un color, pero solo de un color
:- paint(C,H), paint(D,H), C!=D
//añadir esta restriccion nos genera 120 * 120 soluciones

//la regla (1) y la regla (2) son iguales, asi que podemos convertir el predicado en un 
//objeto
//Para esto podemos usar un predicado como argumento. El programa vuelve a empezar asi:

type(person, (brit; swede; dane; german; norw))
type(color, (red;blue;green;yellow;white))
//y esta notificacion la usamos con todos los elementos inciiales
//de esta forma estamos convirtiendo los elementos del problema en valores de un parametro
//type que contiene los valores validos

//Definimos la restriccion para generar los datos usando TYPES
//En cada casa existe un tipo con un valor y el valor es unico para cada casa
1{at(H,T,V):house(H)}1:-type(T,V).
:-at(H,T,V), at (H,T,W), V!=W

//Ahora que tenemos todos los elementos generados empezamos a representar las restricciones
//Esto nos permite eliminar las restricciones no validas

//ejemplo: decimos que no puede ser que en la casa h la persona sea britanica y no sea rojo
//por lo tanto, el britanico bebe en la casa de color rojo
:-at (H, person, brit), not at (H, color, red)

:-at (H, person, sweede), not at (H, pet, dog).
:-at (H, person, dane), not at (H, drink, tea).
:-at(H, color, white), not at (H-1, color, green).
:-at(H, color, green), not at (H-1, color, white).
:-at(H, color, green), not at (H, drink, coffee).
:-at(H, tobaco, pall), not at (H, pet, bird).
:-at(H, color, yellow), not at (H, smoke, dunhill)

//no puede ser que en la casa h se fume blends si no se puede probar que en 
//h+1 hay un gato o en h-1 hay un gato
:-at(H, tobacco, blends), not at (pet, cat, H-1), not at (pet, cat, H+1)


//si usamos gringo podemos printear todas las reglas como si fuese clasp


//usamos x para ver la solucion
solution(x) :- at (H, pet, fish), at(H person, x)
#show solution/1