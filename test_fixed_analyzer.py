#!/usr/bin/env python3
"""
Script de prueba para demostrar que el analizador de sentimientos corregido funciona.
"""

from sentiment_analyzer import SentimentAnalyzer
from colorama import Fore, Style, init

# Inicializar colorama
init()

def test_analyzer():
    """Prueba el analizador con diferentes tipos de textos."""
    
    analyzer = SentimentAnalyzer()
    
    # Textos de prueba
    test_texts = [
        "Me encanta este producto, es fantástico y excelente",
        "Odio este servicio, es terrible y horrible",
        "El clima está normal hoy",
        "¡Qué maravilloso día! Me siento muy feliz",
        "Estoy muy decepcionado y frustrado con este resultado",
        "I love this amazing product",
        "This is terrible and awful",
        "The weather is okay today",
        "¡Increíble! Todo salió perfecto",
        "Esto es un desastre total, muy malo"
    ]
    
    print(f"{Fore.CYAN}=== PRUEBA DEL ANALIZADOR DE SENTIMIENTOS CORREGIDO ==={Style.RESET_ALL}\n")
    
    results = []
    
    for i, text in enumerate(test_texts, 1):
        print(f"{Fore.YELLOW}Prueba {i}:{Style.RESET_ALL}")
        print(f"Texto: \"{text}\"")
        
        try:
            result = analyzer.analyze_text(text)
            results.append(result)
            
            # Mostrar resultado con colores
            sentiment = result['sentiment']
            if sentiment == "POSITIVO":
                color = Fore.GREEN
            elif sentiment == "NEGATIVO":
                color = Fore.RED
            else:
                color = Fore.YELLOW
            
            print(f"Sentimiento: {color}{sentiment}{Style.RESET_ALL}")
            print(f"Polaridad: {result['polarity']}")
            print(f"Descripción: {analyzer.get_polarity_description(result['polarity'])}")
            print(f"Subjetividad: {result['subjectivity']}")
            print("-" * 50)
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            print("-" * 50)
    
    # Mostrar resumen
    if results:
        print(f"\n{Fore.CYAN}=== RESUMEN DE RESULTADOS ==={Style.RESET_ALL}")
        summary = analyzer.get_analysis_summary(results)
        
        print(f"Total de textos analizados: {summary['total_texts']}")
        print(f"Positivos: {summary['positive_count']} ({summary['positive_percentage']}%)")
        print(f"Negativos: {summary['negative_count']} ({summary['negative_percentage']}%)")
        print(f"Neutrales: {summary['neutral_count']} ({summary['neutral_percentage']}%)")
        print(f"Polaridad promedio: {summary['average_polarity']}")
        print(f"Subjetividad promedio: {summary['average_subjectivity']}")
        
        # Verificar que no todo sea neutral
        if summary['positive_count'] > 0 and summary['negative_count'] > 0:
            print(f"\n{Fore.GREEN}✓ ÉXITO: El analizador está funcionando correctamente{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Detecta sentimientos positivos y negativos apropiadamente{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}✗ PROBLEMA: El analizador aún no está funcionando correctamente{Style.RESET_ALL}")

if __name__ == "__main__":
    test_analyzer()

