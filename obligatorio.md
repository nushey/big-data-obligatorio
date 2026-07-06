# Parte 1
## Consigna
Para el obligatorio deberá utilizar las herramientas usadas en el curso, levantadas en la máquina virtual de Azure. (En su
defecto para quienes no tengan créditos, está disponible una VM que puede utilizar en su máquina local). Deberá
seleccionar un conjunto de datos tabulares con más de 4 tablas, que deberá ser aprobado por los docentes, y deberá
seleccionar 5 preguntas relativas a los datos que seleccionó, para contestarlas con las herramientas analíticas que también
deberán ser aprobados por los docentes. Se restaran puntos a quienes no tengan el conjunto de datos y las preguntas
aprobadas. Deberá indicar la fuente de dónde obtuvo los datos. La misma no podrá ser Kaggle. En caso de tener un modelo
de datos al estilo OBT, se podrá utilizar siempre y cuando se pase a modelo normalizado antes de la ingesta de datos y no se
puede volver a un modelo OBT en la etapa de modelado. Deberá presentar el código urilizado para cambiar el modelo de
datos de OBT a normalizado.
Alternativamente queda como opción armar el conjunto de datos con las herramientas que tenga disponible para crear 3
fuentes ficticias de datos a integrar luego en un modelo de datos, o utilizar datos reales de una organización que los brinde
para realizar el obligatorio, respetando no utilizar datos personales o confidenciales.

## Los pasos a seguir son:
* Preparar la Ingesta. Se deben dejar los datos en un lugar accesible a NiFi. Puede ser por ejemplo un
repositorio en git al que se accede de forma remota vía HTTP, o puede ser una carpeta en la máquina virtual donde
están instaladas las herramientas. No se debe subir a HDFS los datos directamente vía comando.
* Crear en HDFS las regiones que considere necesarias para trabajar con los datos, estas deben ser
exactamente las regiones que se dieron en clase. Recuerde que en HDFS se deben definir “zonas” utilizando la
estructura de directorio del file system. Cada zona debe llevar un nombre acorde para lo que es utilizada, se deben
definir los criterios para utilizar las zonas, dejarlos por escrito, y respetarlos. La ingesta debe dejar los datos en un
lugar predefinido para ese uso. Se debe utilizar buenas prácticas de NiFi a la hora de hacer la ingesta (Usar process
groups, y utilizar funnels entre otros).
* Luego se deberá realizar un análisis exploratorio de los datos identificando el tipo de datos que hay en
cada columna y que significado tienen dentro del dominio de los datos. Dentro de un Jupyter notebook se mostrará,
una vista previa de las primeras filas, cantidad de columnas de cada tabla, nombre de cada columna, descripción de
los datos de cada tabla, cómo está compuesto el esquema de los datos, revisar valores nulos o faltantes y limpiarlos
si es necesario. Revisar registros duplicados. Claves primarias únicas. Reglas de negocio que deba considerar para
el refinamiento. Estos nuevos archivos se guardarán en el hdfs, en otra ubicación como la versión refinada de los
datos. Para todo se debe utilizar únicamente spark.
* Una vez que termine con la exploración y limpieza de datos, deberá elegir una forma de modelarlos, esta
puede ser, Normalizada, Diagrama Estrella, Data Vault, o OBT. Si para el modelo seleccionado necesita crear
nuevos archivos, deben guardarse en una nueva ubicación dentro de HDFS. A esta ubicación apuntarán las tablas
externas que luego definirá con HIVE.
* Después de elegir una forma de modelar los datos, deberá bosquejar cómo sería el esquema que relaciona
las tablas con el modelo elegido (se sugiere usar draw.io, mermaid o excalidraw pero puede utilizar otra
herramienta).
* Una vez tenga los dataframes de las tablas que va a utilizar en su modelo de datos, deberá guardarlas
como tabla de HIVE en un esquema nuevo.
* A partir de las tablas de Hive se contestarán las preguntas seleccionadas en un nuevo notebook. Deberá
utilizar spark con sintaxis SQL o con los distintos métodos que provee pyspark. No se pueden contestar las
preguntas llevando los archivos a dataframe directamente. Solo se contará como válido, utilizar las tablas HIVE del
modelo de datos creado.
* Del resultado obtenido de tres de las preguntas contestadas, llevar ese resultado a dataframe de pandas y
crear dos visualizaciones distintas en el notebook de jupyter, utilizando alguna de las librerías de visualización
vistas en clase.
* Para las otras dos preguntas, conservarlas como archivo dentro de HDFS en una región donde guarde
resultados de analíticas de datos. Crear nuevas tablas HIVE que apunten a esos archivos.
* Utilizar las tablas HIVE para realizar una visualización en SuperSet que ayude a contestar las dos
preguntas realizadas. (HIVE es solo utilizado para conectar a SuperSet en el obligatorio, pero no es lo
recomendado para poner en producción para un caso de Big Data Real). 

## Detalle de entrega final
La entrega final consiste en un informe donde se detalle todo el proceso realizado y todo lo aprendido durante la realización
del obligatorio. Se puede apoyar mediante capturas de pantalla o code snippets para explicar lo realizado. Se debe explicar
el dominio de los datos seleccionados, que significa cada columna de cada tabla y que tipo de dato debe tener. Se plantearán
y responderan las preguntas seleccionadas y se explicará la arquitectura del datalake las tecnologías utilizadas y cómo
contribuyen a su solución de big data para hacer análisis de datos. También se deben entregar los notebooks utilizados, los
dashboards creados en SuperSet y todo lo que resulte relevante para el trabajo que los alumnos consideren necesario como
evidencia que se cumplieron todos los pasos de la Parte 1.

# Parte 2
## Consigna
Seleccionar una organización, real o ficticia. Si en la parte 1 utilizó los datos de una organización real, puede utilizar las
mismas fuentes de datos, de lo contrario deberá utilizar datos distintos. Listar las fuentes de datos, sus esquemas si es que
los tienen, y como los integrarían en un nuevo modelo de datos, y que pregunt de negocio contestarían con ese modelo de
datos. Deberán investigar una posible solución para armar un datalake, con otras tecnologías distintas a las utilizadas para el
obligatorio (a excepción de Spark), sean nativas de una nube, de software libre o propietarias. Explicitar con qué otras
herramientas armarían su datalake y que función cumpliría cada una. Como sería todo el proceso desde el origen de los
datos hasta los consumidores finales para el nuevo caso seleccionado. Realizar un diagrama con su nuevo stack para armar
otro datalake. Redactar todo el proceso desde la fuente hasta los consumidores de datos con el nuevo datalake. Si selecciona
herramientas nativas de un proveedor cloud, no puede mezclar con herramientas de otra nube.
