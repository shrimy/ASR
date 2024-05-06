import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import time

# Zmienne globalne
graf_wygenerowany = False  # Zmienna określająca, czy graf został wygenerowany
graf = None  # Zmienna przechowująca wygenerowany graf

# Funkcje generujące grafy losowe
def generuj_graf_skierowany(l_wierzcholkow, l_krawedzi):
    # Funkcja generująca losowy graf skierowany z wagami na krawędziach
    if l_krawedzi < l_wierzcholkow:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()  # Tworzenie nowego pustego grafu skierowanego
    nodes = range(1, l_wierzcholkow + 1)  # Tworzenie listy wierzchołków
    G.add_nodes_from(nodes)  # Dodanie wierzchołków do grafu

    # Dodanie krawędzi od wierzchołka i do i+1, aby utworzyć cykl
    for i in range(1, l_wierzcholkow):
        waga = random.randint(1, 20)  # Losowanie wagi krawędzi
        G.add_edge(i, i + 1, weight=waga)
    waga = random.randint(1, 20)
    G.add_edge(l_wierzcholkow, 1, weight=waga)  # Połączenie ostatniego wierzchołka z pierwszym, tworząc cykl

    # Obliczenie maksymalnej liczby krawędzi
    maks_krawedzi = l_wierzcholkow * (l_wierzcholkow - 1)
    l_krawedzi = min(l_krawedzi, maks_krawedzi)

    # Losowe dodawanie krawędzi, upewniając się, że nie powtarzają się
    while G.number_of_edges() < l_krawedzi:
        u = random.randint(1, l_wierzcholkow)
        v = random.randint(1, l_wierzcholkow)
        if u != v and not G.has_edge(u, v):
            waga = random.randint(1, 20)
            G.add_edge(u, v, weight=waga)
            if G.has_edge(v, u):
                G[u][v]['weight'] = G[v][u]['weight']  # Ustawienie wagi dla obu kierunków krawędzi
    return G

def generuj_pelny_graf_skierowany(l_wierzcholkow):
    # Funkcja generująca losowy pełny graf skierowany z wagami na krawędziach
    G = nx.DiGraph()  # Tworzenie nowego pustego grafu skierowanego
    nodes = range(1, l_wierzcholkow + 1)  # Tworzenie listy wierzchołków
    G.add_nodes_from(nodes)  # Dodanie wierzchołków do grafu

    # Dodanie krawędzi między każdą parą wierzchołków (poza sam do siebie)
    for u in nodes:
        for v in nodes:
            if u != v:
                waga = random.randint(1, 20)  # Losowanie wagi krawędzi
                G.add_edge(u, v, weight=waga)
                if G.has_edge(v, u):
                    G[u][v]['weight'] = G[v][u]['weight']  # Ustawienie wagi dla obu kierunków krawędzi

    return G

# Funkcje wczytujące i zapisujące istniejący graf
def wczytaj_graf(nazwa_pliku):
    # Funkcja wczytująca graf z pliku tekstowego w formacie GML
    try:
        graf = nx.read_gml(nazwa_pliku)
        print("Graf został wczytany z pliku:", nazwa_pliku)

        # Konwersja wierzchołków na typ int
        graf = nx.convert_node_labels_to_integers(graf, first_label=1, ordering='default')

        return graf
    except FileNotFoundError:
        print("Podany plik nie istnieje.")
    except nx.NetworkXError:
        print("Nie udało się wczytać grafu z pliku.")
    return None

def zapisz_graf(graf, nazwa_pliku):
    # Funkcja zapisująca graf do pliku w formacie GML
    nx.write_gml(graf, nazwa_pliku)

# Funkcje rysujące
def rysuj_graf_z_trasa(graf, trasa):
    # Funkcja rysująca graf z podświetloną trasą
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graf)
    edge_labels = nx.get_edge_attributes(graf, 'weight')
    nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)

    # Podświetlenie krawędzi na trasie
    for i in range(len(trasa) - 1):
        u = trasa[i]
        v = trasa[i + 1]
        nx.draw_networkx_edges(graf, pos, edgelist=[(u, v)], width=2.0, edge_color='red')
        nx.draw_networkx_edges(graf, pos, edgelist=[(v, u)], width=2.0, edge_color='red')

    nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)
    plt.title("Wygenerowany graf z najkrótszą trasą")
    plt.show()

# Funkcje edycji grafu
def dodaj_krawedz(graf, u, v, waga):
    # Funkcja dodająca krawędź do grafu
    graf.add_edge(u, v, weight=waga)

