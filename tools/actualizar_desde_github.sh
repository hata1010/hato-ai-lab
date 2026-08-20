#!/bin/bash

# ============================================================
# HATO AI LAB — ACTUALIZAR DESDE GITHUB
# ============================================================

set -e

REPO_PATH="$(git rev-parse --show-toplevel)"
BRANCH="main"

cd "$REPO_PATH"

echo
echo "============================================================"
echo "       HATO AI LAB — ACTUALIZAR DESDE GITHUB"
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
    exit 1
fi

# ------------------------------------------------------------
# Verificar cambios locales
# ------------------------------------------------------------

if [ -n "$(git status --porcelain)" ]; then

    echo "⚠️ TIENES CAMBIOS LOCALES."
    echo
    git status --short
    echo
    echo "❌ No se realizará ninguna actualización."
    echo
    echo "Primero guarda esos cambios en GitHub."
    exit 2
fi

# ------------------------------------------------------------
# Obtener información de GitHub
# ------------------------------------------------------------

echo "📡 Consultando GitHub..."
git fetch origin

LOCAL="$(git rev-parse main)"
REMOTE="$(git rev-parse origin/main)"

# ------------------------------------------------------------
# Ya actualizado
# ------------------------------------------------------------

if [ "$LOCAL" = "$REMOTE" ]; then

    echo
    echo "✅ Tu proyecto ya está actualizado."
    echo
    git log -1 --oneline

    exit 0
fi

# ------------------------------------------------------------
# Determinar diferencia
# ------------------------------------------------------------

AHEAD=$(git rev-list --count origin/main..main)
BEHIND=$(git rev-list --count main..origin/main)

echo
echo "📊 Estado:"
echo "   Commits locales que GitHub no tiene: $AHEAD"
echo "   Commits de GitHub que local no tiene: $BEHIND"
echo

# ------------------------------------------------------------
# GitHub tiene cambios
# ------------------------------------------------------------

if [ "$BEHIND" -gt 0 ]; then

    echo "⬇️ Descargando cambios desde GitHub..."

    git pull --rebase origin main

    echo
    echo "============================================================"
    echo "✅ ACTUALIZACIÓN COMPLETADA"
    echo "============================================================"
    echo
    git log -1 --oneline

    exit 0
fi

# ------------------------------------------------------------
# Solo hay cambios locales
# ------------------------------------------------------------

if [ "$AHEAD" -gt 0 ]; then

    echo "ℹ️ Tu máquina tiene cambios que todavía no están en GitHub."
    echo
    echo "No hay nada que descargar."
    echo "Usa guardar_en_github.sh para publicarlos."

    exit 0
fi
