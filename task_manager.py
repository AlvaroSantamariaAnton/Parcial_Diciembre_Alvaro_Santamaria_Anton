import heapq
import json
import os
from datetime import datetime

# Archivo donde se guardan las tareas para persistencia
TASKS_FILE = "tasks.txt"

class TaskManager:
    def __init__(self):
        # Cola de prioridad para las tareas
        self.heap = []
        # Conjunto para registrar tareas completadas
        self.completed_tasks = set()
        # Cargar tareas desde el archivo al iniciar
        self.load_tasks()

    def save_tasks(self):
        """Guardar las tareas en el archivo con formato JSON."""
        # Convertir datetime a cadena ISO antes de guardar
        serializable_heap = [
            (priority, due_date.isoformat(), task) for priority, due_date, task in self.heap
        ]
        data = {
            "heap": serializable_heap,
            "completed_tasks": list(self.completed_tasks)
        }
        with open(TASKS_FILE, "w") as file:
            json.dump(data, file)

    def load_tasks(self):
        """Cargar tareas desde el archivo al iniciar el programa."""
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                data = json.load(file)
                self.completed_tasks = set(data.get("completed_tasks", []))
                # Convertir las fechas de cadena a datetime
                self.heap = [
                    (priority, datetime.fromisoformat(due_date), task)
                    for priority, due_date, task in data.get("heap", [])
                ]
                heapq.heapify(self.heap)

    def add_task(self, name, priority, due_date, dependencies=None):
        """Añadir una nueva tarea al sistema."""
        if not name.strip():
            raise ValueError("El nombre de la tarea no puede estar vacío.")
        if not isinstance(priority, int):
            raise ValueError("La prioridad debe ser un número entero.")
        
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        if dependencies is None:
            dependencies = []

        task = {
            "name": name,
            "priority": priority,
            "due_date": due_date.isoformat(),
            "dependencies": dependencies
        }
        heapq.heappush(self.heap, (priority, due_date, task))
        self.save_tasks()

    def show_pending_tasks(self):
        """Mostrar todas las tareas, indicando si están bloqueadas o ejecutables."""
        pending_tasks = []
        for _, _, task in sorted(self.heap):
            is_executable = self._is_executable(task)
            task["due_date"] = datetime.fromisoformat(task["due_date"]).strftime("%Y-%m-%d")
            task["status"] = "Ejecutable" if is_executable else "Bloqueada por dependencias"
            pending_tasks.append(task)
        return pending_tasks

    def mark_task_complete(self, name):
        """Marcar una tarea como completada."""
        # Buscar la tarea en la cola
        task = next((t for _, _, t in self.heap if t["name"] == name), None)
        
        if not task:
            print(f"Tarea '{name}' no encontrada.")
            return

        # Verificar si tiene dependencias no completadas
        unresolved_dependencies = [dep for dep in task["dependencies"] if dep not in self.completed_tasks]
        if unresolved_dependencies:
            # Mostrar mensaje de error y salir del método
            print(f"No puedes completar '{name}'. Faltan dependencias: {', '.join(unresolved_dependencies)}")
            return  # Salida inmediata si hay dependencias no resueltas

        # Si no tiene dependencias pendientes, marcar como completada
        self.completed_tasks.add(name)
        # Eliminar la tarea de la cola
        self.heap = [(p, d, t) for p, d, t in self.heap if t["name"] != name]
        heapq.heapify(self.heap)
        self.save_tasks()
        
        # Mensaje de éxito
        print(f"Tarea '{name}' marcada como completada.")

    def get_next_task(self):
        """Obtener la siguiente tarea ejecutable de mayor prioridad."""
        for priority, due_date, task in sorted(self.heap):
            if self._is_executable(task):
                task["due_date"] = due_date.strftime("%Y-%m-%d")
                return task
        return None

    def _is_executable(self, task):
        """Verificar si una tarea es ejecutable (todas sus dependencias están completadas)."""
        return all(dep in self.completed_tasks for dep in task["dependencies"])

def main():
    manager = TaskManager()
    
    while True:
        print("\nGestor de Tareas")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Marcar tarea como completada")
        print("4. Obtener la siguiente tarea de mayor prioridad")
        print("5. Salir")
        choice = input("Elige una opción: ").strip()

        try:
            if choice == "1":
                # Añadir una nueva tarea
                name = input("Nombre de la tarea: ").strip()
                priority = int(input("Prioridad (número entero, menor es mejor): "))
                due_date = input("Fecha de vencimiento (YYYY-MM-DD): ").strip()
                dependencies = input("Dependencias (separadas por comas, o deja vacío): ").strip()
                dependencies = dependencies.split(",") if dependencies else []
                manager.add_task(name, priority, due_date, dependencies)
                print(f"Tarea '{name}' añadida.")
            elif choice == "2":
                # Mostrar todas las tareas pendientes
                tasks = manager.show_pending_tasks()
                if tasks:
                    print("\nTareas pendientes:")
                    for task in tasks:
                        print(f"- {task['name']} (Prioridad: {task['priority']}, Fecha: {task['due_date']}, Estado: {task['status']})")
                else:
                    print("No hay tareas pendientes.")
            elif choice == "3":
                # Marcar una tarea como completada
                name = input("Nombre de la tarea completada: ").strip()
                manager.mark_task_complete(name)
            elif choice == "4":
                # Obtener la tarea de mayor prioridad
                task = manager.get_next_task()
                if task:
                    print(f"La siguiente tarea de mayor prioridad es: {task['name']} (Prioridad: {task['priority']}, Fecha: {task['due_date']})")
                else:
                    print("No hay tareas ejecutables.")
            elif choice == "5":
                # Salir del programa
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
