# Manual Técnico

### Fernando José Vicente Velásquez, 202111576
### Lenguajes Formales y de Programación

#### Para la realización del programa, se realizó en 3 módulos. Estos módulos llevan por nombre:
- main.py (acá lleva la GUI del proyecto, además de la inserción de los tokens, errroes y sentencias)
- Parser.py (en este módulo se encuentra el analizador léxico del programa, es con lo que genera las sentencias para mongoDB)
- scanner.py (se le colocó scanner para un nombre más propio, pues es así como se conoce al analizador léxico en ingles). Como su nombre indica, en este módulo es donde pasa el archivo de entrada y es separado por Tokens, teniendo palabras claves y delimitadores para el proceso de creación de los ya mencionados.

### Explicación del código
#### Como se mencionó previamente, se realizó en 3 módulos el proyecto, siendo esta la explicación para cada uno:
- main.py: la funcionalidad se centra en este módulo, pues es recibe las sentencias para mongoDB. La función es esta:
![Analyze_Code](/images/Analyze_Code.jpg)
- además se pueden agregar las funciones 'update_error_table' y 'show_tokens'. La primera función analiza si existe algún error dentro de la entrada del archivo, y en dado caso exista, lo alamacenará en una tabla.
La siguiente función agrega los tokens obtenidos desde el analizados léxico, es decir, scanner.py.
Las funciones son las siguientes:
![update_tokens](/images/update_tokens.jpg) 
- scanner.py: Ahora se centrará en el analizador léxico, pues es donde todo inicia. En este módulo se trabajo con los pasos que se realizó el AFD, en una tabla de estados. Esta tabla de estados se siguió para poder separar en tokens los diferentes identificadores del archivo de entrada. Claro, estos archivos de entrada necesitaban de palabras claves y delimitadores, siendo estos los utilizados:
![Claves_Delimitadores](/images/Claves_Delimitadores.jpg)
- La tabla de transiciones es la siguiente:

![TT](/images/TT.jpg)

- Parse.py: en este módulo se lleva a cabo el análisis sintáctico del los tokens obtenidos, en este módulo es donde se forman las sentencias para MongoDB. Esta es pasada por un parser, el cual identificará las palabras claves y delimitadores para crear correctamente la sentencia. Pues lo que recibe es la entrada de tokens ya analizados por el scanner, entonces acá se desglozan y se vuelven sentencias, por ejemplo, esta es el código para generar la sentencia parar crear una base de datos en MongoDB:
![CREATE_DB](/images/CREATE_DB.jpg)
- Pues este código devolverá el nombre que se le adjuntó en el archivo de entrada de formato JSON, dando como resultado ' use('ID'); (que ID es el nombre que se le adjudica)

#### La expresión regular utilizada para generar los tokens del programa, es la siguiente:
![ER](/images/ER.jpg)

##### Esta expresión regular se separa en 4 partes
- (CREATE_DB|DROP_DB|CREATE_COLLECTION|DROP_COLLECTION|INSERT_ONE|UPDATE_ONE|DELETE_ONE|FIND_ALL|FIND_ONE): Esta parte reconoce uno de los verbos posibles en la cadena.

- \s+: Esta parte reconoce uno o más espacios en blanco.

- [a-zA-Z0-9_]+: Esta parte reconoce una cadena alfanumérica que no puede contener espacios en blanco.

- La parte final es opcional y reconoce una lista de cadenas alfanuméricas separadas por comas. Cada cadena debe estar encerrada entre comillas dobles y no puede contener espacios en blanco.