def usun_krawedz(graf, u, v):
    # Funkcja usuwająca krawędź z grafu
    if graf.has_edge(u, v):
        graf.remove_edge(u, v)

def dodaj_wierzcholek(graf, nowy_wierzcholek):
    # Funkcja dodająca wierzchołek do grafu
    graf.add_node(nowy_wierzcholek)

def usun_wierzcholek(graf, wierzcholek):
    # Funkcja usuwająca wierzchołek z grafu
    if graf.has_node(wierzcholek):
        graf.remove_node(wierzcholek)

# Funkcje związane z algorytmami
def generuj_macierz_wag(graf):
    # Funkcja generująca macierz wag dla grafu
    l_wierzcholkow = len(graf.nodes())
    macierz_wag = np.zeros((l_wierzcholkow, l_wierzcholkow))

    for u, v, weight in graf.edges(data='weight'):
        u = int(u) - 1  # Konwersja numeru wierzchołka na indeks (indeksujemy od zera)
        v = int(v) - 1  # Konwersja numeru wierzchołka na indeks (indeksujemy od zera)
        macierz_wag[u][v] = int(weight)

    return macierz_wag

def wypisz_macierz_incydencji(graf):
    # Funkcja wypisująca macierz incydencji grafu
    macierz_incydencji = nx.incidence_matrix(graf, oriented=True).toarray()
    print("Macierz incydencji:")
    print(macierz_incydencji)

def dijkstra(graf, wierzcholek_startowy):
    # Algorytm Dijkstry do znajdowania najkrótszych ścieżek w grafie
    odleglosci = {node: float('inf') for node in graf.nodes()}
    odleglosci[wierzcholek_startowy] = 0
    odwiedzone = set()

    while len(odwiedzone) < len(graf.nodes()):
        aktualny_wierzcholek = min((node for node in graf.nodes() if node not in odwiedzone), key=lambda node: odleglosci[node])
        odwiedzone.add(aktualny_wierzcholek)

        for sasiad, waga in graf[aktualny_wierzcholek].items():
            odleglosci[sasiad] = min(odleglosci[sasiad], odleglosci[aktualny_wierzcholek] + waga['weight'])

    return odleglosci

def bellman_ford_moore(graf, wierzcholek_startowy):
    # Algorytm Bellmana-Forda-Moorea do znajdowania najkrótszych ścieżek w grafie
    odleglosci = {node: float('inf') for node in graf.nodes()}
    odleglosci[wierzcholek_startowy] = 0

    for _ in range(len(graf.nodes()) - 1):
        for u, v, waga in graf.edges(data=True):
            if odleglosci[u] != float('inf') and odleglosci[u] + waga['weight'] < odleglosci[v]:
                odleglosci[v] = odleglosci[u] + waga['weight']

    return odleglosci

def floyd_warshall(graf):
    # Algorytm Floyda-Warshalla do znajdowania najkrótszych ścieżek w grafie
    l_wierzcholkow = len(graf.nodes())
    odleglosci = np.full((l_wierzcholkow, l_wierzcholkow), float('inf'))

    for wierzcholek in graf.nodes():
        odleglosci[wierzcholek-1][wierzcholek-1] = 0

    for u, v, waga in graf.edges(data=True):
        odleglosci[u-1][v-1] = waga['weight']

    for k in range(l_wierzcholkow):
        for i in range(l_wierzcholkow):
            for j in range(l_wierzcholkow):
                odleglosci[i][j] = min(odleglosci[i][j], odleglosci[i][k] + odleglosci[k][j])

    return odleglosci

