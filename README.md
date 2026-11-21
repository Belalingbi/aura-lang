# 🌟 Langage de Programmation Aura (Aura Language)

![Logo](Logo.jpg)

Aura est un langage de programmation moderne, expressif et orienté objet, doté d'une syntaxe épurée basée sur des accolades `{ ... }`, d'un typage dynamique et d'une double architecture d'exécution (Interpréteur d'AST et Machine Virtuelle Bytecode à pile avec ramasse-miettes *Mark-and-Sweep*).

---

## ⚡ Caractéristiques Principales

- **Double moteur d'exécution :**
  - **Voie AST :** Interpréteur à arbre syntaxique direct pour le REPL interactif et le prototypage rapide.
  - **Voie Bytecode VM :** Compilateur vers chunks d'opcodes et Machine Virtuelle à pile avec GC *Mark-and-Sweep*.
- **Programmation Orientée Objet complète :** Classes, constructeurs (`__init__` / `init`), héritage (`extends`), liaisons d'instances (`self` / `this`), `super`, méthodes statiques.
- **Fonctions modernes & closures :** Fonctions nommées, lambdas anonymes `fn(x) { return x * 2 }`, paramètres variables `...args`, décorateurs `@decorator`, et générateurs `yield` / `.next()`.
- **Interpolation de chaînes (f-strings) :** Évaluation dynamique d'expressions `f"Bonjour {nom}, score : {score * 2}"`.
- **Collections riches & fonctionnelles :**
  - Listes avec `.map()`, `.filter()`, `.reduce()`, `.push()`, `.pop()`, `.join()`.
  - Compréhensions de listes `[x * 2 for x in items if x > 2]`.
  - Dictionnaires associatifs `{ "clé": valeur }` avec accès par point `dict.cle` ou par index `dict["cle"]`.
  - Ensembles `set([1, 2, 3])` avec opérations ensemblistes (`union`, `intersection`, `difference`).
- **Gestion structurée des exceptions :** `try / catch / finally` et `throw`.
- **Concurrence CSP :** Canaux de communication typés Go (`AuraChannel`), multiplexage et supervision de processus (`AuraSupervisor`).
- **Sécurité intégrée (Security-by-Design) :** Protection contre la traversée de chemin (*Path Traversal* `../../`) et sandboxing des accès fichiers.
- **Outillage CLI complet :** `aura run`, `aura repl`, `aura test`, `aura new`, `aura fmt`, `aura doc`, `aura bench`, `aura vm`.

---

## 🚀 Installation & Démarrage Rapide

### 1. Cloner ou télécharger le dépôt
```bash
git clone https://github.com/Belalingbi/aura-lang.git
cd aura-lang
```

### 2. Installation en mode package global
Installez Aura dans votre environnement Python avec la commande suivante :
```bash
pip install -e .
```

Une fois installé, la commande `aura` est disponible **partout dans votre terminal** (PowerShell, CMD, Bash), quel que soit le dossier où vous vous trouvez :
```bash
aura run main.aura
aura repl
aura test
```

### 3. Utilisation directe sans installation
Si vous préférez exécuter Aura directement sans l'installer via pip :
```powershell
# Naviguer dans le dossier du projet
cd C:\Users\belal\Downloads\AURA

# Exécuter un script avec l'interpréteur
python main.py main.aura
python main.py test_global.aura

# Exécuter sur la Machine Virtuelle Bytecode
python cli.py vm programme_vm.aura
```

---

## 📖 Guide de la Syntaxe

### 1. Variables & F-Strings
```aura
nom = "Aura"
mut score = 100
score = score + 25

print(f"Bienvenue dans {nom} ! Score : {score}")
```

### 2. Classes & Héritage
```aura
class CompteBancaire {
    fn __init__(self, titulaire, solde) {
        self.titulaire = titulaire
        self.solde = solde
    }

    fn deposer(montant) {
        self.solde = self.solde + montant
        print(f"[{self.titulaire}] Nouveau solde : {self.solde} €")
    }
}

class CompteEpargne extends CompteBancaire {
    fn appliquerInterets() {
        self.solde = self.solde + (self.solde * 0.05)
    }
}

compte = CompteEpargne("Alice", 1000)
compte.deposer(500)
compte.appliquerInterets()
```

### 3. Collections & Programmation Fonctionnelle
```aura
nombres = [1, 2, 3, 4, 5, 6]

// map & filter
carres = nombres.map(fn(x) { return x * x })
pairs = nombres.filter(fn(x) { return x % 2 == 0 })

// Compréhension de liste
cubes = [x * x * x for x in nombres if x > 2]

// Dictionnaire
utilisateur = { "nom": "Alice", "role": "Admin" }
print(utilisateur.nom)
```

### 4. Concurrence CSP (Canaux)
```aura
ch = channel(2)
ch.send("Donnée 1")
ch.send("Donnée 2")

valeur = ch.receive()
print(f"Message reçu : {valeur}")
```

---

## 🛠️ Référence des Commandes CLI

| Commande | Action |
| :--- | :--- |
| `aura run <fichier.aura>` | Exécute un fichier source avec l'interpréteur AST |
| `aura repl` | Démarre la boucle interactive REPL |
| `aura test` | Lance la suite complète de tests unitaires du projet |
| `aura vm <fichier.aura>` | Compile et exécute via la VM Bytecode + GC |
| `aura fmt [chemin]` | Formate automatiquement le code source (indentation 4 espaces) |
| `aura doc [chemin]` | Génère la documentation d'API Markdown (`DOCS.md`) |
| `aura bench <fichier.aura>` | Mesure les performances et le temps moyen d'exécution |
| `aura new <nom>` | Initialise un nouveau projet avec structure standard |

---

## 📦 Exporter le Projet sur GitHub

Pour publier ce projet sur votre compte GitHub afin que tout le monde puisse l'utiliser :

```powershell
# 1. Naviguez dans le dossier du projet
cd C:\Users\belal\Downloads\AURA

# 2. Initialisez le dépôt Git local
git init
git add .
git commit -m "feat: release initiale du langage Aura 1.0.0"

# 3. Liez à votre dépôt distant GitHub
git remote add origin https://github.com/Belalingbi/aura-lang.git
git branch -M main
git push -u origin main
```

N'importe quel développeur pourra ensuite l'installer directement avec :
```bash
pip install git+https://github.com/Belalingbi/aura-lang.git
```
Et exécuter `aura` directement dans son terminal !
