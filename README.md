# Gestor de Tareas con Prioridades

Este programa es un sistema de gestión de tareas que permite añadir tareas con prioridades, dependencias y fechas de vencimiento. Las tareas se organizan en una cola de prioridad para que las más importantes o urgentes se puedan completar primero.

## Funcionalidades

1. **Añadir Tarea**
   - Especifica un nombre, prioridad (número entero, menor es mejor), fecha de vencimiento (formato `YYYY-MM-DD`) y dependencias (opcional).
   
2. **Mostrar Tareas Pendientes**
   - Muestra todas las tareas pendientes, indicando si están ejecutables o bloqueadas por dependencias.

3. **Marcar Tarea como Completada**
   - Completa una tarea, siempre que todas sus dependencias estén resueltas.

4. **Obtener Siguiente Tarea**
   - Muestra la tarea ejecutable de mayor prioridad sin eliminarla del sistema.

5. **Persistencia**
   - Todas las tareas se guardan automáticamente en un archivo `tasks.txt` para que persistan entre ejecuciones del programa.

## Requisitos

- Python 3.8 o superior.
- Librerías estándar (no requiere instalación adicional).

## Cómo Usar

1. Ejecuta el programa:
   ```bash
   python gestor_tareas.py

## Link al reporsitorio

https://github.com/AlvaroSantamariaAnton/Parcial_Diciembre_Alvaro_Santamaria_Anton.git