# Funkcje interakcji z użytkownikiem
def wybierz_i_wyswietl_algorytm_z_trasa():
    global graf_wygenerowany, graf
    if graf_wygenerowany:
        wypisz_macierz_incydencji(graf)
        macierz_wag_graf = generuj_macierz_wag(graf)
        print("Macierz wag grafu:")
        print(macierz_wag_graf)

        while True:
            try:
                wybor_algorytmu = input("Wybierz algorytm (dijkstra/bellman_ford/floyd_warshall): ").lower()
                if wybor_algorytmu not in ["dijkstra", "bellman_ford", "floyd_warshall"]:
                    raise ValueError("Niewłaściwy wybór algorytmu.")
                break
            except ValueError as e:
                print(e)

        if wybor_algorytmu == "floyd_warshall":
            czas_start = time.time()
            odleglosci = floyd_warshall(graf)
            czas_wykonania = time.time() - czas_start

            print("Macierz odległości:")
            print(odleglosci)
            print("Czas wykonania: %.6f sekund" % czas_wykonania)
        else:
            while True:
                try:
                    wybor_sciezek = input("Wybierz opcję (wszystkie/konkretna): ").lower()
                    if wybor_sciezek not in ["wszystkie", "konkretna"]:
                        raise ValueError("Niewłaściwy wybór opcji.")
                    break
                except ValueError as e:
                    print(e)

            if wybor_sciezek == "wszystkie":
                czas_start = time.time()
                if wybor_algorytmu == "dijkstra":
                    odleglosci = {}
                    for wierzcholek in graf.nodes():
                        odleglosci[wierzcholek] = dijkstra(graf, wierzcholek)
                elif wybor_algorytmu == "bellman_ford":
                    odleglosci = {}
                    for wierzcholek in graf.nodes():
                        odleglosci[wierzcholek] = bellman_ford_moore(graf, wierzcholek)
                czas_wykonania = time.time() - czas_start

                print("Najkrótsze odległości:")
                for wierzcholek, wyniki in odleglosci.items():
                    print(f"Od wierzchołka {wierzcholek}: {wyniki}")
                print("Czas wykonania: %.6f sekund" % czas_wykonania)
            else:
                while True:
                    try:
                        wierzcholek_startowy = int(input("Podaj wierzchołek startowy: "))
                        if wierzcholek_startowy not in graf.nodes():
                            raise ValueError("Wierzchołek nie istnieje w grafie.")
                        break
                    except ValueError as e:
                        print(e)

                czas_start = time.time()
                if wybor_algorytmu == "dijkstra":
                    odleglosci = dijkstra(graf, wierzcholek_startowy)
                elif wybor_algorytmu == "bellman_ford":
                    odleglosci = bellman_ford_moore(graf, wierzcholek_startowy)
                czas_wykonania = time.time() - czas_start

                print("Najkrótsze odległości:")
                for wierzcholek, odleglosc in odleglosci.items():
                    print(f"Od wierzchołka {wierzcholek}: {odleglosc}")
                print("Czas wykonania: %.6f sekund" % czas_wykonania)

                while True:
                    try:
                        czy_rysowac = input("Czy narysować trasę (tak/nie): ").lower()
                        if czy_rysowac not in ["tak", "nie"]:
                            raise ValueError("Niewłaściwa odpowiedź.")
                        break
                    except ValueError as e:
                        print(e)

                if czy_rysowac == "tak":
                    while True:
                        try:
                            wierzcholek_koncowy = int(input("Podaj wierzchołek końcowy: "))
                            if wierzcholek_koncowy not in graf.nodes():
                                raise ValueError("Wierzchołek nie istnieje w grafie.")
                            break
                        except ValueError as e:
                            print(e)

                    try:
                        trasa = nx.shortest_path(graf, source=wierzcholek_startowy, target=wierzcholek_koncowy, weight='weight')
                        rysuj_graf_z_trasa(graf, trasa)
                    except nx.NetworkXNoPath:
                        print("Brak ścieżki między podanymi wierzchołkami.")

    else:
        print("Najpierw wygeneruj graf!")

def czy_graf_spojny(graf):
    return nx.is_strongly_connected(graf)

def menu():
    print("\n----- MENU -----")
    print("1. Generuj losowy graf skierowany")
    print("2. Generuj losowy pełny graf skierowany")
    print("3. Wczytaj graf z pliku")
    print("4. Zapisz graf do pliku")
    print("5. Dodaj krawędź")
    print("6. Usuń krawędź")
    print("7. Dodaj wierzchołek")
    print("8. Usuń wierzchołek")
    print("9. Wybierz i wyświetl algorytm z trasą")
    print("10. Sprawdź spójność grafu")
    print("0. Zakończ")

