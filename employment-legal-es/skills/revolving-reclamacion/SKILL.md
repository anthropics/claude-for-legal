---
name: revolving-reclamacion
description: Revolving credit usury claim under STS 149/2020 (Wizink test) — TAE comparison, SAC letter, escalation
argument-hint: "Contract date, TAE contractual, current balance, card type (Revolving/Crédito)"
---

# Reclamación Nulidad por Usura — Tarjeta Revolving

## Purpose

Analyze viability of usury claim against revolving credit card under **STS 149/2020 (Wizink)** and **Ley Azcárate 1908 (Art. 1 usura)**.

## Legal Framework

### STS 149/2020 (Sentencia Tribunal Supremo, case Wizink)

**Core test for usura revolving:**
- TAE contractual del tarjeta > TAE normal para crédito al consumo (CER Banco de España) + margen desproporcionado
- "Desproporcionado" typically means TAE × 1.5 o mayor (e.g., CER 8% → TAE > 12%)
- Cálculo CER = promedio TAE sector crédito al consumo (trimestral, Banco de España estadísticas)
- **Prueba**: si TAE notablemente superior al normal en el momento contrato, presunción de usura

### Ley Azcárate 1908 (Art. 1 Usura)

- "Será nulo todo contrato de crédito o préstamo en que se estipule un interés notablemente superior al normal del dinero"
- No hay límite legal máximo TAE, pero jurisprudencia fija test STS 149/2020
- **Prueba burden**: acreedor (banco) debe justificar que TAE normal para el momento

### PSD2 + Normativa Banco de España

- **Plazo respuesta SAC**: 1 mes (30 días hábiles, Banco de España)
- **Documentos obligatorios**: Banco debe proporcionar contrato original, FIPRE (folleto información precontractual), condiciones generales
- **Silencio SAC**: si no responde en 30 días, presunción de incumplimiento → escalación Banco de España

---

## Workflow

### Step 1: Recopilar datos contractuales

Ask:
- **Fecha contrato revolving?** (YYYY-MM-DD)
- **TAE contractual?** (en porcentaje, ej. "22,42%")
- **TIN?** (tipo interés nominal, ej. "1,70%")
- **Saldo actual?** (en euros, ej. "5.186,00 €")
- **Banco?** (La Caixa, Santander, Asnef, Bnext, otro)
- **Tipo producto?** (Revolving, Crédito Ampliable, Línea de Crédito, Tarjeta Visa/Mastercard)
- **Contrato original tienes?** (sí/no/digital)

Record: `[fecha_contrato]`, `[tae_contractual]`, `[tin]`, `[saldo_actual]`, `[banco]`, `[tipo_producto]`, `[contrato_original]`

---

### Step 2: Obtener CER histórico Banco de España

Ask (or verificar online):
- **¿Tienes el CER trimestral del trimestre de firma del contrato?**

Si no:
- Acceder: https://www.bde.es/wbe/es/estadisticas/
- Buscar: "Tipos de interés activos de nuevas operaciones de crédito" → "Crédito al consumo"
- Seleccionar trimestre firma contrato
- **CER (promedio sector)** típicamente 5-9% (crédito consumer)
- Documento importante: **Banco de España decisión oficial sobre CER ese trimestre**

Record: `[cer_trimestral]`, `[fuente_cer]`, `[fecha_cer]`

---

### Step 3: Aplicar test STS 149/2020

Create decision table:

| Test | Resultado | Implicación |
|---|---|---|
| **TAE contractual > CER × 1.5?** | [Sí/No] | ✅ Presunción usura si SÍ |
| **Diferencia en puntos porcentuales** | TAE - CER = [X pp] | [>8 pp es elevada] |
| **Ratio TAE/CER** | [Y.Z] | [> 1.5 claramente usura] |
| **Producto "revolving" explícito?** | [Sí/No] | ✅ Refuerza usura (jurisprudencia) |
| **Contrato anterior o similar?** | [Sí/No/Desconocido] | [Patrón comercial banco] |

---

### Step 4: Comparar contra jurisprudencia conocida

Reference cases (STS, ATs):

