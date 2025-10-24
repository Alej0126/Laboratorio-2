# pylint: disable=missing-class-docstring,missing-function-docstring

import math
import pandas as pd
import heapq 



class Vertice:

    def __init__(self, codigo, aeropuerto, ciudad, pais, latitud, longitud):
        self.codigo = codigo
        self.aeropuerto = aeropuerto
        self.ciudad = ciudad
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud



class Grafo:

    def __init__(self, n, ponderado=False, dirigido=False):
        self.n = n
        self.ponderado = ponderado
        self.dirigido = dirigido
        self.adyacencia = []
        self.vertices = [None] * n

        for _ in range(n):
            lista_vecinos = []
            self.adyacencia.append(lista_vecinos)

    def vertice_por_indice(self, i):
        return self.vertices[i] if 0 <= i < self.n else None

    def info_vertice(self, i):
        v = self.vertice_por_indice(i)
        if not v:
            return "Vértice no válido"
        return (f"Código: {v.codigo}\n"
                f"Aeropuerto: {v.aeropuerto}\n"
                f"Ciudad: {v.ciudad}\n"
                f"País: {v.pais}\n"
                f"Lat: {v.latitud}\n"
                f"Lon: {v.longitud}")

    def info_vertice_por_codigo(self, codigo):
        idx = self.indice_por_codigo(codigo)
        if idx == -1:
            return None, -1
        return self.info_vertice(idx), idx

    def dijkstra(self, fuente_idx):
        INF = float('inf')
        dist = [INF] * self.n
        prev = [-1] * self.n

        dist[fuente_idx] = 0.0
        pq = [(0.0, fuente_idx)]  # (dist, node)

        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue

            # Normaliza la lista de vecinos (tu adyacencia guarda (v,p) si ponderado)
            for elem in self.adyacencia[u]:
                if self.ponderado:
                    v, w = elem
                else:
                    v, w = elem, 1.0
                nd = d + float(w)
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))

        return dist, prev
    
    def reconstruir_camino(self, prev, destino_idx):
        camino = []
        cur = destino_idx
        while cur != -1:
            camino.append(cur)
            cur = prev[cur]
        camino.reverse()
        return camino 
    
    def top10_caminos_minimos_mas_largos(self, codigo_fuente):
        fuente_idx = self.indice_por_codigo(codigo_fuente)
        if fuente_idx == -1:
            return None, "Código de aeropuerto no encontrado."

        dist, prev = self.dijkstra(fuente_idx)

        # destinos alcanzables distintos de la fuente
        candidatos = [(dist[i], i) for i in range(self.n)
                    if dist[i] not in (float('inf'), 0.0) and self.vertices[i] is not None]
        if not candidatos:
            print("No hay destinos alcanzables desde la fuente.")
            return [], None

        # orden descendente por distancia y tomar top-10
        candidatos.sort(reverse=True, key=lambda x: x[0])
        top = candidatos[:10]

        print(f"\n--- Top 10 'caminos mínimos' más largos desde {codigo_fuente} ---")
        resultado = []
        for k, (d, i) in enumerate(top, 1):
            v = self.vertices[i]
            # reconstruir camino
            camino_idx = self.reconstruir_camino(prev, i)
            path_codes = [self.vertices[j].codigo for j in camino_idx if self.vertices[j] is not None]

            print(f"{k:2d}) {v.codigo} - {v.aeropuerto}")
            print(f"    Ciudad: {v.ciudad}, País: {v.pais}")
            print(f"    Distancia (camino mínimo): {d:.2f} km")
            print(f"    Camino: {' → '.join(path_codes)}\n")

            resultado.append({
                "codigo": v.codigo,
                "aeropuerto": v.aeropuerto,
                "ciudad": v.ciudad,
                "pais": v.pais,
                "lat": v.latitud,
                "lon": v.longitud,
                "distancia": d,
                "camino": path_codes
            })
        return resultado, None

    def agregar_vertice(self, indice, vertice):
        if 0 <= indice < self.n:
            self.vertices[indice] = vertice


    def indice_por_codigo(self, codigo):
        for i, vertice in enumerate(self.vertices):
            if vertice and vertice.codigo == codigo:
                return i
        return -1
    
    def resumen_simple(self):
        vistas = set()        # (min(u,v), max(u,v)) para contar arista única
        loops = 0
        multiaristas = 0      # repeticiones en la MISMA lista de u
        total_dirigidas = 0   # total de entradas en listas (contará 2 por arista no dirigida)

        for u, vecinos in enumerate(self.adyacencia):
            vistos_en_u = set()
            for e in vecinos:
                v, _w = e if isinstance(e, tuple) else (e, 1.0)
                total_dirigidas += 1

                if u == v:
                    loops += 1
                    continue

                # multiarista: mismo v aparece más de una vez en la lista de u
                if v in vistos_en_u:
                    multiaristas += 1
                else:
                    vistos_en_u.add(v)

                a, b = (u, v) if u < v else (v, u)
                vistas.add((a, b))

        print(f"Vértices (con datos): {sum(1 for x in self.vertices if x)}")
        print(f"Aristas únicas (no dirigidas): {len(vistas)}")
        print(f"Entradas en listas (esperable ~2*aristas): {total_dirigidas}")
        print(f"Bucles detectados: {loops}")
        print(f"Multiaristas reales (mismo u->v repetido): {multiaristas}")




    def agregar_arista(self, u, v, peso=1):
        if self.ponderado:

            if (v, peso) not in self.adyacencia[u]:
                self.adyacencia[u].append((v, peso))
            if not self.dirigido:
                if (u, peso) not in self.adyacencia[v]:
                    self.adyacencia[v].append((u, peso))
        else:
            if v not in self.adyacencia[u]:
                self.adyacencia[u].append(v)
            if not self.dirigido and u not in self.adyacencia[v]:
                self.adyacencia[v].append(u)

    def mostrar(self): 
        print("Lista de adyacencia del grafo:")
        for i in range((self.n)):
            vertice = self.vertices[i]
            if vertice:
                nombre_vertice = f"{vertice.codigo}"
            else:
                nombre_vertice = f"Vértice {i}"
           
            if self.ponderado:
                vecinos = []
                for vecino, peso in self.adyacencia[i]:
                    vertice_vecino = self.vertices[vecino]
                    if vertice_vecino:
                        nombre_vecino = f"{vertice_vecino.codigo}"
                    else:
                        nombre_vecino = f"Vértice {vecino}"
                    vecinos.append((nombre_vecino, peso))
                print(f"Vértice {i}: {nombre_vertice} -> {vecinos}")
            else:
                vecinos = []
                for vecino in self.adyacencia[i]:
                    vertice_vecino = self.vertices[vecino]
                    if vertice_vecino:
                        nombre_vecino = f"{vertice_vecino.codigo} ({vertice_vecino.ciudad})"
                    else:
                        nombre_vecino = f"Vértice {vecino}"
                    vecinos.append(nombre_vecino)
                print(f"Vértice {i}: {nombre_vertice} -> {vecinos}")



    # Metodos csv
    def aeropuertos(self, df):
        aeropuertos = []

        for _, fila in df.iterrows():
            origen = (
                fila["Source Airport Code"],
                fila["Source Airport Name"],
                fila["Source Airport City"],
                fila["Source Airport Country"],
                fila["Source Airport Latitude"],
                fila["Source Airport Longitude"]
            )
            destino = (
                fila["Destination Airport Code"],
                fila["Destination Airport Name"],
                fila["Destination Airport City"],
                fila["Destination Airport Country"],
                fila["Destination Airport Latitude"],
                fila["Destination Airport Longitude"]
            )
        
            origen_repetido = False
            for a in aeropuertos:
                if a[0] == origen[0]:
                    origen_repetido = True
                    break

            if not origen_repetido:
                aeropuertos.append(origen)

            destino_repetido = False
            for a in aeropuertos:
                if a[0] == destino[0]:
                    destino_repetido = True
                    break

            if not destino_repetido:
                aeropuertos.append(destino)

        df_aeropuertos = pd.DataFrame(aeropuertos, columns=[
        "CODE", "AIRPORT", "CITY", "COUNTRY", "LAT", "LON"])

        self.n = len(df_aeropuertos)
        self.vertices = [None] * self.n
        self.adyacencia = [[] for _ in range(self.n)]

        for i, fila in df_aeropuertos.iterrows():
            vertice = Vertice(
                fila["CODE"],
                fila["AIRPORT"],
                fila["CITY"],
                fila["COUNTRY"],
                fila["LAT"],
                fila["LON"]
            )
            self.agregar_vertice(i, vertice)


    def haversine(self, df):
        R = 6371.0

        distancias = []
        for _, fila in df.iterrows():
            lat1, lon1 = fila["Source Airport Latitude"], fila["Source Airport Longitude"]
            lat2, lon2 = fila["Destination Airport Latitude"], fila["Destination Airport Longitude"]

            lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
            lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad

            a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = R * c

            distancias.append(distancia)

        df["Haversine"] = distancias
        return df


    def vuelos(self, df, columna_peso=None):

        peso_min = {} 

        for _, fila in df.iterrows():
            u = self.indice_por_codigo(fila["Source Airport Code"])
            v = self.indice_por_codigo(fila["Destination Airport Code"])
            if u == -1 or v == -1:
                continue

         
            if u == v:
                continue

           
            if columna_peso and columna_peso in fila:
                peso = float(fila[columna_peso])
            else:
                peso = 1.0

            a, b = (u, v) if u < v else (v, u)
      
            if (a, b) not in peso_min or peso < peso_min[(a, b)]:
                peso_min[(a, b)] = peso

        for (a, b), w in peso_min.items():
            self.agregar_arista(a, b, w)



    # Punto 1
    def conexidad(self):
        if self.n == 0:
            return True
        
        visitados = [False] * self.n
        componentes = 0
        n_componentes = []
        
        def dfs(vertice):
            visitados[vertice] = True
            vecinos = self.adyacencia[vertice]
            tam = 1
            
            lista_vecinos = []
            for elemento in vecinos:
                if isinstance(elemento, tuple):
                    vertice_vecino, peso = elemento
                    lista_vecinos.append(vertice_vecino)
                else:
                    lista_vecinos.append(elemento)
                
            for vecino in lista_vecinos:
                if not visitados[vecino]:
                    tam += dfs(vecino)

            return tam
        
        for i in range(self.n):
            if not visitados[i]:
                componentes += 1
                tam_componente = dfs(i)
                n_componentes.append(tam_componente)
        
        if componentes == 0:
            componentes = 1
        
        print("\nConexidad: ")
        if componentes == 1:
            print("Grafo conexo")
        else:
            print("Grafo no conexo")
            print(f"\nNumero de componentes: {componentes}")
            for i in range(componentes):
                print (f"Componente {i+1}: {n_componentes[i]} vertices")



    # Punto 2
    def prim_vertice(self, inicio, visitados):
        aristas_arbol = []
        peso_total = 0
        
        cola = []
        cola.append((0, inicio, -1))
        
        while cola:
            indice_menor = 0
            for i in range(1, len(cola)):
                if cola[i][0] < cola[indice_menor][0]:
                    indice_menor = i
            
            peso, vertice_actual, vertice_padre = cola.pop(indice_menor)
            
            if visitados[vertice_actual]:
                continue
            
            visitados[vertice_actual] = True
            if vertice_padre != -1:
                aristas_arbol.append((peso, vertice_padre, vertice_actual))
                peso_total += peso
            
            for elemento in self.adyacencia[vertice_actual]:
                if self.ponderado:
                    vecino, peso_arista = elemento
                else:
                    vecino, peso_arista = elemento, 1
                
                if not visitados[vecino]:
                    cola.append((peso_arista, vecino, vertice_actual))
        
        return peso_total, aristas_arbol

    

    def prim_grafo(self):
        if self.n == 0:
            return []
        
        visitados = [False] * self.n
        todos_arboles = []
        
        for vertice_inicio in range(self.n):
            if not visitados[vertice_inicio]:
                peso, aristas = self.prim_vertice(vertice_inicio, visitados)
                todos_arboles.append((peso, aristas))
        
        return todos_arboles
    


    def arbol_expasion(self):
        arboles = self.prim_grafo()
        
        print("\nARBOLES DE EXPANSIÓN MÍNIMA")
        
        for i in range(len(arboles)):
            peso_componente, aristas_componente = arboles[i]
             
            print(f"\nComponente {i+1}")
            print(f"Peso total: {peso_componente}")
            print(f"Vértices: {len(aristas_componente) + 1}")
            print("Aristas:")
            
            for arista in aristas_componente:
                peso, u, v = arista
                nombre_u = self.vertices[u].codigo if self.vertices[u] else f"V{u}"
                nombre_v = self.vertices[v].codigo if self.vertices[v] else f"V{v}"
                print(f"  {peso} : {nombre_u} -> {nombre_v}")

        return arboles
    
    def top10_caminos_minimos(self, codigo_fuente):
        fuente_idx = self.indice_por_codigo(codigo_fuente)
        if fuente_idx == -1:
            print("No se encontró el aeropuerto fuente.")
            return

        dist, _ = self.dijkstra(fuente_idx)

        alcanzables = [(dist[i], i) for i in range(self.n) if dist[i] != float('inf') and dist[i] != 0.0]

        if not alcanzables:
            print("No hay aeropuertos alcanzables desde este origen.")
            return

        alcanzables.sort(reverse=True, key=lambda x: x[0])

        print(f"\n--- 10 caminos mínimos más largos desde {codigo_fuente} ---")
        for k, (d, i) in enumerate(alcanzables[:10], 1):
            v = self.vertices[i]
            print(f"{k:2d}) {v.codigo} - {v.aeropuerto}")
            print(f"    Ciudad: {v.ciudad}, País: {v.pais}")
            print(f"    Latitud: {v.latitud}, Longitud: {v.longitud}")
            print(f"    Distancia del camino: {d:.2f} km\n")

    def camino_minimo(self, codigo_origen, codigo_destino):
        origen_idx = self.indice_por_codigo(codigo_origen)
        destino_idx = self.indice_por_codigo(codigo_destino)

        if origen_idx == -1 or destino_idx == -1:
            print("Uno o ambos códigos no existen en el grafo.")
            return None, None, None

        dist, prev = self.dijkstra(origen_idx)

        if dist[destino_idx] == float('inf'):
            print(f"No hay camino entre {codigo_origen} y {codigo_destino}.")
            return None, None, None

        camino_indices = self.reconstruir_camino(prev, destino_idx)
        distancia_total = dist[destino_idx]
        return camino_indices, distancia_total, prev






