q_clasificacion = """SELECT alias.ID, alias.numerodocumento, alias.clasificacion_ID, alias.titulo, alias.niveldescripcion_ID
    FROM (
        SELECT a.ID, a.numerodocumento, a.clasificacion_ID, a.titulo, a.niveldescripcion_ID, ROW_NUMBER() 
            OVER (ORDER BY a.clasificacion_ID, a.numerodocumento) as row 
        FROM archivo.dbo.archivo a 
            WHERE a.clasificacion_ID LIKE '{clasificacion_id}' 
            AND (numerodocumento IS NOT NULL) ) as alias
    ORDER BY alias.clasificacion_ID, alias.niveldescripcion_ID"""

q_archivo = "SELECT * FROM archivo.dbo.archivo WHERE ID = {archivo_id}"

q_productor = """SELECT P.nombre, A.titulo  FROM archivo.dbo.archivo AS A
                    INNER JOIN archivo.dbo.archivo_productor AS AP ON A.ID = AP.archivo_ID
                    INNER JOIN archivo.dbo.productor AS P ON AP.productor_ID = P.ID
                    WHERE A.ID = {archivo_id};"""

q_lugar = """SELECT L.nombre FROM archivo.dbo.archivo AS A
                    INNER JOIN archivo.dbo.archivo_lugar AS AL ON A.ID = AL.archivo_ID
                    INNER JOIN archivo.dbo.lugar AS L ON AL.lugar_ID = L.ID
                    WHERE A.ID = {archivo_id};"""

q_materia = """SELECT M.nombre, A.titulo  FROM archivo.dbo.archivo AS A
                INNER JOIN archivo.dbo.archivo_materia AS AM ON A.ID = AM.archivo_ID
                INNER JOIN archivo.dbo.materia AS M ON AM.materia_ID = M.ID
                WHERE A.ID = {archivo_id};"""

q_fechas = """SELECT archivo_ID, fechaIni, tipoIni, fechaFin, tipoFin 
                 FROM archivo.dbo.rangofechas WHERE archivo_ID = {archivo_id} ORDER BY fechaIni, fechaFin"""

q_fechas_descripcion = """SELECT R.* FROM archivo.dbo.archivo AS A
                            INNER JOIN archivo.dbo.rangofechasdescripcion AS R ON A.ID = R.archivo_ID
                            WHERE A.ID = {archivo_id};"""

q_get_archivo_by_clas_and_level = """SELECT * FROM archivo.dbo.archivo 
                                    WHERE clasificacion_ID LIKE '{clas}' 
                                    AND niveldescripcion_ID = {level};"""

q_recurso = """SELECT * FROM archivo.dbo.recurso WHERE archivo_ID = {archivo_id}
			ORDER BY 
			  CASE 
			    WHEN CHARINDEX('ADUGT-', url) > 0
			      THEN CONVERT(INT, SUBSTRING(url, CHARINDEX('_', url) + 1, CHARINDEX('.', url) - CHARINDEX('_', url) - 1))
			    ELSE url
			  END;"""

q_recurso_no_order = """SELECT * FROM archivo.dbo.recurso WHERE archivo_ID = {archivo_id}"""

q_rango_signaturas = """SELECT * FROM archivo.dbo.rangosignaturas WHERE archivo_ID = {archivo_id} ORDER BY signaturaIni, signaturaFin"""

q_personas = """SELECT P.nombre, A.titulo, A.clasificacion_ID FROM archivo.dbo.archivo AS A
                  INNER JOIN archivo.dbo.archivo_persona AS AP ON A.ID = AP.archivo_ID
                  INNER JOIN archivo.dbo.persona AS P ON AP.persona_ID = P.ID
                  WHERE A.ID = {archivo_id};"""

q_entidades = """SELECT E.nombre, A.titulo, A.clasificacion_ID FROM archivo.dbo.archivo AS A
                  INNER JOIN archivo.dbo.archivo_entidad AS AP ON A.ID = AP.archivo_ID
                  INNER JOIN archivo.dbo.entidad AS E ON AP.entidad_ID = E.ID
                  WHERE A.ID = {archivo_id};"""