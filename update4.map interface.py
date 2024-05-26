import tkinter as tk
from PIL import Image, ImageTk


class Nava:
    def __init__(self, dimensiune):
        self.coordonate = None
        self.dimensiune = dimensiune
        self.forma = [['O' for _ in range(dimensiune)]]

    def pozitioneaza(self, start_x, start_y, orientare):
        self.coordonate = []
        if orientare == 'orizontal':
            for i in range(self.dimensiune):
                self.coordonate.append((start_x, start_y + i))
        else:
            for i in range(self.dimensiune):
                self.coordonate.append((start_x + i, start_y))


class Jucator:
    def __init__(self, nume):
        self.nume = nume
        self.nave = []
        self.harta = [['' for _ in range(8)] for _ in range(8)]

    def plaseaza_nava(self, start_x, start_y, dimensiune, orientare):
        nava = Nava(dimensiune)
        if self.verifica_pozitionare(start_x, start_y, dimensiune, orientare):
            nava.pozitioneaza(start_x, start_y, orientare)
            self.adauga_nava_pe_harta(nava)
            self.nave.append(nava)
            return True
        return False

    def verifica_pozitionare(self, start_x, start_y, dimensiune, orientare):
        if orientare == 'orizontal':
            if start_y + dimensiune > 8:
                return False
            for i in range(dimensiune):
                if self.harta[start_x][start_y + i] != '':
                    return False
        else:
            if start_x + dimensiune > 8:
                return False
            for i in range(dimensiune):
                if self.harta[start_x + i][start_y] != '':
                    return False
        return True

    def adauga_nava_pe_harta(self, nava):
        for (x, y) in nava.coordonate:
            self.harta[x][y] = 'O'


