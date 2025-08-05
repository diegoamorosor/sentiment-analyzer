---

<p align="center"> 
  <img src="https://imgur.com/f4mybwy.png" alt="Sentiment-Analysis" /> 
</p>

<h1 align="center">Sentiment Analyzer with TextBlob</h1>

Welcome! This repository demonstrates how to perform sentiment analysis on text using **TextBlob**, a natural language processing library for Python. The application classifies text as **positive**, **negative**, or **neutral**, and provides detailed metrics for polarity and subjectivity.

---

## 📖 What is Sentiment Analysis?

Sentiment analysis is an NLP technique used to determine the emotional tone behind a body of text. Using **TextBlob** with custom enhancements, this application can:

* **Automatically classify**: Determine if a text is positive, negative, or neutral.
* **Measure polarity**: Scores range from -1 (very negative) to +1 (very positive).
* **Evaluate subjectivity**: Scores range from 0 (objective) to 1 (subjective).
* **Process multiple languages**: Optimized for both Spanish and English.
* **Enhanced detection**: Uses Spanish keyword matching for higher accuracy.

### Analysis Metrics:

| **Metric**         | **Range**    | **Description**                                      |
| ------------------ | ------------ | ---------------------------------------------------- |
| **Polarity**       | -1.0 to +1.0 | Indicates sentiment direction (negative to positive) |
| **Subjectivity**   | 0.0 to 1.0   | Measures objectivity vs. subjectivity                |
| **Classification** | Categorical  | Positive, Negative, or Neutral based on polarity     |

---

## 🚀 Application Features

* Interactive color-based console interface.
* Real-time analysis of individual texts.
* Batch processing from text files.
* Analysis history with timestamps.
* Statistical summaries of multiple texts.
* Input validation and error handling.
* Improved detection with Spanish sentiment keywords.
* Fine-tuned classification thresholds for better accuracy.

---

## 📋 Requirements

Make sure you have:

* Python 3.7+
* TextBlob
* Colorama

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 📝 Usage

### 1. Clone the Repository

```bash
git clone https://github.com/diegoamorosor/sentiment-analyzer.git
cd sentiment-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Test the Analyzer

```bash
python test_fixed_analyzer.py
```

### 4. Run the Main Application

```bash
python main.py
```

### 5. Menu Options

The application includes an interactive menu:

```
1. Analyze single text
2. Analyze text file
3. View analysis history
4. Exit
```

---

## 🖼 Example Output

For the text: *"Me encanta este producto, es fantástico"*, the analysis will display:

```text
═══════════════════════════════════════════════════════════════
                    ANALYSIS RESULT
═══════════════════════════════════════════════════════════════

📝 Analyzed Text:
"Me encanta este producto, es fantástico"

📊 Sentiment Metrics:
• Polarity: 0.6 (Moderately positive)
• Subjectivity: 0.0 (Objective)

🎯 Classification: POSITIVE

📈 Interpretation:
The text expresses a clearly positive sentiment with keywords
like "encanta" and "fantástico" reinforcing the classification.

⏰ Analysis Timestamp: 2025-07-31 14:30:25
```

### Test Results:

```text
=== RESULTS SUMMARY ===
Total texts analyzed: 10
Positive: 6 (60.0%)
Negative: 4 (40.0%)
Neutral: 0 (0.0%)
✓ SUCCESS: Analyzer is working as expected
```

---

## 💡 Core Functions

| **Function**                       | **Description**                                   |
| ---------------------------------- | ------------------------------------------------- |
| `analyze_text(text)`               | Analyzes individual text with enhanced detection. |
| `_adjust_polarity_with_keywords()` | Boosts polarity based on sentiment keywords.      |
| `_classify_sentiment(polarity)`    | Improved thresholds for classification.           |
| `analyze_file(file_path)`          | Processes multiple texts from a file.             |
| `get_analysis_summary(results)`    | Generates summary stats from multiple analyses.   |

---

## 🧪 Test File

Includes `test_fixed_analyzer.py`, which demonstrates:

* Analysis of positive, negative, and neutral texts.
* Support for both Spanish and English.
* Verification that the "only neutral" bug is resolved.
* Performance statistics of the sentiment analyzer.

---

## 🔍 Future Improvements

Planned features include:

1. Support for additional languages (French, Italian, Portuguese).
2. Social media API integration.
3. Web interface with Flask or Django.
4. Specific emotion detection (joy, sadness, anger).
5. Graphical visualizations of sentiment trends.
6. Custom machine learning models for domain-specific texts.

---

## 📚 Resources

* [TextBlob Documentation](https://textblob.readthedocs.io/)
* [NLTK Book](https://www.nltk.org/book/)
* [Sentiment Analysis Guide](https://www.sciencedirect.com/science/article/pii/S131915782400137X)
* [Colorama Documentation](https://pypi.org/project/colorama/)

---

> ## 🛠 Version Improvements Note
>
> This version includes important fixes from a previous implementation that was returning mostly neutral results. Classification thresholds were adjusted (from ±0.1 to ±0.05), and a keyword-based polarity boost was added for Spanish-language input. These changes significantly improved detection accuracy.

