# Red Judicial — Chile

Red Judicial integra el corpus legal chileno a Claude. Expone una sola herramienta MCP, `redjudicial_search`, que busca en fuentes cruzadas:

- **Jurisprudencia de tribunales** — más de 2,5 millones de sentencias: 287.000+ de la Corte Suprema (2005 a la fecha) y ~1,4M de Cortes de Apelaciones (backfill activo hacia ~2M), con texto completo e indexación diaria.
- **Tribunal Constitucional** — sentencias del TC (12.000+).
- **Jurisprudencia administrativa y especializada** — dictámenes de Contraloría (90.000+), autoridad tributaria y Tribunales Tributarios y Aduaneros (SII, TTA), Dirección del Trabajo, mercado financiero (CMF), seguridad social (SUSESO), libre competencia (TDLC), consumidor (SERNAC), tribunales ambientales, tribunal de propiedad industrial (TDPI) e Instituto Nacional de Derechos Humanos (INDH).
- **Legislación** — alrededor de 19.000 normas vigentes de BCN / LeyChile, con granularidad por artículo.
- **Doctrina** — artículos académicos de acceso abierto (SciELO y repositorios universitarios).
- **Primera instancia** (civil, laboral, penal, familia, cobranza) — laboral (~214.000) y cobranza completos; civil, penal y familia en incorporación activa.

Cada resultado incluye una cita verificable con enlace a la fuente oficial (Poder Judicial, BCN y el organismo emisor). La herramienta es de solo lectura; no escribe en los sistemas del usuario.

Pensado para abogados y estudios jurídicos en Chile y América Latina hispanohablante.

## Casos de uso

1. Investigar cómo ha resuelto la Corte Suprema sobre lucro cesante en responsabilidad contractual en los últimos cinco años.
2. Recuperar la versión vigente de un artículo del Código Civil junto con la jurisprudencia más reciente que lo interpreta.
3. Cruzar un fallo de la Corte Suprema sobre despido injustificado con doctrina académica chilena sobre la misma materia.
4. Preparar una minuta con los criterios dominantes de un ministro específico de la Corte Suprema en materia tributaria (en combinación con el producto público de Red Judicial).

## Cuándo usarlo

- Consultas respondibles desde jurisprudencia, legislación o doctrina chilena de acceso abierto.
- Búsqueda del texto vigente de una ley, decreto o reglamento chileno, junto con su última interpretación jurisprudencial.
- Investigación cruzada que combine un holding de la Corte Suprema, la norma de base y comentario académico.
- Investigación comparada entre jurisprudencia chilena y otras jurisdicciones de América Latina hispanohablante (expansión planificada).

## Cuándo no usarlo

- Derecho primario de Estados Unidos u otras jurisdicciones no chilenas — fuera del corpus actual. Red Judicial no cubre esas jurisdicciones; para otras jurisdicciones, usa el plugin correspondiente del marketplace.
- Sentencias de primera instancia — laboral y cobranza completas; civil, penal y familia en incorporación activa.
- Seguimiento en tiempo real del estado procesal de una causa específica — no soportado.
- Redacción de escritos o contratos chilenos — Red Judicial provee fuentes primarias para investigación; la redacción queda en manos del abogado.
- Predicción del resultado de un caso concreto — el corpus apoya la investigación, no la predicción.

## Autenticación

El servidor MCP en `https://ia.redjudicial.cl/mcp/v1` está protegido con OAuth 2.0, **Dynamic Client Registration** (RFC 7591) y **PKCE** (RFC 7636). Los clientes que soportan DCR — entre ellos Claude.ai web (Custom Connectors) — descubren el servidor de autorización a través del endpoint estándar de metadatos en `https://ia.redjudicial.cl/.well-known/oauth-authorization-server` (RFC 8414) y se registran automáticamente. No se requiere client ID precompartido.

El usuario final inicia sesión con su cuenta de Red Judicial y otorga consentimiento al connector antes de que la herramienta quede disponible.

## Cobertura por jurisdicción

| Jurisdicción | Fuente | Estado |
|---|---|---|
| Chile — Corte Suprema | Poder Judicial | ✅ en vivo (287.000+ sentencias, 2005 a la fecha) |
| Chile — Cortes de Apelaciones | Poder Judicial | ✅ en vivo (~1,4M, backfill activo hacia ~2M) |
| Chile — Tribunal Constitucional | Tribunal Constitucional | ✅ en vivo (12.000+) |
| Chile — Contraloría General | CGR | ✅ en vivo (90.000+ dictámenes) |
| Chile — tributario (SII, Tribunales Tributarios y Aduaneros) | SII / TTA | ✅ en vivo |
| Chile — laboral (Dirección del Trabajo) | DT | ✅ en vivo |
| Chile — mercados financieros, seguridad social, libre competencia, consumidor | CMF / SUSESO / TDLC / SERNAC | ✅ en vivo |
| Chile — tribunales ambientales, propiedad industrial, DDHH | TA / TDPI / INDH | ✅ en vivo |
| Chile — legislación y decretos | BCN / LeyChile | ✅ en vivo (alrededor de 19.000 normas vigentes) |
| Chile — doctrina de acceso abierto | SciELO, repositorios universitarios | ✅ parcial (alrededor de 2.500 artículos) |
| Chile — primera instancia: laboral + cobranza | Poder Judicial | ✅ en vivo (~245.000) |
| Chile — primera instancia: civil, penal, familia | Poder Judicial | 🚧 en incorporación activa |
| Expansión LATAM hispanohablante (Colombia, México, Argentina) | Múltiples | 🔭 exploratorio |

## Cumplimiento y privacidad

- Operado por **Simpley SpA**, sociedad chilena (RUT 77.983.964-8), bajo la marca **Red Judicial**.
- Datos alojados en `sa-east-1` (AWS São Paulo).
- No se entrena con consultas de usuarios. Cada solicitud se procesa y descarta, excepto los contadores de uso para facturación.
- Hoja de ruta de cumplimiento alineada con la Ley 21.719 (protección de datos personales en Chile, vigente desde el 1 de diciembre de 2026): DPO designado y evaluación de impacto en privacidad en curso.
- Política de privacidad: https://ia.redjudicial.cl/legal/privacidad
- Términos de servicio: https://ia.redjudicial.cl/legal/terminos

## Aviso legal

Red Judicial entrega investigación jurídica con fuentes verificables. No constituye asesoría legal ni reemplaza a un abogado. Cada resultado enlaza a su fuente oficial y debe verificarse ahí antes de usarse; la decisión profesional y la responsabilidad por cualquier escrito o consejo son del abogado.

## Suscripción y facturación

Red Judicial usa un modelo basado en créditos con cinco planes. Cada llamada a `redjudicial_search` consume un crédito. Hay una franquicia mensual gratuita; los planes pagados amplían el techo y desbloquean herramientas adicionales a medida que se publican (`redjudicial_get_norm`, `redjudicial_get_sentence`, `redjudicial_research_brief` — planificadas). Precios y registro: https://ia.redjudicial.cl/pricing

### Enlaces

- **Documentación:** https://ia.redjudicial.cl/mcp
- **Registro y precios:** https://ia.redjudicial.cl/pricing
- **Soporte:** contacto@redjudicial.cl
- **Operador:** Simpley SpA (Chile, RUT 77.983.964-8)
- **Licencia:** Apache-2.0
