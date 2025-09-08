import math
import random
from typing import List, Tuple, Dict
from datetime import datetime
import json
import pandas as pd

class Cliente:
    def __init__(self, id_cliente: str, latitud: float, longitud: float):
        self.id_cliente = id_cliente
        self.latitud = latitud
        self.longitud = longitud

class OptimizadorRutas:
    def __init__(self, punto_partida: Tuple[float, float] = None):
        self.punto_partida = punto_partida  # (latitud, longitud)
        self.clientes = []
        
    def agregar_cliente(self, cliente: Cliente):
        """Agrega un cliente a la lista"""
        self.clientes.append(cliente)
    
    def agregar_clientes_desde_lista(self, lista_clientes: List[Dict]):
        """Agrega múltiples clientes desde una lista de diccionarios"""
        for cliente_data in lista_clientes:
            cliente = Cliente(
                id_cliente=cliente_data['id'],
                latitud=cliente_data['latitud'],
                longitud=cliente_data['longitud'],
            )
            self.agregar_cliente(cliente)
    
    def calcular_distancia(self, punto1: Tuple[float, float], 
                          punto2: Tuple[float, float]) -> float:
        """Calcula distancia entre dos puntos usando fórmula de Haversine"""
        lat1, lon1 = punto1
        lat2, lon2 = punto2
        
        # Radio de la Tierra en kilómetros
        R = 6371.0
        
        # Convertir grados a radianes
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Diferencias
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distancia = R * c
        return distancia
    
    def crear_matriz_distancias(self) -> List[List[float]]:
        """Crea matriz de distancias entre todos los puntos"""
        puntos = []
        
        # Agregar punto de partida si existe
        if self.punto_partida:
            puntos.append(self.punto_partida)
        
        # Agregar todos los clientes
        for cliente in self.clientes:
            puntos.append((cliente.latitud, cliente.longitud))
        
        n = len(puntos)

        matriz = [[0.0 for _ in range(n)] for _ in range(n)]
        print("--------------------------------------------------------------")
        for i in range(n):
            print(f"\nCalculando distancia entre {puntos[i]} y los puntos:")
            for j in range(n):
                if i != j:
                    matriz[i][j] = self.calcular_distancia(puntos[i], puntos[j])
                    print(f"Con el punto {puntos[j]} - Distancia: {matriz[i][j]} km")

        #Imprime la matriz de distancias completa
        print("--------------------------------------------------------------")
        print("\nMatriz de distancias completa:\n")

        for fila in matriz:
            print(fila) 
        print("--------------------------------------------------------------")

        return matriz
    
    def algoritmo_vecino_cercano(self, matriz_distancias: List[List[float]]) -> List[int]:
        """Implementa el algoritmo del vecino más cercano"""

        print("\nDefiniendo ruta inicial con el algoritmo del vecino más cercano...")
        n = len(matriz_distancias)

        if n == 0:
            return []
        
        # Empezar desde el punto de partida (índice 0) si existe, sino desde el primer cliente
        punto_actual = 0
        ruta = [punto_actual]
        visitados = {punto_actual}
        
        while len(ruta) < n:
            distancia_minima = float('inf')
            siguiente_punto = -1
            
            # Buscar el punto más cercano no visitado
            for i in range(n):
                if i not in visitados and matriz_distancias[punto_actual][i] < distancia_minima:
                    distancia_minima = matriz_distancias[punto_actual][i]
                    siguiente_punto = i
            
            if siguiente_punto != -1:
                ruta.append(siguiente_punto)
                visitados.add(siguiente_punto)
                punto_actual = siguiente_punto

        print("\nRuta inicial definida: ", ruta)
        print("--------------------------------------------------------------")

        return ruta
    
    def optimizar_2opt(self, ruta: List[int], matriz_distancias: List[List[float]]) -> List[int]:
        """Optimiza la ruta usando el algoritmo 2-opt"""

        print("\nOptimizando ruta con el algoritmo 2-opt...")
        mejor_ruta = ruta[:]
        mejor_distancia = self.calcular_distancia_total(mejor_ruta, matriz_distancias)
        mejora = True
        while mejora:
            mejora = False
            for i in range(1, len(ruta) - 2):
                for j in range(i + 1, len(ruta)):
                    if j - i == 1:
                        continue
                    
                    # Crear nueva ruta intercambiando el segmento
                    nueva_ruta = ruta[:i] + ruta[i:j+1][::-1] + ruta[j+1:]
                    nueva_distancia = self.calcular_distancia_total(nueva_ruta, matriz_distancias)
                    print("\nCalculando la distancia de la ruta: ", nueva_ruta,)
                    print("Distancia: ", nueva_distancia)
                    if nueva_distancia < mejor_distancia:
                        mejor_ruta = nueva_ruta[:]
                        mejor_distancia = nueva_distancia
                        ruta = nueva_ruta[:]
                        mejora = True
        print("--------------------------------------------------------------")
        print("\nRuta optimizada: ", mejor_ruta, "\n")
        return mejor_ruta
    
    def calcular_distancia_total(self, ruta: List[int], 
                                matriz_distancias: List[List[float]]) -> float:
        """Calcula la distancia total de una ruta"""
        distancia_total = 0.0
        
        for i in range(len(ruta) - 1):
            distancia_total += matriz_distancias[ruta[i]][ruta[i + 1]]
        return distancia_total
    
    def optimizar_ruta(self) -> Dict:
        """Optimiza la ruta y retorna los resultados"""
        if not self.clientes:
            return {"error": "No hay clientes para optimizar"}
        
        # Crear matriz de distancias
        matriz_distancias = self.crear_matriz_distancias()
        
        # Aplicar algoritmo del vecino más cercano
        ruta_inicial = self.algoritmo_vecino_cercano(matriz_distancias)
        
        # Optimizar con 2-opt
        ruta_optimizada = self.optimizar_2opt(ruta_inicial, matriz_distancias)
        
        # Calcular estadísticas
        distancia_total = self.calcular_distancia_total(ruta_optimizada, matriz_distancias)
        tiempo_viaje = distancia_total * 3  # Estimado: 3 min por km en moto
        
        
        return {
            "ruta": ruta_optimizada,
            "distancia_total_km": round(distancia_total, 2),
            "tiempo_viaje_min": round(tiempo_viaje, 1),
        }
    
    def generar_lista_ruta(self) -> str:
        """Genera la lista de ruta en formato texto"""
        resultados = self.optimizar_ruta()
        
        if "error" in resultados:
            return resultados["error"]
        
        ruta = resultados["ruta"]
        output = []
        
        # Encabezado
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        output.append("=" * 50)
        output.append(f"RUTA ÓPTIMA - {fecha_actual}")
        output.append("=" * 50)
        
        if self.punto_partida:
            output.append(f"Punto de partida:")
            output.append(f"   Latitud, Longitud")
            output.append(f"   {self.punto_partida[0]}, {self.punto_partida[1]}")
        
        output.append("")
        
        # Lista de clientes en orden
        contador = 1
        for i in ruta:
            if self.punto_partida and i == 0:
                continue  # Saltar el punto de partida en la lista
            
            # Ajustar índice si hay punto de partida
            indice_cliente = i - 1 if self.punto_partida else i
            
            if 0 <= indice_cliente < len(self.clientes):
                cliente = self.clientes[indice_cliente]
                output.append(f"{contador}. Cliente: {cliente.id_cliente}")
                output.append(f"   Latitud, Longitud")
                output.append(f"   {cliente.latitud}, {cliente.longitud}")
                output.append("")
                contador += 1
        
        # Resumen
        output.append("-" * 30)
        output.append("RESUMEN DEL RECORRIDO")
        output.append("-" * 30)
        output.append(f"Distancia total: {resultados['distancia_total_km']} km")
        output.append(f"Tiempo de viaje: {resultados['tiempo_viaje_min']} min")
        
        return "\n".join(output)

