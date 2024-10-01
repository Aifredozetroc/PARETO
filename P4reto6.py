# Test de streamlit
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO  # Importar BytesIO
from matplotlib.backends.backend_pdf import PdfPages

# Usar el backend 'Agg' para evitar problemas con Streamlit
import matplotlib
matplotlib.use('Agg')

# Lista de causas
causas = [
    'Causa 1', 'Causa 2', 'Causa 3', 'Causa 4', 'Causa 5', 
    'Causa 6', 'Causa 7', 'Causa 8', 'Causa 9', 'Causa 10', 
    'Causa 11', 'Causa 12', 'Causa 13', 'Causa 14', 'Causa 15',
    'Causa 16', 'Causa 17', 'Causa 18', 'Causa 19', 'Causa 20',
    'Causa 21', 'Causa 22', 'Causa 23', 'Causa 24', 'Causa 25'
]

# Función para generar frecuencias aleatorias
def generar_ejemplo():
    # Generar un número de causas aleatorio entre 10 y 25
    num_causas = np.random.randint(10, 26)
    causas_seleccionadas = np.random.choice(causas, size=num_causas, replace=False)
    
    # Dividir las causas en 20% y 80%
    num_causas_20 = max(1, int(0.3 * num_causas))  # Al menos una causa estará en el 30%
    num_causas_80 = num_causas - num_causas_20
    
    # Asignar frecuencias
    total_frecuencia = 600  # Frecuencia total (puedes ajustarla)
    
    # El 80% de las frecuencias para el 20% de las causas
    frecuencias_20 = np.random.randint(50, 100, size=num_causas_20)  # Frecuencias más altas
    frecuencias_20 = frecuencias_20 / frecuencias_20.sum() * 0.7 * total_frecuencia  # Escalar al 80% del total
    
    # El 20% de las frecuencias para el 80% de las causas
    frecuencias_80 = np.random.randint(1, 50, size=num_causas_80)  # Frecuencias más bajas
    frecuencias_80 = frecuencias_80 / frecuencias_80.sum() * 0.2 * total_frecuencia  # Escalar al 20% del total
    
    # Combinar las frecuencias
    frecuencias = np.concatenate([frecuencias_20, frecuencias_80]).astype(int)
    
    # Crear el DataFrame con las causas y frecuencias
    df = pd.DataFrame({'Causa': causas_seleccionadas, 'Frecuencia': frecuencias})
    df = df.sort_values(by='Frecuencia', ascending=False)
    return df

# Configuración de la navegación en la barra lateral
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio", "Aplicación", "Aprendiendo", "Next" ])

# Control de navegación con el estado de sesión
if "page" not in st.session_state:
    st.session_state.page = "Inicio"

# Navigation Manager
if page == "Inicio":
    st.session_state.page = "Inicio"
elif page == "Aplicación":
    st.session_state.page = "Aplicación"
elif page == "Aprendiendo":
    st.session_state.page = "Aprendiendo"
elif page == "Next":
    st.session_state.page = "Next"

