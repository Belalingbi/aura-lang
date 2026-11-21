# Product Requirements Document (PRD) — Langage de Programmation Aura

- **Version :** 1.0 (Spécification consolidée)
- **Statut :** Brouillon de conception / Évolution continue
- **Public cible :** Développeurs, créateurs d'outils de scripting/automatisation, étudiants et ingénieurs sécurité (analyse de code, sandboxing, tests).

---

## 1. Vision et Proposition de Valeur

**Aura** est un langage de programmation moderne, expressif et orienté objet, doté d'une syntaxe épurée basée sur des accolades (`{ ... }`), sans points-virgules obligatoires, et d'un typage dynamique. Il vise à combiner :
1. **La fluidité d'écriture** d'un langage de script moderne (POO avec `class`, `extends`, `super`, `static`, fonctions anonymes/lambdas, f-strings `f"..."`, destructuration de listes et dictionnaires, compréhensions de listes, `switch/case`, opérateur ternaire `? :`, intervalles `0..10`).
2. **La résilience et la maintenabilité** grâce à la gestion structurée des exceptions (`try / catch / finally / throw`), aux assertions (`assert`), à la modularité (`import ... as ...`), au formateur (`aura fmt`) et au générateur de documentation (`aura doc`).
3. **La montée en puissance d'exécution** via un double moteur (interpréteur AST pour l'itération rapide et le REPL interactif, complété par une machine virtuelle à pile avec ramasse-miettes *Mark-and-Sweep*, compilation AOT vers C, FFI et concurrence CSP avec `go`, canaux, `select` et supervision).
4. **Une posture Security-by-Design** : protéger l'hôte et les programmes contre les dénis de service, l'accès non contrôlé au système de fichiers/réseau/FFI, les fuites de mémoire et les injections.

---

## 2. Périmètre Fonctionnel (Features)

### 2.1 Syntaxe, Types et Structures de Données
- **Primitives :** nombres (`int`/`float`), chaînes de caractères (`string`), booléens (`true`/`false`), valeur nulle (`nil`/`None`).
- **Interpolation de chaînes (f-strings) :** évaluation d'expressions `{expr}` au sein de chaînes `f"..."`.
- **Collections :** tableaux dynamiques (`[a, b]`, `.push()`, `.pop()`, `.join()`, `.contains()`, `.len()`, `.map()`, `.filter()`, `.reduce()`), compréhensions de listes (`[expr for x in iter if cond]`), dictionnaires clé-valeur (`{"k": v}`, `.keys()`, `.values()`, `.items()`, `.get()`), ensembles (`set(...)`, `.add()`, `.remove()`, `.union()`, `.intersection()`, `.difference()`, `.toList()`).
- **Destructuration :** déballage de listes (`[x, y] = liste`) et de dictionnaires (`{"a": x} = dict`).

### 2.2 Contrôle de Flux et Fonctions
- **Conditionnelles et boucles :** `if / else`, opérateur ternaire `cond ? vrai : faux`, `switch / case / default`, `while`, `for ... in ...`, intervalles `debut..fin`, `break` et `continue`.
- **Opérateurs :** arithmétiques (`+`, `-`, `*`, `/`, `%`), comparaisons (`==`, `!=`, `>`, `<`, `>=`, `<=`), logiques avec court-circuit (`and`, `or`, `not`).
- **Fonctions :** nommées, récursives, anonymes (lambdas `fn(x) { ... }`), arguments par défaut, paramètres variables (`...args`), décorateurs (`@dec`) et générateurs (`yield` / `.next()`).

### 2.3 Programmation Orientée Objet et Modules
- **POO :** classes, constructeurs (`init` / `__init__`), contexte d'instance (`this` / `self`), héritage (`extends`), appel parent (`super`), méthodes et propriétés statiques (`static`).
- **Modularité :** `import "fichier.aura"` et `import "fichier.aura" as Alias` avec isolation d'environnement et prévention des imports multiples.

