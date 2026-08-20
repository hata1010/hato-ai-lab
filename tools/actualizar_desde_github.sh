#!/bin/bash

# ============================================================
# HATO AI LAB — ACTUALIZAR DESDE GITHUB
# ============================================================
# Uso:
#   ./tools/actualizar_desde_github.sh
#       Actualiza la rama actualmente activa.
#
#   ./tools/actualizar_desde_github.sh <rama>
#       Cambia a la rama indicada, la actualiza y la deja activa.
# ============================================================

set -e

REPO_PATH="$(git rev-parse --show-toplevel)"
CURRENT_BRANCH="$(git branch --show-current)"
TARGET_BRANCH="${1:-$CURRENT_BRANCH}"

cd "$REPO_PATH"

echo
echo "============================================================"
echo "       HATO AI LAB — ACTUALIZAR DESDE GITHUB"
echo "============================================================"
echo
echo "📁 Repositorio:"
echo "   $REPO_PATH"
echo
echo "🌿 Rama actual:"
echo "   ${CURRENT_BRANCH:-'(sin rama)'}"
echo
echo "🎯 Rama solicitada:"
echo "   $TARGET_BRANCH"
echo

# ------------------------------------------------------------
# Verificar que Git tenga una rama activa
# ------------------------------------------------------------

if [ -z "$CURRENT_BRANCH" ]; then
    echo "❌ Error: el repositorio no tiene una rama activa."
    exit 1
fi

# ------------------------------------------------------------
# Verificar cambios locales ANTES de cambiar de rama
# ------------------------------------------------------------

if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️ TIENES CAMBIOS LOCALES."
    echo
    git status --short
    echo
    echo "❌ No se realizará ninguna actualización ni cambio de rama."
    echo "   Primero guarda o publica esos cambios."
    exit 2
fi

# ------------------------------------------------------------
# Obtener información de GitHub
# ------------------------------------------------------------

echo "📡 Consultando GitHub..."
git fetch origin

# ------------------------------------------------------------
# Verificar que la rama solicitada exista en GitHub
# ------------------------------------------------------------

if ! git show-ref --verify --quiet "refs/remotes/origin/$TARGET_BRANCH"; then
    echo
    echo "❌ Error: la rama '$TARGET_BRANCH' no existe en origin."
    echo
    echo "🌿 Ramas disponibles en GitHub:"
    git for-each-ref --format='   %(refname:strip=3)' refs/remotes/origin/ | sort
    exit 3
fi

# ------------------------------------------------------------
# Cambiar a la rama solicitada si es necesario
# ------------------------------------------------------------

if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    echo "🔀 Cambiando de rama: $CURRENT_BRANCH → $TARGET_BRANCH"

    if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
        git switch "$TARGET_BRANCH"
    else
        git switch --track -c "$TARGET_BRANCH" "origin/$TARGET_BRANCH"
    fi
fi

# ------------------------------------------------------------
# Verificar estado después del cambio
# ------------------------------------------------------------

ACTIVE_BRANCH="$(git branch --show-current)"
if [ "$ACTIVE_BRANCH" != "$TARGET_BRANCH" ]; then
    echo "❌ Error: no fue posible activar la rama '$TARGET_BRANCH'."
    exit 4
fi

LOCAL="$(git rev-parse "$TARGET_BRANCH")"
REMOTE="$(git rev-parse "origin/$TARGET_BRANCH")"

# ------------------------------------------------------------
# Ya actualizado
# ------------------------------------------------------------

if [ "$LOCAL" = "$REMOTE" ]; then
    echo
echo "============================================================"
    echo "✅ TU PROYECTO YA ESTÁ ACTUALIZADO"
    echo "============================================================"
    echo
echo "🌿 Rama activa:"
    echo "   $ACTIVE_BRANCH"
    echo
echo "📌 Commit:"
    git log -1 --oneline
    echo
    exit 0
fi

# ------------------------------------------------------------
# Determinar diferencia
# ------------------------------------------------------------

AHEAD=$(git rev-list --count "origin/$TARGET_BRANCH..$TARGET_BRANCH")
BEHIND=$(git rev-list --count "$TARGET_BRANCH..origin/$TARGET_BRANCH")

echo
echo "📊 Estado:"
echo "   Commits locales que GitHub no tiene: $AHEAD"
echo "   Commits de GitHub que local no tiene: $BEHIND"
echo

# ------------------------------------------------------------
# Hay cambios locales publicados/no sincronizados
# ------------------------------------------------------------

if [ "$AHEAD" -gt 0 ]; then
    echo "⚠️ Tu máquina tiene commits que todavía no están en GitHub."
    echo
    echo "❌ No se realizará un pull automático para evitar sobrescribir trabajo."
    echo "   Usa guardar_en_github.sh para publicarlos cuando corresponda."
    exit 5
fi

# ------------------------------------------------------------
# GitHub tiene cambios
# ------------------------------------------------------------

if [ "$BEHIND" -gt 0 ]; then
    echo "⬇️ Descargando cambios desde GitHub..."
    git pull --rebase origin "$TARGET_BRANCH"
fi

# ------------------------------------------------------------
# Confirmación final
# ------------------------------------------------------------

FINAL_BRANCH="$(git branch --show-current)"
FINAL_COMMIT="$(git rev-parse HEAD)"
REMOTE_FINAL="$(git rev-parse "origin/$TARGET_BRANCH")"

echo
echo "============================================================"
if [ "$FINAL_COMMIT" = "$REMOTE_FINAL" ] && [ "$FINAL_BRANCH" = "$TARGET_BRANCH" ]; then
    echo "✅ ACTUALIZACIÓN COMPLETADA"
else
    echo "⚠️ ACTUALIZACIÓN INCOMPLETA — REVISAR ESTADO"
fi
echo "============================================================"
echo
echo "🌿 Rama activa:"
echo "   $FINAL_BRANCH"
echo
echo "📌 Commit:"
git log -1 --oneline
echo