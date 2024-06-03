#!/bin/bash

# Adresse MAC du périphérique Bluetooth
DEVICE_MAC="D0:DC:74:5C:A6:46"

# UUID de la caractéristique à lire
CHARACTERISTIC_UUID="00002a5b-0000-1000-8000-00805f9b34fb"

# Fichier de sortie pour enregistrer les données
OUTPUT_FILE="donnees_cadence.txt"

# Fonction pour se connecter au périphérique Bluetooth
connect_bluetooth_device() {
    echo -e "power on\nscan on" | bluetoothctl
    echo -e "connect $DEVICE_MAC\n" | bluetoothctl
}

# Fonction pour lire et enregistrer les données
read_and_record_data() {
    while true
    do
        # Lire les données de la caractéristique
        result=$(gatttool -b $DEVICE_MAC --char-read --uuid=$CHARACTERISTIC_UUID 2>/dev/null)
	
	echo "result ?! $result"	
	
        # Vérifier si une donnée a été lue
        if [[ $result =~ "value:" ]]; then
            # Extraire la valeur hexadécimale
            value=$(echo $result | sed -n 's/^.*value: //p')

            # Afficher la valeur lue
            echo "Valeur de la caractéristique : $value"

            # Enregistrer la valeur dans le fichier de sortie avec la date et l'heure actuelles
            echo "$(date +"%Y-%m-%d %H:%M:%S"),$value" >> $OUTPUT_FILE
        fi
        
        # Attendre quelques secondes avant de lire à nouveau les données
        sleep 5
    done
}

# Connecter au périphérique Bluetooth
connect_bluetooth_device
#sleep 5  # Attendre que la connexion soit établie

echo "connected"

# Lire et enregistrer les données
read_and_record_data
