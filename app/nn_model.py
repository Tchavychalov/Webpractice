import torch
from transformers import AutoModelForSequenceClassification, BertTokenizerFast

# Указываем путь к локальным весам
tokenizer = BertTokenizerFast.from_pretrained('./model/tokenizer')
model = AutoModelForSequenceClassification.from_pretrained('./model')

def predict(text: str) -> int:
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted
