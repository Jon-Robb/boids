# Boids

## Pour tous les pushs, à la fin du titre, [INITIALES PILOTE - INITIALES COPILOTES]


##  Requis ###
    - Frame principal
    - Zone de simulation (image)
    - Zone de contrôle (gauche):
                                  - Zone de contrôle
                                  - Zone de paramétrisation
                                  - Zone de paramètres visuels 
                                  
    - La zone de l'image doit avoir : - width
                                      - height
                                      - draw()
                                      - tick()
                                      
    - Éléments de simulations : - Items (cercles -> tout est un cercle, peu importe ce qu'on ajoute à l'interface graphique doit être un cercle)
                                                 -> items doivent avoir : - position
                                                                          - couleur
                                                                          - rayon
                                                                          - draw()
                                                                          - tick()
                                                  -> les items sont soit : - statiques (obstacles, ...)
                                                                           - dynamiques : - vitesse
                                                                                          - vitesse max
                                                                            - Les items dynamiques peuvent être pilotés : - acceleration
                                                                                                                          - distance de ralentissement
                                                                                                                          - force de pilotage 
                                                                                                                          - stratégies de pilotage  
                                                                                                              
                                - Le monde lui-mpeme n'est pas un cercle
