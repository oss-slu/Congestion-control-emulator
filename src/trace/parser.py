import csv
from dataclasses import dataclass

@dataclass
class packet:
    time : int
    protocol: str
    destination: str
    source: str

def parser_csv(file):
    stored_data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = packet(row["Time"], row["Protocol"], row["Destination"], row["Source"])
            stored_data.append(p)
    return stored_data

def main():
    parser_csv("test.txt")
    
if __name__ == "__main__":
    main()
