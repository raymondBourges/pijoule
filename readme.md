# PiJoule

## Objectif
L’objectif initial était de mesurer des consommations de courants avec un Raspberry Pico ou un Raspberry Pi. Finalement ça c’est transformé en Pico et Pi !

## Matériel
### Pourquoi PICO *et* PI
* Un Pico seul ne me permettait pas d’installer des fonctionnalités de haut niveau, comme un serveur prometheus par ex. 
* Un Pi seul (équipé d'un convertisseur analogique numérique (ADC) communiquant en I2C) ne me permettait pas de lire avec une fréquence suffisante les informations en provenance des pinces ampèremétriques.
### Détail du matériel
* Un [Raspberry Pi 4 Modèle B – 2GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* Un [Seeed Studio XIAO RP2040](https://wiki.seeedstudio.com/XIAO-RP2040/)
  * Il est basé sur un RP2040 comme un Raspberry Pico tout en étant plus petit, et surtout, proposant 4 entrées ADC et pas seulement 3.
* Un [transformateur 230 AC/ 9 AC](https://www.cartelectronic.fr/serveur-wes/126-alimentation-9v-ac-mesure-tension-3760313520097.html)
  * Au final, je suis un peu déçu, car son signal ne semble pas régulier et sa tension de sortie n’est pas de 9V comme annoncé mais de 12V ce qui m’a obligé à revoir mon montage.
* Des pinces ampèremétriques
  * [100A](https://www.cartelectronic.fr/capteurs-1wire-etc/40-pince-amp-100a.html)
  * [30 A](https://www.mouser.fr/ProductDetail/810-CCT2616313006-02)
  * [20 A](https://www.cartelectronic.fr/serveur-wes/137-pince-amp-20a.html)
* Quelques composants pour mesurer l’intensité dans les pinces ampèremétriques et la tension du transformateur
  * Schéma de montage sur le projet [PicoJoule](https://github.com/raymondBourges/picojoule)

## Inspiration
Après pas mal de recherches et tests je me suis finalement très largement inspiré du projet [OpenEnergyMonitor](https://openenergymonitor.org/) qui est très bien documenté. Je vous conseille notamment de lire « [Learn: Electricity Monitoring](https://docs.openenergymonitor.org/electricity-monitoring/index.html) ».
Par contre, contrairement à ce projet :
* Je n’utilise pas le C mais Python
* Pas un arduino mais un RP2040
* Et pour communiqué entre le Pi et le RP2040, j’utilise la liaison USB (qui sert également à l’alimentation du RP2040)

## Schéma de principe
![Schéma de principe](https://onedrive.live.com/embed?resid=65F636FF783E0000%21451&authkey=%21AK-kaD4n0OKI5oE&width=1011&height=651)
* Le (ou les) RP2040 lit les informations fournies par les pinces ampèremétriques et le transformateur
* Le (ou les) programme pince.py lit l’entrée USB et dépose les métriques dans une base sqlite
* FastAPI lit la base afin d’exposer les métriques au format prometheus
* Prometheus collecte et archive ces métriques
* Grafana permet de visualiser ces métriques

## Futur
* Lire les données TIC du compteur électrique
* Lire les impulsions de compteurs d’énergie ou d’eau
