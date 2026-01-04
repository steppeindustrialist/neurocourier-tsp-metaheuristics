from typing import List
from neurocourier.tsp.types import Tour
from neurocourier.tsp.tour import tour_length, nearest_neighbor_tour

def solve_greedy_2opt(dist_matrix: List[List[float]]) -> Tour:
    """
    Önce Greedy (En Yakın Komşu) ile bir başlangıç rotası oluşturur, 
    ardından 2-opt yerel arama ile rotayı iyileştirir. [cite: 164]
    """
    
    # 1. Aşama: Greedy (Açgözlü) Başlangıç
    current_tour = nearest_neighbor_tour(dist_matrix)
    current_len = tour_length(current_tour, dist_matrix)
    
    # 2. Aşama: 2-opt İyileştirme (Hill Climbing)
    # Rota üzerinde herhangi bir iyileştirme yapılamayana kadar döner.
    n = len(current_tour)
    improved = True
    
    while improved:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n):
                if j - i == 1: continue # Yan yana olan kenarları atla
                
                # 2-opt swap hamlesi 
                new_tour = current_tour[:]
                new_tour[i:j] = list(reversed(new_tour[i:j]))
                new_len = tour_length(new_tour, dist_matrix)
                
                # Eğer yeni yol daha kısaysa, rotayı güncelle ve aramaya devam et
                if new_len < current_len:
                    current_tour = new_tour
                    current_len = new_len
                    improved = True
                    break # İyileştirme bulundu, iç döngüden çık
            if improved:
                break # Dış döngüden çık ve yeni rotayla baştan başla
                
    return current_tour