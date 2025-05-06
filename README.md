# p2p-credit-risk


GitHub Repository for Applications of Artificial Intelligence in Business project: **Adversarial Learning for Robust Credit Risk Assessment in P2P Lending**
## Dataset

Download the dataset manually from Kaggle:

https://www.kaggle.com/datasets/marcobeyer/bondora-p2p-loans/versions/257?resource=download

After downloading, place the file in:  `data/LoanData.csv` (you may need to create the `data` folder).

## Environment Setup

### 1. Python

Use Python 3.12 or later. It is recommended to use a virtual environment (e.g., `venv` or `pipenv`) to manage dependencies.

### 2. Install Required Packages

In the project folder, run:

```bash
pip install -r requirements.txt
```

This installs all required packages listed in the file.

## Adding New Packages

After installing a new package, update `requirements.txt` by running:

```bash
pip freeze > requirements.txt
```

## Cloning the Repository

To get a local copy of the project:

```bash
git clone {repo_url}
cd p2p-credit-risk
```

Alternatively, you can click the green "Code" button on GitHub and download the ZIP file, then unzip it.