| Caso / Jurisprudencia | Año | TAE | CER | Resultado | Relevancia |
|---|---|---|---|---|---|
| **STS 149/2020 (Wizink)** | 2020 | 26,82 % | ~7-8 % | ✅ Nulo por usura | Sentencia clave — banco liquidó |
| **STS 680/2019 (Revolving)** | 2019 | 24,6 % | 7,5 % | ✅ Nulo por usura | Revolving específicamente |
| **STS 853/2018 (Tarjeta)** | 2018 | 22,5 % | 6-7 % | ✅ Nulo por usura | Consumidor similar |
| **STS 366/2017 (Límite)** | 2017 | 18-20 % | ~6 % | 🟡 Caso límite, depende contexto | Frontera delicada |

**Patrón**: TAE > 20% casi siempre nulo; 15-20% depende CER; <10% casi nunca nulo.

**Tu caso (ej. 22,42%)**: Si CER trimestre firma < 15%, presunción fuerte de usura.

---

### Step 5: Redactar argumentario para SAC

Template (copiar, llenar, revisar antes enviar):

```markdown
# Argumentario Reclamación Nulidad por Usura

**Prestatario:** [Tu nombre, DNI]
**Entidad:** [Banco]
**Contrato:** [número oficial, ej. 9612.50.3937782-94]
**Fecha contrato:** [date]
**Saldo reclamado:** [amount]

## Hechos

1. Celebré contrato de crédito revolving [fecha] con [banco].
2. TAE pactada: **[TAE]%**
3. Saldo pendiente desde entonces: **[saldo]€**
4. Banco ha cobrado intereses sobre TAE contractual durante X años.

## Base Legal

- **Ley Azcárate 1908, Art. 1 usura**: nulidad si TAE notablemente superior al normal.
- **STS 149/2020 (Wizink)**: test TAE > CER × 1.5 aproximadamente.
- **STS 680/2019**: aplicación explícita a productos revolving.

## Argumentación

### 1. TAE Contractual vs CER Histórico

| Dato | Valor |
|---|---|
| **TAE contrato** | [TAE]% |
| **CER trimestre [fecha]** | [CER]% (Banco de España) |
| **Ratio TAE/CER** | [TAE]/[CER] = [ratio] |
| **Diferencia pp** | [TAE-CER] pp |

**Conclusión:** TAE es **[notablemente superior / superior / comparable]** al normal del dinero en [fecha].

### 2. Jurisprudencia Aplicable

STS 149/2020 fija que TAE > CER + margen desproporcionado = presunción usura. En tu caso:
- TAE [TAE]% vs CER [CER]% = diferencia [X pp]
- Jurisprudencia similar (STS 680/2019, STS 853/2018) también declaró usura productos revolving con TAE 22-26%.

### 3. Efecto Nulidad

Si contrato es nulo por usura (Ley Azcárate):
- **Intereses cobrados ilegalmente** = restitución (toda cantidad cobrada en exceso del capital)
- **Capital original**: sigue siendo adeudado, pero SIN intereses
- **Banco debe calcular**: cantidad intereses cobrados = diferencia entre (intereses pagados) − (intereses normales al CER)

### Petitorio

1. **Declaración nulidad contrato** por usura (Ley Azcárate 1908).
2. **Restitución intereses cobrados** desde [date] hasta hoy.
3. **Revisión saldo deudor**: capital solo, sin TAE ni intereses contractuales posteriores.
4. **Gastos de tramitación**: aparcados a pendencia resolución.

**Firma**

---

---
[Tu nombre, DNI]

[Domicilio]

[Teléfono / Email]

```

---

### Step 6: Redactar carta SAC (bancaria)

**Cómo enviar:**
- Imprime + firma a mano
- **Envía por correo certificado CON ACUSE de recibo** a dirección SAC banco
- Guarda resguardo imposición
- Plazo respuesta: **30 días hábiles** (Banco de España)

**Plantilla carta SAC (simplificada, legal):**

