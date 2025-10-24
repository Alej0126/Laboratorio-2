# ✈️ LAB 2 — Grafos: Rutas de Transporte Aéreo

Este proyecto implementa un sistema de análisis de rutas aéreas utilizando grafos ponderados. Permite estudiar la conectividad entre aeropuertos, calcular árboles de expansión mínima, encontrar caminos mínimos (Dijkstra), y visualizar los resultados mediante mapas interactivos generados con Folium.

## ■ Objetivos

•⁠  ⁠Modelar una red de aeropuertos y rutas como un grafo no dirigido y ponderado.

•⁠  ⁠Aplicar algoritmos clásicos de grafos (conexidad, MST, Dijkstra).

•⁠  ⁠Integrar visualizaciones geográficas interactivas con mapas.

•⁠  ⁠Fortalecer el manejo de estructuras de datos en Python.

## ■ Estructura del Proyecto

•⁠  ⁠⁠ Grafo.py ⁠ — Implementación principal de la estructura de grafo

•⁠  ⁠⁠ Grafos.py ⁠ — Archivo del menú principal

•⁠  ⁠⁠ Mapa.py ⁠ — Generación de mapas interactivos con Folium

•⁠  ⁠⁠ README.md ⁠ — Documento descriptivo del proyecto

## ■ Instalación

1.⁠ ⁠Clonar el repositorio con ⁠ git clone ⁠.
2.⁠ ⁠Crear entorno virtual (opcional).
3.⁠ ⁠Instalar dependencias: ⁠ pip install folium ⁠

## ■ Uso

Ejecutar el programa principal: Python Grafos.py 
El menú permite: 
1) Construir el grafo
2) Verificar conexidad
3) Calcular árbol de expansión mínima
4) Mostrar información de aeropuertos
5) Calcular camino mínimo y generar mapa
6) Mostrar grafo completo en mapa
7) Ver resumen general

## ■ Visualización

•⁠  ⁠El punto 5 genera un mapa con el camino más corto (⁠ camino_minimo.html ⁠).

•⁠  ⁠El punto 6 genera un mapa general (⁠ mapa_simple.html ⁠).

Ambos se abren automáticamente en el navegador.

## ■ Errores comunes corregidos

Durante el desarrollo del laboratorio se presentaron varios desafíos, entre ellos:

1.⁠ ⁠*Problemas de importación entre archivos*
   Algunos módulos no se encontraban correctamente, especialmente el de mapas (⁠ Mapa.py ⁠). Esto se resolvió verificando los nombres y rutas de los archivos, además de importar con ⁠ import mapa as Mapa ⁠.

2.⁠ ⁠*Mapas que no se generaban o quedaban vacíos (0 KB)*
   El mapa no mostraba nada porque el grafo no estaba completamente cargado o no se estaban agregando los vértices. Se corrigió agregando validaciones para asegurarse de que los vértices existan antes de dibujar.

3.⁠ ⁠*Aeropuertos aislados sin conexiones visibles*
   Algunos aeropuertos no aparecían en el mapa porque no tenían aristas (rutas). Se añadió una opción adicional para visualizarlos todos, aunque no estén conectados.

4.⁠ ⁠*Errores en la visualización de caminos mínimos*
   Al ejecutar el algoritmo de Dijkstra, el mapa no se abría porque no se encontraba el módulo de mapa o el archivo HTML no se generaba correctamente. Se solucionó con una mejor gestión de excepciones y asegurando que siempre se guarde el archivo ⁠ .html ⁠ antes de abrirlo.

5.⁠ ⁠*Coherencia entre Visual Studio Code y Google Colab*
   Al trabajar entre ambos entornos, se presentaron diferencias en rutas relativas y codificación de archivos. Esto se resolvió manteniendo una estructura de carpetas clara y verificando los import al pasar de un entorno al otro.

6.⁠ ⁠*Integración con GitHub y forks del proyecto*
   Hubo confusiones al unir la versión del repositorio original con la editada en Colab. Se resolvió utilizando ramas y pull requests para sincronizar los cambios de manera ordenada.

## ■ Autores

*Autores:* Alejandro Cantillo, Manuela Maiguel y Yulissa Tapia  
*Estudiantes de Ciencia de Datos e Ing. de Sistemas*
