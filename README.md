# OpenRewrite hors ligne — 24 septembre 2026

## Versions et validation

| Artefact | Version stable vérifiée sur Maven Central | Licence déclarée |
|---|---|---|
| org.openrewrite.maven:rewrite-maven-plugin | 6.46.1 | Apache 2.0 |
| org.openrewrite.recipe:rewrite-spring | 6.37.1 | Moderne Source Available |
| org.openrewrite.recipe:rewrite-migrate-java | 3.42.1 | Moderne Source Available |

La recette `org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0` est présente dans `META-INF/rewrite/spring-boot-40.yml` du JAR ; copie dans `preuves/`.
Les modules `rewrite-java-17`, `rewrite-java-21`, `rewrite-java-25` sont inclus en **8.89.0 et 8.90.2**, ainsi que leurs dépendances. Ces versions différentes proviennent des graphes du plugin et des recettes ; ne pas les supprimer.

Tests : macOS 27 arm64, Maven **3.9.15 / JDK 17.0.18, 21.0.10, 25.0.2**, puis Maven **3.9.9 / JDK 17 et 25**. Les deux `dryRun` réussissent avec `-o`, sans cache POM OpenRewrite, et sans marqueur d'erreur dans les patches. Projet : Boot **3.5.0**, Java 17, web + JPA + Jackson, avec source Java compilée. Le patch Spring migre le parent vers **4.0.8**, le starter web vers `webmvc` et les imports vers Jackson 3 ; le patch Java passe `java.version` à **25**.

Archive : **361,640,969 octets (361.64 Mo / 344.89 Mio)**. Après extraction dans un nouveau dépôt, les deux `dryRun`, les deux `run` successifs et le build final Boot 4 / Java 25 réussissent aussi hors ligne. Voir `preuves/verification.md`.

## Import sans écrasement

Le ZIP contient directement les dossiers `org/`, `com/`, etc. Sa destination est **`~/.m2/repository`**, pas `~/.m2` et pas `~/.m2/repository/rewrite-repo`.

Depuis ce dossier, Python 3.10+ (Linux/macOS) :

```sh
python3 import-repo.py --destination "$HOME/.m2/repository"
```

Windows PowerShell :

```powershell
py -3 import-repo.py --destination "$HOME/.m2/repository"
```

Le script ajoute les fichiers absents et conserve tous les fichiers existants. Il signale les différences. Avec un décompresseur, choisir « ignorer les fichiers existants », jamais remplacer le dépôt entier. Sous Linux/macOS : `unzip -n rewrite-repo.zip -d "$HOME/.m2/repository"`.

**Reproductibilité :** si des fichiers ou métadonnées déjà présents diffèrent, utiliser un dépôt neuf (`python3 import-repo.py --destination ./rewrite-repo`) et pointer `-Dmaven.repo.local` dessus. Les métadonnées locales embarquées sont nécessaires aux sélecteurs `4.0.x` / `3.x` des recettes ; elles ne doivent pas être omises. Elles représentent un instantané de Central, pas la promesse que toutes les versions qu'elles listent sont incluses.

`_remote.repositories`, fichiers de verrouillage et échecs `.lastUpdated` ne sont pas archivés : les artefacts importés ne sont ainsi pas liés à l'identifiant de dépôt `central` face au miroir Artifactory. POM, JAR et sommes de contrôle d'origine sont conservés. `SHA256SUMS` permet de contrôler le ZIP.

## Commandes exactes dans le projet à migrer

Garder `settings.xml` fourni (`<settings/>`) dans un emplacement accessible. Il neutralise aussi les réglages globaux avec `-gs`. Définir les chemins absolus, puis se placer à la racine du projet.

Linux/macOS :

```sh
SETTINGS="/chemin/absolu/livrable/settings.xml"
REPO="$HOME/.m2/repository"
export JAVA_HOME="/chemin/vers/jdk-25"
export PATH="$JAVA_HOME/bin:$PATH"
mvn -version
```

Windows PowerShell :

```powershell
$SETTINGS = "C:/chemin/livrable/settings.xml"
$REPO = "$HOME/.m2/repository"
$env:JAVA_HOME = "C:/chemin/jdk-25"
$env:Path = "$env:JAVA_HOME/bin;$env:Path"
mvn -version
```

Les lignes suivantes fonctionnent dans les deux shells. Utiliser un JDK 25 pour toute la séquence : après modification de `java.version`, Maven doit pouvoir compiler en 25. Faire d'abord le `dryRun`, examiner `target/rewrite/rewrite.patch`, puis exécuter le `run` correspondant.

### Spring Boot 4

```sh
mvn -o -s "$SETTINGS" -gs "$SETTINGS" "-Dmaven.repo.local=$REPO" org.openrewrite.maven:rewrite-maven-plugin:6.46.1:dryRun -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:6.37.1 -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0 -Drewrite.exportDatatables=true -Drewrite.pomCacheEnabled=false
mvn -o -s "$SETTINGS" -gs "$SETTINGS" "-Dmaven.repo.local=$REPO" org.openrewrite.maven:rewrite-maven-plugin:6.46.1:run -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:6.37.1 -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0 -Drewrite.exportDatatables=true -Drewrite.pomCacheEnabled=false
```

### Java 25

