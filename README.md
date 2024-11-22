# REPOSITORIO PARA PRÁCTICAS DE CLOUD COMPUTING

## Documento explicativo del propósito de este repositorio

Este respositorio parte del trabajo realizado en mi Trabajo de Fin de Grado. 
El desarrollo de la aplicación se dividió en tres grandes partes:
- Gestión de preguntas con distintos atributos (tipo, respuestas correctas, puntuación estimada...)
- Confección de exámenes en base al desglose establecido de la asignatura, además de otras opciones (número de preguntas, dificultad estimada...)
- Importación y visualización de diferentes estadísticos de resultados del examen. 

Explicando la organización básica de las carpetas del repositorio, cabe destacar que el proyecto se divide en dos grandes módulos. 

### Organización del módulo del backend.

Estos son algunos de los directorios del repositorio propio del backend: 
- ``db``: contiene la configuración para la base de datos.  
- ``docker``: contiene los archivos para establecer un contenedor de docker en la que se ejecutará la aplicación.
- ``models``: contiene directorios de cada uno de los modelos necesarios para la aplicación. Su estructura se compone del archivo de inicialización, el archivo de definición de atributos y operaciones, y el archivo de esquemas de entrada y salida de datos.  
- ``services``: contiene archivos para cada uno de los modelos que da servicios a través de endpoints sobre los que realizar las operaciones.  
- ``utils``: contiene archivos con funciones de utilidad varia para todos los modelos.

### Organización del módulo de frontend.

La gran parte del contenido de este módulo se encuentra en el directorio ``app`` del directorio ``src``, que tiene la siguiente estructura de carpetas: 
- ``components``: contiene los HTML, TS y CSS correspondientes a cada una de las pantallas en las que se pueden hacer operaciones, organizándolos a su vez en cada uno de los objetos que conforman el proyecto (Preguntas, Exámenes, Asignaturas...).  
- ``models``: contiene los archivos para establecer la lógica de cada objeto en la aplicación.
- ``services``: contiene los servicios que realizan las peticiones HTTP a la API generada por el frontend. Estos servicios también se organizan según los elementos del proyecto.  
- ``app.routes.ts``: contiene todas las rutas válidas para la aplicación.  


Para conocer más sobre este proyecto, se recomienda acceder a sus repositorios en GitHub:   
https://github.com/rafadgvc/TFG-frontend.git    
https://github.com/rafadgvc/TFG-backend.git

A partir del trabajo previamente realizado se busca implementar un nuevo proyecto, en el que se vayan incorporando las mejoras sugeridas para convertir este proyecto en un servicio en la nube. Además, para que este servicio tenga más sentido, se intentará implementar un sistema para que distintos profesores puedan hacer uso de las mismas asignaturas y de sus recursos. 
