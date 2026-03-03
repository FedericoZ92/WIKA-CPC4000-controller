import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import messagebox

# --- DEFAULT VALUES ---
def detect_com_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        try:
            ser = serial.Serial(port.device, 57600, timeout=10)
            ser.write(b"Units?\r\n")
            time.sleep(0.2)
            response = ser.readline().decode(errors="ignore").strip()
            ser.close()
            if response and ("WIKA" in response.upper() or "CPC4000" in response.upper()):  # Adjust this check based on the actual response from the device
                return port.device
        except Exception:
            continue
    return ports[0].device if ports else "COM1"  # fallback if none found

DEFAULTS = {
    "PORTA_SERIALE": detect_com_port(),
    "BAUDRATE": 57600,
    "CICLI": 100,
    "TEMPO_MANTENIMENTO": 1,
    "TARGET_A": 0.1,
    "TARGET_B": 10
}

def invia_comando(ser, comando, aspetta_risposta=False):
    comando_completo = comando + "\r\n"
    ser.write(comando_completo.encode('ascii'))
    time.sleep(0.1)
    
    if aspetta_risposta:
        risposta = ser.readline().decode('ascii').strip()
        return risposta
    return None

def attendi_stabilita(ser, max_wait_seconds=300):
    stabile = False
    start_time = time.time()
    while not stabile:
        risposta = invia_comando(ser, "Stable?", aspetta_risposta=True)
        print(f"[DEBUG] attendi_stabilita: risposta='{risposta}'")
        if risposta and "YES" in risposta.upper():
            stabile = True
        else:
            if time.time() - start_time > max_wait_seconds:
                print(f"[DEBUG] Timeout: attesa stabilita superata ({max_wait_seconds} secondi)")
                break
            time.sleep(2)

def esegui_test(params):
    try:
        ser = serial.Serial(params["PORTA_SERIALE"], int(params["BAUDRATE"]), timeout=10)
        print(f"Connesso al CPC4000 sulla porta {params['PORTA_SERIALE']}")

        print("Impostazione unità in Bar...")
        invia_comando(ser, "Units 14")

        print("Avvio modalità Controllo...")
        invia_comando(ser, "Mode Control")

        for i in range(1, int(params["CICLI"]) + 1):
            print(f"\n--- Inizio Ciclo {i} di {params['CICLI']} ---")


            print(f"Imposto pressione a {params['TARGET_A']} bar...")
            risposta_a = invia_comando(ser, f"Setpt {params['TARGET_A']}", aspetta_risposta=True)
            if not risposta_a:
                print(f"[WARNING] Nessuna risposta a Setpt {params['TARGET_A']}")
            else:
                print(f"[DEBUG] Risposta a Setpt {params['TARGET_A']}: {risposta_a}")
            attendi_stabilita(ser)
            time.sleep(float(params["TEMPO_MANTENIMENTO"]))


            print(f"Imposto pressione a {params['TARGET_B']} bar...")
            risposta_b = invia_comando(ser, f"Setpt {params['TARGET_B']}", aspetta_risposta=True)
            if not risposta_b:
                print(f"[WARNING] Nessuna risposta a Setpt {params['TARGET_B']}")
            else:
                print(f"[DEBUG] Risposta a Setpt {params['TARGET_B']}: {risposta_b}")
            attendi_stabilita(ser)
            time.sleep(float(params["TEMPO_MANTENIMENTO"]))

        print("\nCicli terminati! Avvio Vent...")
        invia_comando(ser, "Mode Vent")

    except Exception as e:
        messagebox.showerror("Errore", f"Errore di connessione:\n{e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Porta seriale chiusa.")

def avvia_con_parametri():
    try:
        params = {key: entries[key].get() for key in entries}
        root.destroy()
        esegui_test(params)
    except ValueError:
        messagebox.showerror("Errore", "Controlla i valori inseriti.")

# --- GUI ---
root = tk.Tk()
root.title("Configurazione Test CPC4000")

entries = {}

row = 0
for key, value in DEFAULTS.items():
    tk.Label(root, text=key).grid(row=row, column=0, padx=5, pady=5, sticky="w")
    entry = tk.Entry(root)
    entry.insert(0, str(value))
    entry.grid(row=row, column=1, padx=5, pady=5)
    entries[key] = entry
    row += 1

tk.Button(root, text="Avvia Test", command=avvia_con_parametri).grid(row=row, columnspan=2, pady=10)

root.mainloop()