```sh
mvn -o -s "$SETTINGS" -gs "$SETTINGS" "-Dmaven.repo.local=$REPO" org.openrewrite.maven:rewrite-maven-plugin:6.46.1:dryRun -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:3.42.1 -Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava25 -Drewrite.exportDatatables=true -Drewrite.pomCacheEnabled=false
mvn -o -s "$SETTINGS" -gs "$SETTINGS" "-Dmaven.repo.local=$REPO" org.openrewrite.maven:rewrite-maven-plugin:6.46.1:run -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:3.42.1 -Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava25 -Drewrite.exportDatatables=true -Drewrite.pomCacheEnabled=false
```

Les datatables sont sous `target/rewrite/datatables/` (répertoire courant). `dryRun` ne modifie pas les sources ; `run` les modifie. Examiner le diff Git avant de conserver la migration.

## Préparation réalisée

Dépôt initialement vide, settings utilisateur **et globaux** vides. Pour chacun des trois GAV du tableau :

```sh
mvn -B -ntp -s settings.xml -gs settings.xml -Dmaven.repo.local=./rewrite-repo org.apache.maven.plugins:maven-dependency-plugin:3.11.0:get -Dartifact=org.openrewrite.maven:rewrite-maven-plugin:6.46.1 -Dtransitive=true
mvn -B -ntp -s settings.xml -gs settings.xml -Dmaven.repo.local=./rewrite-repo org.apache.maven.plugins:maven-dependency-plugin:3.11.0:get -Dartifact=org.openrewrite.recipe:rewrite-spring:6.37.1 -Dtransitive=true
mvn -B -ntp -s settings.xml -gs settings.xml -Dmaven.repo.local=./rewrite-repo org.apache.maven.plugins:maven-dependency-plugin:3.11.0:get -Dartifact=org.openrewrite.recipe:rewrite-migrate-java:3.42.1 -Dtransitive=true
```

Puis build `package` en ligne du projet fourni dans le même dépôt ; ajout des métadonnées Central et des dépendances cibles/intermédiaires Boot 3.5.16, Boot 4.0.8, Jackson 3.1.7. Les premiers essais ont révélé des erreurs de résolution malgré `BUILD SUCCESS` ; les tests finaux vérifient aussi les patches et datatables. Journaux et patches finaux : `preuves/`.

## Limites à connaître

- **Projet réel :** ce ZIP couvre les deux recettes et le projet témoin, pas les dépendances propres à tout projet d'entreprise. Précharger votre projet, ses parents, extensions, plugins et profils avec votre configuration Artifactory habituelle avant le passage hors ligne. Toute branche supplémentaire des recettes peut demander d'autres artefacts cibles.
- **Hors ligne :** `-o` désactive les téléchargements Maven ; le résolveur interne OpenRewrite peut encore tenter des accès HTTP. Les tests finaux ont réussi avec le réseau bloqué par le sandbox et `rewrite.pomCacheEnabled=false`. Pour garantir zéro tentative réseau, bloquer également le réseau au niveau OS. Le bundle ne dépend pas d'un cache `~/.rewrite-cache` préexistant.
- **Maven :** 3.9.9 et 3.9.15 testés. La version exacte de votre poste était un placeholder : aucune autre version n'est certifiée. Le descripteur du plugin indique Maven >= 3.3.1, mais son build utilise >= 3.9.6 ; le projet Boot 4 impose ses propres contraintes. Préférer Maven 3.9.9 ou plus récent. Les JDK sont à installer séparément.
- **Systèmes :** tests exécutés sur macOS arm64 seulement ; Windows/Linux non exécutés. Les JAR conservent leurs ressources natives. Le cache RocksDB est désactivé dans les commandes fournies pour éviter une dépendance à son état ou à ses bibliothèques natives.
- **Licences :** les recettes Spring et Java sont sous [Moderne Source Available](https://docs.moderne.io/licensing/moderne-source-available-license/), distincte d'Apache 2.0. Vérification interne recommandée selon l'usage prévu. Les tiers ont aussi des licences MIT/BSD/EPL/LGPL/CDDL, etc. Voir l'inventaire : ne pas attribuer Apache 2.0 à tout le dépôt. Six anciens POM auxiliaires n'ont pas de licence identifiée dans leurs POM/parents ; ils sont explicitement marqués à vérifier.
- **Provenance :** tous les artefacts téléchargés proviennent de [Maven Central](https://repo.maven.apache.org/maven2/), aucune dépendance hors Central requise pour les tests. Des POM mentionnent d'autres dépôts ou des distributions/snapshots ; cette mention n'implique pas un téléchargement depuis ceux-ci. Les trois artefacts principaux sont stables ; certains POM auxiliaires transitifs portent des versions beta/RC.

Sources des versions : [plugin Maven](https://repo.maven.apache.org/maven2/org/openrewrite/maven/rewrite-maven-plugin/maven-metadata.xml), [rewrite-spring](https://repo.maven.apache.org/maven2/org/openrewrite/recipe/rewrite-spring/maven-metadata.xml), [rewrite-migrate-java](https://repo.maven.apache.org/maven2/org/openrewrite/recipe/rewrite-migrate-java/maven-metadata.xml). Copies de ces métadonnées dans `preuves/`.

## Téléchargement GitHub

Télécharger `rewrite-repo.zip` depuis la [Release v2026-09-24](https://github.com/rachiddaoud/openrewrite-offline-springboot4-java25/releases/tag/v2026-09-24), puis le placer à côté de `import-repo.py`.
