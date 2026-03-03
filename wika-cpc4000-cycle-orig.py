import serial
import time

# --- CONFIGURAZIONE ---
PORTA_SERIALE = 'COM24'   # Sostituisci con la porta COM assegnata al CPC4000
BAUDRATE = 57600         # Baudrate di default del CPC4000
CICLI = 10              # Numero esatto di cicli desiderati
TEMPO_MANTENIMENTO = 1   # Secondi di attesa a pressione stabile

def invia_comando(ser, comando, aspetta_risposta=False):
    """Invia un comando testuale Mensor al CPC4000 e legge la risposta se richiesta"""
    # Aggiunge Carriage Return + Line Feed (CRLF) richiesti dallo strumento
    comando_completo = comando + "\r\n" 
    ser.write(comando_completo.encode('ascii'))
    time.sleep(0.1)
    
    if aspetta_risposta:
        risposta = ser.readline().decode('ascii').strip()
        return risposta
    return None

def attendi_stabilita(ser):
    """Interroga lo strumento finché la pressione non è stabile nel range"""
    stabile = False
    while not stabile:
        risposta = invia_comando(ser, "Stable?", aspetta_risposta=True)
        # Il comando "Stable?" ritorna "YES" quando il setpoint è raggiunto stabilmente
        if risposta and "YES" in risposta.upper():
            stabile = True
        else:
            time.sleep(0.5) # Attende mezzo secondo prima di richiedere lo stato

def main():
    try:
        # Inizializzazione della connessione seriale
        ser = serial.Serial(PORTA_SERIALE, BAUDRATE, timeout=1)
        print(f"Connesso al CPC4000 sulla porta {PORTA_SERIALE}")

        # --- 1. CONFIGURAZIONE INIZIALE DELLO STRUMENTO ---
        print("Impostazione unità in Bar...")
        invia_comando(ser, "Units 14") # Il codice 14 imposta l'unità di misura in Bar
        
        print("Avvio modalità Controllo...")
        invia_comando(ser, "Mode Control") # Attiva l'erogazione
        
        # --- 2. ESECUZIONE DEI CICLI ---
        for i in range(1, CICLI + 1):
            print(f"\n--- Inizio Ciclo {i} di {CICLI} ---")
            
            # Fase di scarico (1 bar)
            print("Imposto pressione a 1 bar. In attesa di stabilità...")
            invia_comando(ser, "Setpt 1")
            attendi_stabilita(ser)
            print(f"Pressione stabile a 1 bar. Mantengo per {TEMPO_MANTENIMENTO} secondi.")
            time.sleep(TEMPO_MANTENIMENTO)

            # Fase di carico (50 bar)
            print("Imposto pressione a 50 bar. In attesa di stabilità...")
            invia_comando(ser, "Setpt 50")
            attendi_stabilita(ser)
            print(f"Pressione stabile a 50 bar. Mantengo per {TEMPO_MANTENIMENTO} secondi.")
            time.sleep(TEMPO_MANTENIMENTO)

        # --- 3. FINE DEL TEST E MESSA IN SICUREZZA ---
        print("\nCicli terminati con successo! Avvio lo sfiato (Vent) dell'impianto...")
        invia_comando(ser, "Mode Vent") # Apre la valvola di sfiato atmosferico

    except Exception as e:
        print(f"Si è verificato un errore di connessione: {e}")
    finally:
        # Assicura che la porta venga chiusa anche in caso di errori
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Porta seriale chiusa.")

if __name__ == '__main__':
    main()
