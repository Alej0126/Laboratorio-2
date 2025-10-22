import folium
import webbrowser

def mostrar_grafo(grafo):
    if not grafo.vertices or len(grafo.vertices) == 0:
        print("No hay vértices en el grafo.")
        return
    
    # Mapa
    mapa = folium.Map(location=[grafo.vertices[0].latitud, grafo.vertices[0].longitud], zoom_start=3)
    
    # Vertices
    for v in grafo.vertices:
        if v:
            folium.Marker(
                location=[v.latitud, v.longitud],
                popup=f"{v.codigo} - {v.ciudad}, {v.pais}",
                tooltip=v.aeropuerto
            ).add_to(mapa)

    # Aristas
    for i, lista_vecinos in enumerate(grafo.adyacencia):
        for vecino, peso in lista_vecinos:
            origen = grafo.vertices[i]
            destino = grafo.vertices[vecino]
            if origen and destino:
                folium.PolyLine(
                    locations=[(origen.latitud, origen.longitud), (destino.latitud, destino.longitud)],
                    color="blue",
                    weight=1,
                    opacity=0.4
                ).add_to(mapa)


    mapa.save("Mapa.html")
    webbrowser.open("Mapa.html")