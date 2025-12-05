# Agentic AI & LLM Based Analytics

## Enterprise-Grade Data Analytics with AI

Agentic AI & LLM Based Analytics is a professional data analytics platform that leverages Large Language Models (LLMs) and Agentic AI to transform raw data into actionable insights. Built for data analysts, business intelligence teams, and decision-makers who need powerful analytics capabilities.

## Core Technologies

### Agentic AI Architecture
- **Autonomous Analysis**: AI agents independently analyze data patterns and generate insights
- **Context-Aware Processing**: Understands business domains (sales, finance, HR, etc.)
- **Adaptive Learning**: Adjusts analysis approach based on data characteristics
- **Multi-Step Reasoning**: Performs complex analytical workflows automatically

### Large Language Models (LLM)
- **Natural Language Interface**: Query your data using conversational language
- **Automated Insights Generation**: AI-powered data interpretation and recommendations
- **Intelligent Code Generation**: Creates visualizations from text descriptions
- **Business Context Understanding**: Translates data patterns into business implications

### Deep Learning
- **Anomaly Detection**: Autoencoder neural networks identify outliers
- **Pattern Recognition**: Discovers hidden relationships in complex datasets
- **Dimensionality Reduction**: PCA for high-dimensional data visualization
- **Predictive Analytics**: Statistical modeling for trend analysis

### Data Processing
- **Multi-Format Support**: CSV, Excel (XLSX, XLS)
- **Intelligent Parsing**: Auto-detects delimiters, encodings, and data types
- **Multi-File Analysis**: Combines multiple datasets for unified insights
- **Real-Time Processing**: Efficient handling of large datasets

## Features

### Data Analysis
- Comprehensive data profiling and statistics
- Automated data quality assessment
- Missing value analysis and visualization
- Correlation and relationship detection
- Interactive filtering and segmentation

### Visualizations
- 8+ chart types (Scatter, Line, Bar, Box, Histogram, Heatmap, Pie, Area)
- Interactive and responsive designs
- Automatic chart recommendations
- Custom color schemes and themes
- Export capabilities

### AI-Powered Features
- Natural language data queries
- Automated insight generation
- Business recommendations
- Domain-specific analysis
- Conversational AI assistant

### Advanced Analytics
- Deep learning anomaly detection
- 3D PCA visualization
- Statistical modeling
- Trend analysis
- Correlation matrices

## Installation

### Prerequisites
- Python 3.9 or higher
- LLM API access (Google Gemini, OpenAI, or similar)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ghufranakbar/Agentic-AI-LLM-Based-Data-Analysis.git
cd Agentic-AI-LLM-Based-Data-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

4. Run the application:
```bash
streamlit run agent.py
```

## Docker Deployment

For containerized deployment:

```bash
# Using Docker Compose
docker-compose up -d

# Manual Docker
docker build -t dataviz-pro .
docker run -d -p 8501:8501 -e GEMINI_API_KEY=your_key dataviz-pro
```

See `DOCKER.md` for complete deployment guide.

## Usage

### 1. Upload Data
- Click file uploader in sidebar
- Select one or more CSV/Excel files
- Supports various encodings and delimiters
- Multiple files are automatically combined

### 2. Extract & Analyze
- Click "Extract & Analyze Data" button
- System processes and profiles the data
- AI generates initial insights
- Data is cached for performance

### 3. Explore Insights

**Overview Tab**
- Key metrics and statistics
- Data quality assessment
- Preview and export options

**Visualizations Tab**
- Choose from 8+ chart types
- Interactive filtering and customization
- Auto-generated insight dashboard

**Deep Analysis Tab**
- Anomaly detection with neural networks
- 3D PCA visualization
- Pattern identification

**AI Insights Tab**
- Automated business analysis
- Domain-specific recommendations
- Correlation analysis
- Data quality reports

**AI Assistant Tab**
- Natural language queries
- Custom visualization requests
- Interactive data exploration
- Real-time code execution

### 4. Filter & Refine
- Categorical filters in sidebar
- Numeric range sliders
- Source file filtering (multi-file uploads)
- Real-time data updates

