# OpenRewrite hors ligne — `UpgradeSpringBoot_4_0` (5 octobre 2026)

Dépôt Maven local contenant tout le nécessaire pour exécuter la recette
`org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0` sans accès à Maven Central.

## Versions exactes

| Artefact | Version |
|---|---|
| `org.openrewrite.maven:rewrite-maven-plugin` | **6.46.1** |
| `org.openrewrite.recipe:rewrite-spring` | **6.37.0** |
| `org.openrewrite.recipe:rewrite-recipe-bom` (source des versions) | 3.37.0 |
| Projet témoin : Spring Boot avant → après | 3.5.16 → **4.0.8** (Java 21) |

Choix des versions : le dernier BOM publié sur Central, **3.38.0** (26/08/2026), référence
`rewrite-spring:6.38.0`, `rewrite-maven-plugin:6.47.0` et `rewrite-bom:8.91.0`, **qui n'existent pas
sur Central (404)** — il est donc inutilisable. Le BOM précédent, **3.37.0** (12/08/2026), est cohérent :
`rewrite-spring 6.37.0` et `rewrite-maven-plugin 6.46.1` ont été publiés le même jour.
La recette est bien présente dans `META-INF/rewrite/spring-boot-40.yml` du JAR `rewrite-spring-6.37.0`.

## Contenu

| Chemin | Rôle |
|---|---|
| `dist/m2repo-rewrite-spring-6.37.0.tar.gz.part-00..03` | Archive du dépôt Maven (325 Mo), découpée en 4 parties (limite GitHub de 100 Mo/fichier) |
| `dist/m2repo-rewrite-spring-6.37.0.tar.gz.sha256` | SHA-256 de l'archive réassemblée |
| `sample/` | Projet témoin Boot 3.5.16 d'origine (`@RestController`, `@Entity`, repository JPA, tests `@WebMvcTest`/`@MockBean` et `@SpringBootTest`/`TestRestTemplate`) |
| `preuves/` | Journaux des exécutions online/offline, diff de migration, pom migré |

L'archive contient directement `org/`, `com/`, `io/`… (racine = racine du dépôt local). Les fichiers
`_remote.repositories`, `*.lastUpdated` et `resolver-status.properties` ont été supprimés : Maven
n'associe donc pas les artefacts au dépôt `central` et les accepte derrière un autre miroir.

## Installation

