# 🔐 Demo – Sécurité dans les pipelines CI/CD
### OWASP A08 : Software and Data Integrity Failures

---

## Structure du repo

```
demo-repo/
├── .github/
│   └── workflows/
│       └── security.yml       ← Pipeline GitHub Actions
├── app/
│   ├── app.py                 ← Code VULNÉRABLE (phase 1)
│   └── app_fixed.py           ← Code CORRIGÉ (phase 2)
├── requirements.txt           ← Dépendances vulnérables
├── requirements_fixed.txt     ← Dépendances corrigées
└── README.md
```

---

## 🎬 Script de démonstration

### PHASE 1 — Le pipeline détecte et bloque

1. Montrer `app/app.py` → pointer les 3 failles
2. Montrer `requirements.txt` → Flask 0.12.2 avec CVE
3. Faire un commit :
   ```bash
   git add .
   git commit -m "feat: ajout de l'application"
   git push origin main
   ```
4. Ouvrir GitHub → onglet **Actions**
5. Montrer le pipeline qui tourne : SAST → SCA → ❌ FAIL
6. Cliquer sur les logs pour montrer les vulnérabilités détectées

### PHASE 2 — On corrige, le pipeline passe

1. Remplacer `app.py` par `app_fixed.py`
2. Remplacer `requirements.txt` par `requirements_fixed.txt`
3. Commit :
   ```bash
   git add .
   git commit -m "fix: correction des vulnérabilités détectées"
   git push origin main
   ```
4. Montrer le pipeline qui passe : SAST ✅ → SCA ✅ → Build ✅ → DAST ✅

---

## Failles présentes dans app.py

| Faille | Type | Outil qui la détecte |
|--------|------|---------------------|
| `API_KEY = "sk-prod-abc123..."` | Secret hardcodé | SAST (Semgrep) |
| `"SELECT * WHERE name = '" + username + "'"` | Injection SQL | SAST (Semgrep) |
| `return "<h1>Hello, " + name + "!</h1>"` | XSS | SAST (Semgrep) |
| Flask 0.12.2 | CVE-2019-1010083 | SCA (Dependency-Check) |
| Werkzeug 1.0.0 | CVE-2022-29361 | SCA (Dependency-Check) |

---

## Résultat attendu

```
✅ sast     → FAIL  (3 vulnérabilités détectées)
✅ sca      → FAIL  (2 CVE HIGH/CRITICAL)
⏭ build    → SKIPPED (bloqué par sast + sca)
⏭ dast     → SKIPPED
```

**Après correction :**
```
✅ sast     → PASS
✅ sca      → PASS
✅ build    → PASS
✅ dast     → PASS
```