class JocBattleship:
    def __init__(self):
        self.ocean_photo = None
        self.image_label = None
        self.photo = None
        self.jucator1 = Jucator("Jucator 1")
        self.jucator2 = Jucator("Jucator 2")
        self.jucator_activ = self.jucator1
        self.jucator_inactiv = self.jucator2
        self.root = tk.Tk()
        self.root.title("Battleship")

        # Creează frame-ul principal care conține atât canvas-ul cât și imaginea
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # Canvas pentru grid-ul de joc
        self.canvas = tk.Canvas(self.main_frame, width=500, height=500)
        self.canvas.pack(side="left")

        # Imaginea pentru secțiunea de imagine
        self.image_frame = tk.Frame(self.main_frame, width=200, height=500)
        self.image_frame.pack(side="right")

        # Încarcă imaginea și o convertește în PhotoImage
        self.load_image()

        self.afisare_imagine()

        self.canvas.bind("<Button-1>", self.click)

        self.faza = "plasare"
        self.nave_de_plasat = [2, 3, 4]
        self.nume_nave = {2: "submarin", 3: "fregată", 4: "distrugător"}

        # Interfața de plasare a navelor
        self.placare_frame = tk.Frame(self.root)
        self.placare_frame.pack()

        self.label_coord = tk.Label(self.placare_frame, text="Introduceți coordonatele (ex. A1):")
        self.label_coord.grid(row=0, column=0)
        self.entry_coord = tk.Entry(self.placare_frame)
        self.entry_coord.grid(row=0, column=1)

        self.label_orientare = tk.Label(self.placare_frame, text="Introduceți orientarea (H/V):")
        self.label_orientare.grid(row=1, column=0)
        self.entry_orientare = tk.Entry(self.placare_frame)
        self.entry_orientare.grid(row=1, column=1)

        self.button_plaseaza = tk.Button(self.placare_frame, text="Plasează nava", command=self.plaseaza_nava)
        self.button_plaseaza.grid(row=2, column=0, columnspan=2)

        self.mesaj_label = tk.Label(self.root, text="")
        self.mesaj_label.pack()

        self.nava_label = tk.Label(self.root, text="")
        self.nava_label.pack()

        self.actualizeaza_mesaj()

        self.afisare_harta(self.jucator_activ)

    def click(self, event):
        x, y = event.x // 50, event.y // 50
        if 0 <= x < 8 and 0 <= y < 8:
            if self.faza == "atac":
                print(f"Jucatorul {self.jucator_activ.nume} a selectat poziția {x}, {y}")
                # Cod pentru atacul pe harta adversarului
                self.afisare_harta(self.jucator_activ)

    def plaseaza_nava(self):
        coord_text = self.entry_coord.get().upper()
        orientare_text = self.entry_orientare.get().upper()

        if len(coord_text) < 2 or orientare_text not in ['H', 'V']:
            print("Coordonate sau orientare invalidă!")
            return

        try:
            start_y = ord(coord_text[0]) - ord('A')
            start_x = int(coord_text[1:]) - 1
        except ValueError:
            print("Coordonate invalide!")
            return

        if not (0 <= start_x < 8 and 0 <= start_y < 8):
            print("Coordonatele sunt în afara grilei!")
            return

        if self.nave_de_plasat:
            dimensiune = self.nave_de_plasat[0]
            orientare = 'orizontal' if orientare_text == 'H' else 'vertical'
            if self.jucator_activ.plaseaza_nava(start_x, start_y, dimensiune, orientare):
                self.nave_de_plasat.pop(0)
                self.afisare_harta(self.jucator_activ)
                self.actualizeaza_mesaj()
                if not self.nave_de_plasat:
                    if self.jucator_activ == self.jucator1:
                        self.jucator_activ = self.jucator2
                        self.jucator_inactiv = self.jucator1
                        self.nave_de_plasat = [2, 3, 4]
                        self.reset_harta()
                        self.mesaj_label.config(text=f"{self.jucator2.nume}, este rândul tău să îți plasezi navele.")
                        print(f"{self.jucator2.nume}, este rândul tău să îți plasezi navele.")
                        self.actualizeaza_mesaj()
                    else:
                        self.faza = "atac"
                        self.jucator_activ = self.jucator1
                        self.jucator_inactiv = self.jucator2
                        self.mesaj_label.config(text="Faza de atac a început!")
                        print("Faza de atac a început!")
                        self.nava_label.config(text="")
            else:
                print("Plasare invalidă! Încercați din nou.")
        else:
            print("Toate navele au fost plasate!")

    def reset_harta(self):
        self.canvas.delete("all")
        # Afișează imaginea de fundal
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.ocean_photo)
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                             outline="white")

        for i in range(8):
            self.canvas.create_text(25, i * 50 + 75, text=str(i + 1), fill="white")
            self.canvas.create_text(i * 50 + 75, 25, text=chr(65 + i), fill="white")

    def afisare_harta(self, jucator):
        self.canvas.delete("all")
        # Afișează imaginea de fundal
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.ocean_photo)
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                             outline="white")
                if jucator.harta[i][j] == 'O':
                    culoare = "darkblue" if jucator == self.jucator1 else "darkred"
                    self.canvas.create_rectangle(j * 50 + 50, i * 50 + 50, (j + 1) * 50 + 50, (i + 1) * 50 + 50,
                                                 fill=culoare)

        for i in range(8):
            self.canvas.create_text(25, i * 50 + 75, text=str(i + 1), fill="white")
            self.canvas.create_text(i * 50 + 75, 25, text=chr(65 + i), fill="white")

    def actualizeaza_mesaj(self):
        if self.nave_de_plasat:
            dimensiune = self.nave_de_plasat[0]
            nume_nava = self.nume_nave[dimensiune]
            self.nava_label.config(text=f"{self.jucator_activ.nume} selectează {nume_nava} ({dimensiune} pătrate).")

    def load_image(self):
        # Încarcă imaginea folosind PIL (Pillow)
        image = Image.open("Radar.png")
        # Redimensionează imaginea pentru a se potrivi cu dimensiunea frame-ului
        image = image.resize((300, 400), Image.LANCZOS)
        # Convertirea imaginii într-un obiect PhotoImage
        self.photo = ImageTk.PhotoImage(image)

        # Încarcă imaginea de fundal pentru ocean
        ocean_image = Image.open("Ocean.png")  # Asigură-te că ai o imagine de fundal cu oceanul denumită "Ocean.png"
        ocean_image = ocean_image.resize((500, 500), Image.LANCZOS)
        self.ocean_photo = ImageTk.PhotoImage(ocean_image)

    def afisare_imagine(self):
        # Adăugarea imaginii pe canvas
        self.canvas.create_image(800, 250, anchor=tk.CENTER, image=self.photo)
        self.image_label = tk.Label(self.image_frame, image=self.photo)
        self.image_label.image = self.photo  # Reține o referință către imagine pentru a preveni garbage collection
        self.image_label.pack()

    def start(self):
        self.root.mainloop()


# Rulează jocul
joc = JocBattleship()
joc.start()
