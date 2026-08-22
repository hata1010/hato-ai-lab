# Protocolo Oficial de Actualización y Validación de la VM — Hato

**Código:** VM-UPDATE-001  
**Versión:** 1.0  
**Estado:** OFICIAL  
**Fuente de verdad:** `origin/main`

## 1. Propósito

Establecer un único ciclo operativo, reproducible y versionado para actualizar la VM de Hato, validar un PR y dejar finalmente la VM sincronizada y validada sobre `main`.

## 2. Regla fundamental

GitHub `origin/main` es la fuente oficial del código. La VM es un entorno de ejecución y validación.

No se considera una rama `feature/*` como fuente oficial permanente de la VM.

## 3. Ciclo único: 22 comandos

Para una actualización/validación completa, los 22 pasos se ejecutan en este orden. El PR concreto sustituye la rama y el módulo de pruebas correspondientes.

### Preparación y sincronización

**1. Entrar en la raíz del repositorio**
```bash
cd ~/Sistemas/Hato
```

`~/Sistemas/Hato` es la raíz del repositorio y del proyecto Django: contiene `.git/`, `manage.py`, `apps/` y la configuración del proyecto. `apps/ganado` es un módulo, no la raíz del repositorio.

**2. Comprobar estado inicial**
```bash
git status
```

**3. Volver a la fuente oficial**
```bash
git checkout main
```

**4. Sincronizar `main`**
```bash
git pull origin main
```

**5. Confirmar rama**
```bash
git branch --show-current
```

**6. Confirmar commit actual**
```bash
git log -1 --oneline
```

**7. Actualizar referencias remotas sin modificar el árbol de trabajo**
```bash
git fetch origin
```

### Identificación y entrada al PR

**8. Identificar el commit remoto de `main`**
```bash
git rev-parse origin/main
```

**9. Identificar el commit remoto del PR**
```bash
git rev-parse origin/feature/movilidad-operativa
```

> Para otro PR se sustituye `feature/movilidad-operativa` por la rama real de ese PR.

**10. Entrar en la rama del PR**
```bash
git checkout feature/movilidad-operativa
```

**11. Confirmar rama**
```bash
git branch --show-current
```

**12. Confirmar commit que será probado**
```bash
git log -1 --oneline
```

**13. Confirmar estado de trabajo**
```bash
git status
```

### Chequeos y pruebas

**14. Chequeo de Django**
```bash
python manage.py check
```

**15. Chequeo de migraciones**
```bash
python manage.py showmigrations
```

**16. Tests específicos del módulo afectado**
```bash
python manage.py test apps.ganado
```

El módulo se sustituye según el PR que se esté validando.

**17. Tests globales**
```bash
python manage.py test
```

Después de estos comandos se realiza la validación funcional en la interfaz cuando el PR lo requiera.

### Retorno a `main` y validación final

**18. Regresar a `main`**
```bash
git checkout main
```

**19. Sincronizar nuevamente `main`**
```bash
git pull origin main
```

**20. Confirmar estado final**
```bash
git status
```

**21. Confirmar commit final**
```bash
git log -1 --oneline
```

**22. Validación final de Django y regresión**
```bash
python manage.py check
python manage.py test
```

## 4. Regla de ejecución

El usuario ejecuta los comandos en orden y entrega las salidas. La salida de cada comando determina si el ciclo puede continuar.

- Si el comando termina correctamente: continuar.
- Si aparece una advertencia: evaluar antes de continuar cuando pueda afectar la validación.
- Si aparece un error: detener el ciclo y resolver el problema antes de ejecutar el siguiente paso.

No se deben ejecutar los comandos restantes a ciegas después de un error.

## 5. Regla sobre `pull` de ramas de PR

No se utiliza como mecanismo rutinario:

```bash
git pull origin feature/...
```

La actualización de referencias se hace con `git fetch origin` y posteriormente se identifica explícitamente el commit candidato que será validado. Esto mantiene separado el concepto de fuente oficial (`main`) del candidato (`feature/*`).

## 6. Tests específicos y globales

Los tests específicos del paso 16 corresponden al módulo afectado por el PR. Por ejemplo, PR #8 de movilidad se valida dentro de `apps.ganado` porque la funcionalidad pertenece al módulo de ganado.

El paso 17 ejecuta la suite global para detectar regresiones fuera del módulo.

## 7. Criterio de cierre

El ciclo se considera completo cuando la VM termina nuevamente en `main`, sincronizada con `origin/main`, con estado de trabajo controlado y con los chequeos/tests finales ejecutados.

Para declarar un PR publicado/cerrado, además deben existir las evidencias correspondientes de revisión, pruebas, memoria y merge del PR.

## 8. No improvisación

Este documento es el protocolo operativo versionado. Ante una operación futura que contradiga este procedimiento, se debe detener la ejecución y revisar este documento antes de continuar.

## 9. Ejemplo actual

Para PR #8:

- Rama: `feature/movilidad-operativa`
- Módulo de pruebas: `apps.ganado`

Para PR posteriores, se reemplazan esos valores por la rama y módulo reales del PR en cuestión.
