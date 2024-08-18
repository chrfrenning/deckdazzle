import subprocess
import sys

topics = [
    "HVORDAN TEMME KI?",
    "1,5-GRADERSMÅLET ER TAPT. HVA ER PLANEN?",
    "ER TVILLINGTRANSFORMASJON I DET HELE TATT MULIG?",
    "HVA ER BLÅTT KVANTESPRANG?",
    "KRÆSJKURS OM ATOMKRAFT",
    "HVORDAN LYKKES MED HELSEPLATFORMEN I HELE NORGE",
    "HVORDAN DEEPFAKES VIL PÅVIRKE VALGET I 2025",
    "HVORDAN SKAL NORGE BLI EN TALENTMAGNET INNENFOR BÆREKRAFT OG DIGITALISERING?",
    "HVOR GÅR VI MED GENERATIV KI I OFFENTLIG SEKTOR?",
    "SKAL NORSKE SPRÅKMODELLER SNAKKE ALLE DIALEKTER?",
    "SJEFEN ELLER ARBEIDEREN – HVEM ERSTATTES FØRST AV KI?",
    "KAN IT-BUDSJETTER SLANKES MED OZEMPIC?"
]

def run_with_retries(command, retries=2):
    for attempt in range(retries + 1):
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError:
            if attempt < retries:
                print(f"Attempt {attempt + 1} failed. Retrying...")
            else:
                print(f"Attempt {attempt + 1} failed. No more retries.")
                return False

# for each topic, run new.py with the topic as argument
for topic in topics:
    print(f"Running new.py with topic '{topic}'")
    if not run_with_retries(["python", "new.py", topic]):
        sys.exit(1)
    print("\n\n\n")

sys.exit(0)