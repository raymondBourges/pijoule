## Pinces
* <del>s'inspirer de pince.py et rusb.py pour écrire en base les données lues sur le port USB en provenance du RP2040
* faire un sh de lancement prenant en paramètre le port USB à utiliser
  * le mettre en start auto avec du log
* <del>supprimer pince*
* adapter le fastapi pour afficher les données en base
* installer prometheus et le brancher sur fastapi

## TIC
* Faire le paralèlle pour la lecture de la TIC

## DOC
* Faire une doc expliquant l'ensemble
  * expliquer que c'est une adaptation de https://docs.openenergymonitor.org/electricity-monitoring/index.html mais avec un RP2040 via USB + boitier TIC en USB également
  * pi
  * RP2040 (avec adaptation en python de https://github.com/openenergymonitor/EmonLib/blob/master/EmonLib.cpp)
  * montage et calibrage