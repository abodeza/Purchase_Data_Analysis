# Purchase Data Analysis

Analysis and categorization of purchase order data.

## Description



## Demo
Link + screenshots

## Getting Started

### Prerequisites

* Used python 3.10
* Required libraries (listed in requirements.txt)

### Running locally

```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

REM ----- Disambiguation data for Camel-tools -----
camel_data -i light

streamlit run home.py
```


## Project Structure


```
Purchase_data_analysis/
├── .gitignore    
├── LICENSE    
├── README.md    
├── requirements.txt  
├── assets/    
│   ├── AR_stop_words.txt
│   ├── MUSE.png
│   ├── trie_diagram.png
│   ├── unigram_laplace_smoothing.png
│   ├── wiki.trimmed.align.vec
│   └── models/
│       ├── kmeans_best.pkl 
│       └── umap_best.pkl
├── data/
│   ├── processed-purchase-order-items.xlsx # Processed dataset
│   ├── purchase-order-items.xlsx           # Origianl dataset
│   └── analyze/
│       ├── reconstructed_entries.xlsx      # Disjointed letters vs. after rejoinig 
│       ├── unknown_tokens.xlsx             # Tokens in my vocab but not in FastText's (e.g. S201-C10)
│   └── checkpoints/
│       ├── cleaned_num.xlsx                # Result of EDA
│       ├── fully_preprocessed_item_names.xlsx # Interpretable Item Names 
│   └── clusters/
│       ├── cluster_previews.xlsx           # Clusters with their most common tokens and size
│       ├── cluster_to_category_mapping.xlsx
│       ├── mixnlp_entry_level.xlsx         # Attempt to cluster entries based on soft voting - ignore
│       ├── mixnlp_token_level.xlsx         # Attempt to cluster tokens - ignore
│   └── vocab/
│       ├── finalized_vocabulary.xlsx       # Vocabulary after consulting FastText's vocab
│       ├── vocabulary.xlsx                 # All the words after cleaning the corpus
├── notebooks/  
│   ├── EDA.ipynb                           # Clean and analyze the data - 1st step
│   ├── NLP.ipynb                           # Handle Item Name column - 2nd step
│   └── Categorize.ipynb                    # Categorizing the data - 3rd step (last)
└── streamlit_app/                          # A streamlit app to visualize and interact with the clean data
    └── ...  

```


## Contributing

Guidelines for contributors:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 

## Author

Abdullah Alzahrani
- Email: [abdullah.alzahrani.p@gmail.com](mailto:abdullah.alzahrani.p@gmail.com)
- GitHub: [@abodeza](https://github.com/abodeza)
- LinkedIn: [a-a-alzahrani](https://linkedin.com/in/a-a-alzahrani)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
