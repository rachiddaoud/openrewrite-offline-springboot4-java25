Objet : autoriser OpenRewrite pour la migration Spring Boot 4 / Java 25

Bonjour,

Merci de rendre disponibles dans notre proxy Artifactory de Maven Central les artefacts suivants et leurs dépendances transitives :

| Coordonnées | Licence déclarée |
|---|---|
| org.openrewrite.maven:rewrite-maven-plugin:6.46.1 | Apache 2.0 |
| org.openrewrite.recipe:rewrite-spring:6.37.1 | Moderne Source Available |
| org.openrewrite.recipe:rewrite-migrate-java:3.42.1 | Moderne Source Available |
| org.openrewrite:rewrite-java-17:8.89.0 et 8.90.2 | Apache 2.0 |
| org.openrewrite:rewrite-java-21:8.89.0 et 8.90.2 | Apache 2.0 |
| org.openrewrite:rewrite-java-25:8.89.0 et 8.90.2 | Apache 2.0 |

GroupIds OpenRewrite : `org.openrewrite`, `org.openrewrite.recipe`, `org.openrewrite.maven`, **`org.openrewrite.meta`, `org.openrewrite.tools`, `org.openrewrite.gradle.tooling`**.

Les tiers comprennent notamment `com.fasterxml.jackson.*`, `tools.jackson.*`, `org.antlr`, `org.ow2.asm`, `org.jetbrains.*`, `org.apache.maven.*`, `org.apache.maven.resolver`, `org.codehaus.plexus`, `org.eclipse.*`, `org.rocksdb`, `io.micrometer`, `io.quarkus.gizmo`, `com.google.*`, `org.springframework.*`, `org.hibernate.*`, `jakarta.*`. La liste **exacte et exhaustive des 148 groupIds**, sans approximation par wildcard, est jointe dans **groupIds.txt** ; les **833 GAV et leurs licences déclarées** sont dans **inventaire-licences.csv** (incluant parents/BOM et le projet témoin).

Source unique du lot : **https://repo.maven.apache.org/maven2/**. Merci d'autoriser POM/JAR, checksums et `maven-metadata.xml` : les recettes utilisent ces métadonnées pour résoudre leurs versions cibles. Les versions de chaque transitive et le lien Central exact de chaque POM figurent dans le CSV.

Attention : Moderne Source Available n'est pas Apache 2.0. Les licences des autres recettes varient également ; le CSV les détaille par GAV. Les tiers ne sont pas tous Apache : les licences déclarées sont conservées, y compris MIT/BSD/EPL/LGPL/CDDL. Six anciens POM auxiliaires sont marqués « NON DECLAREE / A VERIFIER » plutôt que de leur attribuer une licence non vérifiée. Référence MSAL : https://docs.moderne.io/licensing/moderne-source-available-license/.

Merci.
