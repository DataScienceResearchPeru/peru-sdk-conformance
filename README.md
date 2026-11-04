# Peru SDK: conformidad

Corpus común y versionado de pruebas sintéticas para los SDKs nativos. Licencia MIT.

`cases.json` contiene 17 entradas de consulta SUNAT, 17 respuestas y 3 consultas de identidad simulada. `manifest.json` fija el formato, la versión y el SHA-256 revisado del corpus. Los casos provienen de la prueba inicial de Peru SDK; no se importan suites de otros proyectos.

```bash
python3 tools/check.py
stage=$(mktemp -d /var/tmp/peru-conformance.XXXXXXXX)
python3 tools/build_bundle.py --output "$stage"
```

Para trabajo local, elegir un subdirectorio único de `/var/tmp`. El segundo comando crea un archivo con una lista explícita de cuatro archivos y sus hashes. No contiene implementaciones de SDKs ni credenciales. CI comprueba la integridad antes de producir el artefacto.

Los consumidores fijan un commit y SHA-256 en su `upstream.lock.json`. Cada SDK incluye una copia verificada en sus datos de prueba, de modo que su suite no requiere red ni el checkout de este repositorio. La sincronización es una operación explícita de desarrollo; instalar o usar el SDK no descarga contratos ni pruebas.

Los datos son sintéticos y no demuestran compatibilidad real con una institución. RENIEC sigue siendo un contrato provisional. Los códigos, formatos y decisiones de interpretación se documentan en el repositorio de modelos.
