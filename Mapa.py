import json
import webbrowser
import folium

from folium.plugins import MarkerCluster
from branca.element import Template as BrancaTemplate, MacroElement, Element


try:
    from folium.plugins import MarkerCluster
    HAS_CLUSTER = False
except Exception:
    HAS_CLUSTER = False




def mostrar_grafo(grafo, dibujar_rutas=True):
    if not grafo.vertices:
        print("No hay vértices en el grafo.")
        return

    import folium, webbrowser

    Mapa = folium.Map(
        location=[grafo.vertices[0].latitud, grafo.vertices[0].longitud],
        zoom_start=3
    )
    capa_vertices = folium.FeatureGroup(name="Aeropuertos", show=True)

    # --- Marcadores (con popup informativo; si no quieres popups, ver nota abajo) ---
    for v in grafo.vertices:
        if not v:
            continue
        popup_html = f"""
        <b>{v.aeropuerto}</b> ({v.codigo})<br>
        Ciudad: {v.ciudad}<br>
        País: {v.pais}<br>
        Latitud: {v.latitud:.4f}<br>
        Longitud: {v.longitud:.4f}
        """
        folium.Marker(
            location=[v.latitud, v.longitud],
            popup=popup_html,       # <-- quita este argumento si no quieres popups
            tooltip=v.codigo
        ).add_to(capa_vertices)

    Mapa.add_child(capa_vertices)

    # --- Rutas opcionales (solo dibuja líneas, sin interacción) ---
    if dibujar_rutas:
        capa_rutas = folium.FeatureGroup(name="Rutas (todas)", show=False)
        vistos = set()
        for i, adys in enumerate(grafo.adyacencia):
            for e in adys:
                j, _w = e if isinstance(e, tuple) else (e, 1.0)
                a, b = (i, j) if i < j else (j, i)
                if a == b or (a, b) in vistos:
                    continue
                vistos.add((a, b))
                va, vb = grafo.vertices[a], grafo.vertices[b]
                if va and vb:
                    folium.PolyLine(
                        [(va.latitud, va.longitud), (vb.latitud, vb.longitud)],
                        weight=1, opacity=0.35
                    ).add_to(capa_rutas)
        Mapa.add_child(capa_rutas)

    folium.LayerControl().add_to(Mapa)
    Mapa.save("mapa_simple.html")
    webbrowser.open("mapa_simple.html")


def mostrar_camino_minimo(vertices_camino):
    if not vertices_camino or len(vertices_camino) < 2:
        print("Camino insuficiente para mostrar.")
        return

    Mapa = folium.Map(
        location=[vertices_camino[0].latitud, vertices_camino[0].longitud],
        zoom_start=4
    )

    for v in vertices_camino:
        popup_html = f"""
        <b>{v.aeropuerto}</b> ({v.codigo})<br>
        Ciudad: {v.ciudad}<br>
        País: {v.pais}<br>
        Lat: {v.latitud:.4f} | Lon: {v.longitud:.4f}
        """
        folium.Marker([v.latitud, v.longitud], popup=popup_html, tooltip=v.codigo).add_to(Mapa)

    coords = [(v.latitud, v.longitud) for v in vertices_camino]
    folium.PolyLine(coords, color="red", weight=3, opacity=0.8).add_to(Mapa)

    folium.LayerControl().add_to(Mapa)
    Mapa.save("camino_minimo.html")
    webbrowser.open("camino_minimo.html")