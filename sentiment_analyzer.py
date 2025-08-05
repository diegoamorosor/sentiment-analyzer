"""
Módulo principal del analizador de sentimientos.
Contiene la clase SentimentAnalyzer con todas las funcionalidades principales.
"""

import os
import datetime
from textblob import TextBlob
from typing import List, Dict, Tuple


class SentimentAnalyzer:
    """
    Clase principal para el análisis de sentimientos de textos.
    
    Utiliza TextBlob para analizar la polaridad y subjetividad de textos
    en español e inglés, clasificándolos como positivo, negativo o neutral.
    """
    
    def __init__(self, log_dir: str = "logs"):
        """
        Inicializa el analizador de sentimientos.
        
        Args:
            log_dir (str): Directorio donde se guardarán los logs
        """
        self.log_dir = log_dir
        self._ensure_log_dir()
        
        # Palabras clave para mejorar la detección en español
        self.positive_keywords = [
            'excelente', 'fantástico', 'increíble', 'maravilloso', 'perfecto',
            'genial', 'bueno', 'buena', 'amor', 'feliz', 'alegre', 'contento',
            'satisfecho', 'encanta', 'gusta', 'hermoso', 'bella', 'éxito'
        ]
        
        self.negative_keywords = [
            'terrible', 'horrible', 'malo', 'mala', 'pésimo', 'odio', 'detesto',
            'triste', 'enojado', 'molesto', 'frustrado', 'decepcionado', 'error',
            'problema', 'falla', 'defecto', 'disgusto', 'desagradable'
        ]
    
    def _ensure_log_dir(self):
        """Crea el directorio de logs si no existe."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analiza el sentimiento de un texto individual.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            Dict: Diccionario con los resultados del análisis
        """
        if not text or not text.strip():
            raise ValueError("El texto no puede estar vacío")
        
        # Crear objeto TextBlob
        blob = TextBlob(text)
        
        # Obtener polaridad y subjetividad
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Aplicar corrección basada en palabras clave para español
        adjusted_polarity = self._adjust_polarity_with_keywords(text.lower(), polarity)
        
        # Clasificar el sentimiento
        sentiment_label = self._classify_sentiment(adjusted_polarity)
        
        # Crear resultado
        result = {
            'text': text.strip(),
            'polarity': round(adjusted_polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment_label,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return result
    
    def _adjust_polarity_with_keywords(self, text_lower: str, original_polarity: float) -> float:
        """
        Ajusta la polaridad basándose en palabras clave en español.
        
        Args:
            text_lower (str): Texto en minúsculas
            original_polarity (float): Polaridad original de TextBlob
            
        Returns:
            float: Polaridad ajustada
        """
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        # Si TextBlob no detectó sentimiento pero hay palabras clave
        if abs(original_polarity) < 0.1:
            if positive_count > negative_count:
                return 0.3 + (positive_count * 0.1)
            elif negative_count > positive_count:
                return -0.3 - (negative_count * 0.1)
        
        # Amplificar la polaridad existente si hay palabras clave
        if positive_count > 0 and original_polarity > 0:
            return min(1.0, original_polarity + (positive_count * 0.2))
        elif negative_count > 0 and original_polarity < 0:
            return max(-1.0, original_polarity - (negative_count * 0.2))
        
        return original_polarity
    
    def analyze_file(self, file_path: str) -> List[Dict[str, any]]:
        """
        Analiza múltiples textos desde un archivo.
        
        Args:
            file_path (str): Ruta al archivo con textos (uno por línea)
            
        Returns:
            List[Dict]: Lista con los resultados de cada análisis
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if line:  # Ignorar líneas vacías
                        try:
                            result = self.analyze_text(line)
                            result['line_number'] = line_num
                            results.append(result)
                        except Exception as e:
                            print(f"Error analizando línea {line_num}: {e}")
                            continue
        except Exception as e:
            raise Exception(f"Error leyendo el archivo: {e}")
        
        return results
    
    def _classify_sentiment(self, polarity: float) -> str:
        """
        Clasifica la polaridad numérica en categorías comprensibles.
        Umbrales ajustados para mejor detección.
        
        Args:
            polarity (float): Valor de polaridad entre -1 y 1
            
        Returns:
            str: Clasificación del sentimiento
        """
        if polarity > 0.05:  # Umbral más bajo para positivo
            return "POSITIVO"
        elif polarity < -0.05:  # Umbral más bajo para negativo
            return "NEGATIVO"
        else:
            return "NEUTRAL"
    
    def get_polarity_description(self, polarity: float) -> str:
        """
        Obtiene una descripción textual de la intensidad de la polaridad.
        
        Args:
            polarity (float): Valor de polaridad entre -1 y 1
            
        Returns:
            str: Descripción de la intensidad
        """
        abs_polarity = abs(polarity)
        
        if abs_polarity >= 0.7:
            intensity = "Muy"
        elif abs_polarity >= 0.3:
            intensity = "Moderadamente"
        elif abs_polarity >= 0.05:
            intensity = "Ligeramente"
        else:
            return "Neutral"
        
        sentiment_type = "positivo" if polarity > 0 else "negativo"
        return f"{intensity} {sentiment_type}"
    
    def get_subjectivity_description(self, subjectivity: float) -> str:
        """
        Obtiene una descripción textual de la subjetividad.
        
        Args:
            subjectivity (float): Valor de subjetividad entre 0 y 1
            
        Returns:
            str: Descripción de la subjetividad
        """
        if subjectivity >= 0.7:
            return "Muy subjetivo"
        elif subjectivity >= 0.4:
            return "Moderadamente subjetivo"
        elif subjectivity >= 0.1:
            return "Ligeramente subjetivo"
        else:
            return "Objetivo"
    
    def save_to_log(self, results: List[Dict[str, any]], filename: str = None):
        """
        Guarda los resultados del análisis en un archivo de log.
        
        Args:
            results (List[Dict]): Lista de resultados a guardar
            filename (str): Nombre del archivo (opcional)
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_analysis_{timestamp}.log"
        
        log_path = os.path.join(self.log_dir, filename)
        
        try:
            with open(log_path, 'w', encoding='utf-8') as file:
                file.write("=== ANÁLISIS DE SENTIMIENTOS ===\n")
                file.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total de textos analizados: {len(results)}\n\n")
                
                for i, result in enumerate(results, 1):
                    file.write(f"--- Análisis #{i} ---\n")
                    file.write(f"Texto: \"{result['text']}\"\n")
                    file.write(f"Sentimiento: {result['sentiment']}\n")
                    file.write(f"Polaridad: {result['polarity']} ({self.get_polarity_description(result['polarity'])})\n")
                    file.write(f"Subjetividad: {result['subjectivity']} ({self.get_subjectivity_description(result['subjectivity'])})\n")
                    if 'line_number' in result:
                        file.write(f"Línea del archivo: {result['line_number']}\n")
                    file.write(f"Timestamp: {result['timestamp']}\n\n")
                
            print(f"Resultados guardados en: {log_path}")
            
        except Exception as e:
            print(f"Error guardando el log: {e}")
    
    def get_analysis_summary(self, results: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Genera un resumen estadístico de los análisis realizados.
        
        Args:
            results (List[Dict]): Lista de resultados de análisis
            
        Returns:
            Dict: Resumen estadístico
        """
        if not results:
            return {}
        
        total = len(results)
        positive = sum(1 for r in results if r['sentiment'] == 'POSITIVO')
        negative = sum(1 for r in results if r['sentiment'] == 'NEGATIVO')
        neutral = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
        
        avg_polarity = sum(r['polarity'] for r in results) / total
        avg_subjectivity = sum(r['subjectivity'] for r in results) / total
        
        return {
            'total_texts': total,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'positive_percentage': round((positive / total) * 100, 1),
            'negative_percentage': round((negative / total) * 100, 1),
            'neutral_percentage': round((neutral / total) * 100, 1),
            'average_polarity': round(avg_polarity, 3),
            'average_subjectivity': round(avg_subjectivity, 3)
        }

