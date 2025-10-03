def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open(file_path, encoding='utf-8' ) as f:
            libri = {}
            chiave = ['titolo', 'autore', 'anno', 'pagine', 'sezione']

            for i, line in enumerate(f):
                line = line.strip()
                field = line.split(',')
                if i == 0:
                    num_sezioni = int(field[0])
                else:
                    if len(field) == len(chiave):
                        diz = dict(zip(chiave,field))
                        libri[i] = diz
                    else:
                        continue
            return libri, num_sezioni
    except FileNotFoundError:
        print('None')
        return None


def aggiungi_libro(libri, num_sezioni, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    #controllo che il libro non sia già presente
    for libro in libri.values():
    #.values() perchè sto iterando sui valori non sulle chiavi
        if libro['titolo'] == titolo:
            print('Errore: libro già esistente')
            return None
    #controllo che la sezione sia presente
    if sezione > num_sezioni:
        print('Errore: Sezione non valida')
        return None

    #dopo aver superato i controlli
    #sovrascrivo nel file della biblioteca
    try:
        file = open(file_path, 'a', encoding='utf-8')
        file.write(titolo + ',' + autore + ','+str(anno) + ',' + str(pagine) + ',' + str(sezione) + '\n' )
        file.close()

        # se il file è stato sovrascritto posso aggiungere il libro al diz
        chiave = ['titolo', 'autore', 'anno', 'pagine', 'sezione']
        diz = dict(zip(chiave, [titolo, autore, anno, pagine, sezione]))
        indice = len(libri) + 1
        libri[indice] = diz

        return libri

    except FileNotFoundError:
        print('Errore: File non trovato')
        return None



def cerca_libro(libri, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    for libro in libri.values():
        if libro['titolo'] == titolo:
            risultato = f"{libro['titolo']}, {libro['autore']}, {libro['anno']}, {libro['pagine']}, {libro['sezione']}"
            return risultato
        else:
            return None


def elenco_libri_sezione_per_titolo(libri, num_sezioni,  sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    libri_per_sezione = []
    sezioni = []
    if 0 < int(sezione) <= int(num_sezioni) :
    #controllo che la sezione sia valida
        for libro in libri.values():
            if int(libro['sezione']) == int(sezione):
                libri_per_sezione.append(libro['titolo'])
            # i libri della stessa sezione vengono 'appesi' in una lista
    else:
        print('Errore: Sezione non valida')
        return None
    ordinati = sorted(libri_per_sezione)
    #print(ordinati)

    return ordinati


def main():
    biblioteca = {}
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca, num_sezioni = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, num_sezioni, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, num_sezioni, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()