```
[Tu nombre]
[DNI]
[Domicilio]
[Teléfono / Email]

[Ciudad], [fecha]

**Solicitud de información y declaración nulidad por usura**
Contrato: [número contrato]

SEÑORES,

Por la presente hago formalmente SOLICITUD y COMUNICACIÓN A SAC (Servicio de Atención al Cliente):

**1. SOLICITUD INFORMACIÓN PRECONTRACTUAL FALTANTE**

Declaro haber celebrado contrato de crédito revolving de fecha [fecha] bajo número [número]. A la fecha de hoy no obran en mi poder:
- Copia original contrato suscrito por ambas partes
- FIPRE (Folleto Información Precontractual) original
- Condiciones Generales aplicables en [fecha]
- Certificación de TAE conforme suscrito

Solicito formalmente que, en el plazo de **15 días**, envíe por correo certificado:
1. Contrato original digitalizado (o copia auténtica)
2. FIPRE del [fecha]
3. CG aplicables
4. Histórico completo de movimientos desde [fecha] hasta hoy
5. Desglose cálculo intereses cobrados (TIN aplicado, días, cálculo)

**2. MANIFESTACIÓN RECLAMACIÓN POR USURA**

Con conocimiento de la documentación solicitada, reafirmo mi intención de reclamar **nulidad del contrato por usura** conforme a:

- Ley Azcárate 1908, artículo 1 (usura)
- STS 149/2020 (sentencia de referencia, caso Wizink)
- STS 680/2019 (nulidad revolving por usura)

**Base sucinta:**
- TAE contrato: [TAE]%
- CER público trimestre [fecha] (Banco de España): [CER]%
- Diferencia: [X] pp, ratio [Y], notablemente superior al normal

A reserva de revisión formal una vez recibida la documentación oficial, apercibo que consideraré el contrato **NULO POR USURA** salvo que la entidad justifique lo contrario en forma legal (peritación, dictamen asesor, etc.).

**3. PLAZO Y APERCIBIMIENTO**

Conforme a regulación Banco de España (PSD2 + Código Monetario y Financiero):
- Plazo respuesta SAC: **30 días hábiles** desde recepción
- Silencio SAC = incumplimiento potencial regulatorio

Si SAC no responde en 30 días o respuesta es insatisfactoria, elevaré reclamación a:
1. **Banco de España** (Dirección General Regulación)
2. **Juzgado de lo Mercantil** (demanda nulidad + restitución intereses)

**4. NOTIFICACIÓN LEGAL**

Desde esta fecha queda expresamente comunicado que se inicia trámite administrativo previo a demanda. Cualquier acción posterior de cobro, embargante o similar será resistida jurídicamente.

Queda a su disposición para aclaraciones.

Atentamente,

[Tu firma a mano]

[Tu nombre impreso]
[DNI]

---

**ANEXOS:**
- Fotocopia DNI ambas caras
- Última facturación/extracto banco (si aplica, para prueba saldo)
```

---

### Step 7: Escalación si SAC rechaza (o silencia)

**Árbol de decisión:**

```
SAC responde en 30 días
  ├─ ✅ SÍ responde + acepta nulidad
  │   └─ Fin: banco calcula restitución, saldo se revisa
  ├─ ✅ SÍ responde + rechaza → va a Banco de España
  │   └─ "Reclamación Banco de España" (formulario oficial)
  └─ ❌ NO responde (silencia) → presunción incumplimiento
      └─ Juzgado de lo Mercantil (demanda nulidad + intereses)
```

**Paso 1: Banco de España**
- Formulario: https://www.bde.es/bde/es/areas/servicios-consumidor/servicios/formularios-reclamacion/
- Plazo: **2 años desde conocimiento del daño** (prescripción)
- Respuesta: Banco de España media + emite parecer

**Paso 2: Juzgado de lo Mercantil**
- Demanda nulidad contrato + restitución intereses (Art. 1 Ley Azcárate)
- Cuantía típica: [intereses cobrados × Y años] — puede ser 2k-50k€ depende saldo y antigüedad
- Justicia gratuita posible si ingresos < umbral (2026: ~1.100€/mes individual)
- Duración: 12-36 meses típico

---

### Step 8: Documentación checklist

**Antes de enviar SAC:**

- [ ] Contrato original descargado (si disponible vía banca online) o solicitado a banco
- [ ] TAE contractual confirmada
- [ ] CER público Banco de España para trimestre firma descargado
- [ ] Cálculo TAE/CER hecho y documentado
- [ ] Jurisprudencia STS 149/2020 leída (resumen preparado)
- [ ] Carta SAC redactada + revisada (NO errores de cálculo)
- [ ] Dirección SAC banco verificada (no usar email, USA CORREO CERTIFICADO)
- [ ] Fotocopia DNI ambas caras + firma carta a mano
- [ ] Resguardo correos (conservar 2+ años)
- [ ] Email borrador de carta guardado (por si SAC pregunta qué se envió)

