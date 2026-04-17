# PRD: The Black Box Auditor - Financial Intelligence Agent

**Visión:** Desarrollar un sistema multi-agente capaz de auditar la narrativa corporativa de empresas públicas mediante el contraste automatizado entre discursos mediáticos (noticias/entrevistas) y datos financieros reales (SEC filings/Alpha Vantage).

**Objetivo:**
Proporcionar a inversores o analistas un reporte "Due Diligence" de alta fidelidad que identifique discrepancias, riesgos ocultos y niveles de confianza en la comunicación de una empresa, eliminando el sesgo de las notas de prensa tradicionales.

---

## 1. Alcance del Proyecto (MVP)

### 1.1 Funcionalidades Clave
* **Ingesta Dual de Datos:** Extracción de métricas financieras cuantitativas (vía Alpha Vantage) y sentimientos cualitativos (vía herramientas de búsqueda web).
* **Análisis de Disonancia:** Motor de inferencia que compara metas declaradas por la empresa vs. ejecución financiera real.
* **Generación de Reportes:** Exportación de hallazgos en formatos estandarizados (Markdown/PDF) para consumo profesional.

### 1.2 User Personas
* **Analistas de Inversión:** Que necesitan validar si el "hype" de una empresa se respalda en sus balances.
* **Portfolio Managers:** Que buscan un monitoreo pasivo de inconsistencias en sus activos.

---

## 2. Arquitectura de Agentes (CrewAI)

El sistema se dividirá en cuatro agentes con roles estrictamente definidos para evitar la alucinación y maximizar la precisión:

1.  **Financial Data Scraper (El Contador):**
    * **Rol:** Especialista en extracción de datos duros.
    * **Herramientas:** Alpha Vantage API.
    * **Misión:** Obtener estados de resultados, balances y flujo de caja de los últimos 4 trimestres.

2.  **Market Sentiment Analyst (El Sabueso):**
    * **Rol:** Investigador de medios y narrativa.
    * **Herramientas:** Tavily Search / Serper.
    * **Misión:** Recopilar declaraciones del CEO, noticias de lanzamientos y proyecciones de crecimiento publicadas en los últimos 6 meses.

3.  **Dissonance Auditor (El Crítico):**
    * **Rol:** Analista lógico y estratega financiero.
    * **Misión:** Cruzar los datos del "Contador" con las promesas del "Sabueso". Detectar si el gasto en R&D coincide con la narrativa de "innovación" o si la deuda está creciendo más rápido que lo declarado.

4.  **Reporting Officer (El Editor):**
    * **Rol:** Comunicador técnico.
    * **Misión:** Consolidar los hallazgos en un documento `.md` que luego pasa a `.pdf` estructurado, profesional y sin adornos innecesarios.

---

## 3. Stack Tecnológico
* **Framework de Agentes:** CrewAI.
* **Lenguaje:** Python 3.10+.
* **LLM Principal:** GPT-4o (recomendado para el Auditor por su capacidad de razonamiento lógico).
* **APIs Externas:** Alpha Vantage (Finanzas), Tavily/Serper (Búsqueda).
* **Output:** Reporte generado localmente en carpeta `/outputs`.

## 4. Definición de Métricas y Fuentes

### 4.1 Datos Duros (Alpha Vantage API)
* **Ticker Overview:** Market Cap, PE Ratio, Profit Margin.
* **Income Statement (Últimos 4 trimestres):** * `totalRevenue` (Validación de crecimiento).
    * `researchAndDevelopment` (Validación de innovación).
    * `netIncome` (Validación de rentabilidad).

### 4.2 Datos Narrativos (Web Search)
* **Earnings Call Transcripts (Snippets):** Declaraciones sobre proyecciones futuras.
* **News Headlines:** Sentimiento general y anuncios de alianzas estratégicas.

### 4.3 Lógica de Auditoría (Ejemplos de Flags)
* **Flag de Innovación:** Narrativa de "Liderazgo en IA" + R&D estable o decreciente.
* **Flag de Crecimiento:** Narrativa de "Expansión de mercado" + Revenue estancado.
* **Flag de Eficiencia:** Narrativa de "Optimización" + Gastos operativos al alza.

## 5. Interfaz y Flujo de Usuario

### 5.1 Ejecución (Triggers)
* **CLI Entrypoint:** El sistema aceptará inputs vía argumentos de línea de comandos.
* **Modo Demo:** Un comando preconfigurado para ejecutar una auditoría completa de una empresa "hot" del momento (ej. NVIDIA o Tesla) para demostración inmediata.

### 5.2 Visualización (TUI - Terminal User Interface)
* **Librería:** `Rich` para formateo de logs.
* **Componentes:**
    * **Live Progress:** Seguimiento de las tareas de CrewAI en tiempo real.
    * **Agent Dialogue:** Visualización de la colaboración entre agentes (quién le pide qué a quién).
    * **Result Table:** Resumen final de métricas financieras antes de generar el archivo.
    * 

### 5.3 Almacenamiento
* **Directorio:** `/output/`
* **Nomenclatura:** `YYYY-MM-DD_[TICKER]_audit.pdf`

## 6. Flujo de Navegación (TUI Experience)

El sistema operará como una aplicación de consola persistente con los siguientes estados:

### 6.1 Menú Principal (Home)
1. **Nueva Auditoría (New Search):** Inicia el flujo de recolección de datos.
2. **Historial (History):** Visualiza reportes generados anteriormente sin volver a consumir tokens de APIs.
3. **Configuración/Salir:** Gestión de API Keys locales y cierre del sistema.

### 6.2 Flujo de Auditoría Detallado
* **Entrada de Ticker:** Validación de formato (ej: TSLA, AAPL).
* **Fase de Ingesta (Visual):** Spinner activo mientras el agente "Contador" (Alpha Vantage) y el "Sabueso" (Serper/Tavily) recuperan datos.
* **Fase de Procesamiento:** Log dinámico de CrewAI mostrando la colaboración entre el "Auditor" y el "Editor".
* **Fase de Entrega:** Previsualización de las 3 métricas clave en una tabla `Rich` y confirmación de la ruta del archivo generado: `/outputs/YYYY_MM_DD_TICKER.pdf`.

### 6.3 Persistencia (Historial)
* El sistema registrará cada ejecución exitosa en una base de datos liviana (SQLite) para permitir la recuperación de reportes previos desde el menú de "Historial".

