"""
Funciones auxiliares para la aplicación de análisis de sentimientos.
Contiene utilidades para formateo, validación y manejo de archivos.
"""

import os
import glob
from colorama import Fore, Style, init
from typing import List, Dict

# Inicializar colorama para colores en consola
init(autoreset=True)


def print_colored(text: str, color: str = Fore.WHITE):
    """
    Imprime texto con color en la consola.
    
    Args:
        text (str): Texto a imprimir
        color (str): Color del texto (usar constantes de colorama)
    """
    print(f"{color}{text}{Style.RESET_ALL}")


def print_header(title: str):
    """
    Imprime un encabezado formateado.
    
    Args:
        title (str): Título del encabezado
    """
    print_colored("=" * 50, Fore.CYAN)
    print_colored(f" {title.center(46)} ", Fore.CYAN)
    print_colored("=" * 50, Fore.CYAN)


def print_separator():
    """Imprime una línea separadora."""
    print_colored("-" * 50, Fore.YELLOW)


def format_result(result: Dict[str, any], analyzer) -> str:
    """
    Formatea un resultado de análisis para mostrar en consola.
    
    Args:
        result (Dict): Resultado del análisis
        analyzer: Instancia del analizador para obtener descripciones
        
    Returns:
        str: Resultado formateado
    """
    sentiment_colors = {
        'POSITIVO': Fore.GREEN,
        'NEGATIVO': Fore.RED,
        'NEUTRAL': Fore.YELLOW
    }
    
    color = sentiment_colors.get(result['sentiment'], Fore.WHITE)
    
    formatted = f"""
{Fore.CYAN}RESULTADO:{Style.RESET_ALL}
{Fore.WHITE}Texto: "{result['text']}"{Style.RESET_ALL}
{color}Sentimiento: {result['sentiment']}{Style.RESET_ALL}
{Fore.WHITE}Polaridad: {result['polarity']} ({analyzer.get_polarity_description(result['polarity'])}){Style.RESET_ALL}
{Fore.WHITE}Subjetividad: {result['subjectivity']} ({analyzer.get_subjectivity_description(result['subjectivity'])}){Style.RESET_ALL}
{Fore.WHITE}Fecha: {result['timestamp']}{Style.RESET_ALL}
"""
    return formatted


def format_summary(summary: Dict[str, any]) -> str:
    """
    Formatea un resumen estadístico para mostrar en consola.
    
    Args:
        summary (Dict): Resumen estadístico
        
    Returns:
        str: Resumen formateado
    """
    if not summary:
        return f"{Fore.YELLOW}No hay datos para mostrar resumen{Style.RESET_ALL}"
    
    formatted = f"""
{Fore.CYAN}RESUMEN ESTADÍSTICO:{Style.RESET_ALL}
{Fore.WHITE}Total de textos analizados: {summary['total_texts']}{Style.RESET_ALL}

{Fore.GREEN}Positivos: {summary['positive_count']} ({summary['positive_percentage']}%){Style.RESET_ALL}
{Fore.RED}Negativos: {summary['negative_count']} ({summary['negative_percentage']}%){Style.RESET_ALL}
{Fore.YELLOW}Neutrales: {summary['neutral_count']} ({summary['neutral_percentage']}%){Style.RESET_ALL}

{Fore.WHITE}Polaridad promedio: {summary['average_polarity']}{Style.RESET_ALL}
{Fore.WHITE}Subjetividad promedio: {summary['average_subjectivity']}{Style.RESET_ALL}
"""
    return formatted


def validate_file_path(file_path: str) -> bool:
    """
    Valida si un archivo existe y es accesible.
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        bool: True si el archivo es válido
    """
    if not file_path:
        print_colored("Error: Debe especificar una ruta de archivo", Fore.RED)
        return False
    
    if not os.path.exists(file_path):
        print_colored(f"Error: El archivo '{file_path}' no existe", Fore.RED)
        return False
    
    if not os.path.isfile(file_path):
        print_colored(f"Error: '{file_path}' no es un archivo válido", Fore.RED)
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1)  # Intentar leer un carácter
        return True
    except Exception as e:
        print_colored(f"Error: No se puede leer el archivo '{file_path}': {e}", Fore.RED)
        return False


def get_log_files(log_dir: str) -> List[str]:
    """
    Obtiene la lista de archivos de log disponibles.
    
    Args:
        log_dir (str): Directorio de logs
        
    Returns:
        List[str]: Lista de archivos de log
    """
    if not os.path.exists(log_dir):
        return []
    
    pattern = os.path.join(log_dir, "*.log")
    log_files = glob.glob(pattern)
    return sorted(log_files, key=os.path.getmtime, reverse=True)


def display_log_files(log_files: List[str]):
    """
    Muestra la lista de archivos de log disponibles.
    
    Args:
        log_files (List[str]): Lista de archivos de log
    """
    if not log_files:
        print_colored("No hay archivos de historial disponibles", Fore.YELLOW)
        return
    
    print_colored("Archivos de historial disponibles:", Fore.CYAN)
    for i, log_file in enumerate(log_files, 1):
        filename = os.path.basename(log_file)
        file_size = os.path.getsize(log_file)
        mod_time = os.path.getmtime(log_file)
        
        from datetime import datetime
        mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
        
        print_colored(f"{i}. {filename} ({file_size} bytes) - {mod_date}", Fore.WHITE)


def get_user_input(prompt: str, input_type: str = "string") -> any:
    """
    Obtiene entrada del usuario con validación básica.
    
    Args:
        prompt (str): Mensaje para el usuario
        input_type (str): Tipo de entrada esperada ("string", "int", "file")
        
    Returns:
        any: Entrada del usuario validada
    """
    while True:
        try:
            user_input = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
            
            if input_type == "string":
                if user_input:
                    return user_input
                else:
                    print_colored("Error: La entrada no puede estar vacía", Fore.RED)
            
            elif input_type == "int":
                return int(user_input)
            
            elif input_type == "file":
                if validate_file_path(user_input):
                    return user_input
                # Si no es válido, el bucle continúa
            
        except ValueError:
            print_colored("Error: Entrada inválida. Intente nuevamente.", Fore.RED)
        except KeyboardInterrupt:
            print_colored("\nOperación cancelada por el usuario", Fore.YELLOW)
            return None


def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")


def show_menu() -> int:
    """
    Muestra el menú principal y obtiene la selección del usuario.
    
    Returns:
        int: Opción seleccionada por el usuario
    """
    print_header("DETECTOR DE SENTIMIENTOS")
    print_colored("1. Analizar texto individual", Fore.WHITE)
    print_colored("2. Analizar archivo de textos", Fore.WHITE)
    print_colored("3. Ver historial", Fore.WHITE)
    print_colored("4. Salir", Fore.WHITE)
    print_separator()
    
    while True:
        try:
            choice = int(input(f"{Fore.CYAN}Selecciona una opción (1-4): {Style.RESET_ALL}"))
            if 1 <= choice <= 4:
                return choice
            else:
                print_colored("Error: Seleccione una opción válida (1-4)", Fore.RED)
        except ValueError:
            print_colored("Error: Ingrese un número válido", Fore.RED)
        except KeyboardInterrupt:
            print_colored("\nSaliendo del programa...", Fore.YELLOW)
            return 4