---

### Step 9: Output

Format final analysis:

```markdown
## Análisis Usura Tarjeta Revolving — [Tu Nombre]

### Datos Contractuales

| Item | Valor |
|---|---|
| Banco | [banco] |
| Contrato | [número] |
| Fecha firma | [fecha] |
| TAE | [TAE]% |
| TIN | [TIN]% |
| Saldo actual | [saldo]€ |
| Años activa | [N] |

### Análisis STS 149/2020

| Parámetro | Valor | Implicación |
|---|---|---|
| **TAE contrato** | [TAE]% | — |
| **CER [trimestre]** | [CER]% (Banco de España) | Referencia normal |
| **Diferencia pp** | [X] pp | [evaluación] |
| **Ratio TAE/CER** | [Y] | [≥ 1.5 = presunción usura] |
| **Producto revolving?** | [Sí/No] | [jurisprudencia refuerza] |

### Viabilidad Reclamación: [ALTA / MEDIA / BAJA]

**Justificación:**
- [Párrafo explicativo según datos]
- Jurisprudencia más similar: [STS XXXX/20YY, similar TAE/CER]

### Próximos Pasos

**Recomendado:**
1. Descarga contrato original vía banca online [banco]
2. Verifica TAE en extracto o condiciones
3. Obtén CER Banco de España trimestre [fecha]
4. Redacta carta SAC (template arriba)
5. Envía correo certificado con acuse
6. Espera 30 días respuesta
7. Si SAC rechaza o silencia → Banco de España o juzgado

### Estimación Cuantía (si ganas)

Cálculo preliminar:
- Intereses anuales pagados (TAE × saldo promedio) = ~[X]€/año
- Años acumulados: [Y]
- **Total intereses cobrados erróneamente: ~[Z]€** (cifra indicativa)
- Deducción: intereses normales CER (no recuperables, solo exceso)

Ejemplo:
- Intereses pagados 5 años con TAE 22,42%: ~6.500€
- Intereses normales CER 7%: ~1.850€
- **Diferencia a reclamar: ~4.650€** (sin perjuicios ni costas)

### Guardrail

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO —
REVISAR CON ABOGADO ESPECIALIZADO EN REVOLVING O DERECHO BANCARIO
ANTES DE ENVIAR CARTA SAC O INICIAR PROCEDIMIENTO

Análisis es indicativo. Viabilidad final depende de:
- Contrato original (cláusulas exactas)
- CER oficial Banco de España trimestre firma (consultar vía web)
- Jurisprudencia más reciente CENDOJ (juzgados de tu territorio)
- Circunstancias personales (buena fe, capacidad jurídica, etc.)

Si Banco de España o juzgado determina que NO hay usura, perdería el coste procesal + potencial sentencia desfavorable (costas).

Consulta laboralista/mercantilista colegiado en tu territorio ANTES de actuar.
```

---

## Key References

| Reference | Scope |
|---|---|
| **Ley Azcárate 1908, Art. 1** | Nulidad usura |
| **STS 149/2020 (Wizink)** | Test TAE vs CER para revolving |
| **STS 680/2019** | Nulidad revolving por usura |
| **STS 853/2018** | Tarjeta de crédito usura |
| **PSD2** | Plazo SAC 30 días, servicios pago |
| **Banco de España** | CER público, reclamaciones, supervisión |
| **Código Monetario y Financiero** | Marco regulatorio SAC |

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO —
REVISAR CON ABOGADO ESPECIALIZADO EN DERECHO BANCARIO O LABORALISTA
COLEGIADO EN ESPAÑA ANTES DE ACTUAR

Este análisis es indicativo y educativo. La determinación final de usura
es facultad exclusiva de:
1. SAC banco (administrativo)
2. Banco de España (supervisión regulatoria)
3. Juzgados (procedimiento contencioso-administrativo y civil)

Enviar carta SAC sin revisar contrato original y CER oficial puede debilitar
tu posición. Honorio abogado especializado: típicamente 300-600€ consultoría
pre-demanda; contingencia demanda usual 30% sentencia ganada.
```

---