# Mostrar el contenido según la página seleccionada
if st.session_state.page == "Inicio":
    # Página de inicio
    st.image("P4retoImage3.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.title("P4reto Chart 4.0")
    st.header('Instrucciones para preparar los datos de entrada para elaborar el gráfico de Pareto')
    st.markdown("""
                1. Deberemos subir los datos en un archivo de excel (.xlsx o .xls).
                2. Los encabezados pueden ser personalizados, pero deben seguir el siguiente orden: 
                    - Primera columna; colocar las categorias (Fallas, demoras, amenazas, oportunidades, causas), no existe
                    un limite de caracteres para esta categoria, pero un máximo de 25 caracteres mantiene una apariencia legible.
                    - Segunda columna; colocar la frecuencia (tiempo acumulado para cada evento).
                    - El Titulo de la gráfica sera el nombre del archivo sin extensión.*
                    - El nombre de la pestaña aparecera como referencia al pie del gráfico.*
                    - *En construcción
                3. No deben haber celdas en blanco o valores nulos.
                4. La aplicación se encargara de ordenar la severidad de los eventos según la frecuencia en orden descendente.
                5. Un pequeño aspecto diferenciado en esta propuesta de interpretación de Pareto, es el área  
                sombreada correspondiente al 80% de las paradas, esto simplifica bastante la identificación de  
                los aspectos a los cuales prestar más atención, por eso lo hemos llamado "Pay Attention Zone".
                6. Nos gustaria mucho adelantarles que esta simple diferenciación ha venido acompañada de un  
                par de Insights muy valiosos los cuales estaremos desarrollando en los siguientes días, como  
                desafio les dejamos el siguiente cuestionamiento: "Que tan proactivos o reactivos nos consideramos?"  
                """)
    
#if st.button("Ir a la Aplicación"):
    #st.session_state.page = "Aplicación"

elif st.session_state.page == "Aplicación":
    # Página de la aplicación
    st.title("Panel de Análisis de Fallas")
    st.write("Carga los datos de fallas y visualiza el gráfico.")
    
    # Botón para cargar datos
    uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

    # Inicializamos df_data como None
    df_data = None

    # Mostrar botón para generar ejemplo
    st.markdown("### Generar un ejemplo aleatorio")
    st.info("Puede pulsar el botón para generar los datos de fallas y visualizar el gráfico aleatorio.")
    # st.markdown("---")
    if st.button('Generar ejemplo'):
        df_data = generar_ejemplo()
        st.write("Ejemplo generado con éxito:")
        #st.dataframe(df_data)
    
    if uploaded_file is not None:
        # Si se ha cargado el archivo, leemos los datos en un DataFrame
        df_data = pd.read_excel(uploaded_file)
        df_data.rename(columns={df_data.columns[0]: 'Causa', df_data.columns[1]: 'Frecuencia'}, inplace=True)
        st.write("Datos cargados con éxito:")
        #st.dataframe(df_data)

    if df_data is not None:      
        # Procesar datos para el gráfico
        try:
            if 'Frecuencia' in df_data.columns and 'Causa' in df_data.columns:
                df_data['Porcentaje'] = df_data['Frecuencia'] / df_data['Frecuencia'].sum() * 100
                df_data = df_data.sort_values(by='Frecuencia', ascending=False)
                frecuencia_max = df_data['Frecuencia'].max()
                df_data['Porcentaje Acumulado'] = df_data['Porcentaje'].cumsum()
                
                # Pay Attention
                condicion = 80
                for i, valor in enumerate(df_data['Porcentaje Acumulado']):
                    if valor >= condicion:
                        xmax = i + 0.5
                        break
                xmin = -1    
                
                # Crear el gráfico de Pareto
                fig, ax = plt.subplots(figsize=(10, 6))
                plt.title('Gráfico de Pareto 4.0', fontsize=14, pad=10)
                ax.bar(df_data['Causa'], df_data['Frecuencia'], color='blue')
                ax.set_xlabel("Causas")
                ax.set_ylabel("Frecuencia")
                ax.set_xticklabels(df_data['Causa'], rotation=90, fontsize=8)
                ax2 = ax.twinx()
                ax2.plot(df_data['Causa'], df_data['Porcentaje Acumulado'], color='red', linestyle='-')
                ax2.set_ylabel("% Acumulado")
                ax.axvspan(xmin, xmax, color='gray', alpha=0.3)
                ax.text(x= xmax-0.3, y= frecuencia_max, s='Pay Attention\nZone', fontsize=12, color='white', horizontalalignment='right', verticalalignment='top', alpha=0.5)
                plt.tight_layout()
                plt.xlim(-1, len(df_data))
                plt.ylim(0, 105)
                         
                st.write("### Gráfico de Pareto 4.0")
                st.write("Eventos sobre el área sombreada son responsables por 80% de las paradas, Pay Attention!")
                st.pyplot(fig)

                # Descargar el gráfico como PDF
                pdf_buffer = BytesIO()
                with PdfPages(pdf_buffer) as pdf:
                    pdf.savefig(fig)
                    plt.close(fig)
            
                pdf_buffer.seek(0)
                st.download_button(
                    label="Descargar Gráfico en PDF",
                    data=pdf_buffer,
                    file_name="pareto_chart.pdf",
                    mime="application/pdf"
                )

            else:
                st.warning("Asegúrate de que el archivo contiene las columnas correctas: 'Causa', 'Frecuencia'.")
        except KeyError as e:
            st.warning(f"Error al procesar los datos: {e}")
    else:
        # Si no se ha cargado el archivo, mostramos un mensaje
        st.write("### Aguardando los datos")
        st.info("Por favor, carga un archivo Excel con los datos o generar un ejemplo para visualizar el gráfico.")

if st.session_state.page == "Aprendiendo":
    # Página Aprendiendo utilizar Pareto
    st.image("P4retoImage3.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.title("P4reto Chart 4.0")
    st.header('Instrucciones para aprovechar nuevos Insights del tradicional gráfico de Pareto')
    st.markdown("""
                - Pareto no es una herramienta nueva, no pretendemos con este app retrabajar siglos de conocimiento, ya tenemos suficientes
                fuentes de información que inclusive nosotros mismos consultamos en la elaboración de este proyecto, mencionaremos dos links
                para quienes estuvieran comenzando de absoluto cero puedan consultar y despues volver aquí con nosotros.
                - Origen del principio de Pareto: https://es.wikipedia.org/wiki/Vilfredo_Pareto
                - Origen del gráfico de Pareto: https://es.wikipedia.org/wiki/Diagrama_de_Pareto, el articulo esta muy completo pero tiene un 
                pequeño erro seguramente de transcripción, mensionan su creación a comienzo de la decada del 90, cuando en realidad el gráfico 
                fue creado en 1937, poco antes del inicio de la decada del 40.
                - Desde su creación los elementos del gráfico de Pareto siempre habian sido los mismos, Eventos, Frecuencia, y Porcentaje
                Acumulado, posteriormente se realiza un análisis sobre el 20% de eventos que teoricamente ocasionan el 80% de la fallas y en
                función de este análisis se elaboran planes para corregir la causa raiz de los desvios que generan esos eventos, que generan
                retraso o perjudican nuestros procesos, hasta allí todo bien (somos muy creyentes de practicas minimalistas), pero que nos 
                impedia tener un poco más de ayuda visual?, respondemos rapidamente a esa pregunta con el motivo que nos lleva crear y compartir 
                esta app, descubrimos que es una mezcla de limitaciones tecnológicas y conformidad creativa, ya que en el gráfico tradicional de 
                pareto es muy simple tomar un lapiz y destacar cuales son eventos son los que cumplen con la relación 80-20 y adicionalmente a eso
                con las herramientas tradicionales de graficación es un poco complicado resaltar ésa área que nosotros llamamos "Pay Attention Zone"
                de forma automática, con esá combinación de factores, el gráfico de pareto se mantuvo inmutable por casi 90 años.
                - "Pay attention Zone" fue una idea inicialmente fugaz pero que inesperadamente desato una avalancha de insights que vendremos a 
                desarrollar progresivamente, comenzaremos por lo más básico, refrescando cada elemento tradicional y explicando detalladamente
                la importancia de identificar y actuar rapidamente en aquellos eventos que más afectan nuestros procesos...
                - Le invitamos a acompañarnos.  
                """)
    
    st.title("Como interpretar correctamente P4reto Chart 4.0")
    st.text('Estudiemos paso a paso cada elemento')
    st.image("P4retoImage4.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Eventos')
    st.markdown("""
                Eventos: Identificación y Registro para el Análisis de Pareto
                - ¿Qué son los eventos? En el contexto del gráfico de Pareto, los "eventos" se refieren a cualquier suceso, problema o situación que interrumpe o afecta negativamente un proceso. Estos eventos pueden variar dependiendo de la industria o el proceso que estemos analizando, pero en general, los eventos representan los incidentes que impactan la calidad, la productividad o el desempeño operativo.
                - ¿Por qué es importante registrar los eventos? El éxito de un análisis de Pareto depende de la calidad de los datos que alimentan el gráfico. Un registro correcto y completo de los eventos permite visualizar de manera precisa cuáles son las causas más frecuentes o de mayor impacto en un proceso. En otras palabras, identificar y registrar los eventos clave es el primer paso para realizar un diagnóstico eficaz que permita priorizar acciones correctivas.
                - Tipos de eventos a considerar: Dependiendo de la industria y del proceso específico, se pueden registrar diversos tipos de eventos. A continuación, se presentan algunos ejemplos comunes en la industria manufacturera y en mantenimiento industrial:
                    - Paradas de máquina: Un evento crítico es cualquier tiempo de inactividad no planificado debido a fallos técnicos.
                    - Fallas de calidad: Estos son eventos donde el producto final no cumple con las especificaciones requeridas, lo que genera desperdicio o reprocesos.
                    - Retrasos en la producción: Si un proceso productivo se retrasa por problemas logísticos o de abastecimiento, es importante registrar estos eventos.
                    - Accidentes o incidentes de seguridad: En las industrias donde la seguridad es prioritaria, estos eventos son cruciales para identificar patrones y causas recurrentes.
                    de mantenimiento: Incluyen todas las veces que un equipo falla, ya sea por fallas mecánicas, eléctricas u otras, y que requieran intervenciones de mantenimiento.
                
                ¿Qué eventos NO se deben registrar? A menudo, se comete el error de registrar eventos que no contribuyen a un análisis significativo del problema. Algunos ejemplos de eventos que no deben ser considerados en el análisis de Pareto son:  

                    - Eventos aislados o raros: Su impacto en el sistema es mínimo y no generan un 
                    patrón que valga la pena abordar inmediatamente.
                    - Problemas menores o irrelevantes: Incidentes que no afecten de forma significativa 
                    la calidad o productividad.
                    - Eventos fuera del control del proceso: Si un evento no está relacionado directamente 
                    con la operación interna del proceso (por ejemplo, un fallo externo de infraestructura), 
                    estos pueden distraer el análisis del verdadero problema.

                Registro de eventos: Buenas prácticas Para asegurar un análisis de Pareto efectivo, es crucial seguir buenas prácticas en el registro de eventos:
                
                1. Definir un criterio claro: Determinar qué tipo de eventos se deben registrar según el impacto en el proceso (frecuencia, severidad, tiempo de inactividad, costo, etc.).
                2. Mantener consistencia: Los eventos deben ser registrados de manera consistente, utilizando descripciones claras y precisas.
                3. Herramientas de registro: Utilizar software de gestión de mantenimiento o calidad que permita registrar eventos de manera rápida y eficiente.
                4. Capacitar al personal: Es esencial que todo el personal involucrado en el proceso de registro entienda la importancia y el criterio de los eventos que se deben registrar.

                Estas son recomendaciones generales, estamos concientes de que cada proceso es diferente y cada quien debe adaptarse a circunstancias y requisitos legales diferente,   siempre debe prevalecer el sentido común y el buen criterio para que la solución no
                sea peor que el problema que tratamos de solucionar.
                """)
    
    st.image("P4retoImage5.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Frecuencia')
    st.markdown("""
                **Frecuencia: Cómo Medir la Repetición de los Eventos**

                ¿Qué es la frecuencia en el análisis de Pareto? La frecuencia se refiere al número de veces que un evento ocurre en un período de tiempo determinado. Es uno de los parámetros clave en el gráfico de Pareto, ya que nos permite identificar cuáles son los eventos que suceden con mayor regularidad, y, por lo tanto, cuáles deberían recibir mayor atención a la hora de implementar acciones correctivas.
                Importancia de la Frecuencia en la Industria: En el entorno industrial, medir la frecuencia de eventos como fallas de equipos, defectos de producción o interrupciones de procesos es fundamental. Los eventos más frecuentes suelen tener el mayor impacto en la productividad o en los costos operativos. Por ejemplo, si un mismo fallo en una máquina ocurre varias veces en un mes, ese evento probablemente tendrá una mayor prioridad para ser corregido que un evento menos frecuente pero de alta gravedad.
                Cómo registrar la frecuencia: Es esencial contar con un sistema confiable para medir cuántas veces ocurre un evento. Aquí hay algunos consejos para realizar este seguimiento:
                1. Definir claramente los eventos: Como mencionamos en la sección anterior, los eventos deben estar bien definidos para evitar confusiones. Por ejemplo, si estamos midiendo fallas de equipo, se deben establecer criterios claros sobre qué constituye una falla que debe ser registrada.
                2. Establecer un período de tiempo: La frecuencia siempre debe medirse dentro de un período específico, ya sea diario, semanal o mensual, dependiendo del proceso que se esté analizando. Esto permite hacer comparaciones más precisas y detectar tendencias a lo largo del tiempo.
                3. Utilizar software de registro: Sistemas automatizados o semi-automatizados, como los CMMS (sistemas de gestión de mantenimiento computarizados), pueden facilitar el seguimiento de la frecuencia de eventos, asegurando que se registren de manera rápida y precisa.
                4. Asegurarse de que todos los eventos relevantes sean registrados: La omisión de un evento puede sesgar el análisis y dificultar la identificación de los problemas más frecuentes.

                Ejemplos de Frecuencia en la Industria:

                - Fallas mecánicas: Si un componente de una máquina falla repetidamente durante una semana, su alta frecuencia será señalada en el gráfico de Pareto, indicándonos que esa pieza necesita atención prioritaria.
                - Defectos en la producción: Si durante un proceso productivo se detectan fallas frecuentes en una línea específica, esos defectos recurrentes resaltarán en el análisis de Pareto.
                - Accidentes laborales: En un entorno de seguridad, registrar la frecuencia de incidentes puede ayudar a detectar áreas peligrosas o prácticas inseguras recurrentes.

                Cómo usar la frecuencia en el Gráfico de Pareto: El gráfico de Pareto visualiza la frecuencia de los eventos mediante barras ordenadas de mayor a menor. Los eventos que aparecen con más frecuencia tendrán las barras más altas, y serán los primeros en ser considerados para acciones correctivas. Además, se puede visualizar la "frecuencia acumulada" a través de la curva de Pareto, que ayuda a identificar qué porcentaje de los eventos (generalmente el 80%) provienen de un pequeño número de causas (generalmente el 20%).

                Foco en la Acción: La clave es que los asistentes comprendan que, al identificar los eventos más frecuentes, se puede actuar sobre ellos con mayor rapidez, lo que permite mejorar la productividad o evitar pérdidas significativas. A menudo, los eventos más frecuentes representan las "victorias rápidas" en términos de mejora de procesos.

                **Frecuencia vs. Impacto (o Severidad)**

                Frecuencia: Como hemos mencionado, se refiere al número de veces que un evento ocurre en un período determinado. Sin embargo, un evento que ocurre con mucha frecuencia pero que tiene un impacto bajo puede no ser tan prioritario como uno que ocurre con menos frecuencia pero tiene un impacto o severidad mucho mayor.

                Impacto o Severidad: En este contexto, el impacto está relacionado principalmente con el tiempo de inactividad o la magnitud de las pérdidas causadas por un evento. Por ejemplo, una falla que detiene la producción durante 30 minutos tendrá un impacto mayor que una que causa una interrupción de solo 5 minutos, incluso si esta última ocurre más veces.

                El dilema: ¿Qué priorizar?

                    - Frecuencia alta, severidad baja: Son eventos que ocurren con regularidad, pero tienen un
                    impacto relativamente bajo. Un ejemplo clásico en mantenimiento es una falla de baja criticidad 
                    que no detiene el proceso productivo, pero genera pequeñas interrupciones.

                    - Frecuencia baja, severidad alta: Estos eventos son menos frecuentes, pero cuando ocurren, generan 
                    un impacto significativo, como un accidente grave o una parada total de producción que conlleva altos 
                    costos o riesgos de seguridad.


                **Matriz Frecuencia-Severidad:**

                Una estratégia útil es combinar ambos aspectos en una matriz, donde se cruzan la frecuencia y la severidad. Esto permite visualizar de forma clara cuáles eventos deben priorizarse para intervenir:

                    - Alta frecuencia, alta severidad: Prioridad máxima. Eventos que ocurren con frecuencia
                    y tienen un impacto significativo, como paradas frecuentes de máquinas críticas.

                    - Alta frecuencia, baja severidad: Estos eventos pueden ser molestos, pero pueden ser 
                    resueltos con acciones correctivas menos urgentes. Sin embargo, si se repiten constantemente,
                    pueden acumular un impacto significativo en el tiempo.

                    - Baja frecuencia, alta severidad: Aunque estos eventos son poco comunes, deben tener una alta 
                    prioridad, ya que las consecuencias de no abordarlos a tiempo pueden ser graves.

                    - Baja frecuencia, baja severidad: Estos son los eventos de menor prioridad, ya que no afectan 
                    significativamente el rendimiento o la seguridad.


                **Reflexión final**

                Muchas veces deberemos lidiar con la dualidad frecuencia-severidad en nuestros análisis de Pareto, por lo cual es muy importante pensar más allá de la frecuencia bruta y analizar el impacto de los eventos. Un enfoque podría ser aprender cómo calcular el impacto acumulado y cómo este puede influir en las decisiones de mantenimiento y producción.
                """)
    
    st.image("P4retoImage6.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Atención')
    st.markdown("""
                **Pay Attention Zone**

                La incorporación de la "Pay Attention Zone" representa una innovación clave que está transformando nuestra forma de abordar los datos. Tradicionalmente, el gráfico de Pareto se limitaba a mostrar la relación 80/20, ordenando los eventos que generan la mayoría de los problemas en forma descendente, y con ayuda de la línea de Porcentaje Acumulado podiamos deducir la intersección de esta relación entre Porcentajes y Eventos de forma empírica. Sin embargo, al automatizar la generación de un área sombreada que resalta visualmente los eventos responsables del 80% de las paradas, hemos optimizado este proceso. Lo que comenzó como una idea aparentemente fugaz ha revelado ser un catalizador para nuevos insights, ofreciendo una visión mucho más profunda de las causas subyacentes y como resolverlas.

                :rotating_light: Por favor observe nuevamente la imagen que encabeza esta sección, "**Atención**" es la fase del análisis que divide el pasado del futuro. Si bien cada uno de los elementos del análisis es importante, "Atención" resulta especialmente relevante porque concentra ambos esfuerzos: el estudio de los eventos, la frecuencia y la severidad (pasado), el descubrimiento de las causas y la ejecución de las soluciones (futuro). En esta fase, la intervención de un especialista es indispensable. Hemos observado que omitir la participación de un especialista afecta gravemente la eficacia de los análisis de causa raíz (**RCA**). La teoría es fundamental para proporcionar estructura y método al análisis, pero sin una comprensión operativa detallada, es fácil caer en soluciones superficiales que no atacan la raíz del problema.

                La **"Pay Attention Zone"** que hemos implementado tiene el potencial de resaltar visualmente los puntos críticos de manera directa, pero si las personas que realizan el análisis carecen de conocimiento práctico y experiencia, corremos el riesgo de malinterpretar la información o de no profundizar lo suficiente en las causas subyacentes.

                Como analogía, Sun Tzu decía: **"La táctica sin estratégia es el ruido antes de la derrota."** En este contexto, podríamos decir: **"Un análisis de datos sin conocimiento práctico es un ejercicio vacío, condenado al fracaso."** Esto destaca cómo el análisis de Pareto y la "Pay Attention Zone" pueden convertirse en herramientas poderosas solo si son utilizadas correctamente por quienes comprenden tanto la teoría como la práctica.
                :rotating_light:

                Esta "Pay Attention Zone" no solo facilita la interpretación del gráfico, sino que también está cambiando paradigmas al permitir una identificación más intuitiva y rápida de los eventos críticos. Esto, a su vez, ha impactado las acciones que tomamos para resolver la causa raíz de los problemas, ya que ahora es más fácil priorizar intervenciones y recursos. Al poner mayor énfasis en los eventos dentro de esta zona, no solo podemos optimizar el análisis tradicional de Pareto, sino también desarrollar nuevos enfoques que se alineen mejor con la realidad de las operaciones y la producción. 

                En resumen, este simple cambio ha abierto un abanico de oportunidades para reestructurar el análisis, ayudando a tomar decisiones más estratégicas y basadas en datos, ofreciendo una herramienta aún más poderosa para la mejora continua en el contexto industrial. Sabemos que puede parecer exagerado afirmar que una simple área resaltada puede cambiar paradigmas,así que explicaremos mejor esa afirmación en la sección "Next" de esta app.
                """)
    st.image("P4retoImage7.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Insights')
    st.markdown("""
                Una vez que hemos recopilado suficiente evidencia a través del análisis de eventos y frecuencia, la siguiente fase crítica es el descubrimiento de Insights. Los Insights son los hallazgos clave que nos permiten entender las causas subyacentes detrás de cada evento. Para llegar a este punto, es fundamental que los pasos previos se hayan ejecutado con precisión, garantizando que los datos sean confiables y que se cuente con un analista experto que pueda llevar a cabo la fase de atención con el rigor necesario.
                Consideramos importante destacar que Pareto nos ayudará a encontrar los eventos más relevantes o prioritarios, los que necesitan "atención" inmediata, pero no es una fuente de soluciones, para ello, una vez detectadas las oportunidades debe ser implementada una estratégia de Análisis de Causa Raíz (RCA) la cual contempla diferentes metodologías según las circunstancias y las caracteristicas de cada proceso en particular, debe ser seleccionado el más apropiado y es de este análisis de RCA es que vendran nuestros anhelados **Insigts.**

                El Insight surge como resultado de un análisis profundo y estructurado, pero no se debe avanzar sin antes validar las hipótesis. Aquí, es crucial comprobar la veracidad de cada hipótesis formulada sobre las causas de los eventos. Además, debe evaluarse la viabilidad de las posibles soluciones, asegurándose de que sean prácticas y efectivas en el contexto industrial en el que se aplicarán. Saltarse esta etapa puede llevar a implementar acciones incorrectas o ineficaces, perpetuando los problemas en lugar de resolverlos.

                El proceso de descubrir un Insight no solo es técnico, sino también estratégico, ya que establece el puente entre los datos recolectados y las acciones que se tomarán para mejorar el sistema. Asegurar que los Insights sean precisos, esten basados en datos veridicos y no en simples suposiciones, es clave para el éxito en la siguiente fase del análisis de Pareto.
                """)
    st.image("P4retoImage8.png", caption="Generado con Adobe Firefly y Canva", use_column_width=True)  # Ruta de la imagen local
    st.header('Acción')
    st.markdown("""
                El Plan de Acción representa el punto culminante de todo el análisis previo. Es aquí donde convergen los eventos registrados, la frecuencia con la que ocurren, la atención prestada y los insights descubiertos. El éxito de este plan depende directamente de la precisión con la que se haya diagnosticado la causa raíz de los eventos, lo que significa que mientras más minucioso y exacto haya sido el proceso, mejores serán los resultados obtenidos en esta fase.

                El Plan de Acción no es solo una lista de tareas; es una git estructurada que responde directamente a los problemas identificados. Para que sea efectivo, debe estar fundamentado en datos sólidos, una evaluación objetiva y la verificación exhaustiva de las hipótesis planteadas en las fases anteriores. Cada acción debe estar alineada con la realidad operativa y adaptarse a las capacidades de la organización, con un enfoque en resolver definitivamente las causas que generaron los eventos en primer lugar.

                La precisión en el diagnóstico de las causas subyacentes asegura que el Plan de Acción esté dirigido a resolver los problemas de raíz, evitando recurrencias y optimizando recursos. Por lo tanto, cada paso que se implemente debe estar bien justificado, con un enfoque preventivo, correctivo o de mejora, dependiendo del tipo de evento y su impacto. La priorización es clave aquí, centrando esfuerzos en los eventos críticos identificados en la "Pay Attention Zone" para maximizar los resultados y lograr una mejora contínua.
                """)

# Mostrar el contenido según la página seleccionada
if st.session_state.page == "Next":
    # Página de inicio
    st.title("P4reto Chart 4.0")
    st.header('Pequeños cambios pueden generar grandes aprendizajes!')
    st.markdown("""
                **Conscientes de la aparente irrelevancia que una simple área sombreada, nuestra "Pay Attention Zone",
                podría tener, apelamos a su curiosidad e invitamos a descubrir cuánto valor puede aportar este pequeño 
                detalle y cómo puede contribuir a enriquecer la información que tradicionalmente obtenemos de una herramienta 
                tan clásica como el gráfico de Pareto.**
                - Desde su creación, el gráfico de Pareto ha sido una herramienta visual para destacar los eventos que causan
                el 80% de nuestras paradas. Hoy, gracias a los avances tecnológicos, podemos resaltar automáticamente esa área
                (nuestra "Pay Attention Zone"), simplemente añadiendo cinco líneas de código al popular script de Python que
                genera este tipo de gráficos. Para nuestra sorpresa, lo que comenzó como un ajuste simple rápidamente nos reveló
                nuevos insights, abriendo puertas a oportunidades más amplias.
                - Relacionando este pequeño aporte con otros estudios, como la curva de fallas potencial/funcional, hemos comenzado
                a identificar nuevas oportunidades, las cuales compartiremos progresivamente en esta aplicación, como si de un blog
                teórico-práctico se tratara.
                - ¡Sean todos bienvenidos a esta aventura! Sus comentarios, críticas y contribuciones serán altamente valorados.
                Esperamos que **P4reto** sea tan útil para ustedes como lo es para nosotros. Quedamos a su disposición en:
                *elartedelmantenimientosuntzu@gmail.com*
                """)

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 12px;'>
        Si aprecias nuestro trabajo considera hacer una donación via PayPal - elartedelmantenimientosuntzu@gmail.com<br>
        "Gracias por contribuir con el proyecto"
    </p>
    """, unsafe_allow_html=True)


# streamlit run P4reto6.py