# Vérification finale

- ZIP : 361,640,969 octets ; 361.64 Mo ; 344.89 Mio.
- SHA-256 : ee407a0dff1e5ecc14f7bb34a50069e4730bf6141ff8ae760ebc726c55cd28fc.
- Intégrité ZIP vérifiée ; 1232 POM/JAR contrôlés contre les SHA-1 téléchargés depuis Central : aucune différence.
- Présence des 6 JAR rewrite-java-17/21/25, versions 8.89.0 et 8.90.2 : confirmée.
- Maven 3.9.15 : deux dryRun offline sur JDK 17, 21 et 25, tous BUILD SUCCESS.
- Maven 3.9.9 : deux dryRun offline sur JDK 17 et 25, tous BUILD SUCCESS.
- Patches finaux : aucun marqueur d'erreur ; datatables finales sans table Failures/Errors.
- Archive extraite dans validation-repo neuf : deux dryRun, puis run Spring, run Java et package final sous Maven 3.9.9 / JDK 25 : tous BUILD SUCCESS, sans erreur de téléchargement.
- Cache POM OpenRewrite désactivé, settings utilisateur et globaux vides, dépôt local explicitement désigné. Exécutions finales dans le sandbox sans accès réseau.
- Résultat appliqué : Boot 4.0.8, Java 25, starter webmvc, imports tools.jackson ; code effectivement recompilé en Java 25 (bytecode major 69, vérifié par javap).
- Validation limitée au projet témoin et aux environnements indiqués, aucune certification du projet d'entreprise absent.

Les avertissements JDK 25 sur les API internes de Maven (Unsafe/native access) sont non bloquants dans ces tests. Les journaux sont disponibles dans ce dossier.
