import tkinter as tk
import random

class Nava:
    def __init__(self, dimensiune):
        self.coordonate = None
        self.dimensiune = dimensiune
        self.forma = [['O' for _ in range(dimensiune)]]

    def pozitioneaza(self, start_x, start_y, directie):
        self.coordonate = []
        if directie == 'dreapta':
            for i in range(self.dimensiune):
                self.coordonate.append((start_x, start_y + i))
        elif directie == 'stanga':
            for i in range(self.dimensiune):
                self.coordonate.append((start_x, start_y - i))
        elif directie == 'jos':
            for i in range(self.dimensiune):
                self.coordonate.append((start_x + i, start_y))
        elif directie == 'sus':
            for i in range(self.dimensiune):
                self.coordonate.append((start_x - i, start_y))


class Jucator:
    def __init__(self, nume, is_computer=False):
        self.nume = nume
        self.is_computer = is_computer
        self.is_computer_turn = False  # Variabilă pentru a ține evidența rândului computerului
        self.nave = []
        self.harta = [['' for _ in range(8)] for _ in range(8)]
        self.harta_atac = [['' for _ in range(8)] for _ in range(8)]
        self.__harta_computer = [['' for _ in range(8)] for _ in range(8)]  # Harta computerului, accesibilă doar intern

    def plaseaza_nava(self, start_x, start_y, dimensiune, directie):
        # Verificăm dacă este rândul computerului; dacă da, returnăm False
        if self.is_computer and self.is_computer_turn:
            return False

        nava = Nava(dimensiune)
        if self.verifica_pozitionare(start_x, start_y, dimensiune, directie):
            nava.pozitioneaza(start_x, start_y, directie)
            self.adauga_nava_pe_harta(nava)
            self.nave.append(nava)
            return True
        return False

    def verifica_pozitionare(self, start_x, start_y, dimensiune, directie):
        try:
            coordonate = []
            if directie == 'dreapta':
                if start_y + dimensiune > 8:
                    return False
                for i in range(dimensiune):
                    coordonate.append((start_x, start_y + i))
            elif directie == 'stanga':
                if start_y - dimensiune < -1:
                    return False
                for i in range(dimensiune):
                    coordonate.append((start_x, start_y - i))
            elif directie == 'jos':
                if start_x + dimensiune > 8:
                    return False
                for i in range(dimensiune):
                    coordonate.append((start_x + i, start_y))
            elif directie == 'sus':
                if start_x - dimensiune < -1:
                    return False
                for i in range(dimensiune):
                    coordonate.append((start_x - i, start_y))

            for (x, y) in coordonate:
                if self.harta[x][y] != '':
                    return False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.harta[nx][ny] == 'O':
                            return False
            return True
        except IndexError:
            return False

    def adauga_nava_pe_harta(self, nava):
        for (x, y) in nava.coordonate:
            self.harta[x][y] = 'O'

    def ataca(self, x, y, adversar):
        if adversar.harta[x][y] == 'O':
            adversar.harta[x][y] = 'X'
            self.harta_atac[x][y] = 'X'
            return True
        else:
            self.harta_atac[x][y] = '0'
            return False


class JocBattleship:
    def __init__(self):
        self.jucator1 = Jucator("Jucator 1")
        self.jucator2 = Jucator("Computer", is_computer=True)
        self.jucator_activ = self.jucator1
        self.jucator_inactiv = self.jucator2
        self.root = tk.Tk()
        self.root.title("Battleship")

        self.faza = "selectie"
        self.mode_select_window()

    # ca sa poti alege modul de joc
    def mode_select_window(self):
        self.select_frame = tk.Frame(self.root)
        self.select_frame.pack(pady=20)

        self.label_select = tk.Label(self.select_frame, text="Selectează modul de joc:")
        self.label_select.pack(pady=10)

        self.button_1vs1 = tk.Button(self.select_frame, text="1 vs 1", command=self.start_1vs1)
        self.button_1vs1.pack(side=tk.LEFT, padx=10)

        self.button_1vs_computer = tk.Button(self.select_frame, text="1 vs Computer", command=self.start_1vs_computer)
        self.button_1vs_computer.pack(side=tk.LEFT, padx=10)

