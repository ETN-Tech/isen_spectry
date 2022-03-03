# Règles générales
- La clé est le composant auquel on veut ajouter des éléments
- Les values sont les composants qui peuvent être créés (liste déroulante, input...) et deviendront les prochaines clés potentielles
- Tous les objets de niveau 0 contiennent une clé "type"

# Règles par type
## Object
- La sélection d'un object associe un nouvel objet à une clé dans le json
- L'objet contient une liste values d'enfants potentiels
- Les valeurs de value préfixées par un ? sont facultatifs ; les autres sont obligatoires et affichés à la création de l'objet
- Les values sont sélectionnables par liste déroulante

## Array
- La sélection d'un array insère un nouvel objet dans une liste dans le json
- Les autres règles sont héritées de Object

## Chunk_array
- Les values de chaque objet sont regroupés dans un enfant intermédaire (règle affichage seulement)
- Les autres règles sont héritées de Array

## Field
- La sélection d'un field crée une entrée utilisateur suivant les règles décrites dans l'objet désigné par le champ field

## Input
- Première forme d'entrée utilisateur sous forme d'input, dont le type est précisé par le champ nature
- L'input de nature radio et ayant le champ global doit avoir son name commun à tout le document (un seul objet sélectionnable à travers tout le document)

## Select
- Seconde forme d'entrée utilisateur sous forme de liste déroulante, dont les valeurs sont précisées par le champ values
- Les valeurs sélectionnées ici sont terminales

# Enrichissement
Dès qu'on réalise que ces règles ne permettent pas de répondre à une contrainte, on peut ajouter des éléments (symbole de préfixe, nouvelles règles, autres éléments...)