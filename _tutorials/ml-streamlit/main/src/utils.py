import io
import joblib
from Bio import SeqIO
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer
from tabicl import TabICLClassifier

# global variables to load models once
_embedding_model = None
_tokenizer = None
_prediction_model = None

def parse_fasta(uploaded_file) -> dict:
    """
    Parse FASTA file.
    """
    sequences = {}
    fasta_io = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    for rec in SeqIO.parse(fasta_io, "fasta"):
        sequences[rec.id] = str(rec.seq)
    return sequences

def _load_embedding_model():
    """
    Load and cache the embedding model and tokenizer.
    """
    global _embedding_model, _tokenizer
    if _embedding_model is None or _tokenizer is None:
        _embedding_model = AutoModel.from_pretrained(
            "tattabio/gLM2_650M_embed",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        ).cuda()
        _tokenizer = AutoTokenizer.from_pretrained(
            "tattabio/gLM2_650M_embed",
            trust_remote_code=True
        )
    return _embedding_model, _tokenizer

def generate_embeddings(sequences: dict) -> dict:
    """
    Generate embeddings for one or more protein sequences.
    """
    model, tokenizer = _load_embedding_model()
    query_embeddings = {}

    for seq_id, seq in sequences.items():
        tokens = tokenizer([seq], return_tensors="pt")
        with torch.no_grad():
            embedding = model(tokens.input_ids.cuda()).pooler_output.cpu().squeeze(0)
        query_embeddings[seq_id] = embedding.to(torch.float32)

    return query_embeddings

def _load_prediction_model():
    """
    Load and cache the TabICL pre-trained classifier.
    """
    global _prediction_model
    if _prediction_model is None:
        _prediction_model = joblib.load("model.joblib")
    return _prediction_model

def make_prediction(query_embeddings: dict) -> pd.DataFrame:
    """
    Make predictions.
    """
    model = _load_prediction_model()
    emb_df = pd.DataFrame({k: v.numpy() for k, v in query_embeddings.items()}).T
    predictions = model.predict(emb_df)
    return pd.DataFrame({"prediction": predictions}, index=emb.index)
