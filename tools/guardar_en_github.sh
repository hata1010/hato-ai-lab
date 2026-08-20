#!/bin/bash

# ============================================================
# HATO AI LAB — RESPALDO EN GITHUB
# ============================================================

set -e

REPO_PATH="$(git rev-parse --show-toplevel)"
BRANCH="main"

cd "$REPO_PATH"

echo
echo "============================================================"
echo "        HATO AI LAB — RESPALDO EN GITHUB"
echo "============================================================"
echo

echo "📁 Repositorio:"
echo "   $REPO_PATH"
echo

echo "🌿 Rama:"
echo "   $(git branch --show-current)"
echo

# ------------------------------------------------------------
# Verificar rama
# ------------------------------------------------------------

CURRENT_BRANCH="$(git branch --show-current)"

if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
    echo "❌ Error: no estás en la rama $BRANCH."
    echo "   Rama actual: $CURRENT_BRANCH"
    exit 1
fi

# ------------------------------------------------------------
# Mostrar cambios
# ------------------------------------------------------------

echo "📊 Cambios detectados:"
git status --short
echo

# ------------------------------------------------------------
# Verificar si realmente hay cambios
# ------------------------------------------------------------

if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "ℹ️ No hay cambios nuevos para guardar."
    echo
    echo "🔎 Verificando estado remoto..."
    git fetch origin
    git status
    exit 0
fi

# ------------------------------------------------------------
# Agregar cambios
# ------------------------------------------------------------

echo "📥 Agregando cambios..."
git add .

# ------------------------------------------------------------
# Mostrar lo que será guardado
# ------------------------------------------------------------

echo
echo "📦 Archivos preparados para el commit:"
git diff --cached --stat
echo

# ------------------------------------------------------------
# Pedir mensaje
# ------------------------------------------------------------

read -p "📝 Mensaje del commit: " MENSAJE

if [ -z "$MENSAJE" ]; then
    MENSAJE="backup: actualización Hato $(date '+%Y-%m-%d %H:%M:%S')"
fi

# ------------------------------------------------------------
# Commit
# ------------------------------------------------------------

echo
echo "💾 Creando commit..."
git commit -m "$MENSAJE"

# ------------------------------------------------------------
# Sincronizar antes del push
# ------------------------------------------------------------

echo
echo "🔄 Verificando GitHub..."
git fetch origin

LOCAL="$(git rev-parse main)"
REMOTE="$(git rev-parse origin/main)"

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "ℹ️ GitHub ya está actualizado."
    exit 0
fi

# ------------------------------------------------------------
# Verificar divergencia
# ------------------------------------------------------------

AHEAD=$(git rev-list --count origin/main..main)
BEHIND=$(git rev-list --count main..origin/main)

if [ "$BEHIND" -gt 0 ]; then

    echo
    echo "⚠️ GitHub tiene $BEHIND commit(s) que tu máquina no tiene."
    echo "   No voy a sobrescribirlos automáticamente."
    echo
    echo "   Primero debemos sincronizar las dos historias."
    echo

    exit 2
fi

# ------------------------------------------------------------
# Push
# ------------------------------------------------------------

echo
echo "🚀 Subiendo a GitHub..."
git push origin main

echo
echo "============================================================"
echo "✅ RESPALDO COMPLETADO"
echo "============================================================"
echo
echo "Commit:"
git log -1 --oneline
echo
echo "GitHub:"
git remote get-url origin
echo