# Menu
df = pd.read_csv("flights_final.csv")

df1 =  df

g1 = Grafo(len(df1), True, False)
g1.aeropuertos(df1)
df1 = g1.haversine(df1)
g1.vuelos(df1, "Haversine")


def menu():
    print("\nLAB 2 — Grafos - Rutas Transporte Aereo")
    print("1) Grafo")
    print("2) punto 1: Conexidad")
    print("3) punto 2: Arbol de expansion minima")
    print("4) punto 3: Info aeropuerto + Top 10 caminos mínimos más largos")
    print("5) punto 4: Camino mínimo entre dos aeropuertos + mapa")
    print("6) Mostrar grafo")
    print("7) Resumen")
    print("0) Salir")
    return input("Elige opción: ").strip()

while True:
        op = menu()
        if op == "0":
            break

        elif op == "1":
            g1.mostrar()
            

        elif op == "2":
            g1.conexidad()
        
        elif op == "3":
            g1.arbol_expasion()


        elif op == "4":
            
            codigo = input("Ingresa el código IATA del aeropuerto fuente (ej: JFK): ").strip().upper()
            info, idx = g1.info_vertice_por_codigo(codigo)
            if idx == -1:
                print("No se encontró el aeropuerto con ese código.")
                continue

            print("\n Información del aeropuerto fuente ")
            print(info)

            # Top 10 con CAMINOS reconstruidos
            g1.top10_caminos_minimos_mas_largos(codigo)


        elif op == "5":
            origen = input("Código IATA del aeropuerto origen: ").strip().upper()
            destino = input("Código IATA del aeropuerto destino: ").strip().upper()

            camino, distancia_total, _ = g1.camino_minimo(origen, destino)
            if not camino:
                continue

            print(f"\n Camino mínimo entre {origen} y {destino} ")
            print(f"Distancia total: {distancia_total:.2f} km\n")

            vertices_camino = []
            for i in camino:
                v = g1.vertices[i]
                if v:

                    print(f"{v.codigo} - {v.aeropuerto}")
                    print(f"  Ciudad: {v.ciudad}, País: {v.pais}")
                    print(f"  Latitud: {v.latitud}, Longitud: {v.longitud}\n")
                    vertices_camino.append(v)

            import json
            coords = [[float(v.latitud), float(v.longitud)] for v in vertices_camino if v]
            with open("camino_minimo.json", "w", encoding="utf-8") as f:
                json.dump({"coords": coords}, f, indent=2)


            try:
                import Mapa
                Mapa.mostrar_camino_minimo(vertices_camino)
            except Exception as e:
                print("No se pudo mostrar el camino en el mapa:", e)


        elif op == "6":
            import Mapa
            Mapa.mostrar_grafo(g1)

        elif op == "7":
            g1.resumen_simple()