### Tabla de Tokens:
|Token|Significado|Línea|Inicio|Fin|
|-----|-----------|------|-----|----|
|CREATEDB|	CrearBD|	3|	25|	32
|ID|	temp1|	3|	33|	38
|EQUALS|	=|	3|	39|	40
|NEW|	nueva|	3|	41|	46
|CREATEDB|	CrearBD|	3|	47|	54
|LPAREN|	(|	3|	54|	55
|RPAREN|	)|	3|	55|	56
|SEMICOLON|	;|	3|	56|	57
|DROPDB|	EliminarBD|	6|	86|	96
|ID|	temp1|	6|	97|	102
|EQUALS|	=|	6|	103|	104
|NEW|	nueva|	6|	105|110
|DROPDB|	EliminarBD|	6|	111|	121
|LPAREN|	(|	6|	121|	122
|RPAREN|	)|	6|	122|	123
|SEMICOLON|	;|	6|	123|	124
|CREATEDB|	CrearBD|	9|	150|	157
|ID|	temp|	9|	158|	162
|EQUALS|	=|	9|	163|	164
|NEW|	nueva|	9|	165|	170
|CREATEDB|	CrearBD|	9|	171|	178
|LPAREN|	(|	9|	178|	179
|RPAREN|	)|	9|	179|	180
|SEMICOLON|	;|	9|	180|	181
|CREATECOLLECTION|	CrearColeccion|	12|	218|	232
|ID|	colec|	12|	233|	238
|EQUALS|	=|	12|	239|	240
|NEW|	nueva|	12|	241|	246
|CREATECOLLECTION|	CrearColeccion|	12|	247|	261
|LPAREN|	(|	12|	261|	262
|DQUOTE|	"|	12|	262|	263
|ID|	literaturas|	12|	263|	274
|DQUOTE|	"|	12|	274|	275
|RPAREN|	)|	12|	275|	276
|SEMICOLON|	;|	12|	276|	277
|CREATECOLLECTION|	CrearColeccion|	15|	308|	322
|ID|	colec|	15|	323|	328
|EQUALS|	=|	15|	329|	330
|NEW|	nueva|	15|	331|	336
|CREATECOLLECTION|	CrearColeccion|	15|	337|	351
|LPAREN|	(|	15|	351|	352
|DQUOTE|	"|	15|	352|	353
|ID|colectemp|	15|	353|	362
|DQUOTE|	"|	15|	362|	363
|RPAREN|	)|	15|	363|	364
|SEMICOLON|	;|	15|	364|	365
|DROPCOLLECTION|	EliminarColeccion|	18|	399|	416

### Método del árbol derivado de la expresión regular:
![MA](/images/MA.png)

- En este árbol, la raíz es el nodo Sentencia, que representa la operación que se va a realizar en la base de datos. El nodo Verbo representa el verbo de la operación (o sea, una keyword), mientras que el nodo Nombre representa el nombre de la base de datos o colección en la que se realizará la operación. Si la operación incluye argumentos, se creará un nodo Args que tendrá nodos hijos Arg1, Arg2, etc. para cada uno de los argumentos.

### El gráfico del AFD utilizado en el analizador léxico es el siguiente:
![AFD](/images/AFD.png)

- El AFD tiene cinco estados: S0, S1, S2, S3 y S3_end. El estado S0 es el estado inicial y se utiliza para determinar el tipo de token que se está analizando. Si el token es una letra, se transita al estado S1. Si es un delimitador, se transita al estado S2. Si es una comilla, se transita al estado S3.

- En el estado S1, se buscan caracteres alfanuméricos o subrayados para reconocer identificadores. Si se encuentra un carácter que no es alfanumérico ni un subrayado, se transita al estado S0.

- En el estado S2, se buscan delimitadores y se transita al estado S0 si no se encuentra ninguno.

- En el estado S3, se buscan comillas para reconocer cadenas. Si se encuentra una comilla, se transita al estado S3_end.

- En el estado S3_end, se buscan caracteres que no sean comillas para reconocer la cadena. Si se encuentra un carácter que no es una comilla, se transita al estado S0.

### La gramática libre de contexto (GLC) utilizada para el analizador léxico es la siguiente:
![GLC](/images/GLC.jpg)
