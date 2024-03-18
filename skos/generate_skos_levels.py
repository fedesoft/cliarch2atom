from jinja2 import Template
from slugify import slugify
from unidecode import unidecode

levels = ["Archivo Documental",
"Colecciones Fotográficas",
"Fondo Documental",
"Sección Documental",
"Subsección Documental",
"Unidad de Subsección Documental",
"Serie Documental",
"Subserie Documental",
"Unidad Documental",
"Archivo Fotográfico",
"Fondo Fotográfico",
"Sección Fotográfica",
"Reportaje Fotográfico",
"Unidad Fotográfica",
"Sección de la Colección Fotográfica",
"Unidad Fotográfica de la Colección",
"Colección Fotográfica",
"Archivo Gráfico",
"Fondo Gráfico",
"Sección Gráfica",
"Unidad Gráfica",
"Subfondo Documental",
"Fonoteca",
"Fondo Sonoro",
"Sección Sonora",
"Unidad Sonora",
"Videoteca",
"Sección Audiovisual",
"Unidad Audiovisual",
"Fondo Audiovisual",
"Fondos de Procedencia Externa",
"Capitán Vigueras",
"Fondo de Procedencia Externa",
"Sección del Fondo de Procedencia Externa",
"Unidad Documental del Fondo de Procedencia Externa",
"Serie del Fondo de Procedencia Externa",
"Colecciones Gráficas de Procedencia Externa",
"Colección Gráfica de Procedencia Externa",
"Sección de la Colección Gráfica de Procedencia Ext",
"Unidad Gráfica de la Colección de Procedencia Exte",
"Archivo Oral",
"Fondo Oral",
"Sección Oral",
"Memoria Democrática"]


levels = { slugify(x):unidecode(x.strip().lower()) for x in levels }


with open('templates/template_skos.xml') as file_:
    template = Template(file_.read())

print(template.render(levels=levels))