#pt 1vs1
    # pt 1vs1
    def start_1vs1(self):
        self.select_frame.destroy()
        self.setup_game()

    # pt 1vscomputer
    def start_1vs_computer(self):
        self.select_frame.destroy()
        self.setup_game_computer()

    # aici urmeaza implementarea 1vscomputer
    def setup_game_computer(self):
        self.plaseaza_nave_aleatoriu(self.jucator2)
        self.setup_game()
        # Dezactivăm intrările de date în timpul plasării navelor computerului
        self.entry_coord.config(state="disabled")
        self.entry_orientare.config(state="disabled")
        self.button_plaseaza.config(state="disabled")

    def plaseaza_nave_aleatoriu(self, jucator):
        for dimensiune in [2, 3, 4]:
            while True:
                start_x = random.randint(0, 7)
                start_y = random.randint(0, 7)
                directie = random.choice(['sus', 'jos', 'stanga', 'dreapta'])
                if jucator.plaseaza_nava(start_x, start_y, dimensiune, directie):
                    break
                else:
                    continue

    def setup_game(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.faza = "plasare"
        self.nave_de_plasat = [2, 3, 4]
        self.nume_nave = {2: "submarin", 3: "fregată", 4: "distrugător"}

        self.placare_frame = tk.Frame(self.root)
        self.placare_frame.pack()

        self.label_coord = tk.Label(self.placare_frame, text="Introduceți coordonatele (ex. A1):")
        self.label_coord.grid(row=0, column=0)
        self.entry_coord = tk.Entry(self.placare_frame)
        self.entry_coord.grid(row=0, column=1)

        self.label_orientare = tk.Label(self.placare_frame, text="Introduceți orientarea (A/B/R/L):")
        self.label_orientare.grid(row=1, column=0)
        self.entry_orientare = tk.Entry(self.placare_frame)
        self.entry_orientare.grid(row=1, column=1)

        self.button_plaseaza = tk.Button(self.placare_frame, text="Plasează nava", command=self.plaseaza_nava)
        self.button_plaseaza.grid(row=2, column=0)

        # Butonul de renuntare
        self.button_renunta = tk.Button(self.placare_frame, text="Renuntare", command=self.renunta)
        self.button_renunta.grid(row=2, column=1)

        self.mesaj_label = tk.Label(self.root, text="")
        self.mesaj_label.pack()

        self.nava_label = tk.Label(self.root, text="")
        self.nava_label.pack()

        self.actualizeaza_mesaj()

        # Butonul de ajutor
        self.help_button = tk.Button(self.root, text="HELP", command=self.show_help)
        self.help_button.pack()

        self.afisare_harta(self.jucator_activ)

    def plaseaza_nava(self):
        coord_text = self.entry_coord.get().upper()
        orientare_text = self.entry_orientare.get().upper()

        if len(coord_text) < 2 or orientare_text not in ['A', 'B', 'R', 'L']:
            self.mesaj_label.config(text="Coordonate sau orientare invalidă!")
            return

        try:
            start_y = ord(coord_text[0]) - ord('A')
            start_x = int(coord_text[1:]) - 1
        except ValueError:
            self.mesaj_label.config(text="Coordonate invalide!")
            return

        if not (0 <= start_x < 8 and 0 <= start_y < 8):
            self.mesaj_label.config(text="Coordonatele sunt în afara grilei!")
            return

        if self.nave_de_plasat:
            dimensiune = self.nave_de_plasat[0]
            directie = {
                'A': 'sus',
                'B': 'jos',
                'R': 'dreapta',
                'L': 'stanga'
            }.get(orientare_text, 'dreapta')

            succes = self.jucator_activ.plaseaza_nava(start_x, start_y, dimensiune, directie)
            if succes:
                self.nave_de_plasat.pop(0)
                self.actualizeaza_mesaj()
                self.afisare_harta(self.jucator_activ)
                if not self.nave_de_plasat:
                    if self.jucator_activ == self.jucator1:
                        self.mesaj_label.config(text="Randul jucătorului 2")
                        self.afiseaza_fereastra_randul_jucatorului_2()
                    else:
                        self.faza = "atac"
                        self.placare_frame.pack_forget()
                        self.creeaza_interfata_atac()
            else:
                self.mesaj_label.config(text="Pozitionare invalidă!")

    # Pentru a afișa fereastra de schimbare a jucătorului
    def afiseaza_fereastra_randul_jucatorului_2(self):
        self.fereastra_randul2 = tk.Toplevel(self.root)
        self.fereastra_randul2.title("Schimbare jucător")
        mesaj = tk.Label(self.fereastra_randul2, text="Randul jucătorului 2", font=("Arial", 16))
        mesaj.pack(padx=20, pady=20)
        button_ok = tk.Button(self.fereastra_randul2, text="OK", command=self.treci_la_jucatorul_2)
        button_ok.pack(pady=10)

    def treci_la_jucatorul_2(self):
        self.jucator_activ, self.jucator_inactiv = self.jucator_inactiv, self.jucator_activ
        self.nave_de_plasat = [2, 3, 4]
        self.actualizeaza_mesaj()
        self.afisare_harta(self.jucator_activ)
        self.fereastra_randul2.destroy()

    def creeaza_interfata_atac(self):
        self.atac_frame = tk.Frame(self.root)
        self.atac_frame.pack()

        self.label_pozitie = tk.Label(self.atac_frame, text="Introduceți poziția pentru atac (ex. A1):")
        self.label_pozitie.grid(row=0, column=0)
        self.entry_pozitie = tk.Entry(self.atac_frame)
        self.entry_pozitie.grid(row=0, column=1)

        self.button_ataca = tk.Button(self.atac_frame, text="Atacă", command=self.ataca)
        self.button_ataca.grid(row=1, column=0, columnspan=2)

        # Verificăm dacă este rândul jucătorului uman sau al computerului
        if self.jucator_activ == self.jucator2:
            # Dezactivăm intrările de date pentru rândul computerului
            self.entry_pozitie.config(state="disabled")
            self.button_ataca.config(state="disabled")
        else:
            # Activăm intrările de date pentru jucătorul uman
            self.entry_pozitie.config(state="normal")
            self.button_ataca.config(state="normal")

    def afisare_harta(self, jucator):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                             fill="white")
                if jucator.harta[i][j] == 'O':
                    culoare = "blue" if jucator == self.jucator1 else "red"
                    self.canvas.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                                 fill=culoare)
                elif jucator.harta[i][j] == 'X':
                    self.canvas.create_text(j * 50 + 75, i * 50 + 75, text="X", fill="black", font=("Arial", 24))
                elif jucator.harta[i][j] == '0':
                    self.canvas.create_text(j * 50 + 75, i * 50 + 75, text="0", fill="black", font=("Arial", 24))

        for i in range(8):
            self.canvas.create_text(25, i * 50 + 75, text=str(i + 1))
            self.canvas.create_text(i * 50 + 75, 25, text=chr(65 + i))

    def actualizeaza_mesaj(self):
        if self.nave_de_plasat:
            dimensiune = self.nave_de_plasat[0]
            nume_nava = self.nume_nave[dimensiune]
            self.nava_label.config(text=f"{self.jucator_activ.nume} selectează {nume_nava} ({dimensiune} pătrate).")

    def renunta(self):
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajutor")
        help_label = tk.Label(help_window,
                              text="Above(A)-scrii litera A\nBelow(B)-scrii litera B\nRight(R)-scrii litera R\nLeft(L)-scrii litera L\n")
        help_label.pack()

    def ataca(self):
        pozitie_text = self.entry_pozitie.get().upper()

        if len(pozitie_text) < 2:
            self.mesaj_label.config(text="Poziție invalidă!")
            return

        try:
            y = ord(pozitie_text[0]) - ord('A')
            x = int(pozitie_text[1:]) - 1
        except ValueError:
            self.mesaj_label.config(text="Poziție invalidă!")
            return

        if not (0 <= x < 8 and 0 <= y < 8):
            self.mesaj_label.config(text="Poziția este în afara grilei!")
            return

        self.fereastra_atac(x, y)

    def fereastra_atac(self, x, y):
        fereastra = tk.Toplevel(self.root)
        fereastra.title(f"{self.jucator_activ.nume} - Atac")

        canvas_atac = tk.Canvas(fereastra, width=500, height=500)
        canvas_atac.pack()

        hit = self.jucator_activ.ataca(x, y, self.jucator_inactiv)

        for i in range(8):
            for j in range(8):
                canvas_atac.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                             fill="white")
                if self.jucator_activ.harta_atac[i][j] == 'X':
                    canvas_atac.create_text(j * 50 + 75, i * 50 + 75, text="X", fill="black", font=("Arial", 24))
                elif self.jucator_activ.harta_atac[i][j] == '0':
                    canvas_atac.create_text(j * 50 + 75, i * 50 + 75, text="0", fill="black", font=("Arial", 24))
                elif hit and i == x and j == y:
                    canvas_atac.create_text(j * 50 + 75, i * 50 + 75, text="X", fill="black", font=("Arial", 24))
                elif not hit and i == x and j == y:
                    canvas_atac.create_text(j * 50 + 75, i * 50 + 75, text="0", fill="black", font=("Arial", 24))
                    if hit:
                        tk.Label(fereastra, text=f"{self.jucator_activ.nume} a lovit o navă!",
                                 font=("Arial", 16)).pack()
                    else:
                        tk.Label(fereastra, text=f"{self.jucator_activ.nume} a ratat!", font=("Arial", 16)).pack()

                    self.fereastra_atribuie_atac()

    def fereastra_atribuie_atac(self):
        fereastra_2 = tk.Toplevel(self.root)
        fereastra_2.title(f"Schimbare jucător")

        if self.jucator_activ == self.jucator1:
            tk.Label(fereastra_2, text="Randul jucătorului 2", font=("Arial", 16)).pack(padx=20, pady=20)
        else:
            tk.Label(fereastra_2, text="Randul jucătorului 1", font=("Arial", 16)).pack(padx=20, pady=20)

        button_ok = tk.Button(fereastra_2, text="OK", command=self.treci_la_jucatorul_atac)
        button_ok.pack(pady=10)

    def treci_la_jucatorul_atac(self):
        self.jucator_activ, self.jucator_inactiv = self.jucator_inactiv, self.jucator_activ
        self.root.quit()
        self.root.withdraw()
        self.start()
joc = JocBattleship()
joc.start()