## AI Capabilities

### Agentic AI System
- **Autonomous reasoning** over data patterns
- **Multi-step analysis** workflows
- **Context retention** across queries
- **Domain adaptation** based on data type

### Natural Language Interface
- Query data conversationally
- Generate visualizations from descriptions
- Get explanations in business terms
- Request specific calculations

### Example Queries
```
"What does this data represent?"
"Show me trends over time"
"Create a scatter plot of X vs Y"
"What are the top 10 categories?"
"Explain the correlation between these columns"
```

## Technology Stack

**Core Framework**
- Streamlit (Web application)
- Python 3.9+

**Data Processing**
- Pandas (Data manipulation)
- NumPy (Numerical computing)

**Visualization**
- Plotly (Interactive charts)
- Matplotlib (Statistical plots)
- Seaborn (Statistical visualization)

**AI & Machine Learning**
- Large Language Models (Natural language processing)
- TensorFlow (Deep learning)
- Scikit-learn (Machine learning)

**Agentic AI**
- Context-aware reasoning
- Multi-step analysis
- Autonomous insight generation

## Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (Streamlit)      │
├─────────────────────────────────────────┤
│         Agentic AI Layer                │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │   Context   │  │   Reasoning     │   │
│  │   Builder   │  │   Engine        │   │
│  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────┤
│         LLM Integration                 │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │  Prompt     │  │   Response      │   │
│  │  Engineering│  │   Processing    │   │
│  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────┤
│    Data Processing & Analytics          │
│  ┌──────┐ ┌───────┐  ┌─────────────┐    │
│  │Pandas│ │ NumPy │  │  Scikit     │    │
│  └──────┘ └───────┘  └─────────────┘    │
├─────────────────────────────────────────┤
│      Deep Learning (TensorFlow)         │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │ Autoencoder │  │      PCA        │   │
│  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────┘
```

## Key Features

### Multi-File Analysis
Upload and combine multiple datasets for unified analysis. System automatically tracks data sources and provides filtering options.

### Intelligent Parsing
Automatically detects:
- File encodings (UTF-8, Latin1, ISO-8859-1, CP1252)
- Delimiters (comma, semicolon, tab, pipe)
- Data types (numeric, categorical, datetime)
- Column relationships

### Context-Aware AI
The AI system understands:
- Business domain (sales, finance, HR, etc.)
- Data structure and relationships
- Statistical patterns
- Missing data implications
- Correlation significance

### Performance Optimized
- Data caching for fast reloading
- Lazy loading of heavy dependencies
- Efficient memory management
- Responsive UI with minimal latency

## Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
```

### Streamlit Configuration
See `.streamlit/config.toml` for customization options.

## Deployment

### Local Development
```bash
streamlit run agent.py
```

### Production Deployment
See `DOCKER.md` for containerized deployment instructions.

## Security

- API keys stored in environment variables
- No data persistence (in-memory processing)
- HTTPS recommended for production
- Regular dependency updates

## Performance Considerations

- Large files (>100MB): May require increased memory
- Deep learning: Optional, can be skipped for faster processing
- API calls: Rate limits apply based on LLM provider
- Caching: Enabled by default for repeated operations

## Troubleshooting

**Import Errors**
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.9+ required)

**API Key Issues**
- Verify .env file exists and contains valid key
- Check API key format and permissions

**Memory Issues**
- Process files in smaller batches
- Disable deep learning features if not needed
- Increase system resources

## Contributing

Contributions welcome! Areas for improvement:
- Additional visualization types
- More LLM provider integrations
- Enhanced anomaly detection algorithms
- Performance optimizations
- Documentation improvements

## License

MIT License - Free for commercial and personal use

## Support

For issues, questions, or feature requests, please use the GitHub repository issue tracker.

---

Built with Agentic AI and Large Language Models for intelligent data analytics.

For questions, suggestions, or issues, please open an issue on GitHub or contact the repository owner.

---

**Made with ❤️ for data enthusiasts everywhere**