**Méthode recommandée** : télécharger l'archive unique depuis la Release
[`offline-boot4-rewrite-spring-6.37.0`](https://github.com/rachiddaoud/openrewrite-offline-springboot4-java25/releases/tag/offline-boot4-rewrite-spring-6.37.0)
(`m2repo-rewrite-spring-6.37.0.tar.gz` + `.sha256`), puis :

```sh
sha256sum -c m2repo-rewrite-spring-6.37.0.tar.gz.sha256
# attendu : f58c5d2199e307b3959abb431d69fcb2bfcec13490717b83fbababdfa11a9ad2
mkdir -p ~/.m2/repository
tar -xzf m2repo-rewrite-spring-6.37.0.tar.gz -C ~/.m2/repository --skip-old-files
```

Windows PowerShell : `Get-FileHash m2repo-rewrite-spring-6.37.0.tar.gz` pour le contrôle, puis
`tar -xzf m2repo-rewrite-spring-6.37.0.tar.gz -C $HOME\.m2\repository --skip-old-files`
(bsdtar intégré à Windows 10+ ; `-k` si `--skip-old-files` n'est pas reconnu).

La Release est produite par le workflow `.github/workflows/release-offline-bundle.yml`, qui réassemble
les parties de `dist/` et vérifie le SHA-256. Pour une nouvelle version : remplacer les parties, puis
pousser un tag `offline-*` (ou lancer le workflow manuellement).

**Sans accès aux Releases** (clone du dépôt uniquement) : réassembler les parties de `dist/` :

```sh
cd dist
cat m2repo-rewrite-spring-6.37.0.tar.gz.part-* > m2repo-rewrite-spring-6.37.0.tar.gz
sha256sum -c m2repo-rewrite-spring-6.37.0.tar.gz.sha256
tar -xzf m2repo-rewrite-spring-6.37.0.tar.gz -C ~/.m2/repository --skip-old-files
```

Windows PowerShell, réassemblage : `cmd /c copy /b m2repo-rewrite-spring-6.37.0.tar.gz.part-00+m2repo-rewrite-spring-6.37.0.tar.gz.part-01+m2repo-rewrite-spring-6.37.0.tar.gz.part-02+m2repo-rewrite-spring-6.37.0.tar.gz.part-03 m2repo-rewrite-spring-6.37.0.tar.gz`.

Pour une reproduction stricte (aucune interférence avec un dépôt existant), extraire dans un dossier
vide et ajouter `-Dmaven.repo.local=/chemin/vers/ce/dossier` aux commandes ci-dessous.

## Bloc `<plugin>` à coller dans le pom

Dans `<build><plugins>` du projet à migrer :

```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>6.46.1</version>
    <configuration>
        <exportDatatables>true</exportDatatables>
        <activeRecipes>
            <recipe>org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>6.37.0</version>
        </dependency>
    </dependencies>
</plugin>
```

## Exécution

À la racine du projet à migrer :

```sh
# aperçu (ne modifie rien ; patch dans target/rewrite/rewrite.patch)
mvn -o generate-sources rewrite:dryRun -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0

# migration
mvn -o generate-sources rewrite:runNoFork -Drewrite.activeRecipes=org.openrewrite.java.spring.boot4.UpgradeSpringBoot_4_0
```

`-Drewrite.pomCacheEnabled=false` peut être ajouté pour garantir qu'aucun cache OpenRewrite
(`~/.rewrite-cache`) issu d'une exécution antérieure n'est utilisé : toutes les validations ci-dessous
ont été faites ainsi.

## Résultat sur le projet témoin

Voir `preuves/migration.diff`. La recette :

- passe le parent `spring-boot-starter-parent` de 3.5.16 à **4.0.8** ;
- remplace `spring-boot-starter-web` par `spring-boot-starter-webmvc` et ajoute `spring-boot-starter-webmvc-test` ;
- migre `com.fasterxml.jackson.databind.ObjectMapper` → `tools.jackson.databind.ObjectMapper` (Jackson 3) ;
- remplace `@MockBean` par `@MockitoBean`, déplace `@WebMvcTest` et `TestRestTemplate` vers leurs nouveaux packages et ajoute `@AutoConfigureTestRestTemplate`.

**Correction manuelle nécessaire après migration** (non faite par la recette) : un test utilisant
`TestRestTemplate` échoue avec `NoClassDefFoundError: org/springframework/boot/restclient/RestTemplateBuilder`.
Ajouter :

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-restclient-test</artifactId>
    <scope>test</scope>
</dependency>
```

Cet artefact est inclus dans l'archive. Avec lui, `mvn -o verify` du projet migré passe (4 tests OK).
Le pom final est dans `preuves/pom-migre.xml`.

## Validation effectuée

Environnement : Linux, Maven 3.9.11, OpenJDK 21.0.11.

1. Online, dépôt isolé `-Dmaven.repo.local=../m2repo` : `generate-sources rewrite:dryRun`, `generate-sources rewrite:runNoFork`, puis `verify` du projet migré — BUILD SUCCESS (`preuves/1..3`).
2. Le premier test offline réussissait mais produisait un pom différent : OpenRewrite résout certains POM
   (ici `spring-boot-starter-web:4.0.8`, état intermédiaire de la migration) via son propre téléchargeur
   et son cache `~/.rewrite-cache`, pas via le dépôt Maven. Ce POM a été ajouté au dépôt ; plus aucun
   « Failed to download » ensuite.
3. Nettoyage `_remote.repositories` / `*.lastUpdated` / `resolver-status.properties`.
4. Copie propre du projet 3.5.16, `~/.rewrite-cache` et `~/.rewrite` supprimés, `-o`, settings vides,
   proxy réseau neutralisé, `-Drewrite.pomCacheEnabled=false` : `dryRun`, `runNoFork` puis `verify` du
   projet migré — BUILD SUCCESS, résultat identique à l'online (`preuves/4..6`).
5. Archive réassemblée, SHA-256 vérifié, extraite dans un dépôt **vide**, puis
   `mvn -o generate-sources rewrite:runNoFork -Drewrite.activeRecipes=…` — BUILD SUCCESS, résultat
   identique (`preuves/7`).

Limite : validé sur ce projet témoin (web, JPA, validation, actuator, test). Un projet utilisant
d'autres starters ou bibliothèques peut nécessiter des POM supplémentaires ; ils apparaîtraient en
« Failed to download … » dans la sortie de `dryRun`.
