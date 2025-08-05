#!/usr/bin/env python3
"""
Aplicación principal del Detector de Sentimientos.
Interfaz de consola interactiva para análisis de sentimientos de textos.

Autor: Diego Amoroso
Fecha: 2025-07-31
"""

import sys
import os
from sentiment_analyzer import SentimentAnalyzer
from utils import (
    print_colored, print_header, print_separator, format_result, 
    format_summary, get_user_input, clear_screen, pause, show_menu,
    get_log_files, display_log_files, validate_file_path
)
from colorama import Fore, Style


class SentimentApp:
    """
    Clase principal de la aplicación de análisis de sentimientos.
    Maneja la interfaz de usuario y coordina las operaciones.
    """
    
    def __init__(self):
        """Inicializa la aplicación."""
        self.analyzer = SentimentAnalyzer()
        self.running = True
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        print_colored("Iniciando Detector de Sentimientos...", Fore.GREEN)
        print_colored("Cargando modelos de análisis...", Fore.YELLOW)
        
        # Verificar que TextBlob funcione correctamente
        try:
            test_result = self.analyzer.analyze_text("Texto de prueba")
            print_colored("✓ Sistema listo para usar", Fore.GREEN)
        except Exception as e:
            print_colored(f"Error inicializando el sistema: {e}", Fore.RED)
            print_colored("Verifique que las dependencias estén instaladas correctamente", Fore.YELLOW)
            return
        
        pause()
        
        while self.running:
            try:
                clear_screen()
                choice = show_menu()
                self.handle_menu_choice(choice)
            except KeyboardInterrupt:
                print_colored("\n\nSaliendo del programa...", Fore.YELLOW)
                break
            except Exception as e:
                print_colored(f"Error inesperado: {e}", Fore.RED)
                pause()
    
    def handle_menu_choice(self, choice: int):
        """
        Maneja la selección del menú principal.
        
        Args:
            choice (int): Opción seleccionada
        """
        if choice == 1:
            self.analyze_single_text()
        elif choice == 2:
            self.analyze_file()
        elif choice == 3:
            self.view_history()
        elif choice == 4:
            self.exit_application()
    
    def analyze_single_text(self):
        """Analiza un texto individual ingresado por el usuario."""
        clear_screen()
        print_header("ANÁLISIS DE TEXTO INDIVIDUAL")
        
        text = get_user_input("Ingresa el texto a analizar: ", "string")
        if text is None:  # Usuario canceló
            return
        
        try:
            print_colored("\nAnalizando...", Fore.YELLOW)
            result = self.analyzer.analyze_text(text)
            
            print(format_result(result, self.analyzer))
            
            # Preguntar si guardar en log
            save_choice = input(f"{Fore.CYAN}¿Guardar resultado en historial? (s/n): {Style.RESET_ALL}").lower()
            if save_choice in ['s', 'si', 'sí', 'y', 'yes']:
                self.analyzer.save_to_log([result])
            
        except Exception as e:
            print_colored(f"Error analizando el texto: {e}", Fore.RED)
        
        pause()
    
    def analyze_file(self):
        """Analiza múltiples textos desde un archivo."""
        clear_screen()
        print_header("ANÁLISIS DE ARCHIVO")
        
        print_colored("Ingrese la ruta del archivo con textos (uno por línea):", Fore.CYAN)
        print_colored("Ejemplo: examples/sample_texts.txt", Fore.YELLOW)
        
        file_path = get_user_input("Ruta del archivo: ", "file")
        if file_path is None:  # Usuario canceló
            return
        
        try:
            print_colored(f"\nAnalizando archivo: {file_path}", Fore.YELLOW)
            results = self.analyzer.analyze_file(file_path)
            
            if not results:
                print_colored("No se encontraron textos válidos en el archivo", Fore.YELLOW)
                pause()
                return
            
            print_colored(f"\n✓ Análisis completado: {len(results)} textos procesados", Fore.GREEN)
            
            # Mostrar resumen
            summary = self.analyzer.get_analysis_summary(results)
            print(format_summary(summary))
            
            # Preguntar si mostrar resultados detallados
            show_details = input(f"{Fore.CYAN}¿Mostrar resultados detallados? (s/n): {Style.RESET_ALL}").lower()
            if show_details in ['s', 'si', 'sí', 'y', 'yes']:
                print_separator()
                for i, result in enumerate(results, 1):
                    print_colored(f"\n--- Resultado {i}/{len(results)} ---", Fore.CYAN)
                    print(format_result(result, self.analyzer))
                    
                    if i % 3 == 0 and i < len(results):  # Pausa cada 3 resultados
                        continue_choice = input(f"{Fore.CYAN}Continuar mostrando resultados? (s/n): {Style.RESET_ALL}").lower()
                        if continue_choice not in ['s', 'si', 'sí', 'y', 'yes']:
                            break
            
            # Guardar automáticamente en log
            self.analyzer.save_to_log(results)
            
        except FileNotFoundError:
            print_colored(f"Error: El archivo '{file_path}' no existe", Fore.RED)
        except Exception as e:
            print_colored(f"Error procesando el archivo: {e}", Fore.RED)
        
        pause()
    
    def view_history(self):
        """Muestra el historial de análisis previos."""
        clear_screen()
        print_header("HISTORIAL DE ANÁLISIS")
        
        log_files = get_log_files(self.analyzer.log_dir)
        
        if not log_files:
            print_colored("No hay archivos de historial disponibles", Fore.YELLOW)
            print_colored("Realice algunos análisis primero para generar historial", Fore.CYAN)
            pause()
            return
        
        display_log_files(log_files)
        
        try:
            choice = input(f"\n{Fore.CYAN}Seleccione un archivo para ver (número) o Enter para volver: {Style.RESET_ALL}")
            
            if not choice.strip():
                return
            
            file_index = int(choice) - 1
            if 0 <= file_index < len(log_files):
                self.display_log_content(log_files[file_index])
            else:
                print_colored("Selección inválida", Fore.RED)
                pause()
                
        except ValueError:
            print_colored("Entrada inválida", Fore.RED)
            pause()
        except Exception as e:
            print_colored(f"Error accediendo al historial: {e}", Fore.RED)
            pause()
    
    def display_log_content(self, log_file: str):
        """
        Muestra el contenido de un archivo de log.
        
        Args:
            log_file (str): Ruta del archivo de log
        """
        try:
            clear_screen()
            print_header(f"HISTORIAL: {os.path.basename(log_file)}")
            
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print_colored(content, Fore.WHITE)
            
        except Exception as e:
            print_colored(f"Error leyendo el archivo de historial: {e}", Fore.RED)
        
        pause()
    
    def exit_application(self):
        """Termina la aplicación."""
        print_colored("\n¡Gracias por usar el Detector de Sentimientos!", Fore.GREEN)
        print_colored("¡Hasta la próxima!", Fore.CYAN)
        self.running = False


def main():
    """Función principal del programa."""
    try:
        app = SentimentApp()
        app.run()
    except KeyboardInterrupt:
        print_colored("\n\nPrograma interrumpido por el usuario", Fore.YELLOW)
    except Exception as e:
        print_colored(f"Error crítico: {e}", Fore.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()