### 2.4 Bibliothèque Standard et Outillage
- **Fonctions globales :** `print`, `len`, `type`, `assert`, `benchmark`, `jsonParse`, `jsonStringify`, `readFile` / `writeFile` (ou `read_file` / `write_file`).
- **Modules natifs :** `math`, `time`, `random`, `http` (`get`, `post`).
- **Outillage (CLI) :** `aura new`, `aura run`, `aura test`, `aura install`, `aura fmt`, `aura doc`, `aura bench`, `aura build`, serveur LSP (`pygls`) et REPL interactif avec historique et autocomplétion.
- **Exécution avancée & Concurrence :** VM bytecode à pile + GC *Mark-and-Sweep*, transpileur C/GCC, pont FFI (`ctypes`), tâches concurrentes (`go`), canaux CSP (`channel`, `send`, `receive`), multiplexage `select` et superviseur de processus (`AuraSupervisor`).

---

## 3. Exigences de Sécurité, Robustesse et Cybersécurité

### 3.1 Sécurité du Langage et Isolation (Sandboxing)
- **Contrôle des accès système (`readFile`/`writeFile`, `import`, `http`, FFI) :** interdire ou restreindre par défaut l'accès hors du répertoire de travail (prévention de la *Path Traversal* `../../`), encadrer les requêtes `http` (schémas autorisés `https`/`http`, timeouts, limitation de la taille des réponses, protection SSRF de base) et marquer la FFI et la compilation AOT comme des fonctionnalités *unsafe / opt-in* explicitement désactivables en mode bac à sable.
- **Sécurité de l'interpolation (f-strings) et de la désérialisation (`jsonParse`) :** éviter l'exécution arbitraire de code dans les chaînes interpolées ; borner la profondeur et la taille des charges JSON parsées pour éviter les attaques par déni de service (DoS JSON).
- **Sécurité des expressions régulières (`regexMatch`, `regexFindAll`, `regexReplace`) :** encadrer ou limiter les motifs susceptibles de provoquer du *catastrophic backtracking* (ReDoS).

### 3.2 Robustesse du Code et Résilience à l'Exécution
- **Gestion explicite des erreurs :** propagation propre des exceptions (`throw`, `try / catch / finally`) sans masquer les erreurs critiques de runtime, avec conservation d'un contexte d'erreur clair (type, message, ligne/colonne si disponible).
- **Validation des entrées et types dynamiques :** vérifications explicites d'arité, de bornes d'index (listes/ranges), de clés manquantes et de types avant opération afin d'éviter les plantages silencieux ou les comportements indéfinis.
- **Gestion mémoire et concurrence :** le GC *Mark-and-Sweep* doit libérer les objets cycliques/orphelins sans corrompre la pile ni les *upvalues* ; les canaux (`AuraChannel`), `select` et `AuraSupervisor` doivent prévenir les *deadlocks* (timeouts, clôture propre des canaux, plafonnement des redémarrages `max_restarts` avec *backoff*).

### 3.3 Posture Cybersécurité et Usages Offensifs / Hacking
- **Usage défensif, audit et red-teaming autorisé :** Aura doit être conçu comme un outil d'automatisation, d'analyse de logs, de parsing, de tests unitaires/de charge et d'audit de sécurité dans un cadre légal et autorisé.
- **Résistance aux attaques contre le runtime lui-même :** protection contre les bombes mémoire/CPU (boucles infinies, récursion non bornée, allocations massives via `[...]` ou `range`), l'empoisonnement d'environnement global ou de prototypes/classes, et l'injection de commandes lors de la compilation (`build`) ou du téléchargement de paquets (`install` : vérification d'intégrité/checksums, refus des chemins malveillants dans les archives/noms de paquets).
- **Développement sécurisé des scripts Aura :** encourager de bonnes pratiques (pas de secrets en dur, validation des entrées externes, gestion des timeouts réseau, journalisation sans fuite de données sensibles).

---

## 4. Critères de Succès et Métriques

- **Fonctionnel :** 100 % des fonctionnalités du langage (POO, closures, générateurs, f-strings, collections, exceptions, modules, CLI) validées par une suite de tests automatisés (`aura test`).
- **Fiabilité :** aucune erreur Python brute non interceptée sur des entrées Aura malformées (erreurs lexicales, syntaxiques ou d'exécution clairement rapportées).
- **Sécurité & Robustesse :** tests dédiés couvrant la traversée de chemin (`../`), les limites de taille/profondeur JSON, les timeouts réseau/canaux, les cycles mémoire sous le GC et la non-régression des redémarrages supervisés.