# Pętla menu
while True:
    menu()
    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        l_wierzcholkow = int(input("Podaj liczbę wierzchołków: "))
        l_krawedzi = int(input("Podaj liczbę krawędzi: "))
        graf = generuj_graf_skierowany(l_wierzcholkow, l_krawedzi)
        graf_wygenerowany = True

        # Wyświetlanie grafu po jego wygenerowaniu
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(graf)
        nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
        edge_labels = nx.get_edge_attributes(graf, 'weight')
        nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)
        plt.title("Wygenerowany graf skierowany")
        plt.show()

    elif wybor == "2":
        l_wierzcholkow = int(input("Podaj liczbę wierzchołków: "))
        graf = generuj_pelny_graf_skierowany(l_wierzcholkow)
        graf_wygenerowany = True

        # Wyświetlanie grafu po jego wygenerowaniu
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(graf)
        nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
        edge_labels = nx.get_edge_attributes(graf, 'weight')
        nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)
        plt.title("Wygenerowany pełny graf skierowany")
        plt.show()

    elif wybor == "3":
        nazwa_pliku = input("Podaj nazwę pliku do wczytania (z rozszerzeniem .gml): ")
        graf = wczytaj_graf(nazwa_pliku)
        if graf is not None:
            graf_wygenerowany = True

        # Wyświetlanie grafu po jego wygenerowaniu
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(graf)
        nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
        edge_labels = nx.get_edge_attributes(graf, 'weight')
        nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)
        plt.title("Wygenerowany pełny graf skierowany")
        plt.show()

    elif wybor == "4":
        if graf_wygenerowany:
            nazwa_pliku = input("Podaj nazwę pliku: ")
            zapisz_graf(graf, nazwa_pliku)
            print("Graf został zapisany do pliku:", nazwa_pliku)
        else:
            print("Najpierw wygeneruj graf!")


    elif wybor == "5":
        if graf_wygenerowany:
            while True:
                try:
                    u = int(input("Podaj początek krawędzi: "))
                    if u not in graf.nodes:
                        raise ValueError("Podany początek krawędzi nie istnieje w grafie.")
                    v = int(input("Podaj koniec krawędzi: "))
                    if v not in graf.nodes:
                        raise ValueError("Podany koniec krawędzi nie istnieje w grafie.")
                    waga = int(input("Podaj wagę krawędzi: "))
                    dodaj_krawedz(graf, u, v, waga)
                    break  # Jeśli nie ma błędu, przerywamy pętlę
                except ValueError as e:
                    print("Błąd:", e)
                    print("Spróbuj ponownie.")
        else:
            print("Najpierw wygeneruj graf!")



    elif wybor == "6":
        if graf_wygenerowany:
            while True:
                try:
                    u = int(input("Podaj początek krawędzi do usunięcia: "))
                    if u not in graf.nodes:
                        raise ValueError("Podany początek krawędzi nie istnieje w grafie.")
                    v = int(input("Podaj koniec krawędzi do usunięcia: "))
                    if v not in graf.nodes:
                        raise ValueError("Podany koniec krawędzi nie istnieje w grafie.")
                    usun_krawedz(graf, u, v)
                    break  # Jeśli nie ma błędu, przerywamy pętlę
                except ValueError as e:
                    print("Błąd:", e)
                    print("Spróbuj ponownie.")
        else:
            print("Najpierw wygeneruj graf!")

    elif wybor == "7":
        if graf_wygenerowany:
            while True:
                try:
                    nowy_wierzcholek = int(input("Podaj numer nowego wierzchołka: "))
                    if nowy_wierzcholek in graf.nodes:
                        raise ValueError("Podany wierzchołek już istnieje w grafie.")
                    dodaj_wierzcholek(graf, nowy_wierzcholek)
                    break  # Jeśli nie ma błędu, przerywamy pętlę
                except ValueError as e:
                    print("Błąd:", e)
                    print("Spróbuj ponownie.")
        else:
            print("Najpierw wygeneruj graf!")

    elif wybor == "8":
        if graf_wygenerowany:
            while True:
                try:
                    wierzcholek = int(input("Podaj numer wierzchołka do usunięcia: "))
                    if wierzcholek not in graf.nodes:
                        raise ValueError("Podany wierzchołek nie istnieje w grafie.")
                    usun_wierzcholek(graf, wierzcholek)
                    break  # Jeśli nie ma błędu, przerywamy pętlę
                except ValueError as e:
                    print("Błąd:", e)
                    print("Spróbuj ponownie.")
        else:
            print("Najpierw wygeneruj graf!")

    elif wybor == "9":
        wybierz_i_wyswietl_algorytm_z_trasa()

    elif wybor == "10":
        if graf_wygenerowany:
            if czy_graf_spojny(graf):
                print("Graf jest spójny.")
            else:
                print("Graf nie jest spójny.")
                exit()
        else:
            print("Najpierw wygeneruj graf!")

    elif wybor == "0":
        print("Do widzenia!")
        break
    else:
        print("Niewłaściwy wybór! Spróbuj ponownie.")