# Método principal para ejecutar el optimizador
if __name__ == "__main__":

    # Leer el archivo Excel
    df = pd.read_excel(r"..\coordenadas.xlsx")  # asegúrate de que el archivo existe

    # Convertir a lista de diccionarios
    puntos = df.to_dict(orient="records")

    # Crear optimizador con punto de partida (ejemplo: centro de Cúcuta)
    optimizador = OptimizadorRutas(punto_partida=(puntos[0]["latitud"], puntos[0]["longitud"]))

    # Datos de ejemplo de clientes en Cúcuta
    # clientes_ejemplo = [
    #     {
    #         "id": "001",
    #         "latitud": 7.8891,
    #         "longitud": -72.5020,
    #     },
    #     {
    #         "id": "002", 
    #         "latitud": 7.9010,
    #         "longitud": -72.5150,
    #     },
    #     {
    #         "id": "003",
    #         "latitud": 7.8850,
    #         "longitud": -72.4950,
    #     },
    #     {
    #         "id": "004",
    #         "latitud": 7.9100,
    #         "longitud": -72.5200,
    #     }
    # ]
    
    # Agregar clientes
    optimizador.agregar_clientes_desde_lista(puntos[1:])
    
    # Generar y mostrar la ruta optimizada
    lista_ruta = optimizador.generar_lista_ruta()
    print(lista_ruta)
    
    # Opcional: guardar en archivo
    with open("../ruta_optimizada.txt", "w", encoding="utf-8") as archivo:
        archivo.write(lista_ruta)
    print("\n✅ Ruta guardada en 'ruta_optimizada.txt'")